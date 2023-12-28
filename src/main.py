from src.hh import HeadHunterApi
from src.sj import SuperJobAPI
from src.vacancies import VacanciesControl
import json
import os
import pandas

file_in = os.path.abspath('vacancies_json.json')
file_xlsx = os.path.abspath('vacancies_xlsx.xlsx')


def general_function(check_point):
    """
    Запускает основное тело программы
    """
    if check_point:
        start_menu()


def start_menu():
    """
    Меню навигации по программе
    """

    print("-------------------------------------")
    print("Выберите необходимое действие:\n")

    try:
        start_point = int(input("1 - запуск поиска вакансий и сортировка списка\n"
                                "2 - редактирование списка вакансий в файле\n"
                                "3 - запись списка вакансий в формате Excel\n"
                                "4 - выход из программы\n"))

        if start_point == 1:
            list_in = choice_vacancies_portal()
            list_out = VacanciesControl(list_in)
            VacanciesControl.vacancy_start_menu(list_out)
            general_function(True)

        if start_point == 2:
            list_in = reading_json_file(file_in)
            list_for_sort = VacanciesControl(list_in)
            list_for_sort.sort_vacancies_menu()
            general_function(True)

        if start_point == 3:
            list_in = reading_json_file(file_in)
            writing_to_excel_file(list_in, file_xlsx)
            general_function(True)

        if start_point == 4:
            end_program()

    except ValueError:
        input_error()


def choice_vacancies_portal():
    """
    Функция для поиска вакансий по выбранной платформе
    :return: список вакансий
    """
    search_text = input('Введите поисковый запрос (например, "python Москва")\n')

    choice_portal = int(input("Выберите место поиска вакансий:\n"
                              "1 - HeadHunter\n"
                              "2 - SuperJob\n"
                              "3 - совместный поиск\n"))

    if choice_portal == 1:
        hh_list = get_hh_vacancies(search_text)
        print(f"Получено {len(hh_list)} вакансий\n"
              f"-------------------------------------")
        return hh_list

    if choice_portal == 2:
        sj_list = get_sj_vacancies(search_text)
        print(f"Получено {len(sj_list)} вакансий\n"
              f"-------------------------------------")
        return sj_list

    if choice_portal == 3:
        hh_list = get_hh_vacancies(search_text)
        sj_list = get_sj_vacancies(search_text)

        hh_sj_list = get_mixed_vacancies(hh_list, sj_list)
        print(f"Получено {len(hh_sj_list)} вакансий\n"
              f"-------------------------------------")
        return hh_sj_list


def get_hh_vacancies(search_text):
    """
    Получает список вакансий с HeadHunter
    :return:
    """
    get_hh_list = HeadHunterApi(search_text)

    get_hh_list.get_vacancies()

    hh_list_out = get_hh_list.vacancies_list

    return hh_list_out


def get_sj_vacancies(search_text):
    """
    Получает список вакансий с SuperJob
    :return:
    """
    get_sj_list = SuperJobAPI(search_text)

    get_sj_list.get_vacancies()

    sj_list_out = get_sj_list.vacancies_list

    return sj_list_out


def get_mixed_vacancies(list_1, list_2):
    """
    Собирает общий список вакансий,
    если пользователь выбирает совместный поиск по двум сайтам
    :param list_1:
    :param list_2:
    :return:
    """
    for item in list_2:
        list_1.append(item)

    return list_1


def end_program():
    """
    Завершает работу программы
    """
    print("Программа завершила работу")
    general_function(False)


def reading_json_file(file_data):
    """
    Считывает данные из файла в формате json
    :return: список вакансий
    """
    with open(file_data, 'r', encoding='utf-8') as file:
        data_list = json.load(file)
    return data_list


def writing_to_excel_file(list_in, file_to_write):
    """
    Записывает список вакансий в файл в формате Excel
    :param file_to_write: файл для записи вакансий
    :param list_in: список вакансий
    :return:
    """
    data_tab = pandas.DataFrame(data=list_in)
    file = open(file_to_write, 'wb')
    data_tab.to_excel(file, index=False)
    file.close()


def input_error():
    """
    Возвращает в главное меню
    """
    print("Ошибка ввода. Попробуйте снова")
    general_function(True)


if __name__ == '__main__':
    print("Программа предоставляет возможность поиска вакансий "
          "на порталах HeadHunter и SuperJob")

    general_function(True)
