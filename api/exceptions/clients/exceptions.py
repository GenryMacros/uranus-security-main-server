
class ClientExists(Exception):
    def __init__(self, message="Client with same username already exists"):
        self.message = message
        super().__init__(self.message)


class ClientNotFound(Exception):
    def __init__(self, message="Can't find info about asked client in database"):
        self.message = message
        super().__init__(self.message)


class SignupFailed(Exception):
    def __init__(self, message="Failed to signup"):
        self.message = message
        super().__init__(self.message)


class InvalidCredentials(Exception):
    def __init__(self, message="Invalid login or password provided"):
        self.message = message
        super().__init__(self.message)


class InvalidTokens(Exception):
    def __init__(self, message="Invalid refresh or jwt token"):
        self.message = message
        super().__init__(self.message)


class TokenIsExpired(Exception):
    def __init__(self, message="Token is expired"):
        self.message = message
        super().__init__(self.message)
