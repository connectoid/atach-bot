import json
from pprint import pprint
from time import sleep
import os

import requests

from settings.settings import data_list


endpoint = 'https://booking.ata-chukotka.ru/api/flights/search/request'


headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': 'PHPSESSID=3f4054dc2c665a17005e2b24b6e6418c; user_unique_id=07ff0c335895a44e96deb16cfa23248c; nemo_lang=ru; ccCurrency=RUB; nemo_currency=RUB; nemo-FlightsSearchForm={%22segments%22:[[%22DYR%22%2C%22MOW%22%2C%222024-06-21%22%2Cfalse%2Ctrue]]%2C%22passengers%22:{%22ADT%22:1%2C%22CLD%22:1%2C%22SRC%22:0%2C%22YTH%22:0%2C%22INF%22:0%2C%22INS%22:0}%2C%22serviceClass%22:%22Economy%22%2C%22vicinityDates%22:false}',
    'origin': 'https://booking.ata-chukotka.ru',
    'referer': 'https://booking.ata-chukotka.ru/results/aDYRcMOW20240621ADT1CLD1-class=Economy',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

params = {
    'user_language_get_change': 'ru',
}


def request_one_ticket(data):
    date = data['date']
    departure = data['departure']
    arrival = data['arrival']
    data = {
        'request': '{"segments":[{"departure":' + departure + ',"arrival":' + arrival + ',"departureDate":"' + date + '"}],"passengers":[{"type":"ADT","count":1},{"type":"CLD","count":1}],"parameters":{"direct":false,"aroundDates":0,"serviceClass":"Economy","flightNumbers":null,"airlines":[],"delayed":true,"extraValue":null}}',
    }
    response = requests.post(
            endpoint,
            params=params,
            data=data
        )
    if response.status_code == 200:
        request_data = response.json()
        request_id = request_data['flights']['search']['request']['id']
        # print(f'ID запроса: {request_id}')
        result_endpoint = f'https://booking.ata-chukotka.ru/api/flights/search/results/{request_id}'
        result_response = requests.get(
            result_endpoint,
            params=params,
        )
        if result_response.status_code == 200:
            result_data = result_response.json()
            info = result_data['flights']['search']['results']['info']
            with open('result_data.json', 'w') as f:
                json.dump(result_data, f)
            if info['errorCode'] is None:
                flight_price = result_data['flights']['search']['results']['groupsData']['prices']['P1']['flightPrice']
                pprint(flight_price)
                return flight_price
            else:
                departure = departure.split('"IATA":')[-1].split(',')[0].strip('"')
                arrival = arrival.split('"IATA":')[-1].split(',')[0].strip('"')
                date = date.split('T')[0]
                # result_message = f'Билетов по маршруту {departure} -> {arrival} на дату {date} нет.'
                return False
        else:
            print(f'Request 2 error: {response.status_code}')
            return f'Request 2 error: {response.status_code}'
    else:
        print(f'Request 1 error: {response.status_code}')
        return f'Request 2 error: {response.status_code}'


def request_tickets():
    results_list = []
    for data in data_list:
        result_text = request_one_ticket(data)
        if result_text:
            results_list.append(result_text)
    return results_list


if __name__ == '__main__':
    print('Start parsing')
    request_tickets(data_list)