import allure
from allure import severity_level
from pytest import fixture


@allure.severity(severity_level.CRITICAL)
@allure.epic("Тестирование API")
@allure.feature("Получение данных поста API запросом")
@allure.testcase("Задача D2")
@allure.story("Добавление поста прямым запросом к БД и получение данных API запросом")
@allure.title("Получение данных поста")
@allure.description(
    """
    Цель:
        Получение заголовка, текста и статуса поста, используя API запрос

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
                          test_data_for_database: fixture, delete_data: fixture):
    post_id = None
    try:
        with allure.step('Добавить новый пост с заголовком и текстом, используя запрос к БД'):
            post_id = sql_db.db_add_post(test_data_for_database)

        with allure.step('Проверить добавление поста, используя запрос к БД'):
            assert sql_db.db_get_post_by_id(post_id), 'Post is expected to be added'

        with allure.step('Получить данные поста, используя GET запрос к API "wp/v2/posts" с указанием id'):
            response = api_route.request_to_get_post_data(post_id)

        with allure.step('Проверить статус код'):
            assert response.status_code == 200, f'Expected status code "200 OK", but got "{response.status_code}"'

        api_title = response.json()['title']['raw']
        api_content = response.json()['content']['raw']
        api_status = response.json()['status']

        test_title = test_data_for_database.title
        test_content = test_data_for_database.content
        test_status = test_data_for_database.status

        with allure.step('Проверить заголовок поста, используя данные из API запроса'):
            assert test_title == api_title, f'Expected title "{test_title}", but got "{api_title}"'

        with allure.step('Проверить текст поста, используя данные из API запроса'):
            assert test_content == api_content, f'Expected content "{test_content}", but got "{api_content}"'

        with allure.step('Проверить статус поста, используя данные из API запроса'):
            assert test_status == api_status, f'Expected status "{test_status}", but got "{api_status}"'
    finally:
        delete_data(post_id)
