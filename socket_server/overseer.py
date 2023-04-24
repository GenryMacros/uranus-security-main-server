import asyncio
import copy
import json
import logging
import os.path
import sys
import time
from threading import Thread, Lock
from datetime import datetime

import cv2

from ai.background_subtractor import BackgroundSubtractor
from ai.streamer import RealTimeStreamer
from socket_server.events import EventTypeOut
from socket_server.requester import Requester
from socket_server.schemas.user import UserAuthData
from socket_server.utils.recorder import Recorder
from socket_server.utils.visualizer import CamFrame, CamFrame4, InvasionFrame

IS_LOG = True
logger = logging.getLogger(__name__)
if IS_LOG:
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    # do not print twice in sys.stdout
    logger.propagate = False


class Overseer:

    def __init__(self, client, cam_infos, auth_data: UserAuthData, config_path="configs/overseer_config.json"):
        self.config_path = config_path
        config = self.load_from_json()
        self.last_cam2frame = None
        self.last_cam2invasion = {}
        self.client = client
        self.client_sid = ""
        self.cameras = eval(config["cam_ids"])
        self.notification_sent = False
        self.streamer = RealTimeStreamer(self.cameras)
        self.recorder = Recorder(self.cameras, record_path=config["record_path"])
        self.subtractor = BackgroundSubtractor(dramatic_change_thresh=config["invasion_threshold"])
        self.cam_frame_4 = CamFrame4((1920, 1080), frame_name="CAMERAS")
        self.auth_data = auth_data
        self.requster = Requester()
        self.cam_infos = cam_infos
        self.dramatic_change_durations = {cam: 0 for cam in self.cameras}
        self.loop_proc = Thread(target=self.loop)

    def load_from_json(self):
        if not os.path.exists(self.config_path):
            raise Exception("Config not found")

        with open(self.config_path, 'r') as c:
            js = json.load(c)
        return js

    def loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        while True:
            cam2frame = self.streamer.read_frame()
            last_cam2frame = self.subtractor.subtract(cam2frame)
            self.recorder.record(cam2frame)
            for id, frame in last_cam2frame.items():
                if self.subtractor.is_dramatically_changed(frame):
                    if self.dramatic_change_durations[id] == 0:
                        self.dramatic_change_durations[id] = time.time()
                    elif time.time() - self.dramatic_change_durations[id] > 1:
                        logger.info("[OVERSEER] POTENTIAL INVASION")
                        self.last_cam2invasion[id] = True
                        self.recorder.start_record(int(id))
                        if not self.notification_sent:
                            loop.run_until_complete(self.send_invasion_event(int(id)))
                            self.notification_sent = True
                else:
                    self.dramatic_change_durations[id] = 0
                    is_record = self.recorder.is_record_started[id]
                    self.recorder.end_record(int(id))
                    if is_record != self.recorder.is_record_started[id]:
                        if self.auth_data.token is not None:
                            self.requster.register_invasion(os.path.join(self.recorder.records[id].record_folder,
                                                                         "cam.mp4"),
                                                            self.cam_infos[int(id)].back_id, self.auth_data)
                        self.notification_sent = False
                    if not self.recorder.is_record_started[int(id)]:
                        self.last_cam2invasion[id] = False
            lock = Lock()
            lock.acquire()
            self.last_cam2frame = cam2frame
            lock.release()
            self.visualize()

    async def send_invasion_event(self, cam_id: int):
        now = datetime.now()
        await self.client.emit(EventTypeOut.INVASION.value,
                               data={
                                   "cam_id": cam_id,
                                   "date": now.strftime("%m/%d/%Y_%H:%M:%S")
                               }, to=self.client_sid)

    def get_last_cam2frame(self):
        lock = Lock()
        lock.acquire()
        ret = copy.copy(self.last_cam2frame)
        lock.release()
        return ret

    def visualize(self):
        if self.last_cam2frame is None:
            return
        self.cam_frame_4.cam_frames = []
        invasion_frame = InvasionFrame(self.last_cam2invasion)
        self.draw_cam_frames(self.last_cam2frame)
        self.cam_frame_4.add(invasion_frame)
        self.cam_frame_4.show()

        self.cam_frame_4.draw_combined()
        key = cv2.waitKey(3)
        if key == 27:
            return

    def draw_cam_frames(self, cam2frame):
        for cam_id in cam2frame.keys():
            frame = cam2frame[cam_id]
            frame_name = f"CAM:{cam_id}"
            cam_frame = CamFrame(resolution=(1000, 600), frame_name=frame_name, frame=frame)
            cam_frame.draw_frame_name()
            #if cam_id == list(cam2frame.keys())[0]:
            #   cam_frame.draw_text(debug_info, font_scale=1)
            self.cam_frame_4.add(cam_frame)
