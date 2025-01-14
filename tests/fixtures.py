import pytest
from faker import Faker
from pytest import fixture

from data import ServiceAPI, PostsDatabase
from data.data_generators import PostDataGenerator


fake = Faker()


@pytest.fixture
def api_route() -> ServiceAPI:
    """Returns WordPress API URL."""
    yield ServiceAPI()


@pytest.fixture
def sql_db() -> PostsDatabase:
    """Returns Posts database module."""
    yield PostsDatabase()


@pytest.fixture
def test_data_for_api(request) -> dict:
    """Returns test data for requests functions."""
    fields = request.param
    test_data = next(PostDataGenerator().generate_post_data(**fields))
    yield {'title': test_data.title,
           'content': test_data.content,
           'status': test_data.status}


@pytest.fixture
def test_data_for_edit_assert():
    """Returns two test data sets for testing editing functions."""
    ini_data = next(PostDataGenerator().generate_post_data())
    new_data = next(PostDataGenerator().generate_post_data())

    yield [{'title': ini_data.title, 'content': ini_data.content, 'status': ini_data.status},
           {'title': new_data.title, 'content': new_data.content, 'status': new_data.status}]
    
    
@pytest.fixture
def test_data_for_database(request):
    """Returns test data sets for database operations."""
    fields = request.param
    yield next(PostDataGenerator().generate_post_data(**fields))


@pytest.fixture
def get_data(sql_db: fixture, request):
    """Returns data from database by specified id."""
    try:
        data = sql_db.db_get_post_by_id(request.param)
    except Exception as exc:
        exc.add_note('Data getting failed')
        raise
    else:
        return data


@pytest.fixture
def delete_data(sql_db: fixture):
    def delete_test_data(data_id: int | str):
        try:
            if data_id:
                sql_db.db_delete_post_by_id(str(data_id))
        except Exception as exc:
            exc.add_note('Data deletion failed')
            raise
    return delete_test_data
