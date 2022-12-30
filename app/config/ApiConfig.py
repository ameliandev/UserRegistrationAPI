# import whois
import socket


class ApiConfig():

    apiInfo = {
        'name': 'User Account API Registration',
        'description': 'A simple Python API to manage a user platform registration, login, logout, delete, etc. connected with a MySQL Database',
        'author': 'Adrián Melián',
        'site': 'http://amelian.eu',
        'version': '1.0.0',
        'host': socket.gethostbyname(socket.gethostname())
    }

    # Allow platform user account activation
    apiAllowActivation = True
    # When a user registers in platform, this flag allow that the account activation will be activated by admins or by user directly.
    apiRegisterByAdminFirst = False
    apiDomain = '127.0.0.1'
    apiCookieHttpOnlyExpires = 120  # 2min
    apiCookiePath = '/'

    apiMailConfig = {
        'active': True,
        'smtp': {
            'server': '',
            'port': '',
            'accountEmail': '',
            'accountName': '',
            'accountPassword': ''
        },
        'mailFrom': '',
        'mailsTo': ['maile1@gmail.com', 'mail1@testcom.com'],
        'mailType': {
            'userNewAdmin': {
                'subject': '',
                'body': """\
                    <html>
                    <body>
                    </body>
                    </html>
                """
            },
            'userNew': {
                'subject': '',
                'body': """\
                    <html>
                    <body>
                    </body>
                    </html>
                """
            },
            'userDelete': {
                'subject': '',
                'body': """\
                    <html>
                    <body>
                    </body>
                    </html>
                """
            },
            'systemError': {
                'subject': '',
                'body': ''
            }
        }

    }

    def __init__(self) -> None:
        pass
