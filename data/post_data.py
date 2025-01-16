from datetime import datetime, timezone

from faker import Faker


class PostData:
    """Class with required post fields."""
    def __init__(self, title: str = None, content: str = None, status: str = 'draft', author: str = '1',
                 type_: str = 'post', to_ping: str = '', pinged: str = '', content_filtered: str = ''):
        self.fake = Faker()
        self.title = title
        self.content = content
        self.status = status
        self.author = author
        self.type_ = type_
        self.to_ping = to_ping
        self.pinged = pinged
        self.content_filtered = content_filtered

    def generate_post_data(self):
        """Returns dict with post data required fields."""
        if not self.title:
            self.title = self.fake.text(max_nb_chars=20)
        if not self.content:
            self.content = self.fake.sentence(nb_words=5)
        return {'title': self.title,
                'content': self.content,
                'status': self.status,
                'author': self.author,
                'type_': self.type_,
                'date': datetime.now(),
                'date_gmt': datetime.now(timezone.utc),
                'modified': datetime.now(),
                'modified_gmt': datetime.now(timezone.utc),
                'excerpt': self.content,
                'to_ping': self.to_ping,
                'pinged': self.pinged,
                'content_filtered': self.content_filtered}
