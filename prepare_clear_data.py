import sqlite3
from sqlite3 import OperationalError
import csv
import os


class ClearData(object):
    irr_data = 'irr.sqlite'

    def __init__(self):
        self.hours = self.get_hours_from_file
        self.conn = self.create_connection(self.irr_data)

        self.remove_old_rows()

        self.rename_agency_to_owner_name()
        self.rename_owners_if_agency()
        self.remove_agency_if_owner()
        self.create_agency_data()
        self.replace_agency_in_irr_data()
        self.create_name_table()
        self.replace_owner_names_in_irr_data()
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
        try:
            self.conn.execute("""CREATE TABLE agency_data
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, telephone TEXT, agency TEXT)""")
        except OperationalError:
            pass
        agencies_from_irr_data = self.conn.execute("""select telephone, agency from irr_data WHERE agency NOT NULL""")
        agencies_from_agency_data = self.conn.execute("""select telephone, agency from agency_data""")
        phones = [phone[0] for phone in set(agencies_from_agency_data)]
        for data in set(agencies_from_irr_data):
            if data[0] not in phones:
                self.conn.execute("""insert into agency_data(telephone,agency) VALUES (?,?)""", (data[0], data[1]))

    def replace_agency_in_irr_data(self):
        self.conn.execute("""UPDATE irr_data SET agency = (SELECT id FROM agency_data 
                                                                WHERE agency_data.agency = irr_data.agency),
                                                telephone = (SELECT id FROM agency_data 
                                                                WHERE agency_data.telephone = irr_data.telephone) where 
                                                                telephone in (select telephone from irr_data
                                                                        group by telephone having count(*) > %s)                
                                                                """ % self.get_count_phone_number_from_file)

    def create_name_table(self):
        try:
            self.conn.execute("""CREATE TABLE unique_names
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, owner_name TEXT)""")
        except OperationalError:
            pass
        owner_names_from_irr_data = self.conn.execute("""select owner_name from irr_data where owner_name not null """)
        owner_names_from_table_names = self.conn.execute("""select owner_name from unique_names""")
        names = [name for name in owner_names_from_table_names]
        for owner_name in (set(owner_names_from_irr_data)):
            if owner_name not in names:
                self.conn.execute("""insert into unique_names(owner_name) VALUES (?)""", (owner_name))

    def replace_owner_names_in_irr_data(self):
        self.conn.execute("""UPDATE irr_data SET owner_name = (SELECT id FROM unique_names 
                                                                WHERE unique_names.owner_name = irr_data.owner_name)
                                                         """)

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
