from pydantic import BaseModel


class User(BaseModel):
    id: str = ''
    email: str = ''
    password: str | None = ''
    name: str = ''
    surname: str = ''
    username: str = "{0} {1}".format(name, surname)
    birthdate: str = ''
    startdate: str = ''
    enddate: str = ''
    represents: str = ''
    details: str = ''
    phone: str = ''
    image: str = ''
    active: bool = False
    isadmin: bool = False
    emailconfirmation: bool = False
    lastaccessday: str = ''
    userKey: str = ''


# REQUEST MODELS:---------------------


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    """Model to create a new User"""
    email: str
    name: str
    surname: str
    password: str
    birthdate: str
    represents: str
    phone: str
    captcha: str

# END REQUEST MODELS:---------------------
