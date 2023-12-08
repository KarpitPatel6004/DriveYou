import os

SECRET_KEY = os.environ.get('SECRET_KEY')
MONGODB_USER = os.environ.get('MONGODB_USER')
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')
MONGODB_CLUSTER = os.environ.get('MONGODB_CLUSTER')