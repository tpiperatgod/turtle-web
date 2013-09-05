import hashlib


def hash_password(passwd):
    ps = hashlib.md5()
    ps.update(passwd)
    ps.digest()
    return ps 
    