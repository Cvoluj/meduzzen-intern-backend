from passlib.context import CryptContext

class PasswordContext:
    SCHEMES = ['bcrypt']

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return CryptContext(schemes=PasswordContext.SCHEMES).verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return CryptContext(schemes=PasswordContext.SCHEMES).hash(password)

