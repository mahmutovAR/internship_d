import allure
import pytest
from allure import severity_level
from pytest import fixture

from . import data_assert


@allure.severity(severity_level.CRITICAL)
@allure.epic("Тестирование API")
@allure.feature("Редактирование поста")
@allure.testcase("Задача D1")
@allure.story("Редактирование поста, содержащего заголовок и текст, путем внесения нового заголовка и удалением текста автоматически")
@allure.title("Полное редактирование поста")
@allure.description(
    """
    Цель:
        Проверить редактирование поста,
        содержащего заголовок и текст,
        путем внесения нового заголовка и удалением текста автоматически

    Предусловие
        Проект WordPress развернут

    Шаги:
        1. Добавить новый пост с заголовком и текстом,
        используя POST запрос к API "wp/v2/posts"
        2. Проверить, что пост добавлен, используя запрос к БД
        3. Редактировать только заголовок поста,
        используя PUT запрос к API "wp/v2/posts"
        4. Проверить статус код
        5. Проверить заголовок поста, используя запрос к БД
        6. Проверить текст поста, используя запрос к БД

    Постусловие:
        - Удалить пост

    Ожидаемый результат:
        - Пост отредактирован успешно: заголовок отредактирован, текст удален автоматически
        - Статус код "200 OK"
        """)
@pytest.mark.xfail(reason='PATCH and PUT methods work the same way')
@pytest.mark.parametrize('ini_post', [
    {'title': 'post',
     'content': 'with content',
     'status': 'publish'}])
@pytest.mark.parametrize('new_title', ['just new post title'])
def test_put_post(api_route: fixture, sql_db: fixture, delete_data: fixture,
                  ini_post: dict, new_title: str):
    with allure.step('Добавить новый пост с заголовком и текстом,'
                     'используя POST запрос к API "wp/v2/posts"'):
        response = api_route.add_post(ini_post)
        post_id = response.json()['id']
    delete_data.append(post_id)

    with allure.step('Проверить, что пост добавлен, используя запрос к БД'):
        data_assert.post_exists_via_db(sql_db.get_post_data(post_id))

    with allure.step('Редактировать только заголовок поста, используя PUT запрос к API "wp/v2/posts"'):
        response = api_route.put_post(post_id, {'title': new_title})

    with allure.step('Проверить статус код'):
        data_assert.http_status_code(response.status_code, 200)

    db_post = sql_db.get_post_data(post_id)
    db_title = db_post['post_title']
    db_content = db_post['post_content']

    with allure.step('Проверить заголовок поста, используя запрос к БД'):
        data_assert.post_title(new_title, db_title)

    with allure.step('Проверить текст поста, используя запрос к БД'):
        assert ini_post['content'] != db_content, f'Expected content "{ini_post['content']}", but got "{db_content}"'
        assert not db_content, f'Expected no content, but got "{db_content}"'
