import allure
from allure import severity_level
from bs4 import BeautifulSoup
from pytest import fixture

from . import data_assert


@allure.severity(severity_level.CRITICAL)
@allure.epic("Тестирование API")
@allure.feature("Получение данных поста API запросом")
@allure.testcase("Задача D2")
@allure.story("Добавление поста прямым запросом к БД и получение данных API запросом")
@allure.title("Получение данных поста")
@allure.description(
    """
    Цель:
        Проверить получение заголовка, текста и статуса поста, используя API запрос

    Предусловие:
        Проект WordPress развернут
    
    Шаги:
        1. Добавить новый пост с заголовком и текстом,
           используя запрос к БД
        2. Проверить добавление поста, используя запрос к БД
        3. Получить данные поста,
           используя GET запрос к API "wp/v2/posts" с указанием id
        4. Проверить статус код
        5. Проверить заголовок поста, используя данные из API запроса
        6. Проверить текст поста, используя данные из API запроса
        7. Проверить статус поста, используя данные из API запроса
        
    Постусловие:
        - Удалить пост
    
    Ожидаемый результат:
        - Пост добавлен успешно
        - Данные поста получены успешно
        - Статус код "200 OK"
        - Заголовок соответствует введенному в БД значению
        - Текст соответствует введенному в БД значению
        - Статус соответствует введенному в БД значению
        """)
def test_request_get_post(api_route: fixture, sql_db: fixture,
                          test_data_for_db: fixture, delete_data: fixture):
    with allure.step('Добавить новый пост с заголовком и текстом, используя запрос к БД'):
        post_id = sql_db.add_post(test_data_for_db)
    delete_data.append(post_id)

    with allure.step('Проверить добавление поста, используя запрос к БД'):
        data_assert.post_exists_via_db(sql_db.get_post_data(post_id))

    with allure.step('Получить данные поста, используя GET запрос к API "wp/v2/posts" с указанием id'):
        response = api_route.get_post_data(post_id)

    with allure.step('Проверить статус код'):
        data_assert.http_status_code(response.status_code, 200)

    api_title = response.json()['title']['rendered']
    bs = BeautifulSoup(response.json()['content']['rendered'], "html.parser")
    api_content = bs.get_text(strip=True)
    api_status = response.json()['status']

    test_title = test_data_for_db.title
    test_content = test_data_for_db.content
    test_status = test_data_for_db.status

    with allure.step('Проверить заголовок поста, используя данные из API запроса'):
        data_assert.post_title(test_title, api_title)

    with allure.step('Проверить текст поста, используя данные из API запроса'):
        data_assert.post_content(test_content, api_content)

    with allure.step('Проверить статус поста, используя данные из API запроса'):
        data_assert.post_status(test_status, api_status)
