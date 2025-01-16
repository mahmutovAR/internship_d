class DataAssert:
    @staticmethod
    def http_status_code(expected_value: int, value: int) -> None:
        assert expected_value == value, f'Expected status code "{expected_value}", but got "{value}"'

    @staticmethod
    def post_title(expected_value: str, value: str) -> None:
        assert expected_value == value, f'Expected post title "{expected_value}", but got "{value}"'

    @staticmethod
    def post_content(expected_value: str, value: str) -> None:
        assert expected_value == value, f'Expected post content "{expected_value}", but got "{value}"'

    @staticmethod
    def post_status(expected_value: str, value: str) -> None:
        assert expected_value == value, f'Expected post status "{expected_value}", but got "{value}"'

    @staticmethod
    def post_exists_via_db(value: dict | None) -> None:
        assert value, 'Post is expected to be added'

    @staticmethod
    def post_not_exists_via_db(value: dict | None) -> None:
        assert not value, 'Post is expected to be added'


data_assert = DataAssert()
