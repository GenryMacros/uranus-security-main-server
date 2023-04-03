import json
import logging
import os.path
import sys
from threading import Thread

from ai.background_subtractor import BackgroundSubtractor
from ai.streamer import RealTimeStreamer
from socket_server.utils.recorder import Recorder


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
        self.client = client
        self.cameras = eval(config["cam_ids"])
        self.streamer = RealTimeStreamer(self.cameras)
        self.recorder = Recorder(self.cameras, record_path=config["record_path"])
        self.subtractor = BackgroundSubtractor(dramatic_change_thresh=config["invasion_threshold"])
        self.loop_thread = Thread(target=self.loop())

    def start_loop(self):
        self.loop_thread.start()

    def loop(self):
        while True:
            cam2frame = self.streamer.read_frame()
            last_cam2frame = self.subtractor.subtract(cam2frame)
            self.recorder.record(cam2frame)
            for id, frame in last_cam2frame.items():
                if self.subtractor.is_dramatically_changed(frame):
                    logger.info("[OVERSEER] POTENTIAL INVASION")
                    self.recorder.start_record(int(id))
                    self.client.emit('INVASION', {'schemas': 'INVASION', 'cam_id': id})
                else:
                    self.recorder.end_record(int(id))

    def load_from_json(self):
        if not os.path.exists(self.config_path):
            raise Exception("Config not found")

        with open(self.config_path, 'r') as c:
            js = json.load(c)
        return js
