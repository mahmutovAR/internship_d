import allure
from allure import severity_level
from pytest import fixture


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
def test_put_post(api_route: fixture, sql_db: fixture,
                  test_data_for_api_for_edit_assert: fixture, delete_data: fixture):
    try:
        with allure.step('Добавить новый пост с заголовком и текстом,'
                         'используя POST запрос к API "wp/v2/posts"'):
            ini_data = test_data_for_api_for_edit_assert[0]
            ini_title = ini_data['title']
            ini_content = ini_data['content']
            response = api_route.request_to_add_post(ini_data)
            post_id = response.json()['id']

        with allure.step('Проверить, что пост добавлен, используя запрос к БД'):
            assert sql_db.db_get_post_by_id(post_id), 'Post is expected to be added'

        with allure.step('Редактировать только заголовок поста, используя PUT запрос к API "wp/v2/posts"'):
            new_data = test_data_for_api_for_edit_assert[1]
            new_title = new_data['title']
            assert ini_title != new_title, f'Expected new title "{new_title}", but got "{ini_title}"'
            response = api_route.request_to_put_post(post_id, {'title': new_title})

        with allure.step('Проверить статус код'):
            assert response.status_code == 200, f'Expected status code "200 OK", but got "{response.status_code}"'

        db_post = sql_db.db_get_post_by_id(post_id)
        db_title = db_post['post_title']
        db_content = db_post['post_content']

        with allure.step('Проверить заголовок поста, используя запрос к БД'):
            assert new_title == db_title, f'Expected title "{new_title}", but got "{db_title}"'

        with allure.step('Проверить текст поста, используя запрос к БД'):
            assert ini_content != db_content, f'Expected content "{ini_content}", but got "{db_content}"'
            assert not db_content, f'Expected content "{ini_content}", but got "{db_content}"'

    finally:
        delete_data(post_id)
