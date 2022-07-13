import requests
from dotenv import load_dotenv
import os
from itertools import count


SJ_KEY = os.getenv('SJ_KEY')


def predict_rub_salary(salary_from=None, salary_to=None):
    salary = 0
    if salary_from and salary_to:
        salary = (salary_from + salary_to) / 2
    elif salary_to:
        salary = salary_to * 0.8
    elif salary_from:
        salary = salary_from * 1.2
    return salary


def get_hh_vacancies_json(lang):
    hh_url = "https://api.hh.ru/vacancies"
    moscow_id = 1
    vacancies_period = 30
    page = 0
    payload = {
        "text": lang,
        "area": moscow_id,
        "period": vacancies_period,
        "page": page
    }
    vacancies = requests.get(hh_url, params=payload)
    vacancies.raise_for_status()
    vacancies_json = vacancies.json()
    return vacancies_json


def hh_predict_rub_salary(vacancy):
    salary_from = vacancy["salary"]['from']
    salary_to = vacancy["salary"]['to']
    if vacancy["salary"] and vacancy["salary"]['currency'] == 'RUR':
        return predict_rub_salary(salary_from, salary_to), 1


def hh_average_salary(lang):
    amount = 0
    sum = 0
    for page in range(get_hh_vacancies_json(lang)["pages"]):
        vacancies_json = get_hh_vacancies_json(lang)
        salary_json = vacancies_json["items"]
        for vacancy in salary_json:
            if vacancy["salary"] and vacancy["salary"]['currency'] == 'RUR':
                sum += hh_predict_rub_salary(vacancy)[0]
                amount += hh_predict_rub_salary(vacancy)[1]
    average_salary = int(sum//amount)
    return amount, average_salary


def get_hh_vacancies_languages_dict():
    hh_programming_languages = {
        "Python": 0,
        "Java": 0,
        "JavaScript": 0,
        "Ruby": 0,
        "PHP": 0,
        "C++": 0,
        "C#": 0,
        "C": 0,
        "Go": 0
    }
    for lang in hh_programming_languages:
        about_programming_vacancies = {
            "vacancies_found": 0,
            "vacancies_processed": 0,
            "average_salary": 0
        }
        about_programming_vacancies["vacancies_found"] = get_hh_vacancies_json(lang)["found"]
        about_programming_vacancies["vacancies_processed"], about_programming_vacancies["average_salary"] = hh_average_salary(lang)
        hh_programming_languages[lang] = about_programming_vacancies
    return hh_programming_languages


def sj_get_vacancies(page=1, language=''):
    sj_url = "https://api.superjob.ru/2.0/vacancies"
    headers = {
        'X-Api-App-Id': SJ_KEY
    }
    params = {
        'catalogues': 48,
        'town': 'Moscow',
        'period': 30,
        'page': page,
        'keyword': language
    }

    response = requests.get(sj_url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def sj_predict_rub_salary(vacancy):
    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']
    if int(predict_rub_salary(salary_from, salary_to)) == 0:
        return None
    else:
        return predict_rub_salary(salary_from, salary_to)


def sj_average_salary(lang):
    amount = 0
    sum = 0
    for page in count(1, 1):
        vacancies_json = sj_get_vacancies(
            page,
            language=lang
        )
        print(vacancies_json)
        # salary_json = vacancies_json["items"]
        # for vacancy in salary_json:
        #     if vacancy["salary"]:
        #         sum += hh_predict_rub_salary(vacancy)[0]
        #         count += hh_predict_rub_salary(vacancy)[1]
    average_salary = int(sum//amount)
    return amount, average_salary


def get_sj_vacancies_languages_dict():
    sj_programming_languages = {
        "Python": 0,
        "Java": 0,
        "JavaScript": 0,
        "Ruby": 0,
        "PHP": 0,
        "C++": 0,
        "C#": 0,
        "C": 0,
        "Go": 0
    }
    for lang in sj_programming_languages:
        about_programming_vacancies = {
            "vacancies_found": 0,
            "vacancies_processed": 0,
            "average_salary": 0
        }
        about_programming_vacancies["vacancies_found"] = 500
        about_programming_vacancies["vacancies_processed"], about_programming_vacancies["average_salary"] = sj_average_salary(lang)
        sj_programming_languages[lang] = about_programming_vacancies
    return sj_programming_languages


def main():
    load_dotenv()
    sj_vacancies_json = sj_get_vacancies()
    for vacancy in sj_vacancies_json['objects']:
        print(vacancy['profession'] + ', Москва,', sj_predict_rub_salary(vacancy))
    # a = sj_average_salary('Python')
    # hh_vacancies_statistics = get_hh_vacancies_languages_dict()
    # print(hh_vacancies_statistics)
    print(sj_get_vacancies())
    # sj_vacancies_statistics = get_sj_vacancies_languages_dict()
    # print(sj_vacancies_statistics)


if __name__ == "__main__":
    main()
