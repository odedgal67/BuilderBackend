import bcrypt


def hash_password(password: str):
    return bcrypt.hashpw(password)


def compare_password(password: str, hashed_password):
    return bcrypt.hashpw(password) == hashed_password
