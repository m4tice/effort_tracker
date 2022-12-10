"""Version: EF_2.0.1"""

import time
import sqlite3
import hashlib
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


message_box_title = ('Error', 'Warning', 'Info')

def get_hashed_entry(input_string):
    """
    Get hashed form
    """
    return hashlib.sha256(input_string.encode('utf-8')).hexdigest()


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


class Counter:
    """
    Counter Class
    """
    def __init__(self) -> None:
        self.controller = None
        self.time = 1
        self.hours, self.mins, self.secs = 0, 0, 0
        self.timer = None
        self.counting_state = False

        self.set_timer()

    def set_timer(self):
        """
        Set timer content for clock display
        """
        self.timer = render2clock(self.hours, self.mins, self.secs)

    def start(self, current_effort):
        """
        Start timer
        """
        # Start the count
        while self.time >= 1 and self.counting_state is True:

            # Break the count if effort is more than 8 hours
            if self.time > 28800:
                break

            # Main couting loop
            if self.time != 0:
                self.hours, self.mins, self.secs = get_hms(input_time=
                self.time + current_effort)

            # Set the timer based on information of hours, minutes and seconds;
            # and refresh the applications
            self.set_timer()
            self.controller.refresh_application(str(self.timer))

            time.sleep(0.1)
            self.time += 1

    def stop(self)->int:
        """
        Stop counting and reset the count and timer states
        """
        counted_time = self.time
        self.reset_count()
        self.set_counting_state(False)

        return counted_time

    def get_counting_state(self)->bool:
        """
        Get counting state
        """
        return self.counting_state

    def set_counting_state(self, counting_state):
        """
        Set counting state
        """
        self.counting_state = counting_state

    def reset_count(self):
        """
        Reset count to 1
        """
        self.time = 1

    def set_controller(self, controller):
        """
        Set Controller
        """
        self.controller = controller


class Entry:
    """
    Entry class used as entry for database
    """
    def __init__(self, name: str = None) -> None:
        self.entry_name = name
        self.entry_hashed = get_hashed_entry(self.entry_name)
        self.effort = 0

    def set_name(self, name: str):
        """
        Set entry's name and hashed entry
        """
        self.entry_name = name
        self.entry_hashed = get_hashed_entry(self.entry_name)

    def set_effort(self, effort: int):
        """
        Set entry's effort
        """
        self.effort = effort

    def get_info(self):
        """
        Get all info from entry
        """
        return self.entry_hashed, self.entry_name, self.effort

    def get_name(self):
        """
        Get entry's name
        """
        return self.entry_name

    def get_effort(self):
        """
        Get entry's effort
        """
        return self.effort


class Database:
    """
    Database Class
    """
    def __init__(self) -> None:

        # connecting to database
        self.database_name = 'efforts.db'
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()

        # Table : tasks
        self.table_name = 'tasks'
        self.table_initialized = self.table_exist(self.table_name)

        # Check if table exists or not
        if not self.table_initialized:
            query = f"CREATE TABLE {self.table_name} (key, task_name, effort)"
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

    def insert_entry(self, entry):
        """
        Query: insert entry to database
        """
        hashed_name, name, effort = entry.get_info()
        query = f"""INSERT INTO {self.table_name}(key, task_name, effort)
                        VALUES ('{hashed_name}', '{name}' , '{effort}');"""
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
        query =  f"SELECT key FROM {self.table_name};"
        result = self.cursor_execute(query=query).fetchall()
        result = self.result2list(result)

        return result

    def select_all_names(self):
        """
        Query: gets all entries' names
        """
        query =  f"SELECT task_name FROM {self.table_name};"
        result = self.cursor_execute(query=query).fetchall()
        result = self.result2list(result)

        return result

    def select_entry_effort(self, name):
        """
        Query: get effort of a specific entry
        """
        hashed = get_hashed_entry(name)
        query = f"SELECT effort FROM {self.table_name} WHERE key = '{hashed}'"
        result = self.cursor_execute(query=query).fetchall()

        return int(result[0][0])

    def update_effort(self, name, effort):
        """
        Query: update effort of a specific entry
        """
        # Get hashed info and use it to find its latest efforts
        hashed = get_hashed_entry(name)
        current_effort = self.select_entry_effort(name)

        # Update the latest effort information to database
        current_effort += effort
        query = f"UPDATE {self.table_name} SET effort = '{current_effort}' WHERE key = '{hashed}';"
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


