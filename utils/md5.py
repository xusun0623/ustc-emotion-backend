import hashlib

def encode(str):
    Encry = hashlib.md5()  # 实例化md5
    Encry.update(str.encode())  # 字符串字节加密
    md5_pwd = Encry.hexdigest() # 字符串加密
    return md5_pwd
