import os

from dotenv import load_dotenv

load_dotenv('.env.example')

DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')

DB_HOST_TEST = os.environ.get('DB_HOST_TEST')
DB_PORT_TEST = os.environ.get('DB_PORT_TEST')
DB_NAME_TEST = os.environ.get('DB_NAME_TEST')
DB_USER_TEST = os.environ.get('DB_USER_TEST')
DB_PASS_TEST = os.environ.get('DB_PASS_TEST')

REAL_DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:' \
                    f'{DB_PORT}/{DB_NAME}'

REAL_DATABASE_URL_ALEMBIC = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:' \
                            f'{DB_PORT}/{DB_NAME}'

TEST_DATABASE_URL = f'postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@' \
                    f'{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'
