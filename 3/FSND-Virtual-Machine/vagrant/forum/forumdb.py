# "Database code" for the DB Forum.

import datetime
import psycopg2
import bleach

# POSTS = [("This is the first post.", datetime.datetime.now())]

DBNAME = "forum"

def get_posts():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect('dbname=forum')
  c = db.cursor()
  c.execute("SELECT time, content FROM posts ORDER BY time DESC") 
  posts = c.fetchall()
  db.close()
  return posts

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  # POSTS.append((content, datetime.datetime.now()))
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  # print "INSERT INTO posts(content) VALUES('%s')" % "'); delete from posts; --"
  c.execute("INSERT INTO posts VALUES(%s)", (bleach.clean(content),))
  db.commit()
  db.close()

