# UserRegistrationAPI

## Simple Python API to user registration

This is a simple project that will be usefull as "template" to began a new project that
allows User registration.

This project was developed with [FastAPI](https://fastapi.tiangolo.com/) and inmplents the **HttpOnlyCookie** login session.

It's configured to use email registration too, with a basic SMTP configuration.

### Requisites

```bash
$ python3 -m pip install requests
$ pip3 install fastapi
$ pip3 install uvicorn
$ pip3 install pyjwt
$ pip3 install pyjwt[crypto]
$ python3 -m pip install pyjwt
$ pip3 install cryptography
$ pip3 install mysql-connector-python
$ pip3 install python-whois
```

### To Run it

First of all, you must configure some properties in your project

#### Auth Token

To generate new tokens for user login, you must set the Auth token secret key. Go to **app\classes\Auth.py** and set your secret key in **tokenSecret** property.

#### API Config

This API it's parametrized with some properties that you must know. Depends of the value, it works in diferent ways. To configure it, go to **app\config\ApiConfig.py**

##### PROPERTIES

- apiInfo: An API basic info. The hosts is obtained from **socket module**
- apiAllowActivation: Indicates if allow accounts activation.
- apiRegisterByAdminFirst: Indicates if the accounts activation will be managed by Admins. This property is linked to the management of mailing to administrators or users.
- apiDomain: The Domain public IP
- apiCookieHttpOnlyExpires: The expires time for the HttoOnlyCookie used when user login in platform.
- apiCookiePath: The cookie path
- apiMailConfig: An object that has all email configuration
  - active: Indicates if the mail service in API will be active. If not, no email will be sent.
  - smtp: Your SMTP configuration
  - mailFrom: The email that will be displayed in sent emails
  - mailsTo: A list of emails. These emails will be the ones that will receive the mails, whether they are administrators or direct users.
  - mailType: Depends of email type (see the Enum MailType in app.classes.Mail) one configured email or another will be sent.

#### Database Config

Go to **app\config\dbConfig.py** and sets your database configuration.

#### Database Script

This API it's ready to use with a simple database structure allowed in the **app\db.sql** file. Create a DB in your MySQL Service and restore this script on it.

#### Running the service in console

```bash
$ uvicorn app.main:api --reload --host ${HOST} --port ${PORT}
```

