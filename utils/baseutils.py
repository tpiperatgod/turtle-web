import hashlib

def hash_password(passwd):
    ps = hashlib.md5()
    ps.update(passwd)
    return ps.hexdigest() 
    