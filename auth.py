#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests

from conf import USERNAME
from conf import PASSWORD

PASS_CODE_MAP = {
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
        pass_code_list.append(PASS_CODE_MAP.get(index, ""))
    return ",".join(pass_code_list)


class Auth(object):
    def __init__(self, session):
        super(Auth, self).__init__()
        self.session = session

    def get_pass_code(self) -> bool:
        url_get_pass_code = "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand"
        # noinspection PyBroadException
        try:
            resp = self.session.get(url_get_pass_code, verify=False, timeout=10)
            with open("./pass_code.jpg", 'wb') as f:
                f.write(resp.content)
            return True
        except Exception:
            return False

    def get_rand_code(self, pass_code: str) -> str:
        rand_code = image_index_to_pass_code(pass_code)
        url_check_rand_code = "https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn"
        data = {
            'rand': 'sjrand',
            'randCode': rand_code,
        }
        # noinspection PyBroadException
        try:
            resp = self.session.post(url_check_rand_code, data=data, verify=False, timeout=10)
            if resp.json()['data']['result'] == '1':
                return rand_code
        except Exception:
            return ""

    def do_login(self, username: str, password: str, rand_code: str) -> bool:
        url_login = "http://kyfw.12306.cn/otn/login/loginAysnSuggest"
        data = {
            'randCode': rand_code,
            'userDTO.password': password,
            'loginUserDTO.user_name': username,
        }

        # noinspection PyBroadException
        try:
            resp = self.session.post(url_login, data=data, verify=False, timeout=10)
            json_data = resp.json()
            if not json_data["status"]:
                print(",".join(json_data['messages']))
            return json_data['data']['loginCheck'] == 'Y'
        except Exception:
            return False

    def login(self, username: str, password: str) -> bool:
        if not self.get_pass_code():
            print("get pass code fail")
            return False

        pass_code = input("Please input image index: ")
        rand_code = self.get_rand_code(pass_code)

        if rand_code:
            print("pass code ok")
        else:
            print("pass code fail")
            return False

        if self.do_login(username, password, rand_code):
            print("login ok")
        else:
            print("login fail")
            return False
        return True


if __name__ == '__main__':
    _session = requests.Session()
    auth = Auth(_session)
    auth.login(USERNAME, PASSWORD)
