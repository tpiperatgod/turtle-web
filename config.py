from sae.const import MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB

#
# BASE CONFIG
#

DEBUG = False

SECRET_KEY = 'I AM TURTLE ENDER'

#UPLOAD_FOLDER = '/root/uploads/'
DOMAIN_NAME = 'uploadpic'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#
# DATABASE CONFIG
#
MYSQL_PORT = int(MYSQL_PORT)

sql_connection = "mysql://%s:%s@%s:%d/%s" % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)

sql_idle_timeout = 100

sql_connection_debug = 0

sqlite_synchronous = True

sql_connection_trace = True

sql_max_retries = 10

sql_retry_interval = 10

