import pytest
from pytest import fixture

from api import ServiceAPI
from data import PostData
from database import PostsDatabase


@pytest.fixture
def api_route() -> ServiceAPI:
    """Returns WordPress API URL."""
    return ServiceAPI()


@pytest.fixture
def sql_db() -> PostsDatabase:
    """Returns Posts database module."""
    return PostsDatabase()


@pytest.fixture
def test_data_for_db() -> PostData:
    return PostData().generate_post_data()


@pytest.fixture
def test_data_for_api(request) -> dict:
    """Returns test data for requests functions."""
    fields = request.param
    post_data = PostData(**fields).generate_post_data()
    return {'title': post_data['title'],
            'content': post_data['content'],
            'status': post_data['status']}


@pytest.fixture
def delete_data(sql_db: fixture):
    def delete_(data_id: int | str):
        try:
            if data_id:
                sql_db.delete_post(str(data_id))
        except Exception as exc:
            exc.add_note('Data deletion failed')
            raise
    return delete_
