import allure
import pytest
from allure import severity_level
from pytest import fixture


@allure.severity(severity_level.BLOCKER)
@allure.epic("Тестирование API")
@allure.feature("Добавление поста")
@allure.testcase("Задача D1")
@allure.story("Добавление и публикация нового поста, содержащего заголовок и текст")
@allure.title("Добавление нового поста")
@allure.description(
    """
    Цель:
        Проверить добавление и публикацию нового поста с заголовком и текстом
    
    Предусловие:
        Проект WordPress развернут

    Шаги:
        1. Добавить и опубликовать новый пост с заголовком и текстом,
           используя POST запрос к API "wp/v2/posts"
        2. Проверить статус код
        3. Проверить заголовок нового поста, используя запрос к БД
        4. Проверить текст нового поста, используя запрос к БД
        5. Проверить статус нового поста, используя запрос к БД
        
    Постусловие:
        - Удалить пост

    Ожидаемый результат:
        - Пост добавлен успешно
        - Статус код "201 Created"
        - Заголовок соответствует введенному значению
        - Текст соответствует введенному значению
        - Статус нового поста - "publish"
        """)
@pytest.mark.parametrize('test_data_for_api',
                         [{'status': 'publish'}],
                         indirect=True)
def test_add_post(api_route: fixture, sql_db: fixture,
                  test_data_for_api: fixture, delete_data: fixture):
    post_id = None
    try:
        with allure.step('Добавить и опубликовать новый пост с заголовком и текстом,'
                         'используя POST запрос к API "wp/v2/posts"'):
            response = api_route.request_to_add_post(test_data_for_api)
        post_id = response.json()['id']
        api_title = test_data_for_api['title']
        api_content = test_data_for_api['content']
        api_status = test_data_for_api['status']

        db_post = sql_db.db_get_post_by_id(post_id)
        db_title = db_post['post_title']
        db_content = db_post['post_content']
        db_status = db_post['post_status']

        with allure.step('Проверить статус код'):
            assert response.status_code == 201, f'Expected status code "201 Created", but got "{response.status_code}"'

        with allure.step('Проверить заголовок нового поста, используя запрос к БД'):
            assert api_title == db_title, f'Expected title "{api_title}", but got "{db_title}"'

        with allure.step('Проверить текст нового поста, используя запрос к БД'):
            assert api_content == db_content, f'Expected content "{api_content}", but got "{db_content}"'

        with allure.step('Проверить статус нового поста, используя запрос к БД'):
            assert api_status == db_status, f'Expected status "{api_status}", but got "{db_status}"'
    finally:
        delete_data(post_id)
