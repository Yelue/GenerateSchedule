import psycopg2


def create_tables():
    """ create tables in the PostgreSQL database"""
    with open("sql_request.sql", "r") as file_handler:
        commands = file_handler.read()

    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(user='wcqtmsosaglntk',
                                password='9f6497000b9a5f82fd288a15597cc09876c377b17f1b521848bc12a2f42577ef',
                                host='ec2-34-253-148-186.eu-west-1.compute.amazonaws.com',
                                port='5432',
                                database='dful1hqqvuc8a0')
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
