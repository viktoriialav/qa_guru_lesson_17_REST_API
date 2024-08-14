import json
from pathlib import Path

import requests
from jsonschema import validate

import tests

url = "https://reqres.in/api/users"

# response = requests.request("POST", url, data=payload)
# print(response.text)


def file_path(file_name):
    return str(Path(tests.__file__).parent.parent.joinpath(f'schemas/{file_name}').absolute())


def test_api():
    payload = {"name": "morpheus", "job": "leader"}
    response = requests.post(url, data=payload)
    print(response.text)
    assert response.status_code == 201

    body = response.json()
    with open(file_path("../resources/post_users.json")) as file:
        validate(body, schema=json.load(file))


def test_job_name_from_request_returns_in_response():
    '''
    Бизнес-задача: наш API возвращает ровно те значения, которые были переданы
    '''
    job = 'leader'
    name = 'morpheus'
    payload = {"name": name, "job": job}
    response = requests.post(url, data=payload)
    print(response.text)
    body = response.json()

    assert body['name'] == name
    assert body['job'] == job


def test_get():
    '''
    Проверка на уникальность значений списка id
    '''
    response = requests.get(url='https://reqres.in/api/users',
                            params={'page': 2, 'per_page': 4})
    ids = [elem['id'] for elem in response.json()['data']]
    assert len(ids) == len(set(ids))


