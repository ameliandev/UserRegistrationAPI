import jwt
from ..models.User import User
from cryptography.fernet import Fernet


class Auth():
    tokenKey = 'user_Token'
    tokenSecret = ''
    tokenAlgorithm = 'HS256'

    def __init__(self):
        return None

    def GenerateToken(self, Id: str, Email: str, UserName: str):
        """
        Generates new user token
        - @Id: An user uniqueidentifier as Guid
        - @Email: The user email
        - @UserName: The user name
        """

        return jwt.encode(
            payload={
                "guid": Id,
                "email": Email,
                "username": UserName
            },
            key=self.tokenSecret,
            algorithm=self.tokenAlgorithm
        )

    def PasswordIsCorrect(self, userKey: str, userPassword: str, loginPassword: str):
        """
        Check if the request password it's the same as the user password
        """

        userPassword = Fernet(userKey.encode(
            "utf-8")).decrypt(userPassword.encode("utf-8")).decode()

        if (userPassword != loginPassword):
            raise Exception(
                {"code": 401, "message": "Email or password incorrect"})

        return True
