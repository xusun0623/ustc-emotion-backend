import base64
import time
import datetime
import json
import hmac
from hashlib import sha1 as sha

access_key_id = ''
access_key_secret = ''
host = '';
# callback_url为 上传回调服务器的URL
callback_url = "";
upload_dir = ''
expire_time = 300000

def get_iso_8601(expire):
    gmt = datetime.datetime.utcfromtimestamp(expire).isoformat()
    gmt += 'Z'
    return gmt

def getUploadParam():
    now = int(time.time())
    expire_syncpoint = now + expire_time
    expire = get_iso_8601(expire_syncpoint)

    policy_dict = {}
    policy_dict['expiration'] = expire
    condition_array = []
    array_item = []
    array_item.append('starts-with');
    array_item.append('$key');
    array_item.append(upload_dir);
    condition_array.append(array_item)
    policy_dict['conditions'] = condition_array
    policy = json.dumps(policy_dict).strip()
    policy_encode = base64.b64encode(policy.encode())
    h = hmac.new(access_key_secret.encode(), policy_encode, sha)
    sign_result = base64.encodebytes(h.digest()).strip()

    callback_dict = {}
    callback_dict['callbackUrl'] = callback_url;
    callback_dict['callbackBody'] = 'filename=${object}&size=${size}&mimeType=${mimeType}' \
                                    '&height=${imageInfo.height}&width=${imageInfo.width}';
    callback_dict['callbackBodyType'] = 'application/x-www-form-urlencoded';
    callback_param = json.dumps(callback_dict).strip()
    base64_callback_body = base64.b64encode(callback_param.encode());

    token_dict = {}
    token_dict['accessid'] = access_key_id
    token_dict['host'] = host
    token_dict['policy'] = policy_encode.decode()
    token_dict['signature'] = sign_result.decode()
    token_dict['expire'] = expire_syncpoint
    token_dict['dir'] = upload_dir
    token_dict['callback'] = base64_callback_body.decode()
    # result = json.dumps(token_dict)
    result = token_dict
    return result