from enum import Enum


class EventTypeOut(Enum):
    ASK_AUTHENTICATE = "ask_authenticate"
    REAUTH_HAPPENED = "REAUTH_HAPPENED"
    FRAMES = "frames"
    INVASION = "invasion"


class EventTypeIn(Enum):
    GET_CAMERAS = "get_cameras"
    AUTHENTICATE = "authenticate"
    READ_FRAME = "read_frame"
