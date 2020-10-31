from sqlalchemy.engine import create_engine

username = 'wcqtmsosaglntk'
password = '9f6497000b9a5f82fd288a15597cc09876c377b17f1b521848bc12a2f42577ef'
database = 'dful1hqqvuc8a0'
host = 'ec2-34-253-148-186.eu-west-1.compute.amazonaws.com'
port = '5432'

ENGINE_PATH_WIN_AUTH = f'postgres://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(ENGINE_PATH_WIN_AUTH)
