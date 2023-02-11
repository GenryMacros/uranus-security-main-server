from marshmallow_dataclass import dataclass


@dataclass
class LoginResponse:
    id: int
    public_key: str
    auth_token: str
    refresh_token: str


@dataclass
class ClientSignup:
    username: str
    password: str
    email: str


@dataclass
class ClientConfirmationResponse:
    success: bool


@dataclass
class ClientConfirmation:
    token: str


@dataclass
class ClientSecretSchema:
    password_hash: str
    password_salt: str
    user_private: str
    user_public: str


@dataclass
class ClientTokenRefresh:
    user_id: int
    jwt: str
    refresh: str


@dataclass
class ClientPasswordData:
    password_hash: str
    password_salt: str


@dataclass
class ClientKeyPair:
    public: str
    private: str


@dataclass
class ClientCredentials:
    login: str
    password: str


@dataclass
class ClientContactSchema:
    email: str
    phone: str
    telegram: str


@dataclass
class ClientLocationSchema:
    country: str
    city: str
    addr: str
    ind: int
