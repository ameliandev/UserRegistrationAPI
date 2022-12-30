import re


class Utils():

    def __init__(self) -> None:
        pass

    def IsEmail(self, value: str):
        """
        Checks if the value is an email
        """

        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        return re.fullmatch(regex, value)

    def IsGuid(self, value: str):
        """
        Checks if the value is an guid
        """

        regex = re.compile(
            r'[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}')

        return re.fullmatch(regex, value)

    def PasswordValidate(self, password: str):
        """
        ## Validates password length and characters
        Password must contain:
        - at least 6 characters
        - At least 1 upper and 1 lower case letter
        - At least 1 number
        - At least 1 special character
        """

        regex = re.compile(
            r'^.*(?=.{6,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!&$%&? "]).*$'
        )

        return re.fullmatch(regex, password)
