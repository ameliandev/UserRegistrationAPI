from ..data.UserData import UserDataAccess
from ..models.User import User


class UserService:
    """
    Manage calls between controller and data
    """

    def __init__(self) -> None:
        pass

    def Login(self, value: str) -> User:

        try:
            db = UserDataAccess()
            return db.Read(value)
        except Exception as e:
            raise e
        finally:
            db = None

    def Create(self, user: User, userKey: str, encryptedPassword: str) -> str:
        try:
            db = UserDataAccess()
            return db.Create(user, userKey, encryptedPassword)
        except Exception as e:
            raise e
        finally:
            db = None

    def Read(self, userGuid: str) -> User:
        try:
            db = UserDataAccess()
            return db.Read(userGuid)
        except Exception as e:
            raise e
        finally:
            db = None

    def Update(self, user: User) -> bool:
        try:
            db = UserDataAccess()
            return db.Update(user)
        except Exception as e:
            raise e
        finally:
            db = None

    def Delete(self, userGuid: str) -> User | None:
        try:
            db = UserDataAccess()
            return db.Delete(userGuid)
        except Exception as e:
            raise e
        finally:
            db = None

    def Activate(self, userGuid: str) -> bool:
        try:
            db = UserDataAccess()
            return db.Activate(userGuid)
        except Exception as e:
            raise e
        finally:
            db = None
