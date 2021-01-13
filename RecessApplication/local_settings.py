# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

LOCAL_DATABASE_URL = 'postgres://postgres:password@localhost:5432/LocalRecessDB'

DATABASES['default'] = dj_database_url.config(default=LOCAL_DATABASE_URL, conn_max_age=600, ssl_require=False)
