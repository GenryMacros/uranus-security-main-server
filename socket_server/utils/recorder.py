import os
import time
from typing import List
from datetime import datetime
from stream_record import StreamRecorder


class Recorder:
    WAIT_BEFORE_RECORD_END = 2

    def __init__(self, cam_ids: List[int], record_path="../recorded"):
        self.record_path = record_path
        self.cam_ids = cam_ids
        self.is_record_started = {}
        self.records = {}
        self.end_called = {}
        for cam_id in self.cam_ids:
            self.is_record_started[cam_id] = False
            self.records[cam_id] = None

    def record(self, cam2frame):
        for cam_id, is_record in self.is_record_started.items():
            if is_record:
                self.records[cam_id].write_frames(cam2frame[cam_id], cam_id)

    def start_record(self, cam_id: int):
        if self.is_record_started.get(cam_id, None) is None:
            raise ValueError()
        elif self.is_record_started[cam_id]:
            return

        self.is_record_started[cam_id] = True
        dt_string = datetime.now().strftime("%Y-%m-%d %H-%M-%S").replace(' ', 'T')
        self.records[cam_id] = StreamRecorder(os.path.join(self.record_path, str(cam_id), dt_string))
        self.end_called[cam_id] = None

    def end_record(self, cam_id: int):
        if self.is_record_started.get(cam_id, None) is None:
            raise ValueError()
        elif not self.is_record_started[cam_id]:
            return
        if self.end_called[cam_id] is None:
            self.end_called[cam_id] = time.time()
        elif time.time() - self.end_called[cam_id] >= self.WAIT_BEFORE_RECORD_END:
            self.is_record_started[cam_id] = False
            self.records[cam_id].release()
