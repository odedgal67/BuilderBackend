import requests


if __name__ == '__main__':
    payload_register = {
        'username': '316327923',
        'password': 'Oded1234',
        'name': 'Oded Gal'
    }

    payload_login = {
        'username': '123456789',
        'password': 'Password',
    }
    payload_echo = {
        'echo_string': 'Hello World'
    }

    payload_add_project = {
        'project_name': 'Test Project',
        'username': '123456789'
    }

    url_register = 'http://16.170.170.180:80/register'
    url_login = 'http://16.170.170.180:80/login'
    url_echo = 'http://16.170.170.180:80/echo'
    url_add_project = 'http://16.170.170.180:80/add_project'

    # response = requests.post(url_register, json=payload_register)
    # print(response)
    # data = response.json()
    # print(data)

    response = requests.post(url_login, json=payload_login)
    print(response)
    data = response.json()
    print(data)

    # response = requests.post(url_echo, json=payload_echo)
    # print(response)
    # data = response.json()
    # print(data)

    response = requests.post(url_add_project, json=payload_add_project)
    print(response)
    data = response.json()
    print(data)


