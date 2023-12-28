from abc import ABC
import requests
import json
import time

from src.vacancies import Vacancies


class HeadHunterApi(Vacancies, ABC):
    """
    Класс реализует получение вакансий с портала HeadHunter
    """
    def __init__(self, keyword):
        self.keyword = keyword
        self.url_api = 'https://api.hh.ru/vacancies'
        self.vacancies_list = []

    def __repr__(self):
        return f"{self.__class__.__name__}," \
               f"{self.keyword}," \
               f"{self.url_api}," \
               f"{self.vacancies_list}"

    def get_vacancies(self):
        """
        Формирует запрос на API сайта HeadHunter для получения выборки вакансий
        по ключевому слову
        :return: список вакансий по запросу
        """

        per_page_num = 100
        page_num = 10
        vacancies_count = 0

        for page in range(0, page_num):

            params = {
                'text': self.keyword,
                'page': page,
                'per_page': per_page_num
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 "
                              "Safari/537.36",
            }

            req = requests.get(self.url_api, params=params, headers=headers)

            if req.status_code == 200:
                data_in = req.content.decode()
                req.close()

                data_out = json.loads(data_in)

                for vacancy in data_out['items']:

                    vacancy_dict = HeadHunterApi.get_vacancy_dict(vacancy)

                    self.vacancies_list.append(vacancy_dict)
                    vacancies_count += 1

            if req.status_code != 200:
                print("В настоящий момент сайт недоступен. Попробуйте позже.")

            if vacancies_count == data_out['found']:
                break

            time.sleep(0.2)

        return self.vacancies_list

    @classmethod
    def get_vacancy_dict(cls, vacancy):
        """
        Формирует словарь с данными о вакансии из API респонса
        :return:
        """
        vacancy_dict = {}

        vacancy_dict['id'] = int(vacancy['id'])
        vacancy_dict['name'] = vacancy['name']
        if vacancy['salary']:
            if vacancy['salary']['from'] is None:
                vacancy_dict['salary_from'] = 0
            else:
                vacancy_dict['salary_from'] = vacancy['salary']['from']

            if vacancy['salary']['to'] is None:
                vacancy_dict['salary_to'] = 0
            else:
                vacancy_dict['salary_to'] = vacancy['salary']['to']

            if vacancy['salary']['currency'] is None:
                vacancy_dict['currency'] = 'RUR'
            else:
                vacancy_dict['currency'] = vacancy['salary']['currency']
        else:
            vacancy_dict['salary_from'] = 0
            vacancy_dict['salary_to'] = 0
            vacancy_dict['currency'] = 'RUR'
        vacancy_dict['employer'] = vacancy['employer']['name']
        vacancy_dict['vacancy_url'] = vacancy['alternate_url']
        vacancy_dict['description'] = vacancy['snippet']['responsibility']
        vacancy_dict['experience'] = vacancy['experience']['name']

        return vacancy_dict
