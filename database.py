import logging

import mariadb
import sys

import tools


def save_to_one_table(id_name, id_value, table, string_typ, string_value):
    try:
#        mysql_connect()
        queck_the_id_already_exists(id_name, id_value, table)
        mysql_insert(string_typ, string_value, table)
#        mysql_disconnect()

    except mariadb.Error as e:
        logging.error(e)
def save_to_many_to_many_table(id_1, id_2, table, string_value):
    print("hello world")

def mysql_connect():
    global cur, conn
    try:
        config = tools.read_config()

        conn = mariadb.connect(
            user=config['database']['user'],
            password=config['database']['password'],
            host=config['database']['host'],
            port=config['database']['port'],
            database=config['database']['database']
        )
    except mariadb.Error as e:
        logging.error(e)
        exit(1)
    cur = conn.cursor()

def mysql_disconnect():
    try:
        conn.commit()
        conn.close()
    except mariadb.Error as e:
        logging.error(e)

def queck_the_id_already_exists(id_name, id_value, table):
    print(f"SELECT * FROM {table} WHERE {id_name} = {id_value}")

#    try:
#        cur.execute(f"SELECT * FROM {table} WHERE {id_name} = {id_value}")
#        return cur.fetchall()
#    except Exception as e:
#        logging.error(e)

def mysql_insert(types, values, table):
    try:
        insert = f"INSERT INTO {table} (" + types
        value = "VALUES (" + values

        cmd = insert + value

        print(cmd)
#        cur.execute(cmd)
    except mariadb.Error as e:
        logging.error(e)