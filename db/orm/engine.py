from sqlalchemy.engine import create_engine
import os

ENGINE_PATH_WIN_AUTH = os.environ.get('DATABASE_URL')

engine = create_engine(ENGINE_PATH_WIN_AUTH)
