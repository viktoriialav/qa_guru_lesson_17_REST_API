import json
import logging
from pathlib import Path

import allure
import requests
from allure_commons.types import AttachmentType
from jsonschema import validate

import tests

url = "https://reqres.in/api/users"


def reqres_api_get(endpoint, **kwargs):
    with allure.step('API Request'):
        result = requests.get(url='https://reqres.in' + endpoint, **kwargs)
        allure.attach(body=json.dumps(result.json(), indent=4, ensure_ascii=True),
                      name="Response", attachment_type=AttachmentType.JSON, extension='json')
        logging.info(result.request.url)
        logging.info(result.status_code)
        logging.info(result.text)

    return result


def file_path(file_name):
    return str(Path(tests.__file__).parent.parent.joinpath(f'schemas/{file_name}').absolute())


def test_api():
    payload = {"name": "morpheus", "job": "leader"}
    response = requests.post(url, data=payload)
    print(response.text)
    assert response.status_code == 201

    body = response.json()
    with open(file_path("post_users.json")) as file:
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


def test_list_of_users_per_page():
    '''
    Проверка на уникальность значений списка id
    '''
    page = 2
    per_page = 6
    endpoint = '/api/users'

    response = reqres_api_get(endpoint=endpoint, params={'page': page, 'per_page': per_page})

    assert response.json()['per_page'] == per_page
    assert len(response.json()['data']) == per_page
