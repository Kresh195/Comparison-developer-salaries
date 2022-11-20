from __future__ import print_function
from hh_ru import get_hh_vacancies_languages_statistics
from sj_com import get_sj_vacancies_languages_statistics

from terminaltables import AsciiTable


def get_table(title, vacancies_languages_statistics):
    table = [["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
    for language, language_statistics in vacancies_languages_statistics.items():
        table.append([
            language,
            language_statistics["vacancies_found"],
            language_statistics["vacancies_processed"],
            language_statistics["average_salary"]
        ])
    table_instance = AsciiTable(table, title)
    table_instance.justify_columns[2] = 'left'
    return table_instance.table


def main():
    sj_title = "SuperJob Moscow"
    sj_table = get_table(sj_title, get_sj_vacancies_languages_statistics())
    print(sj_table)
    hh_title = "HH.ru Moscow"
    sj_table = get_table(hh_title, get_hh_vacancies_languages_statistics())
    print(sj_table)



if __name__ == '__main__':
    main()
