import json
import logging
import multiprocessing
import os.path
import sys
from threading import Thread

import cv2

from ai.background_subtractor import BackgroundSubtractor
from ai.streamer import RealTimeStreamer
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

    def __init__(self, client, config_path="configs/overseer_config.json"):
        self.config_path = config_path
        config = self.load_from_json()
        self.last_cam2frame = None
        self.last_cam2invasion = {}
        self.client = client
        self.cameras = eval(config["cam_ids"])
        self.streamer = RealTimeStreamer(self.cameras)
        self.recorder = Recorder(self.cameras, record_path=config["record_path"])
        self.subtractor = BackgroundSubtractor(dramatic_change_thresh=config["invasion_threshold"])
        self.cam_frame_4 = CamFrame4((1920, 1080), frame_name="CAMERAS")
        self.loop_proc = Thread(target=self.loop)

    def load_from_json(self):
        if not os.path.exists(self.config_path):
            raise Exception("Config not found")

        with open(self.config_path, 'r') as c:
            js = json.load(c)
        return js

    def loop(self):
        while True:
            cam2frame = self.streamer.read_frame()
            last_cam2frame = self.subtractor.subtract(cam2frame)
            self.recorder.record(cam2frame)
            for id, frame in last_cam2frame.items():
                if self.subtractor.is_dramatically_changed(frame):
                    logger.info("[OVERSEER] POTENTIAL INVASION")
                    self.last_cam2invasion[id] = True
                    self.recorder.start_record(int(id))
                    self.client.emit('INVASION', {'schemas': 'INVASION', 'cam_id': id})
                else:
                    self.recorder.end_record(int(id))
                    if not self.recorder.is_record_started[int(id)]:
                        self.last_cam2invasion[id] = False
            self.last_cam2frame = cam2frame
            self.visualize()

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
