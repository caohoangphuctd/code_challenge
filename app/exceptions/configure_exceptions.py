from typing import Union
from uuid import UUID


class ItemExist(Exception):
    def __init__(self, field: str):
        self.field = field

    def __str__(self):
        return (
            f"{self.field}Exist"
        )


class ItemDoesNotExist(Exception):
    def __init__(self, item: str):
        self.item = item

    def __str__(self):
        return f"{self.item}DoesNotExist"


class BothEmailAndPhoneAreNone(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "BothEmailAndPhoneAreNone"


class ErrorRequestException(Exception):
    def __init__(self, content: str):
        self.content = content

    def __str__(self):
        return self.content


class ErrorInvalidTokenException(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "InvalidToken"


class ErrorAuthenticationException(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "WrongPassword"
