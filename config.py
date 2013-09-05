#
# BASE CONFIG
#

DEBUG = True

SECRET_KEY = 'I AM TURTLE ENDER'

UPLOAD_FOLDER = '/opt/'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py'])
#
# DATABASE CONFIG
#

sql_connection = "mysql://root:123456@192.168.198.128/web_app"

sql_idle_timeout = 100

sql_connection_debug = 0

sqlite_synchronous = True

sql_connection_trace = True

sql_max_retries = 10

sql_retry_interval = 10