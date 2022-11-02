import requests
from itertools import count
from predict_salary import predict_rub_salary


def get_hh_vacancies_json(language='Python', page=0):
    hh_url = "https://api.hh.ru/vacancies"
    moscow_id = 1
    vacancies_period = 30
    payload = {
        "text": language,
        "area": moscow_id,
        "period": vacancies_period,
        "page": page
    }
    vacancies = requests.get(hh_url, params=payload)
    vacancies.raise_for_status()
    vacancies_json = vacancies.json()
    return vacancies_json


def get_hh_vacancies_statistics(language):
    average_salaries = []
    for page in count(0, 1):
        vacancies = get_hh_vacancies_json(language, page)
        if page >= vacancies["pages"] - 1:
            break
        for vacancy in vacancies["items"]:
            if not vacancy["salary"] or vacancy["salary"]["currency"] != "RUR":
                continue
            salary = predict_rub_salary(vacancy["salary"]["from"], vacancy["salary"]["to"])
            average_salaries.append(salary)
    vacancies_processed = len(average_salaries)
    average_salary = sum(average_salaries)//vacancies_processed
    about_programming_vacancies = {
        "vacancies_found": get_hh_vacancies_json()["found"],
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }
    return about_programming_vacancies


def get_hh_vacancies_languages_statistics():
    hh_programming_languages = ["Python", "Java", "JavaScript", "Ruby", "PHP", "C++", "C#", "C", "Go"]
    hh_salary_statistics = {}
    for language in hh_programming_languages:
        hh_salary_statistics[language] = get_hh_vacancies_statistics(language)
    return hh_salary_statistics


def main():
    get_hh_vacancies_languages_statistics()


if __name__ == "__main__":
    main()
