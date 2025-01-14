import allure
from allure import severity_level
from pytest import fixture


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
def test_patch_post(api_route: fixture, sql_db: fixture,
                    test_data_for_edit_assert: fixture, delete_data: fixture):
    try:
        with allure.step('Добавить новый пост с заголовком и текстом,'
                         'используя POST запрос к API "wp/v2/posts"'):
            ini_data = test_data_for_edit_assert[0]
            ini_title = ini_data['title']
            ini_content = ini_data['content']
            ini_status = ini_data['status']
            response = api_route.request_to_add_post(ini_data)
            post_id = response.json()['id']

        with allure.step('Проверить, что пост добавлен, используя запрос к БД'):
            assert sql_db.db_get_post_by_id(post_id), 'Post is expected to be added'

        with allure.step('Редактировать только текст поста, используя PATCH запрос к API "wp/v2/posts"'):
            new_data = test_data_for_edit_assert[1]
            new_content = new_data['content']
            assert ini_content != new_content, f'Expected new content "{new_content}", but got "{ini_content}"'
            response = api_route.request_to_patch_post(post_id, {'content': new_content})

        with allure.step('Проверить статус код'):
            assert response.status_code == 200, f'Expected status code "200 OK", but got "{response.status_code}"'

        db_post = sql_db.db_get_post_by_id(post_id)
        db_title = db_post['post_title']
        db_content = db_post['post_content']
        db_status = db_post['post_status']
        
        with allure.step('Проверить заголовок поста, используя запрос к БД'):
            assert ini_title == db_title, f'Expected title "{ini_title}", but got "{db_title}"'

        with allure.step('Проверить текст поста, используя запрос к БД'):
            assert new_content == db_content, f'Expected content "{new_content}", but got "{db_content}"'

        with allure.step('Проверить статус нового поста, используя запрос к БД'):
            assert ini_status == db_status, f'Expected status "{ini_status}", but got "{db_status}"'

    finally:
        delete_data(post_id)
