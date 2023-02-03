

class InvalidRequest(Exception):
    def __init__(self, message="Request has invalid structure"):
        self.message = message
        super().__init__(self.message)
        