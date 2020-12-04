import psycopg2
import os


def create_tables():
    """ create tables in the PostgreSQL database"""
    with open("sql_request.sql", "r") as file_handler:
        commands = file_handler.read()

    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor()
        # create table one by one

        cur.execute(commands)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
