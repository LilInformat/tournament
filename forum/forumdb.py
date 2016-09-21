#
# Database access functions for the web forum.
#

import time
import psycopg2
import bleach

## Database connection

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    db_conn = psycopg2.connect("dbname=forum")
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM posts")
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in cursor.fetchall()]
    posts.sort(key=lambda row: row['time'], reverse=True)
    db_conn.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    if content:
      db_conn = psycopg2.connect("dbname=forum")
      t = time.strftime('%c', time.localtime())
      #DB.append((t, content))
      content_valid = bleach.clean(content)
      cursor = db_conn.cursor()
      cursor.execute("insert into posts values (%s)",(content_valid,))
      db_conn.commit()
      db_conn.close()
