from app.classes.Auth import Auth
from app.config.ApiConfig import ApiConfig
from fastapi import Request, Response, HTTPException


class Cookie():

    key = Auth.tokenKey
    value: str
    max_age = ApiConfig.apiCookieHttpOnlyExpires
    expires = ApiConfig.apiCookieHttpOnlyExpires
    path = ApiConfig.apiCookiePath
    secure = False
    httponly = True
    domain = ApiConfig.apiDomain

    def HttpCookieOnlyExists(self, request: Request):
        """
        Check if HttpOnly Cookie exists in request header
        """

        if self.key in request.cookies:
            return True
        else:
            return False

    def GetCookie(self, token: str, response: Response):
        """
        Generates a new Cookie and add it to the response
        """

        response.set_cookie(
            key=self.key,
            value=token,
            max_age=self.max_age,
            expires=self.expires,
            path=self.path,
            secure=self.secure,
            httponly=self.httponly,
            samesite="strict",
            domain=self.domain
        )

    def ThrowCookieMustExistsError(self):
        raise HTTPException(status_code=401, detail="User not logged")
