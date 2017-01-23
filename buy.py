#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests

from conf import USERNAME
from conf import PASSWORD

session = requests.Session()

pass_code_map = {
    "1": "40,50",
    "2": "120,50",
    "3": "180,50",
    "4": "260,50",
    "5": "40,120",
    "6": "120,120",
    "7": "180,120",
    "8": "260,120",
}


def image_index_to_pass_code(pass_code: str) -> str:
    pass_code_list = []
    for index in pass_code:
        pass_code_list.append(pass_code_map.get(index, ""))
    return ",".join(pass_code_list)


def get_pass_code() -> bool:
    url_get_pass_code = "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand"
    # noinspection PyBroadException
    try:
        resp = session.get(url_get_pass_code, verify=False, timeout=10)
        with open("./pass_code.jpg", 'wb') as f:
            f.write(resp.content)
        return True
    except Exception:
        return False


def get_rand_code(pass_code: str) -> str:
    rand_code = image_index_to_pass_code(pass_code)
    url_check_rand_code = "https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn"
    data = {
        'rand': 'sjrand',
        'randCode': rand_code,
    }
    # noinspection PyBroadException
    try:
        resp = session.post(url_check_rand_code, data=data, verify=False, timeout=10)
        if resp.json()['data']['result'] == '1':
            return rand_code
    except Exception:
        return ""


def login(username: str, password: str, rand_code: str) -> bool:
    url_login = "http://kyfw.12306.cn/otn/login/loginAysnSuggest"
    data = {
        'randCode': rand_code,
        'userDTO.password': password,
        'loginUserDTO.user_name': username,
    }

    # noinspection PyBroadException
    try:
        resp = session.post(url_login, data=data, verify=False, timeout=10)
        json_data = resp.json()
        if not json_data["status"]:
            print(",".join(json_data['messages']))
        return json_data['data']['loginCheck'] == 'Y'
    except Exception:
        return False


if not get_pass_code():
    print("get pass code fail")
    exit(1)

_pass_code = input("Please input image index: ")
_rand_code = get_rand_code(_pass_code)

if _rand_code:
    print("pass code ok")
else:
    print("pass code fail")
    exit(1)

if login(USERNAME, PASSWORD, _rand_code):
    print("login ok")
else:
    print("login fail")
