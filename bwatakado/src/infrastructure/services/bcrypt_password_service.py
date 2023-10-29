import bcrypt

from bwatakado.src.application.interfaces.ipassword_service import IPasswordService


class BCryptPasswordService(IPasswordService):
    """BCryptPasswordService is a service that implements IPasswordService interface."""

    def __init__(self, salt: bytes):
        self.salt = salt

    def hash(self, password: str) -> str:
        return str(bcrypt.hashpw(password.encode('utf-8'), self.salt))

    def compare(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
