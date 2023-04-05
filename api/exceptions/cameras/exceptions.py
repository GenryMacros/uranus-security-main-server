
class CamerasNotFound(Exception):
    def __init__(self, message="Can't find info about asked camera in database"):
        self.message = message
        super().__init__(self.message)
