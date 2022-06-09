import os

MYSQL_DATABASE_NAME = os.environ.get('MYSQL_DATABASE_NAME', default="muzikantoff")
MYSQL_USER = os.environ.get('MYSQL_USER', default="root")
MYSQL_PASS = os.environ.get('MYSQL_PASS', default=None)
MYSQL_HOST = os.environ.get('MYSQL_HOST', default="localhost")
MYSQL_PORT = os.environ.get('MYSQL_PORT', default=3306)

BOT_TOKEN = os.environ.get('BOT_TOKEN', default="5240230179:AAFyQnlLK8zGqU4ExEbffrr8WixHahDH2QU")

DEBUG_DJANGO = os.environ.get('DEBUG', default=True)
ALLOWED_HOSTS_DJANGO = os.environ.get("ALLOWED_HOSTS")
