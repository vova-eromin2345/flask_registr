import sqlite3

def connect_to_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor

def close_db(conn, cursor):
    cursor.close()
    conn.commit()


def read_from_db(db_path, table, *args):
    _, cursor = connect_to_db(db_path)

    schema_temp = 'SELECT {} from '+ table 

    if '*' in args:
        return cursor.execute(schema_temp.format('*')).fetchall()
    else:
        args_temp = '({})'.format(','.join(args))
        return cursor.execute(schema_temp.format(args_temp)).fetchall()
    

def write_to_db(db_path, table, wait_args:tuple, args:tuple):
    wait_args, args = tuple(wait_args), tuple(args)
    
    conn, cursor = connect_to_db(db_path)

    args_temp = "({})".format( ','.join(['?' for x in wait_args]) )
    schema_temp = f"INSERT INTO {table} ({','.join(wait_args)}) VALUES {args_temp}"
    
    cursor.execute(schema_temp, args)

    close_db(conn, cursor)


def create_table(db_path, table, *rows):
    conn, cursor = connect_to_db(db_path)

    schema = "CREATE TABLE IF NOT EXISTS {} ({})".format(table, ",".join(rows))
    cursor.execute(schema)

    close_db(conn, cursor)