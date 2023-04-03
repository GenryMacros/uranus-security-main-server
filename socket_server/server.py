import logging
import sys
from typing import Dict

from aiohttp import web

import socketio
from ai.background_subtractor import BackgroundSubtractor
from ai.streamer import RealTimeStreamer
from socket_server.utils.recorder import Recorder
from socket_server.overseer import Overseer
from socket_server.schemas.user import UserAuthData, GetCamerasResponse, AuthenticateResponse

IS_LOG = True
logger = logging.getLogger(__name__)

if IS_LOG:
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    # do not print twice in sys.stdout
    logger.propagate = False


HOST = "localhost"
PORT = 8086
sio = socketio.AsyncServer(async_mode='aiohttp')
cameras = [0]
streamer = RealTimeStreamer(cameras)
subtractor = BackgroundSubtractor()
app = web.Application()
sio.attach(app)
last_cam2frame = None
recorder = Recorder(cameras)
users_info_map: Dict[str, UserAuthData] = {}


@sio.event
async def get_cameras(sid):
    logger.info(f"[SERVER] Client {sid} called GET_CAMERAS")
    response: GetCamerasResponse = GetCamerasResponse()
    response_dict = dict(cameras=[], success=True)
    if users_info_map.get(sid, None) is None or not users_info_map[sid].is_authenticated():
        logger.info(f"[SERVER] Client {sid} GET_CAMERAS rejected")
        response_dict["success"] = False
    else:
        for cam in cameras:
            response_dict["cameras"].append(dict(cam_id=cam, is_online=True))
    return response.dump(response_dict)


@sio.event
async def connect(sid, environ):
    logger.info(f"[SERVER] New client connected: {sid} ")
    users_info_map[sid] = UserAuthData(None, None, None, None)
    await sio.emit('my_response', data={'schemas': "aaaa"}, to=sid)


@sio.event
async def authenticate(sid, data):
    logger.info(f"[SERVER] Client {sid} authentication started")
    response: AuthenticateResponse = AuthenticateResponse(False)

    try:
        user_data = UserAuthData.load(data)
        users_info_map[sid] = user_data

        response.success = True
        logger.info(f"[SERVER] Client {sid} authenticated successfully")
    except Exception as e:
        logger.error(f"[SERVER] Exception occurred: {e}")
    return response.dump()


async def read_frame(sid):
    global last_cam2frame
    if last_cam2frame is not None:
        sent_cam2frame = streamer.read_frame()[0].tolist()
    else:
        sent_cam2frame = None
    await sio.emit("FRAMES", data={
        "frames": {
            "buffer": sent_cam2frame,
            "id": 0
        }
    }, to=sid)


@sio.event
def disconnect(sid):
    users_info_map.pop(sid)
    logger.info(f"[SERVER] Client {sid} disconnected")


if __name__ == '__main__':
    config_path = "configs/overseer_config.json"
    overseer = Overseer(sio, config_path)
    overseer.start_loop()
    web.run_app(app, host=HOST, port=PORT)
