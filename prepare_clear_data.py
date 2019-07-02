import sqlite3
import csv
import os


# conn = sqlite3.connect('irr.sqlite')
#
# cur = conn.cursor()
# cur.execute("""UPDATE irr_data SET agency = owner_name where telephone in (
#     select telephone from irr_data
#     group by telephone having count(*) > %s)""" % count_phone_numbers)
#
# cur.execute("""UPDATE irr_data SET owner_name = null where telephone in (
#     select telephone from irr_data
#     group by telephone having count(*) > %s)""" % count_phone_numbers)
#
# cur.execute("""UPDATE irr_data SET agency = null where telephone in (
#     select telephone from irr_data
#     group by telephone having count(*) < %s)""" % (count_phone_numbers + 1))
#
# conn.commit()


class ClearData(object):
    irr_data = 'irr.sqlite'
    agency_date = 'agency_data.sqlite'

    def __init__(self):
        self.hours = self.get_hours_from_file
        self.conn = self.create_connection(self.irr_data)

        self.remove_old_rows()

        self.rename_agency_to_owner_name()
        self.rename_owners_if_agency()
        self.remove_agency_if_owner()
        self.create_agency_data()

        self.finalize()

    def create_connection(self, filename):
        try:
            self.conn = sqlite3.connect(filename)
            return self.conn
        except Exception as e:
            print(e)
        return None

    def remove_old_rows(self):
        self.conn.execute("""DELETE FROM irr_data WHERE (
        published_date <= datetime('now', '-%s hours'))""" % self.get_hours_from_file)

    def rename_agency_to_owner_name(self):
        self.conn.execute("""UPDATE irr_data SET agency = owner_name where telephone in (
            select telephone from irr_data
            group by telephone having count(*) > %s)""" % self.get_count_phone_number_from_file)

    def rename_owners_if_agency(self):
        self.conn.execute("""UPDATE irr_data SET owner_name = null where telephone in (
        select telephone from irr_data
        group by telephone having count(*) > %s)""" % self.get_count_phone_number_from_file)

    def remove_agency_if_owner(self):
        self.conn.execute("""UPDATE irr_data SET agency = null where telephone in (
            select telephone from irr_data
            group by telephone having count(*) < %s)""" % (self.get_count_phone_number_from_file + 1))

    def create_agency_data(self):
        if os.path.exists(self.agency_date):
            pass
        else:
            self.conn.execute("""CREATE TABLE agency_data
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, telephone TEXT, agency TEXT)""")

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    @staticmethod
    def get_data_from_file():
        with open(os.getcwd() + '/config_for_clear_data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for data in csv_reader:
                try:
                    count_phone_numbers, hours = int(data[1]) - 1, int(data[3])
                except IndexError:
                    print('Fill csv file "config_for_clear_data.csv"')
        return count_phone_numbers, hours

    @property
    def get_count_phone_number_from_file(self):
        return self.get_data_from_file()[0]

    @property
    def get_hours_from_file(self):
        try:
            hours = self.get_data_from_file()[1]
        except IndexError:
            hours = 150
            print('Default hours is {}'.format(hours))
        return hours


if __name__ == '__main__':
    ClearData()
