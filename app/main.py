from app.controller.controller import *
from app.config.ApiConfig import ApiConfig
# from datetime import datetime, timedelta
# from typing import Union

# from requests import request
# from http import cookies

from fastapi import FastAPI  # , Response, Cookie, Request, Depends
# from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates

api = FastAPI()
api.include_router(UserController.router)

config = ApiConfig()


@api.get("/")
async def main():
    return ApiConfig.apiInfo
