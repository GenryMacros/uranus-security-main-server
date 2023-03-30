import logging
import sys

import cv2
from typing import List


IS_LOG = True
logger = logging.getLogger("Streamer")

if IS_LOG:
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    logger.propagate = False


class RealTimeStreamer:
    def __init__(self, camera_ids: List[int]):
        self.camera_ids = camera_ids
        self.vids = [cv2.VideoCapture(i) for i in self.camera_ids]
        for i in range(len(self.vids)):
            if not self.vids[i].isOpened():
                logger.error(f"[STREAMER] Can't open camera {i}")
        self.last_frame = None

    def read_frame(self):
        cam2frame = {}
        for i in range(len(self.vids)):
            ret, frame = self.vids[i].read()

            if not ret:
                logger.error(f"[STREAMER] ERROR ON CAMERA FRAMES READ")
            else:
                cam2frame[self.camera_ids[i]] = frame
        self.last_frame = cam2frame
        return cam2frame

    def get_last_frame(self):
        return self.last_frame

    def __del__(self):
        for vid in self.vids:
            vid.release()
