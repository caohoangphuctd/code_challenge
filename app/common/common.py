import string
import random


async def message_format(data=None, message=None):
    return {"data": data, "message": message}


async def get_random_otp(k):
    return ''.join(random.choices(string.digits, k=k))