class Model:
    """
    Model Class
    """
    def __init__(self) -> None:
        self.data_length = 0
        self.last_id = None
        self.dataframe = {}
        self.controller = None
        self.database = None

    def set_controller(self, controller):
        """
        Set controller method for Model Class
        @param: Controller object
        return: None
        """
        self.controller = controller

    def set_database(self, database: Database):
        """
        Set Database
        """
        self.database = database

    def entry_exist(self, entry_name):
        """
        Check if entry already exists in database
        """
        return self.database.entry_exist(entry_name)

    def entry_empty(self, entry_name):
        """
        Check if input entry is null / empty
        """
        empty_condition_1 = entry_name == ""
        return bool(empty_condition_1)

    def add_entry_to_database(self, name):
        """
        Add new entry to database
        """
        # Conditions for a valid entry insertation
        entry_not_exist = not self.database.entry_exist(name)
        entry_name_not_empty = not self.entry_empty(name)

        # Check if entry is valid based on previous conditions
        if entry_not_exist and entry_name_not_empty:
            entry = Entry(name=name)
            self.database.insert_entry(entry=entry)

            # Update task_entry combobox with newly added query
            self.controller.update_task_entry_combobox()

            msg = "New entry has been added."
            title = message_box_title[2]

        # Display error messages in case entry is invalid
        else:
            if not entry_name_not_empty:
                msg = "Cannot add entry. Entry cannot be left empty!"

            if not entry_not_exist:
                msg = "Cannot add entry. Entry already exists!"

            title = message_box_title[0]

        self.controller.display_message(title=title, message=msg)  # Display message

    def update_database_effort(self, task_name, effort):
        """
        Update effort of entry in database
        """
        self.database.update_effort(task_name, effort)

    def get_entries_names(self):
        """
        Get all available task_names from database
        """
        return self.database.select_all_names()

    def get_task_effort(self, task_name):
        """
        Get effort of entry in database
        """
        return self.database.select_entry_effort(task_name)


class View(ttk.Frame):  # pylint: disable=too-many-ancestors, too-many-instance-attributes
    """
    View Class
    """
    def __init__(self, parent_application):
        super().__init__(parent_application)

        self.controller = None
        self.parent_application = parent_application

        # Label : timer
        self.label_timer_var = tk.StringVar()
        self.init_timer = render2clock(hours=0, minutes=0, seconds=0)
        self.label_timer_var.set(self.init_timer)
        self.label_timer = ttk.Label(self, textvariable=self.label_timer_var)
        self.label_timer.grid(row=1, column=2, padx=10)

        # Button : count
        self.button_count_var = tk.StringVar()
        self.button_count = ttk.Button(self,
                                        textvariable=self.button_count_var,
                                        command=self.button_count_clicked)
        self.button_count_var.set("Start")
        self.button_count.grid(row=2, column=2, padx=10)

        # Combobox : task entry
        self.task_entry_var = tk.StringVar()
        self.task_entry = ttk.Combobox(self,
                                        textvariable=self.task_entry_var,
                                        width=10)
        self.task_entry['values'] = ()
        self.task_entry.grid(row=1, column=1, padx=10)
        self.task_entry.bind('<<ComboboxSelected>>', self.task_changed)

        # Button : add task entry
        self.button_add = ttk.Button(self, text="Add", command=self.button_add_clicked)
        self.button_add.grid(row=2, column=1, padx=10)

    def set_controller(self, controller):
        """
        Set controller for View class
        """
        self.controller = controller

    def set_combobox(self, data):
        """
        Set item list for combobox
        """
        self.task_entry['values'] = data

    def get_combobox_current_item(self):
        """
        Get current item that is chosen in combobox
        """
        return self.task_entry_var.get()

    def button_count_clicked(self):
        """
        Action when Button Count is clicked
        """
        if self.controller:
            self.controller.count(self.get_combobox_current_item())

    def button_add_clicked(self):
        """
        Action when Button Add is clicked
        """
        if self.controller:
            self.controller.add(self.task_entry_var.get())

    def task_changed(self, event):  # pylint: disable=unused-argument
        """
        Handle the task_name changed event
        """
        self.label_timer_var.set(self.controller.get_task_effort_display(self.task_entry_var.get()))

    def display_message(self, title, message):
        """
        Display message box
        """
        showinfo(title=title, message=message)

    def update_appplication(self):
        """
        Update main application
        """
        self.parent_application.update()


