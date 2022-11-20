# Сравниваем вакансии программистов
Получение таблиц со средними зарплатами разработчиков на разных языках программирования 
в Москве, получаемых при обработке вакансий с сервисов
[hh](https://hh.ru) и [superjob](https://www.superjob.ru).

## Как установить
Python3 должен быть уже установлен. Затем используйте `pip` (или `pip3`, если 
есть конфликт с Python2) для установки зависимостей:
```sh
pip install -r requirements.txt
```
## Переменные окружения
Переменные окружения — переменные, необходимые для работы кода.
Для работы этого кода, вам необходимо:  
1. Зарегистрируйте приложение SuperJob [по ссылке](https://api.superjob.ru/)
чтобы получить ключ(При регистрации приложения от вас потребуют указать сайт.
Введите любой, они не проверяют.)  
2. Создать рядом с `main.py` файл с названием .env и записать в него следующее:
```python
SJ_KEY=Ваш ключ 
```
## Запуск
Чтобы запустить код, используйте следующую команду в терминале:
```sh
python main.py
```
## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).
 
