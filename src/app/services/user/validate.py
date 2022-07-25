import re


def validate_email(email: str):
    return re.match(pattern=r"^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$", string=email)


def validate_phone(phone: str):
    return re.match(pattern=r"^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$", string=phone)
