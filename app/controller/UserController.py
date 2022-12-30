import datetime
from fastapi import APIRouter, Depends, Request, Response, HTTPException
from ..models.User import User, UserLogin
from ..classes.Auth import Auth
from ..classes.Cookie import Cookie
from ..data.UserData import UserDataAccess
from cryptography.fernet import Fernet
from ..service.UserService import UserService
from app.classes.APIException import APIException
from app.classes.Utils import Utils
from app.config.ApiConfig import ApiConfig
from app.service.MailService import MailService, MailType

router = APIRouter()
auth = Auth()
db = UserDataAccess()
cookie = Cookie()
service = UserService()
utils = Utils()
config = ApiConfig()
mail = MailService()


@router.post("/user/login/")
async def login(login: UserLogin, response: Response, request: Request):
    """
    Login the user in platform retriving a HttpOnly Cookie with the user access token
    - @login : An email and password as UserLogin
    """

    try:

        if (cookie.HttpCookieOnlyExists(request)):
            return True

        dbuser = service.Login(login.email)

        if (not dbuser.active):
            return False

        if (not dbuser.password is None):
            auth.PasswordIsCorrect(
                dbuser.userKey, dbuser.password, login.password)

        token = auth.GenerateToken(dbuser.id, dbuser.email, dbuser.username)

        cookie.GetCookie(token, response)

        dbuser.lastaccessday = datetime.datetime.now()

        service.Update(dbuser)

        return True

    except APIException as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    finally:
        dbuser = None


@router.post("/user/logout/")
async def logout(request: Request, response: Response):
    """
    Remove the user logged HttpOnlyCookie
    - login : An email and password as UserLogin
    """

    if (cookie.HttpCookieOnlyExists(request)):
        response.delete_cookie(key=auth.tokenKey)
        return {"status": True, 'message': 'Good bye'}
    else:
        response.status_code = 400
        return {"status": False, 'message': "Login doesn't exists"}


@router.post("/user/signup/")
async def create(user: User):
    """
    Allow to create an user account
    - @user : An User model with all required properties to store in DB
    """

    try:

        if (not ApiConfig.apiAllowActivation):
            raise APIException(400, "Activation not allowed")

        if (not user.password):
            raise APIException(400, "Password it's required")

        if (not user.password is None):
            if (not utils.PasswordValidate(user.password)):
                raise APIException(400, "User password incorrect properties")

        key = Fernet.generate_key()
        fer = Fernet(key)
        encryptedPassword = fer.encrypt(user.password.encode())

        result = service.Create(user, key.decode(
            'utf-8'), encryptedPassword.decode('utf-8'))

        if (result and ApiConfig.apiMailConfig['active']):
            print("Registro por email activo")
            user.id = result
            if (ApiConfig.apiRegisterByAdminFirst):
                mail.Send(mailType=MailType.USER_NEW_BY_ADMIN, user=user)
            else:
                mail.Send(mailType=MailType.USER_NEW, user=user)

        return result

    except APIException as e:
        raise HTTPException(status_code=e.code, detail=e.message)


@router.get("/user/profile/{userGuid}/")
async def read(userGuid: str, request: Request, response: Response, headerCookie: dict = Depends(cookie.HttpCookieOnlyExists)):
    """
    Gets user profile data (does not show password and key)
    - userGuid : The uniqueidentifier from user
    """

    if (not headerCookie):
        cookie.ThrowCookieMustExistsError()
    else:
        user = service.Read(userGuid)

        if (not user is None):
            user.password = None
            user.userKey = ''

        return user


@router.post("/user/update/")
async def update(user: User, request: Request, response: Response, headerCookie: dict = Depends(cookie.HttpCookieOnlyExists)):
    """
    Updates user profile
    - @user : An User model with all required properties
    """

    if (not headerCookie):
        cookie.ThrowCookieMustExistsError()
    else:
        result = service.Update(user)
        return result


@router.post("/user/delete/{userGuid}/")
async def delete(userGuid: str, request: Request, response: Response, headerCookie: dict = Depends(cookie.HttpCookieOnlyExists)):
    """
    Deletes the user from platform, bases on his/her guid and removes Cookie-Only
    - @userGuid : The uniqueidentifier from user
    """

    if (not headerCookie):
        cookie.ThrowCookieMustExistsError()
    else:
        if (cookie.HttpCookieOnlyExists(request)):
            response.delete_cookie(key=auth.tokenKey)

        result = service.Delete(userGuid)

        if (result):
            mail.Send(mailType=MailType.USER_DELETE, user=result)

        return True


@router.get("/user/activate/{userGuid}/")
async def activate(userGuid: str, request: Request, response: Response) -> bool:
    """
    Activate user with Guid
    - userGuid : The uniqueidentifier from user
    """

    if (not ApiConfig.apiAllowActivation):
        raise APIException(400, "Activation not allowed")

    result = service.Activate(userGuid)
    return result
