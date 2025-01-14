import allure
import pytest
from allure import severity_level
from pytest import fixture


@allure.severity(severity_level.BLOCKER)
@allure.epic("Тестирование API")
@allure.feature("Удаление поста")
@allure.testcase("Задача D1")
@allure.story("Удаление опубликованного поста, содержащего заголовок и текст")
@allure.title("Удаление поста")
@allure.description(
    """   
    Цель:
        Проверить удаление опубликованного поста с заголовком и текстом
    
    Предусловие:
        Проект WordPress развернут

    Шаги:
        1. Добавить и опубликовать новый пост с заголовком и текстом,
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
def test_delete_post(api_route: fixture, sql_db: fixture, test_data_for_api: fixture):
    with allure.step('Добавить и опубликовать новый пост с заголовком и текстом,'
                     'используя POST запрос к API "wp/v2/posts"'):
        response = api_route.request_to_add_post(test_data_for_api)
    post_id = response.json()['id']

    with allure.step('Проверить, что пост добавлен, используя запрос к БД'):
        assert sql_db.db_get_post_by_id(post_id), 'Post is expected to be published'

    with allure.step('Удалить пост, используя DELETE запрос к API "wp/v2/posts"'):
        response = api_route.request_to_delete_post(post_id)

    with allure.step('Проверить статус код'):
        assert response.status_code == 200, f'Expected status code "200 OK", but got "{response.status_code}"'

    with allure.step('Проверить, что пост удален, используя запрос к БД'):
        assert not sql_db.db_get_post_by_id(post_id), 'Post is expected to be deleted'
