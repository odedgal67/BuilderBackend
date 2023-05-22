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

    url_register = 'http://localhost:5000/register'
    url_login = 'http://localhost:5000/login'

    response = requests.post(url_register, json=payload_register)
    print(response)
    # data = response.json()
    # print(data)

    response = requests.post(url_login, json=payload_login)
    print(response)
    # data = response.json()
    # print(data)
