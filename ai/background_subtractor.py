import copy
import time
from typing import Dict

import cv2
import numpy as np

from ai.streamer import RealTimeStreamer


class BackgroundSubtractor:

    def __init__(self, dramatic_change_thresh=0.01):
        self.background = None
        self.background_update_interval = 60 * 30
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        self.dramatic_change_thresh = dramatic_change_thresh

    def subtract(self, cam2frame) -> Dict[str, np.array]:
        result = copy.deepcopy(cam2frame)
        for id, frame in result.items():
            fgmask = self.fgbg.apply(frame)
            kernel = np.ones((5, 5), np.uint8)
            fgmask = cv2.erode(fgmask, kernel, iterations=2)
            fgmask = cv2.dilate(fgmask, kernel, iterations=2)
            result[id] = fgmask
        return result

    def is_dramatically_changed(self, frame):
        return np.count_nonzero(frame) >= (len(frame) * len(frame[0])) * self.dramatic_change_thresh


if __name__ == '__main__':
    streamer = RealTimeStreamer([0])
    subtractor = BackgroundSubtractor()
    while True:
        cam2frame = streamer.read_frame()
        cam2frame = subtractor.subtract(cam2frame)
        for id, frame in cam2frame.items():
            cv2.imshow('frame', frame)
            if subtractor.is_dramaticaly_changed(frame):
                print("ROBBERYY")
            if cv2.waitKey(1):
                break
