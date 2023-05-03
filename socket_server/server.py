import base64
import logging
import sys
from typing import Dict

from aiohttp import web

import socketio
from ai.background_subtractor import BackgroundSubtractor
from socket_server.events import EventTypeOut
from socket_server.requester import Requester
from socket_server.schemas.cameras import CamInfo
from socket_server.utils.recorder import Recorder
from socket_server.overseer import Overseer
from socket_server.schemas.user import UserAuthData, GetCamerasResponse, AuthenticateResponse, TokenRefresh

IS_LOG = True
logger = logging.getLogger(__name__)

if IS_LOG:
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    # do not print twice in sys.stdout
    logger.propagate = False


HOST = "0.0.0.0"
PORT = 8086
sio = socketio.AsyncServer(async_mode='aiohttp', max_http_buffer_size=3000000)
cameras = [0]
app = web.Application()
requester = Requester(UserAuthData(None, None, None, None))
sio.attach(app)
last_cam2frame = None
recorder = Recorder(cameras)
cam_infos: Dict[int, CamInfo] = {}


@sio.event
async def get_cameras(sid):
    logger.info(f"[SERVER] Client {sid} called GET_CAMERAS")
    response: GetCamerasResponse = GetCamerasResponse()
    response_dict = dict(cameras=[], success=True)
    if not requester.auth_data.is_authenticated():
        logger.info(f"[SERVER] Client {sid} GET_CAMERAS rejected")
        response_dict["success"] = False
    else:
        for _, info in cam_infos.items():
            response_dict["cameras"].append(dict(cam_name=info.local_name,
                                                 cam_id=info.back_id,
                                                 is_online=info.is_online))
    return response.dump(response_dict)


@sio.event
async def connect(sid, environ):
    logger.info(f"[SERVER] New client connected: {sid} ")
    overseer.client_sid = sid
    await sio.emit(EventTypeOut.ASK_AUTHENTICATE.value, to=sid)


@sio.event
async def authenticate(sid, data):
    logger.info(f"[SERVER] Client {sid} authentication started")
    response: AuthenticateResponse = AuthenticateResponse(False)
    cam_infos.clear()
    try:
        user_data = UserAuthData.load(data)
        requester.auth_data = user_data
        registered_cameras = requester.get_cameras(requester.auth_data)
        server_registered_cams = [int(cam) for cam in registered_cameras.cam_names]
        non_registered = set(cameras) - set(server_registered_cams)
        if non_registered:
            requester.register_cameras(non_registered)
        full_cams_list = requester.get_cameras(requester.auth_data)
        for cam in full_cams_list.cam_names:
            if cam in cameras:
                is_online = True
            else:
                is_online = False
            cam_infos[cam] = CamInfo(cam,
                                     full_cams_list.cam_ids[full_cams_list.cam_names.index(cam)],
                                     is_online)
        overseer.cam_infos = cam_infos
        response.success = True
        logger.info(f"[SERVER] Client {sid} authenticated successfully")
    except Exception as e:
        logger.error(f"[SERVER] Exception occurred: {e}")
    return response.dump()


@sio.event
async def refresh_auth_data(sid, data):
    logger.info(f"[SERVER] Client {sid} reauth started")
    try:
        refresh_data = TokenRefresh.load(data)
        requester.auth_data.token = refresh_data.token
        logger.info(f"[SERVER] Client {sid} reauth finished")
    except Exception as e:
        logger.error(f"[SERVER] Exception occurred on reauth: {e}")


@sio.event
async def read_frames(sid):
    import imageio
    imageio.imwrite('outfile.jpg', overseer.get_last_cam2frame()[0])
    with open("outfile.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    await sio.emit(EventTypeOut.FRAMES.value, data={
        "frames": [{
            "buffer": encoded_string,
            "id": 0
        }]
    }, to=sid)


@sio.event
def disconnect(sid):
    logger.info(f"[SERVER] Client {sid} disconnected")


if __name__ == '__main__':
    config_path = "configs/overseer_config.json"
    overseer = Overseer(sio, cam_infos, requester, config_path)
    overseer.loop_proc.start()
    web.run_app(app, host=HOST, port=PORT)
