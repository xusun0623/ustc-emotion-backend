import requests

'''
文本审核接口
'''

def toxic_type(text):
    request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"
    params = {"text": text}
    access_token = ''
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        data = response.json()
        if data['conclusion'] == '合规':
            # print(0)
            return -1
        else:
            # print(data['data'][0]['subType'])
            return data['data'][0]['subType']

if __name__ == '__main__':
    toxic_type("习近平")

