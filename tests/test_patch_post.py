import allure
import pytest
from allure import severity_level
from pytest import fixture

from . import data_assert


@allure.severity(severity_level.CRITICAL)
@allure.epic("Тестирование API")
@allure.feature("Редактирование поста")
@allure.testcase("Задача D1")
@allure.story("Частичное редактирование поста, содержащего заголовок и текст, путем внесения изменений только в текст")
@allure.title("Частичное редактирование поста")
@allure.description(
    """
    Цель:
        Проверить частичное редактирование поста,
        содержащего заголовок и текст,
        путем внесения изменений только в текст

    Предусловие
        Проект WordPress развернут
    
    Шаги:
        1. Добавить новый пост с заголовком и текстом,
        используя POST запрос к API "wp/v2/posts"
        2. Проверить, что пост добавлен, используя запрос к БД
        3. Редактировать только текст поста,
        используя PATCH запрос к API "wp/v2/posts"
        4. Проверить статус код
        5. Проверить заголовок поста, используя запрос к БД
        6. Проверить текст поста, используя запрос к БД
        7. Проверить статус нового поста, используя запрос к БД
    
    Постусловие:
        - Удалить пост
    
    Ожидаемый результат:
        - Пост отредактирован успешно: заголовок без изменения, текст отредактирован
        - Статус код "200 OK"
        """)
@pytest.mark.parametrize('ini_post', [
    {'title': 'new test post',
     'content': 'with content',
     'status': 'publish'}])
@pytest.mark.parametrize('new_content', ['just some text'])
def test_patch_post(api_route: fixture, sql_db: fixture, delete_data: fixture,
                    ini_post: dict, new_content: str):
    with allure.step('Добавить новый пост с заголовком и текстом,'
                     'используя POST запрос к API "wp/v2/posts"'):
        response = api_route.add_post(ini_post)
        post_id = response.json()['id']
    delete_data.append(post_id)

    with allure.step('Проверить, что пост добавлен, используя запрос к БД'):
        data_assert.post_exists_via_db(sql_db.get_post_data(post_id))

    with allure.step('Редактировать только текст поста, используя PATCH запрос к API "wp/v2/posts"'):
        response = api_route.patch_post(post_id, {'content': new_content})

    with allure.step('Проверить статус код'):
        data_assert.http_status_code(response.status_code, 200)

    db_post = sql_db.get_post_data(post_id)
    db_title = db_post['post_title']
    db_content = db_post['post_content']
    db_status = db_post['post_status']

    with allure.step('Проверить заголовок поста, используя запрос к БД'):
        data_assert.post_title(ini_post['title'], db_title)

    with allure.step('Проверить текст поста, используя запрос к БД'):
        data_assert.post_content(new_content, db_content)

    with allure.step('Проверить статус нового поста, используя запрос к БД'):
        data_assert.post_status(ini_post['status'], db_status)
