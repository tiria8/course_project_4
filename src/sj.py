from abc import ABC
import requests
import json
import os
import time


from src.vacancies import Vacancies


class SuperJobAPI(Vacancies, ABC):
    """
    Класс реализует получение вакансий с портала Superjob
    """
    def __init__(self, keyword):
        self.keyword = keyword
        self.url_api = 'https://api.superjob.ru/2.0/vacancies'
        self.vacancies_list = []

    def __repr__(self):
        return f"{self.__class__.__name__}," \
               f"{self.keyword}," \
               f"{self.url_api}," \
               f"{self.vacancies_list}"

    def get_vacancies(self):
        """
        Формирует запрос на API сайта SuperJob для получения выборки вакансий
        по ключевому слову
        :return: список вакансий по запросу
        """

        per_page_num = 100
        page_num = 5
        api_key: str = os.getenv('SUPERJOB_API_KEY')
        vacancies_count = 0

        for page in range(0, page_num):
            headers = {"X-Api-App-Id": api_key}
            params = {'count': per_page_num, 'page': page, 'keyword': self.keyword, 'archive': False}

            response = requests.get(self.url_api, params=params, headers=headers)

            if response.status_code == 200:

                data_in = response.content.decode()
                response.close()

                data_out = json.loads(data_in)

                for vacancy in data_out['objects']:
                    vacancy_dict = SuperJobAPI.get_vacancy_dict(vacancy)

                    self.vacancies_list.append(vacancy_dict)

                    vacancies_count += 1

            if response.status_code != 200:
                print("В настоящий момент сайт недоступен. Попробуйте позже.")

            if vacancies_count == data_out['total']:
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

        vacancy_dict['id'] = vacancy['id']
        vacancy_dict['name'] = vacancy['profession']
        vacancy_dict['salary_from'] = vacancy['payment_from']
        vacancy_dict['salary_to'] = vacancy['payment_to']
        vacancy_dict['currency'] = vacancy['currency']
        try:
            vacancy_dict['employer'] = vacancy['client']['title']
        except KeyError:
            vacancy_dict['employer'] = 'Нет данных'
        vacancy_dict['vacancy_url'] = vacancy['link']
        vacancy_dict['description'] = vacancy['vacancyRichText']
        vacancy_dict['experience'] = vacancy['experience']['title']

        return vacancy_dict