import requests


if __name__ == '__main__':
    payload_register = {
        'username': '316327923',
        'password': 'Oded1234',
        'name': 'Oded Gal'
    }

    payload_login = {
        'username': '316327923',
        'password': 'Oded1234',
    }

    url_register = 'http://16.170.170.180:80/register'
    url_login = 'http://16.170.170.180:80/login'

    response = requests.post(url_register, json=payload_register)
    print(response)
    # data = response.json()
    # print(data)

    response = requests.post(url_login, json=payload_login)
    print(response)
    # data = response.json()
    # print(data)
