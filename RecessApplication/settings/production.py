from .base import *

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

PRODUCTION_DATABASE_URL = 'postgres://xgfkiciegnvnhv:edb5aa46c6f7ecad5c50658a44c5c65226ad4f2d84ef9959eb76cc670aba77ab@ec2-54-90-68-208.compute-1.amazonaws.com:5432/deo87b8qamkg3r'

DATABASES = {
    # Connects to the production DB
    'default' : dj_database_url.config(default=PRODUCTION_DATABASE_URL, conn_max_age=600, ssl_require=True),

}