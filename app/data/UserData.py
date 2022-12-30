# from getpass import getpass
import mysql.connector
import datetime
from cryptography.fernet import Fernet
from ..models.User import User
from app.config.dbConfig import DBConfig
from app.classes.Utils import Utils
from app.classes.APIException import APIException

dbConfig = DBConfig()
utils = Utils()


class UserDataAccess:

    dbConnection = mysql.connector.connect(
        host=dbConfig.host,
        port=dbConfig.port,
        user=dbConfig.user,
        password=dbConfig.password,
        database=dbConfig.database
    )

    def __init__(self) -> None:
        pass

    def _ValidateLoginRequest(self, email: str):
        """
        # Validates login data
        #
        """

        if (not self.Exists(email)):
            raise APIException(404, "User not exists")

        if (not self.Confirmed(email)):
            raise APIException(
                401, "User account hasn't been confirmed by email")
        else:
            if (not self.Activated(email)):
                raise APIException(
                    401, "User not activated by administrators yet")

    def _ValidateCreateRequest(self, email: str, password: str | None) -> None:
        """
        # Validates user creation
        - user # Usuario a validar
        - db  # Clase de acceso a las peticiones de Usuario en la BBDD
        #
        """

        if (self.Exists(email)):
            raise APIException(400, "User alredy exists")

    def _ParseDate(self, date: datetime.datetime) -> str:
        """
        Returns a transformated date with a compatible DB value
        """

        if (date is None):
            return ''
        else:
            return str(date)

    def Connect(self):
        """
        Check if exists a active connection with DB
        """

        if not self.dbConnection.is_connected():
            self.dbConnection = mysql.connector.connect(
                host=dbConfig.host,
                port=dbConfig.port,
                user=dbConfig.user,
                password=dbConfig.password,
                database=dbConfig.database
            )

    def Close(self):
        """
        Close the active connection with DB
        """

        if self.dbConnection.is_connected():
            self.dbConnection.close()

    def Create(self, user: User, userKey: str, encryptedPassword: str) -> str:
        """
        Create a new register in User table and sets the key and the encrypted password
        - @user : An User model with all required properties.
        - @userKey : An user key generated with Fernet.generate_key() decoded as utf-8.
        - @encryptedPassword : An encrypted password generated with the Fernet key, decoded as utf-8.
        """

        guid: str = "00000000-0000-0000-0000-000000000000"

        try:
            if (user.password is None):
                raise APIException(400, "Password it's required")

            self._ValidateCreateRequest(user.email, user.password)

            if not self.dbConnection.is_connected():
                self.Connect()

            self.dbConnection.autocommit = False

            dbCursor = self.dbConnection.cursor()

            try:

                birthDate = datetime.datetime(int(user.birthdate.split(
                    '/')[2]), int(user.birthdate.split('/')[1]), int(user.birthdate.split('/')[0])).strftime('%Y-%m-%d %H:%M:%S')

                identifier = "SELECT id FROM User WHERE email = '{0}'".format(
                    user.email)
                insertQuery = "INSERT INTO User (email, password, name, surname, birthday, startdate, represents, details, phone, active, isAdmin, emailConfirmation) "
                insertValues = "VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}',{9},{10},{11})".format(
                    user.email, encryptedPassword, user.name, user.surname, birthDate, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user.represents, user.details, user.phone, 0, 0, 0)

                query = insertQuery + insertValues

                dbCursor.execute(query)

                query = identifier
                dbCursor.execute(query)
                records = dbCursor.fetchone()

                guid = str(records).replace("(", "").replace(
                    ")", "").replace(",", "").replace("'", "")

                query = "INSERT INTO UserKey (`userId`, `key`) VALUES ('{0}','{1}')".format(
                    guid, userKey)
                dbCursor.execute(query)

                self.dbConnection.commit()

            except mysql.connector.Error as e:
                raise e
            finally:
                dbCursor.close()
                self.Close()

        except APIException as ex:
            raise ex
        finally:
            pass

        return guid

    def Activate(self, userGuid: str) -> bool:
        """
        Sets the active value to 1 in DB to the user with specified Guid
        - @userGuid : The uniqueidentifier from user
        """

        try:

            if (not utils.IsGuid(userGuid)):
                raise APIException(400, "Guid not valid")

            if (self.Activated(userGuid)):
                raise APIException(400, "Account alredy activated")

            if not self.dbConnection.is_connected():
                self.Connect()

            self.dbConnection.autocommit = False

            dbCursor = self.dbConnection.cursor()

            update = "UPDATE User SET active={0}, emailConfirmation={1} ".format(
                1, 1)
            where = "WHERE id='{0}'".format(userGuid)

            query = update + where

            dbCursor = self.dbConnection.cursor()
            dbCursor.execute(query)
            self.dbConnection.commit()

            if (dbCursor.rowcount > 0):
                return True
            else:
                return False

        except APIException as ex:
            raise ex
        finally:
            pass

    def Read(self, value: str) -> User | None:
        """
        Get all user data
        - @value: An email or guid
        """

        try:

            query = ""

            if (utils.IsEmail(value)):
                self._ValidateLoginRequest(value)
                query = "SELECT U.*, UK.key FROM User AS U INNER JOIN UserKey UK ON U.id = UK.userId WHERE U.email = '{0}'".format(
                    value)

            if (utils.IsGuid(value)):
                query = "SELECT U.*, UK.key FROM User AS U INNER JOIN UserKey UK ON U.id = UK.userId WHERE U.id = '{0}'".format(
                    value)

            if not self.dbConnection.is_connected():
                self.Connect()

            dbCursor = self.dbConnection.cursor()
            dbCursor.execute(query)
            records = dbCursor.fetchall() or []
            user = User()

            if (dbCursor.rowcount == 0):
                return None

            if (dbCursor.rowcount > 0):
                # print(records)
                row = records[0]
                user.id = row[0]
                user.email = row[1]
                user.password = row[2]
                user.name = row[3]
                user.surname = row[4]
                user.birthdate = row[5]
                user.startdate = row[6]
                user.enddate = row[7]
                user.represents = row[8]
                user.details = row[9]
                user.phone = row[10]
                user.image = row[11]
                user.active = row[12]
                user.isadmin = row[13]
                user.emailconfirmation = row[14]
                user.lastaccessday = row[15]
                user.username = "{0} {1}".format(user.name, user.surname)
                user.userKey = row[16]

            return user

        except mysql.connector.Error as e:

            ex = APIException()

            if (e.msg):
                ex = APIException(500, e.msg)
            else:
                ex = APIException(500, "Unknow error in database request")

            raise ex
        except APIException as ex:
            raise ex
        finally:
            self.Close()

    def Update(self, user: User):
        """
        Updates user profile in DB
        - @user : An User model with all required properties
        """

        if not self.dbConnection.is_connected():
            self.Connect()

        try:

            update = "UPDATE User SET email='{0}', name='{1}', surname='{2}', birthday='{3}', represents='{4}', phone='{5}' ".format(
                user.email, user.name, user.surname, user.birthdate, user.represents, user.phone)
            where = "WHERE id='{0}'".format(user.id)

            if (user.image):
                update += ",image='{0}' ".format(user.image)

            if (not user.lastaccessday is None):
                update += ", last_access_day='{0}' ".format(
                    user.lastaccessday.strftime('%Y-%m-%d %H:%M:%S'))

            query = update + where

            dbCursor = self.dbConnection.cursor()
            dbCursor.execute(query)
            self.dbConnection.commit()

            if (dbCursor.rowcount > 0):
                return True
            else:
                return False

        except mysql.connector.Error as e:
            raise e
        finally:
            self.Close()

    def Delete(self, guid: str) -> User | None:
        """
        Sets the active value to 0 in DB to the user with specified Guid
        - @userGuid : The uniqueidentifier from user
        """

        try:

            if (not self.Exists(guid)):
                raise APIException(404, "User not exists")

            user = self.Read(guid)

            if not self.dbConnection.is_connected():
                self.Connect()

            delte = "UPDATE User SET active=0 "
            where = "WHERE id='{0}'".format(guid)

            query = delte + where

            dbCursor = self.dbConnection.cursor()
            dbCursor.execute(query)
            self.dbConnection.commit()

            if (dbCursor.rowcount > 0):
                return user
            else:
                return None

        except mysql.connector.Error as e:
            raise e
        finally:
            self.Close()

    def Exists(self, value: str):
        """
        Checks if user with email/guid exists on DB
        - @value : An email or the uniqueidentifier from user
        """

        try:

            valid: bool = False
            query = ''

            if not self.dbConnection.is_connected():
                self.Connect()

            if (utils.IsEmail(value)):
                query = "SELECT id FROM User WHERE email = '{0}'".format(value)

            if (utils.IsGuid(value)):
                query = "SELECT id FROM User WHERE id = '{0}'".format(value)

            dbCursor = self.dbConnection.cursor()
            dbCursor.execute(query)
            records = dbCursor.fetchone() or ''

            if (dbCursor.rowcount > 0):
                valid = True

            return valid
        except mysql.connector.Error as e:
            raise e
        finally:
            self.Close()

    def Activated(self, value: str):
        """Indicates that the user was the active propety with value to 1
        - @value : An email or the uniqueidentifier from user
        """

        try:

            valid: bool = False
            query = ''

            if not self.dbConnection.is_connected():
                self.Connect()

            if (utils.IsEmail(value)):
                query = "SELECT active FROM User WHERE email = '{0}'".format(
                    value)

            if (utils.IsGuid(value)):
                query = "SELECT active FROM User WHERE id = '{0}'".format(
                    value)

            if (not query):
                raise APIException(400, "Invalid call")

            dbCursor = self.dbConnection.cursor()
            dbCursor.execute(query)
            records = dbCursor.fetchone() or []

            if (dbCursor.rowcount > 0):
                valid = records[0]

            return valid

        except mysql.connector.Error as e:
            raise e
        finally:
            self.Close()

    def Confirmed(self, email: str):
        """
        Indicates that the user has the emailConfirmation propety with value to 1
        - @value : An email or the uniqueidentifier from user
        """

        try:

            valid: bool = False

            if not self.dbConnection.is_connected():
                self.Connect()

            query = "SELECT emailConfirmation FROM User WHERE email = '{0}'".format(
                email)
            dbCursor = self.dbConnection.cursor()
            dbCursor.execute(query)
            records = dbCursor.fetchone() or []

            if (dbCursor.rowcount > 0):
                valid = records[0]

            return valid

        except mysql.connector.Error as e:
            raise e
        finally:
            self.Close()
