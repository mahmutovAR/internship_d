from data.data_classes import PostData
from . import BaseGenerator


class PostDataGenerator(BaseGenerator):
    """Post data generator class."""
    def generate_post_data(self, title: str = None, content: str = None, status: str = None,
                           author: str = None, post_type: str = None, to_ping: str = None,
                           pinged: str = None, content_filtered: str = None):
        yield PostData(title=self.generate_post_title(title),
                       content=self.generate_post_content(content),
                       status=self.generate_post_status(status),
                       author=self.generate_post_author(author),
                       post_type=self.generate_post_type(post_type),
                       date=self.generate_post_date(),
                       date_gmt=self.generate_post_date_gmt(),
                       modified=self.generate_post_date(),
                       modified_gmt=self.generate_post_date_gmt(),
                       excerpt=self.generate_post_excerpt(content),
                       to_ping=self.generate_post_to_ping(to_ping),
                       pinged=self.generate_post_pinged(pinged),
                       content_filtered=self.generate_post_content_filtered(content_filtered))
