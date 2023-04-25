import bcrypt

salt = bcrypt.gensalt()
ENCODE_TYPE = 'utf-8'


def hash_password(password: str):
    hashed_password = bcrypt.hashpw(password.encode(ENCODE_TYPE), salt)
    return hashed_password


def compare_password(password: str, hashed_password):
    return bcrypt.checkpw(password.encode(ENCODE_TYPE), hashed_password)
