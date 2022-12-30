import smtplib
# import ssl
from enum import Enum
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid
from app.config.ApiConfig import ApiConfig


class MailType(Enum):
    SYSTEM_ERR = 0
    USER_NEW_BY_ADMIN = 1
    USER_NEW = 2
    USER_DELETE = 3


class MailConfig():
    Port: int
    Server: str
    Password: str
    Account: str
    From: str
    To = []
    Subject: str
    Body: str

    def __init__(self) -> None:
        self.Port = ''
        self.Server = ''
        self.Password = ''
        self.Account = ''
        self.From = ''
        self.To = []
        self.Subject = ''
        self.Body = ''


class Mail():

    def __init__(self) -> None:
        pass

    def _createMessage(self, mailFrom, mailsTo, mailSubject, mailBody):

        msg = MIMEMultipart("alternative")
        msg["Subject"] = mailSubject
        msg["From"] = mailFrom
        msg["To"] = mailsTo
        msg.add_header('Content-Type', 'text/html')
        msg.add_header('message-id', make_msgid(domain=ApiConfig.apiDomain))

        part = MIMEText(mailBody, "html")

        msg.attach(part)

        return msg

    def Send(self, config: MailConfig):

        SMTP_CODE_OK = '235'
        SMTP_MSG_OK = 'Authentication successful'
        SMTP_CODE_ERROR = '535'
        SMTP_MSG_ERROR = 'Email authentication failed'

        try:

            with smtplib.SMTP(config.Server, config.Port) as server:

                server.ehlo()
                server.starttls()
                server.ehlo()

                reply = server.login(config.Account, config.Password)

                replyCode = str(reply).replace(
                    '(', '').replace(')', '').split(',')[0]
                replyMessage = str(reply).replace(
                    '(', '').replace(')', '').split(',')[1]

                if (replyCode != SMTP_CODE_OK or replyMessage.find(SMTP_MSG_OK) == -1):
                    server.close()
                    raise Exception(SMTP_MSG_ERROR)

                for mail in config.To:

                    message = self._createMessage(
                        config.From, mail, config.Subject, config.Body)
                    sendError = server.sendmail(
                        config.From, mail, message.as_string())

                    if (sendError):
                        raise Exception(sendError)

                server.close()

        except Exception as e:
            raise e
        # finally:
