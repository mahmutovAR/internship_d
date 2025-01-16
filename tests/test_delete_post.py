import allure
import pytest
from allure import severity_level
from pytest import fixture

from . import data_assert


@allure.severity(severity_level.BLOCKER)
@allure.epic("Тестирование API")
@allure.feature("Удаление поста")
@allure.testcase("Задача D1")
@allure.story("Удаление поста, содержащего заголовок и/или текст")
@allure.title("Удаление поста")
@allure.description(
    """   
    Цель:
        Проверить удаление поста с заголовком и/или текстом
    
    Предусловие:
        Проект WordPress развернут

    Шаги:
        1. Добавить (опубликовать) новый пост с заголовком и/или текстом,
           используя POST запрос к API "wp/v2/posts"
        2. Проверить, что пост добавлен, используя запрос к БД
        3. Удалить пост, используя DELETE запрос к API "wp/v2/posts"
        4. Проверить статус код
        5. Проверить, что пост удален, используя запрос к БД

    Ожидаемый результат:
        - Пост удален успешно
        - Статус код "200 OK"
        """)
@pytest.mark.parametrize('test_data_for_api',
                         [{'status': 'publish'}],
                         indirect=True)
def test_delete_post(api_route: fixture, sql_db: fixture,
                     test_data_for_api: fixture, delete_data: fixture):
    with allure.step('Добавить (опубликовать) новый пост с заголовком и/или текстом,'
                     'используя POST запрос к API "wp/v2/posts"'):
        response = api_route.add_post(test_data_for_api)
        post_id = response.json()['id']
    delete_data.append(post_id)

    with allure.step('Проверить, что пост добавлен, используя запрос к БД'):
        data_assert.post_exists_via_db(sql_db.get_post_data(post_id))

    with allure.step('Удалить пост, используя DELETE запрос к API "wp/v2/posts"'):
        response = api_route.delete_post(post_id)

    with allure.step('Проверить статус код'):
        data_assert.http_status_code(response.status_code, 200)

    with allure.step('Проверить, что пост удален, используя запрос к БД'):
        data_assert.post_not_exists_via_db(sql_db.get_post_data(post_id))
