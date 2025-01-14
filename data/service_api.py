from os import getenv
from os.path import join as os_path_join

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from requests.models import Response

load_dotenv()


class ServiceAPI:
    """Service API endpoints and HTTP methods."""
    def __init__(self):
        self.route = getenv('POSTS_ROUTE')
        self.username = getenv('POSTS_USERNAME')
        self.password = getenv('POSTS_PASSWORD')

    def request_to_get_all_posts(self) -> Response:
        """Requests all posts."""
        return requests.get(self.route)

    def request_to_add_post(self, post_data: dict) -> Response:
        """Requests post creation with the specified data."""
        return requests.post(self.route,
                             json=post_data,
                             auth=HTTPBasicAuth(self.username, self.password))

    def request_to_delete_post(self, post_id: int) -> Response:
        """Requests post deletion by the specified id."""
        return requests.delete(os_path_join(self.route, str(post_id)),
                               params={'force': True},
                               auth=HTTPBasicAuth(self.username, self.password))

    def request_to_patch_post(self, post_id: int, new_data: dict) -> Response:
        """Requests partial post editing by the specified id and with the specified data."""
        return requests.patch(os_path_join(self.route, str(post_id)),
                              json=new_data,
                              auth=HTTPBasicAuth(self.username, self.password))

    def request_to_put_post(self, post_id: int, new_data: dict) -> Response:
        """Requests post editing by the specified id and with the specified data."""
        return requests.put(os_path_join(self.route, str(post_id)),
                            json=new_data,
                            auth=HTTPBasicAuth(self.username, self.password))
