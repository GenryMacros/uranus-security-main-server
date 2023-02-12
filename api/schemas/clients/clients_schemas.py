
from marshmallow_dataclass import dataclass


@dataclass
class ClientPasswordData:
    password_hash: str
    password_salt: str


@dataclass
class ClientKeyPair:
    public: str
    private: str
