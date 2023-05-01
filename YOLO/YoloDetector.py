import os

import cv2
import torch
from pathlib import PosixPath

from YOLO.yolov5.utils.dataloaders import LoadImages
from YOLO.yolov5.utils.plots import Annotator, colors
from YOLO.yolov5.utils.torch_utils import select_device
from YOLO.yolov5.models.common import DetectMultiBackend
from YOLO.yolov5.utils.general import check_img_size, non_max_suppression, scale_boxes
from YOLO.yolov5.utils.general import Profile


class YoloDetector:
    def __init__(self):
        self.inference_size = (640, 640)
        print(os.getcwd())
        self.weights_path = os.path.join("..", "YOLO", "yolov5", "runs", "train", "exp13", "weights", "best.pt")
        self.device = select_device(0)
        self.data = PosixPath("../YOLO/yolov5/data/coco128.yaml")
        self.model = DetectMultiBackend(self.weights_path,
                                        device=self.device,
                                        data=self.data,
                                        fp16=False,
                                        dnn=False)
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt
        self.imgsz = check_img_size(self.inference_size, s=self.stride)
        self.model.warmup(imgsz=(1 if self.pt or self.model.triton else 1, 3, *self.imgsz))
        self.confidence_threshold = 0.25
        self.seen, self.windows, self.dt = 0, [], (Profile(), Profile(), Profile())

    def predict(self, image):
        path = "frame.jpg"
        cv2.imwrite(path, image)
        dataset = LoadImages(path, img_size=self.imgsz, stride=self.stride, auto=self.pt,
                             vid_stride=1)
        for path, im, im0s, vid_cap, s in dataset:
            with self.dt[0]:
                im = torch.from_numpy(im).to(self.model.device)
                im = im.half() if self.model.fp16 else im.float()  # uint8 to fp16/32
                im /= 255  # 0 - 255 to 0.0 - 1.0
                if len(im.shape) == 3:
                    im = im[None]
            with self.dt[1]:
                pred = self.model(im, augment=False, visualize=False)

            # NMS
            with self.dt[2]:
                pred = non_max_suppression(pred, self.confidence_threshold,
                                           0.45, None, False, max_det=10)
            for i, det in enumerate(pred):
                annotator = Annotator(image, line_width=2, example=str(self.model.names))
                labels = []
                if len(det):
                    det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], image.shape).round()

                    for *xyxy, conf, cls in reversed(det):
                        c = int(cls)
                        labels.append(self.model.names[c])
                        label = f'{self.model.names[c]} {conf:.2f}'
                        annotator.box_label(xyxy, label, color=colors(c, True))
                return annotator.result(), labels
