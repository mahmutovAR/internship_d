from datetime import datetime, timezone

from faker import Faker

from . import PostFields


class PostData:
    """Class with required post fields."""
    def __init__(self):
        self.fake = Faker()

    def generate_post_data(self, title: str = None, content: str = None, status: str = 'draft', author: str = '1',
                           type_: str = 'post', to_ping: str = '', pinged: str = '', content_filtered: str = ''):
        if not title:
            title = self.fake.text(max_nb_chars=20)
        if not content:
            content = self.fake.sentence(nb_words=5)
        return PostFields(title=title,
                          content=content,
                          status=status,
                          author=author,
                          type_=type_,
                          date=datetime.now(),
                          date_gmt=datetime.now(timezone.utc),
                          modified=datetime.now(),
                          modified_gmt=datetime.now(timezone.utc),
                          excerpt=content,
                          to_ping=to_ping,
                          pinged=pinged,
                          content_filtered=content_filtered)
