"""Export database to .csv"""

import sys
from datetime import datetime

sys.path.append('D:/TUAN/Workspace/Python/EF/EF_2.0.0')

from application__2_1_0 import Db2, print_info  # pylint: disable=wrong-import-position

weekdict = {
    "0": "Mon",
    "1": "Tue",
    "2": "Wed",
    "3": "Thu",
    "4": "Fri",
    "5": "Sat",
    "6": "Sun",
}

### Main Prototype section
class ExportJob:
    """
    ExportJob class
    """
    def __init__(self) -> None:
        self.data = None

    def set_data(self, data):
        """
        set data
        """
        self.data = data

    def extract_entry_info(self, entry):
        """
        extract entry info
        """
        _, task, effort, date = entry
        return task, effort, date

    def extract_date_info(self, date: str):
        """
        extract date info
        """
        try:
            date_splitted = date.split(" ")
            date_ymd, date_hms = date_splitted[0], date_splitted[1]
            date_year, date_month, date_day = date_ymd.split("-")
            date_hour, date_minute, _ = date_hms.split(":")

            print_info("{}-{}-{}_{}:{}".format(  # pylint: disable = consider-using-f-string
                date_year,
                date_month,
                date_day,
                date_hour,
                date_minute)
            )

        except Exception:  # pylint: disable = broad-except
            pass

    def export_csv(self):
        """
        Export to csv
        """
        export_time = datetime.now()
        export_time_year = export_time.year
        export_time_month = export_time.month
        export_time_day = export_time.day
        export_time_hour = export_time.hour
        export_time_minute = export_time.minute
        export_time_weekday = export_time.weekday()

        csv_file_name = f"database_{export_time_year}_{export_time_month}_{export_time_day}__{export_time_hour}_{export_time_minute}_{export_time_weekday}.csv"  # pylint: disable = "line-too-long"

        print(csv_file_name)

        for entry in self.data:
            _, _, date = self.extract_entry_info(entry)
            self.extract_date_info(date)

### Main Prototype section ends here


def prototype_exec():
    """
    Prototype testing method
    """
    prototype_db = Db2()
    query_data = prototype_db.select_all()
    print(query_data)

    exporter = ExportJob()
    exporter.set_data(query_data)
    exporter.export_csv()

prototype_exec()
