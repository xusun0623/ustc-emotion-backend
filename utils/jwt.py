from datetime import datetime
import jwt

JWT_SECRET_KEY = "123456"

def vaild_token(encoded_jwt):
    try:
        decode_jwt_token(encoded_jwt)
    except Exception as e :
        print(e) #Token解析失败
        return False
    return True

def get_jwt_token(username, roledata="student", user_id=0):
    payload = {
        'time': str(datetime.utcnow()),
        'data': {'username': username, 'roledata': roledata, 'user_id': user_id}
    }
    encoded_jwt = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return str(encoded_jwt)

def decode_jwt_token(encoded_jwt):
    de_code = jwt.decode(encoded_jwt, JWT_SECRET_KEY, algorithms=['HS256'])
    return de_code