class Controller:
    """
    Controller Class
    """
    def __init__(self, model: Model = None, view: View = None):
        self.model = model
        self.view = view
        self.counter = None
        self.application = None

    def count(self, task_name):
        """
        Counting time method
        """
        # Conditions for checking if selected entry is valid to start timer
        entry_exist = self.model.entry_exist(task_name)
        entry_name_not_empty = not self.model.entry_empty(task_name)

        # If entry is valid
        if entry_exist and entry_name_not_empty:

            # Start timer if it is not in couting state
            if self.counter.get_counting_state() is False:
                self.view.button_count_var.set("Stop")
                self.counter.set_counting_state(True)
                current_effort = self.get_task_effort(task_name)
                self.counter.start(current_effort=current_effort)

            # Stop timer if it is countings
            else:
                effort = self.counter.stop()
                self.view.button_count_var.set("Start")
                self.model.update_database_effort(task_name, effort)

        # Display error message box if entry is invalid
        else:

            if not entry_name_not_empty:
                msg = 'Counter fails to start as task name cannot be empty!'

            elif not entry_exist:
                msg = 'Counter fails to start as task name cannot be found!'

            else:
                msg = 'Counter fails to start!'

            title = message_box_title[0]
            self.display_message(title=title, message=msg)

    def add(self, name):
        """
        Add entry to database by calling Model's method
        """
        self.model.add_entry_to_database(name)

    def update_task_entry_combobox(self):
        """
        Update items in task combobox with data from database
        """
        combobox_items_tuple = self.model.get_entries_names()
        self.view.set_combobox(combobox_items_tuple)

    def refresh_application(self, timer):
        """
        Refresh application base on timer counting event
        """
        self.view.label_timer_var.set(timer)
        self.view.update_appplication()

    def set_model(self, model: Model):
        """
        Set Model
        """
        self.model = model

    def set_view(self, view: View):
        """
        Set View
        """
        self.view = view

    def set_application(self, application):
        """
        Set Application
        """
        self.application = application

    def set_counter(self, counter: Counter):
        """
        set view
        """
        self.counter = counter

    def get_task_effort(self, task_name):
        """
        Get raw effort (in terms of second) from task
        """
        return self.model.get_task_effort(task_name)

    def get_task_effort_display(self, task_name):
        """
        Get effort from task in form of hours, mins and seconds
        """
        effort = self.get_task_effort(task_name)
        hours, minutes, seconds = get_hms(effort)

        return render2clock(hours, minutes, seconds)

    def display_message(self, title, message):
        """
        Display message box
        """
        self.view.display_message(title=title, message=message)


class Aplication(tk.Tk):
    """
    Application Class
    """
    def __init__(self) -> None:
        super().__init__()

        # MVC components initialization
        # Model
        self.model = Model()
        self.database = Database()
        self.model.set_database(database=self.database)

        # View
        self.view = View(self)
        # View : Window's setting initialization
        self.title("Prototype")
        self.view.grid(row=0, column=0, padx=10, pady=10)
        self.resizable(0, 0)

        # Controller
        self.controller = Controller(self)

        # Model-View components linking
        self.model.set_controller(controller=self.controller)
        self.view.set_controller(controller=self.controller)

        # Controller linking
        # Services
        self.counter = Counter()
        self.counter.set_controller(self.controller)
        self.controller.set_counter(self.counter)

        # MVC
        self.controller.set_model(model=self.model)
        self.controller.set_view(view=self.view)
        self.controller.set_application(self)
        self.controller.update_task_entry_combobox()


def main():
    """
    main function
    """
    app = Aplication()
    app.mainloop()


if __name__ == "__main__":
    main()
