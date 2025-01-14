from datetime import datetime, timezone

from faker import Faker


class BaseGenerator:
    """Base data generator class."""
    def __init__(self):
        self.fake = Faker()
        self.fake_title = self.fake.text(max_nb_chars=20)
        self.fake_content = self.fake.sentence(nb_words=5)

    def generate_post_title(self, post_title: str) -> str:
        if post_title is None:
            return self.fake_title
        return post_title

    def generate_post_content(self, post_content: str) -> str:
        if post_content is None:
            return self.fake_content
        return post_content

    @staticmethod
    def generate_post_status(post_status: str) -> str:
        if post_status is None:
            return 'draft'
        return post_status

    @staticmethod
    def generate_post_author(post_author: str) -> str:
        if post_author is None:
            return '1'
        return post_author

    @staticmethod
    def generate_post_type(post_type: str) -> str:
        if post_type is None:
            return 'post'
        return post_type

    @staticmethod
    def generate_post_date() -> datetime:
        return datetime.now()

    @staticmethod
    def generate_post_date_gmt() -> datetime:
        return datetime.now(timezone.utc)

    def generate_post_excerpt(self, post_excerpt: str) -> str:
        if post_excerpt is None:
            return self.fake_content
        return post_excerpt

    @staticmethod
    def generate_post_to_ping(to_ping: str) -> str:
        if to_ping is None:
            return ''
        return to_ping

    @staticmethod
    def generate_post_pinged(pinged: str) -> str:
        if pinged is None:
            return ''
        return pinged

    @staticmethod
    def generate_post_content_filtered(content_filtered: str) -> str:
        if content_filtered is None:
            return ''
        return content_filtered
