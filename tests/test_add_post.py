import allure
import pytest
from allure import severity_level
from pytest import fixture

from . import data_assert


@allure.severity(severity_level.BLOCKER)
@allure.epic("Тестирование API")
@allure.feature("Добавление поста")
@allure.testcase("Задача D1")
@allure.story("Добавление (публикация) поста, содержащего заголовок и/или текст")
@allure.title("Добавление поста")
@allure.description(
    """
    Цель:
        Проверить добавление (публикацию) поста, содержащего заголовок и/или текст
    
    Предусловие:
        Проект WordPress развернут

    Шаги:
        1. Добавить (опубликовать) пост с заголовком и/или текстом,
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
        - Статус соответствует введенному значению
        """)
@pytest.mark.parametrize('title, content, status',
                         [('post with title and content', 'some text', 'draft'),
                          ('post without content', '', 'draft'),
                          ('publish this post!!', 'and add content', 'publish'),
                          ('', 'no title', 'draft'),
                          ('', 'publish without title', 'publish')])
def test_add_post(api_route: fixture, sql_db: fixture, delete_data: fixture,
                  title: str, content: str, status: str):
    with allure.step('Добавить (опубликовать) пост с заголовком и/или текстом,'
                     'используя POST запрос к API "wp/v2/posts"'):
        response = api_route.add_post({'title': title, 'content': content, 'status': status})
    post_id = response.json()['id']
    delete_data.append(post_id)
    db_post = sql_db.get_post_data(post_id)
    db_title = db_post['post_title']
    db_content = db_post['post_content']
    db_status = db_post['post_status']

    with allure.step('Проверить статус код'):
        data_assert.http_status_code(response.status_code, 201)

    with allure.step('Проверить заголовок нового поста, используя запрос к БД'):
        data_assert.post_title(title, db_title)

    with allure.step('Проверить текст нового поста, используя запрос к БД'):
        data_assert.post_content(content, db_content)

    with allure.step('Проверить статус нового поста, используя запрос к БД'):
        data_assert.post_status(status, db_status)
