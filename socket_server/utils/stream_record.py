import os
from multiprocessing.pool import ThreadPool
from typing import Dict

import cv2
from numpy import ndarray


class StreamRecorder:
    REPLAY_FPS = 15
    VIDEO_FILE_PREFIX = "cam"

    def __init__(self, record_folder: str):
        self.record_folder = record_folder
        self.out = {}
        self.is_init = False
        self.tp = None
        self.frame_count = 0
        self.released = False

    def write_frames(self, frame, cam_id):
        if not self.is_init:
            self.is_init = True
            cam_ids = [cam_id]
            self.tp = ThreadPool(processes=len(cam_ids))

            os.makedirs(self.record_folder, exist_ok=True)

            resolution = frame.shape[:2][::-1]
            fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
            video_file_name = f"{self.VIDEO_FILE_PREFIX}.avi"
            video_file_path = os.path.join(self.record_folder, video_file_name)
            self.out[cam_id] = cv2.VideoWriter(video_file_path, fourcc, self.REPLAY_FPS, resolution)

        if self.is_init:
            frames_ordered = [frame]
            self.tp.starmap(self.write_static, zip(self.out.values(), frames_ordered))
            self.frame_count += 1

    @staticmethod
    def write_static(out: cv2.VideoWriter, frame: ndarray):
        out.write(frame)

    def release(self):
        if self.tp is not None:
            self.tp.close()
            self.tp.join()
        for cam_id, writer in self.out.items():
            self.out[cam_id].release()
        self.released = True
