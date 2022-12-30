"""Database 2.0"""

import sqlite3
import hashlib

from datetime import datetime


def get_hashed_entry(input_string):
    """
    Get hashed form from lower case non-whitespace input string
    """
    non_whitespace_input_string = input_string.replace(" ", "")
    lowercase_input_string = non_whitespace_input_string.lower()

    return hashlib.sha256(lowercase_input_string.encode('utf-8')).hexdigest()


def get_hms(input_time):
    """
    Get hours, minutes, seconds from count
    """
    minutes, seconds = divmod(input_time, 60)
    hours, minutes = divmod(minutes, 60)

    return hours, minutes, seconds


def render2clock(hours, minutes, seconds):
    """
    Create clock display
    """
    return '{:04d}:{:02d}:{:02d}'.format(hours, minutes, seconds)  # pylint: disable=consider-using-f-string


def print_info(msg: str):
    """
    print message under INFO type
    """
    msg = f"[INFO]: {msg}"
    print(msg)

    return msg


class Entry:
    """
    Entry Class
    """
    def __init__(self) -> None:
        self.hashed = None
        self.task_name = None
        self.effort = 5
        self.date = datetime.now()

    def set_name(self, task_name):
        """
        Set Name
        """
        self.task_name = task_name
        self.hashed = get_hashed_entry(task_name)

    def get_name(self):
        """
        Get entry's name
        """
        return self.task_name

    def get_info(self):
        """
        Get all information of an entry
        """
        return self.hashed, self.task_name, self.effort, self.date


class DB2:
    """
    Database Class
    """
    def __init__(self) -> None:

        # connecting to database
        self.database_name = 'prototype.db'
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()
        self.columns = "(hashed, task_name, effort, date)"

        # Table : tasks
        self.table_name = 'tasks'
        self.table_initialized = self.table_exist(self.table_name)

        # Check if table exists or not
        if not self.table_initialized:
            print_info("Initializing new table")
            query = f"CREATE TABLE {self.table_name} {self.columns}"
            self.cursor_execute(query=query)
            self.table_initialized = True

    def conn_commit(self):
        """
        Commit changes
        """
        self.connection.commit()

    def cursor_execute(self, query):
        """
        Calling cursor to execute query
        """
        return self.cursor.execute(query)

    def table_exist(self, table_name):
        """
        Check if table exist
        """
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        list_of_tables = self.cursor.execute(query).fetchall()

        return bool(len(list_of_tables) > 0)

    def select_all(self):
        """
        Query: get all entry in database
        """
        query =  f"SELECT * FROM {self.table_name};"
        result = self.cursor_execute(query=query).fetchall()

        return result

    def insert_entry(self, entry: Entry):
        """
        Query: insert entry to database
        """
        hashed_name, name, effort, effort_date = entry.get_info()
        query = f"""INSERT INTO {self.table_name}{self.columns}
                        VALUES ('{hashed_name}', '{name}' , '{effort}', '{effort_date}');"""
        self.cursor_execute(query=query)
        self.conn_commit()

    def delete_all(self):
        """
        Query: delete everything from database
        """
        query = f"DELETE FROM {self.table_name}"
        self.cursor_execute(query=query)

    def select_all_key(self):
        """
        Query: get all existing keys in database
        """
        query =  f"SELECT hashed FROM {self.table_name};"
        result = self.cursor_execute(query=query).fetchall()
        result = self.result2list(result)

        return set(result)

    def select_all_names(self):
        """
        Query: gets all entries' names
        """
        query =  f"SELECT task_name FROM {self.table_name};"
        result = self.cursor_execute(query=query).fetchall()
        result = self.result2list(result)

        return set(result)

    def select_entry_effort(self, name: str):
        """
        Query: get effort of a specific entry
        """
        hashed = get_hashed_entry(name)
        query = f"SELECT effort FROM {self.table_name} WHERE hashed = '{hashed}'"
        result = self.cursor_execute(query=query).fetchall()
        result_list = [int(item[0]) for item in result]

        return sum(result_list)

    def update_effort(self, name, effort):
        """
        Query: update effort of a specific entry
        """
        # Get hashed info and use it to find its latest efforts
        hashed = get_hashed_entry(name)
        current_effort = self.select_entry_effort(name)

        # Update the latest effort information to database
        current_effort += effort
        query = f"UPDATE {self.table_name} SET effort='{current_effort}' WHERE hashed='{hashed}';"
        self.cursor_execute(query=query)
        self.conn_commit()

    def result2list(self, result):
        """
        Convert query result to list type
        """
        return tuple([item[0] for item in result])  # pylint: disable=consider-using-generator

    def entry_exist(self, name):
        """
        Check if an entry exists in database or not
        """
        hashed = get_hashed_entry(name)
        keys = self.select_all_key()

        return hashed in keys


def prototype():
    """
    Testing prototypes
    """
    db2 = DB2()

    entry1 = Entry()
    entry1.set_name("Chang")

    entry2 = Entry()
    entry2.set_name("Tuan")


prototype()
