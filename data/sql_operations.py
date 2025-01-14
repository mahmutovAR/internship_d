import mysql.connector as sql

from data.data_classes import PostData
from . import DatabaseConfig


class PostsDatabase:
    """Class with main database SQL operations."""
    def __init__(self):
        self.db_config = DatabaseConfig.config

    def db_count_posts(self) -> int:
        """Returns the total number of posts."""
        with sql.connect(**self.db_config) as conn:
            with conn.cursor() as cur:
                sql_command = 'SELECT count( * ) FROM wp_posts'
                cur.execute(sql_command)
                total_posts = cur.fetchone()[0]
        return total_posts

    def db_get_all_posts(self) -> list:
        """Returns all posts."""
        with sql.connect(**self.db_config) as conn:
            with conn.cursor() as cur:
                sql_command = 'SELECT * FROM wp_posts ORDER BY id'
                cur.execute(sql_command)
                all_posts = cur.fetchall()
        return all_posts

    def db_add_post(self, post_data: PostData) -> int:
        """Inserts post with the specified data."""
        with sql.connect(**self.db_config) as conn:
            with conn.cursor(dictionary=True) as cur:
                post_title = post_data.title
                post_content = post_data.content
                post_status = post_data.status
                post_author = post_data.author
                post_type = post_data.post_type
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

    def db_get_post_by_id(self, post_id: str | int) -> dict:
        """Returns post data with the specified id."""
        with sql.connect(**self.db_config) as conn:
            with conn.cursor(dictionary=True) as cur:
                sql_command = """SELECT * FROM wp_posts
                            WHERE id = %s"""
                cur.execute(sql_command, (post_id,))
                post_data = cur.fetchone()
        return post_data

    def db_delete_post_by_id(self, post_id: str | int) -> None:
        """Deletes post by the specified id."""
        with sql.connect(**self.db_config) as conn:
            with conn.cursor(dictionary=True) as cur:
                sql_command = "DELETE FROM wp_posts WHERE id = %s"
                cur.execute(sql_command, (post_id,))
            conn.commit()
