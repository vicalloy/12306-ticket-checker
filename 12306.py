#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from typing import List
from typing import Mapping
import time

import requests

from slackclient import SlackClient
from conf import SLACK_TOKEN
from conf import TRAIN_DATES, FROM_STATIONS, TO_STATIONS, TICKET_TYPES, NEED_COUNT

INTERVAL_FOR_QUERY = 6


def slack_send_message(message):
    sc = SlackClient(SLACK_TOKEN)

    sc.api_call(
        "chat.postMessage",
        channel="#ticket",
        text=message
    )


def send_message(message):
    slack_send_message(message)
    print(message)


def get_train_info(train_date, from_station, to_station='HZH') -> List[Mapping[str, str]]:
    # url = "https://kyfw.12306.cn/otn/leftTicket/queryZ"
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?' \
          'leftTicketDTO.train_date={train_date}' \
          '&leftTicketDTO.from_station={from_station}' \
          '&leftTicketDTO.to_station={to_station}' \
          '&purpose_codes=ADULT'
    params = {
        'train_date': train_date,  # leftTicketDTO.
        'from_station': from_station,  # leftTicketDTO.
        'to_station': to_station,  # leftTicketDTO.
        'purpose_codes': 'ADULT',
    }
    train_info_list = []
    # noinspection PyBroadException
    try:
        # FIXME use params will fail on some server, the reason is unkonwn
        # r = requests.get(url, params=params, verify=False)
        url = url.format(**params)
        r = requests.get(url, verify=False)
        return_data = r.json()
        train_info_list = [e['queryLeftNewDTO'] for e in return_data['data']]
        print('get_train_info succ')
    except Exception:
        print('get_train_info fail')
    return train_info_list


class TicketChecker(object):
    def __init__(
            self, train_dates: List[str], from_stations: List[str],
            to_stations: List[str], ticket_types: List[str], need_count: int):
        super(TicketChecker, self).__init__()
        self.train_dates = train_dates
        self.from_stations = from_stations
        self.to_stations = to_stations
        self.ticket_types = ticket_types
        self.need_count = need_count

    def get_ok_ticket_types(self, train_info: Mapping[str, str]) -> List[str]:
        ok_ticket_types = []
        for ticket_type in self.ticket_types:
            left_ticket = get_left_ticket(ticket_type, train_info)
            if left_ticket > self.need_count:
                ok_ticket_types.append(ticket_type)
        return ok_ticket_types

    @staticmethod
    def send_notification(train_info, ticket_type, train_date, from_station, to_station):
        message = ('日期：{train_date} 类型：{ticket_type} 车次：{train_code} '
                   '开车时间：{start_time}  到达时间：{arrive_time} 余票：{left_ticket} '
                   '历时:{lishi} 出发：{from_station} 达到：{to_station}').format(
            train_date=train_date, from_station=from_station, to_station=to_station,
            start_time=train_info['start_time'],
            ticket_type=train_info.get('train_class_name'),
            left_ticket=train_info.get('%s_num' % ticket_type),
            lishi=train_info.get('lishi'),
            arrive_time=train_info.get('arrive_time'),
            train_code=train_info['station_train_code'],
        )
        send_message(message)

    def check_ticket(self):
        for train_date in self.train_dates:
            for from_station in self.from_stations:
                for to_station in self.to_stations:
                    time.sleep(INTERVAL_FOR_QUERY)  # sleep
                    train_info_list = get_train_info(train_date, from_station, to_station)
                    for train_info in train_info_list:
                        ok_ticket_types = self.get_ok_ticket_types(train_info)
                        for ok_ticket_type in ok_ticket_types:
                            self.send_notification(train_info, ok_ticket_type, train_date, from_station, to_station)


def get_left_ticket(ticket_type: str, train_info) -> int:
    """
    str_count: --,无,有,1,12
    """
    str_count = train_info.get('%s_num' % ticket_type)
    if str_count == '有':
        return 9999
    try:
        return int(str_count)
    except ValueError:
        return 0


ticket_checker = TicketChecker(TRAIN_DATES, FROM_STATIONS, TO_STATIONS, TICKET_TYPES, NEED_COUNT)
while True:
    ticket_checker.check_ticket()
