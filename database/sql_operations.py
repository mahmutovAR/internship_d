import mysql.connector as sql

from data import PostFields
from . import DatabaseConfig


class PostsDatabase:
    """Class with main database SQL operations."""
    def __init__(self):
        self.db_config = DatabaseConfig.config

    def add_post(self, post_data: PostFields) -> int:
        """Inserts post with the specified data."""
        with sql.connect(**self.db_config) as conn:
            with conn.cursor(dictionary=True) as cur:
                post_title = post_data.title
                post_content = post_data.content
                post_status = post_data.status
                post_author = post_data.author
                post_type = post_data.type_
                post_date = post_data.date
                post_date_gmt = post_data.date_gmt
                post_modified = post_data.modified
                post_modified_gmt = post_data.modified_gmt
                post_excerpt = post_data.excerpt
                to_ping = post_data.to_ping
                pinged = post_data.pinged
                post_content_filtered = post_data.content_filtered

                sql_command = ("""INSERT
                INTO wp_posts (post_title, post_content, post_status, post_author, post_type, post_date, post_date_gmt, post_modified, post_modified_gmt, post_excerpt, to_ping, pinged, post_content_filtered)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
                sql_data = (post_title, post_content, post_status, post_author, post_type, post_date, post_date_gmt, post_modified, post_modified_gmt, post_excerpt, to_ping, pinged, post_content_filtered)
                cur.execute(sql_command, sql_data)

                cur.execute("SELECT LAST_INSERT_ID()")
                post_id = cur.fetchone()['LAST_INSERT_ID()']
            conn.commit()
        return post_id

    def get_post_data(self, post_id: str | int) -> dict:
        """Returns post data with the specified id."""
        with sql.connect(**self.db_config) as conn:
            with conn.cursor(dictionary=True) as cur:
                sql_command = """SELECT * FROM wp_posts
                            WHERE id = %s"""
                cur.execute(sql_command, (post_id,))
                post_data = cur.fetchone()
        return post_data

    def delete_post(self, post_id: str | int) -> None:
        """Deletes post by the specified id."""
        with sql.connect(**self.db_config) as conn:
            with conn.cursor(dictionary=True) as cur:
                sql_command = "DELETE FROM wp_posts WHERE id = %s"
                cur.execute(sql_command, (post_id,))
            conn.commit()

    def truncate_post_table(self) -> None:
        """Deletes all data from database."""
        with sql.connect(**self.db_config) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM wp_posts")
            conn.commit()
