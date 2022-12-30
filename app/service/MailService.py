from email.utils import formataddr
from app.classes.Mail import MailConfig, Mail, MailType
from app.models.User import User
from app.config.ApiConfig import ApiConfig


class MailService:
    """
    Class to send SMTP emails
    """

    mailType: MailType
    config: MailConfig
    mail: Mail
    apiMailConfig = ApiConfig.apiMailConfig

    def __init__(self) -> None:

        self.mail = Mail()
        self.config = MailConfig()

        self.config.Account = self.apiMailConfig['smtp']['accountEmail']
        self.config.Password = self.apiMailConfig['smtp']['accountPassword']
        self.config.Port = self.apiMailConfig['smtp']['port']
        self.config.Server = self.apiMailConfig['smtp']['server']

    def Send(self, mailType: int, user: User = None) -> bool:
        """
        Send an email with user data.
        - user: An User data model with all user data
        """

        if (mailType in MailType):
            if (mailType is MailType.USER_NEW_BY_ADMIN):
                config = self._GetNewUserByAdminMailConfig(user)
                self.mail.Send(config)
                return True

            if (mailType is MailType.USER_NEW):
                config = self._GetNewUserMailConfig(user)
                self.mail.Send(config)
                return True

            if (mailType is MailType.USER_DELETE):
                config = self._GetDeleteUserMailConfig(user)
                self.mail.Send(config)
                return True
        else:
            return False

    def _GetNewUserByAdminMailConfig(self, user: User) -> MailConfig:

        try:

            self.config.From = formataddr(
                (self.apiMailConfig['smtp']['accountName'], self.apiMailConfig['mailFrom']))
            self.config.To = self.apiMailConfig['mailsTo']
            self.config.Subject = self.apiMailConfig['mailType']['userNewAdmin']['subject']
            self.config.Body = self.apiMailConfig['mailType']['userNewAdmin']['body']

            self.config.Body = self.config.Body.format(
                "{0} {1}".format(user.name, user.surname), user.email, user.details, ApiConfig.apiDomain, user.id)

            return self.config

        except Exception as e:
            raise e
        finally:
            db = None

    def _GetNewUserMailConfig(self, user: User) -> MailConfig:

        try:

            self.config.From = formataddr(
                (self.apiMailConfig['smtp']['accountName'], self.apiMailConfig['mailFrom']))
            self.config.To = self.apiMailConfig['mailsTo']
            self.config.Subject = self.apiMailConfig['mailType']['userNew']['subject']
            self.config.Body = self.apiMailConfig['mailType']['userNew']['body']

            usernNAME = "{0} {1}".format(user.name, user.surname)

            self.config.Body = self.config.Body.format(usernNAME, user.id)

            return self.config

        except Exception as e:
            raise e
        finally:
            db = None

    def _GetDeleteUserMailConfig(self, user: User) -> MailConfig:

        try:

            self.config.From = formataddr(
                (self.apiMailConfig['smtp']['accountName'], self.apiMailConfig['mailFrom']))
            self.config.To = self.apiMailConfig['mailsTo']
            self.config.Subject = self.apiMailConfig['mailType']['userDelete']['subject']
            self.config.Body = self.apiMailConfig['mailType']['userDelete']['body']

            fullName = "{0} {1}".format(user.name, user.surname)
            self.config.Body = self.config.Body.format(fullName, user.email)

            return self.config

        except Exception as e:
            raise e
        finally:
            db = None
