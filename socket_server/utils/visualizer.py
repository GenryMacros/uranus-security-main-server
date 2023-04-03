import cv2
import numpy as np
import webcolors


class BaseFrame:
    DEFAULT_FONT = cv2.FONT_HERSHEY_SIMPLEX
    DEFAULT_STYLE = cv2.LINE_AA
    DEFAULT_COLOR = (0, 255, 0)

    DEFAULT_Y_DRAW_STEP = 120
    NUM_EVENTS_FOR_PAGE = 18
    DEFAULT_THICKNESS = 4
    DEFAULT_FONT_SCALE = 2
    DEFAULT_PAD = (30, 30)

    def __init__(self, resolution=(540, 960), frame_name="default_frame", scale=0.5):
        self.height, self.width = resolution
        self.scale = scale
        self.resolution = (self.height, self.width)
        self.frame_name = frame_name
        self.frame = None
        self.draw_pointer = list(self.DEFAULT_PAD)

    def make_blackboard(self):
        self.frame = np.zeros([self.height, self.width, 3], dtype=np.uint8)
        self.draw_pointer = list(self.DEFAULT_PAD)

    def set_draw_pointer(self, x=None, y=None):
        if x is None:
            x = self.draw_pointer[0]
        if y is None:
            y = self.draw_pointer[1]
        self.draw_pointer = [x, y]

    def draw_text(self, text, **kwargs):
        scale = kwargs.get("scale", self.scale)
        if isinstance(scale, tuple):
            mean_scale = np.mean(scale)
        else:
            mean_scale = scale
            scale = (scale, scale)

        font = kwargs.get("font", self.DEFAULT_FONT)
        font_scale = kwargs.get("font_scale", self.DEFAULT_FONT_SCALE * mean_scale)
        color = kwargs.get("color", self.DEFAULT_COLOR)
        thickness = kwargs.get("thickness", self.DEFAULT_THICKNESS * mean_scale)
        style = kwargs.get("style", self.DEFAULT_STYLE)
        y_pad = kwargs.get("y_pad", int(self.DEFAULT_Y_DRAW_STEP * mean_scale))
        if "draw_pointer" not in kwargs:
            draw_pointer = tuple(self.draw_pointer)
            self.draw_pointer[1] += y_pad
        else:
            draw_pointer = kwargs["draw_pointer"]
            draw_pointer = (int(draw_pointer[0] * scale[0]), int(draw_pointer[1] * scale[1]))

        thickness = int(np.round(thickness))
        text_length = cv2.getTextSize(text=text, fontFace=font, fontScale=font_scale, thickness=int(thickness))[0][0]
        frame_length = self.frame.shape[1]
        if text_length > frame_length:
            ratio = text_length / len(text) + 1
            for i in range(text_length // frame_length + 1):
                cv2.putText(self.frame, text[int(i * frame_length / ratio): int((i + 1) * frame_length / ratio)],
                            draw_pointer, font, font_scale, color, thickness, style)
                draw_pointer = tuple(self.draw_pointer)
                self.draw_pointer[1] += y_pad
        else:
            cv2.putText(self.frame, text, (self.draw_pointer[0], 80), font, font_scale, color, thickness, style)

    def draw_frame_name(self):
        self.draw_text(self.frame_name)

    def draw_rectangles(self, bboxes):
        for box in bboxes:
            cv2.rectangle(self.frame, (box[0], box[1]), (box[2], box[3]), self.DEFAULT_COLOR, self.DEFAULT_THICKNESS)

    def draw_events(self, events, **kwargs):
        size = len(events)
        from_last_some_ind = size % self.NUM_EVENTS_FOR_PAGE + 1
        for action in events[-from_last_some_ind:]:
            kwargs["color"] = self.get_color("white")
            self.draw_text(str(action), **kwargs)

    @classmethod
    def get_color(cls, color_name):
        webcolor = webcolors.name_to_rgb(color_name)[::-1]
        return webcolor

    def show(self):
        cv2.imshow(self.frame_name, self.frame)

    @classmethod
    def resize(cls, frame, resolution, preserve_proportion=False):
        if frame.shape[1] != resolution[1] and frame.shape[0] != resolution[0]:
            k = tuple(resolution[i] / frame.shape[i] for i in (1, 0))
            if preserve_proportion:
                k = min(k)
                target_size = tuple(int(round(frame.shape[i] * k)) for i in (1, 0))
                new_frame = np.zeros(resolution + (3,), dtype=np.uint8)
                new_frame[:target_size[1], :target_size[0]] = cv2.resize(frame, target_size)
                frame = new_frame
                k = (k, k)
            else:
                frame = cv2.resize(frame, resolution[::-1])
        else:
            k = (1., 1.)
        return frame, k

    def get_resized(self, resolution):
        return self.resize(self.frame, resolution)[0]

    def clean(self):
        self.draw_pointer = list(self.DEFAULT_PAD)
        self.frame.fill(0)

    def draw_actions(self, actions_list):
        font_scale, text_thickness, default_y_pad = 2, 2, 60
        size = len(actions_list)
        from_last_some_ind = size % self.NUM_EVENTS_FOR_PAGE + 1
        for action in actions_list[-from_last_some_ind:]:
            color = self.get_color("white")
            self.draw_text(str(action), color=color, font_scale=font_scale, thickness=text_thickness,
                           y_pad=default_y_pad)


class CamFrame(BaseFrame):
    DEFAULT_HAND_RADIUS = 50
    DEFAULT_NEAR_HH_PROD_PAD = 25
    KEYPOINT_PAIRS = [
        (0, 1), (0, 2), (1, 3), (2, 4), (5, 6), (5, 7), (7, 9), (6, 8), (8, 10), (17, 11),
        (17, 12), (11, 13), (12, 14), (13, 15), (14, 16)
    ]
    COLORS = [(158, 0, 99), (93, 1, 161), (213, 0, 42), (39, 0, 216), (252, 2, 3), (2, 0, 254)]
    LIMB_COLORS = {(4, 2): (232, 1, 22), (2, 0): (186, 0, 70), (0, 1): (126, 0, 130), (1, 3): (66, 0, 188),
                   (3, 5): (20, 0, 235)}
    KEYPOINTS_SIZE = 17
    KEYPOINT_CIRCLE_RADIUS = 6
    LIMB_THICKNESS = 2
    KEYPOINT_CONFIDENCE = 0.00001
    UPPER_BODY_KEYPOINT = [(5, 6), (5, 7), (7, 9), (6, 8), (8, 10)]
    DEFAULT_X_CARD_STEP = 300

    def __init__(self, resolution, frame_name, frame, scale=0.5):
        super().__init__(resolution, frame_name, scale)
        self.frame, self.scale = self.resize(frame, resolution)
        self.mean_scale = np.mean(self.scale)

    def draw_card(self, person_cards, y_pad=None):
        x_pad = self.DEFAULT_PAD[0]
        if y_pad is None:
            y_pad = self.draw_pointer[1]
        for basket_id, basket in person_cards.items():
            if isinstance(basket_id, tuple):
                show_name, uiid = basket_id
            else:
                show_name, uiid = basket_id, None
            self.set_draw_pointer(x=x_pad, y=y_pad)
            self.draw_text(f" {show_name} ")
            if uiid is not None:
                self.draw_text(f" {str(uiid)[:10]} ")
            for product_name, prod_num in basket.items():
                if isinstance(prod_num, list):
                    prod_num = len(prod_num)
                self.draw_text(
                    f"{product_name} {prod_num}",
                    color=(255, 255, 255), font_scale=0.8
                )
            x_pad += self.DEFAULT_X_CARD_STEP
        self.set_draw_pointer(y=0)


class CamFrame4(BaseFrame):

    def __init__(self, resolution, frame_name):
        super().__init__(resolution, frame_name)
        self.res_small = (self.height // 2, self.width // 2)
        self.cam_frames = []
        self.make_blackboard()

    def add(self, cam_frame):
        self.cam_frames.append(cam_frame)

    def get_frame_size(self):
        return len(self.cam_frames)

    def clean(self):
        super().clean()
        self.cam_frames = []

    def draw_combined(self):
        cam_size = self.get_frame_size()
        x_pad, y_pad = self.res_small[1], self.res_small[0]
        if cam_size > 0:
            self.frame[:y_pad, :x_pad] = self.cam_frames[0].get_resized(self.res_small)
        if cam_size > 1:
            self.frame[:y_pad, x_pad:] = self.cam_frames[1].get_resized(self.res_small)
        if cam_size > 2:
            self.frame[y_pad:, x_pad:] = self.cam_frames[2].get_resized(self.res_small)
        if cam_size > 3:
            self.frame[y_pad:, :x_pad] = self.cam_frames[3].get_resized(self.res_small)


class InvasionFrame(BaseFrame):
    y_pad_grid = 30
    x_pad_grid = 15
    y_pad = 40

    def __init__(self, id2status, resolution=(800, 800)):
        super().__init__(resolution, "Invasion")
        self.make_blackboard()
        cv2.putText(self.frame, "", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        x_coord = 0
        y_coord = 30
        for id, status in id2status.items():
            draw_coord = (x_coord, y_coord)
            x_coord += 150
            #y_coord += 50
            cv2.putText(self.frame, f"Is {id} invaded: {status}", draw_coord, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
