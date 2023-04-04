import re
from passlib.context import CryptContext    # type: ignore
from passlib.exc import UnknownHashError    # type: ignore

from app.exceptions.configure_exceptions import (
    ErrorRequestException, ErrorAuthenticationException
)


class PasswordHandler:

    @property
    def pwd_context(self):
        return CryptContext(
            schemes=["bcrypt"],
            deprecated="auto"
        )

    @staticmethod
    async def validate_password(password):
        regex_pattern = "(?=.{8,}).*$"
        if not re.match(regex_pattern, password):
            raise ErrorRequestException("InvalidPassword")

    async def verify_password(self, plain_password, hashed_password):
        try:
            verify = False
            if plain_password is not None and hashed_password is not None:
                verify = self.pwd_context.verify(
                    secret=plain_password,
                    hash=hashed_password
                )
        except UnknownHashError:
            raise ErrorAuthenticationException
        if not verify:
            raise ErrorAuthenticationException

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
