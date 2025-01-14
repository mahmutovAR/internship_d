from dataclasses import dataclass
from datetime import datetime


@dataclass
class PostData:
    """Class contains required post fields."""
    title: str = None
    content: str = None
    status: str = None
    author: str = None
    post_type: str = None
    date: datetime = None
    date_gmt: datetime = None
    modified: datetime = None
    modified_gmt: datetime = None
    excerpt: str = None
    to_ping: str = None
    pinged: str = None
    content_filtered: str = None
