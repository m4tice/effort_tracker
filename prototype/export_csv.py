# pylint: skip-file

"""Export database to .csv"""

import os
import sys
import csv

from datetime import datetime

sys.path.append('D:/TUAN/Workspace/Python/EF/EF_2.0.0')

from application__2_1_0 import Db2  # pylint: disable=wrong-import-position

### Main Prototype section
class ExportJob:
    """
    Export database to csv
    """
    def __init__(self) -> None:
        self.data = None
        self.weekdict = {
            0: "Mon",
            1: "Tue",
            2: "Wed",
            3: "Thu",
            4: "Fri",
            5: "Sat",
            6: "Sun",
        }

        self.csv_path = "./exports"

        if not os.path.isdir(self.csv_path):
            os.makedirs(self.csv_path)

    def set_data(self, data):
        """
        Set data
        """
        self.data = data

    def export_csv(self):
        """
        Export data to csv
        """
        export_time = datetime.now()
        export_time_year = export_time.year
        export_time_month = export_time.month
        export_time_day = export_time.day
        export_time_hour = export_time.hour
        export_time_minute = export_time.minute
        export_time_weekday = self.weekdict[export_time.weekday()]

        csv_file_name = f"database_{export_time_year}_{export_time_month}_{export_time_day}__{export_time_hour}_{export_time_minute}_{export_time_weekday}.csv"  # pylint: disable = "line-too-long"
        csv_file_full_path = os.path.join(self.csv_path, csv_file_name)

        print(csv_file_full_path)

        with open(csv_file_full_path, 'a', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(self.data)

    def extract_entry_info(self, entry):
        """
        extract entry info
        """
        _, task, effort, year, month, day, hour, minute, weekday = entry
        return task, effort, year, month, day, hour, minute, weekday


### Main Prototype section ends here


def prototype_exec():
    """
    Prototype testing method
    """
    prototype_db = Db2()
    query_data = prototype_db.select_all_without_hashed()

    exporter = ExportJob()
    exporter.set_data(query_data)
    exporter.export_csv()

prototype_exec()
