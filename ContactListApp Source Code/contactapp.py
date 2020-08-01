from tkinter import ttk
from tkinter import *
import mysql.connector as mysql


class ContactApp:
    def __init__(self, window):
        self.connection = mysql.connect(host="localhost", user="root", password="dbms@1234", database="contactlistdb")
        self.wind = window
        self.wind.title('Contacts List Application')

        # Creating a Frame Container
        frame = LabelFrame(self.wind, text="Search a String")
        frame.grid(row=0, column=0, columnspan=3, pady=20)


        # Search Label
        Label(frame, text="Search ContactDB: ").grid(row=2, column=0)
        self.search_string = Entry(frame)
        self.search_string.grid(row=2, column=1)

        # Button Search String
        ttk.Button(frame, text="Search", command=self.search_contact).grid(row=5, columnspan=2, sticky=W + E)

        # Output Messages
        self.message = Label(text="", fg="red")
        self.message.grid(row=5, column=0, columnspan=2, sticky=W + E)

        # Table
        # Mentioning 3 columns gives 4 in the GUI

        s = ttk.Style()
        s.configure('Treeview', rowheight="45")
        self.tree = ttk.Treeview(height=10, columns=(
            'FirstName', 'MiddleName', 'LastName', 'Address List', 'PhoneList', 'DateList'))

        self.tree.grid(row=4, column=0, columnspan=4)
        self.tree.heading('#0', text="Contact_id", anchor=CENTER)
        self.tree.column("#0", minwidth=0, width=100, stretch=NO)
        self.tree.heading('#1', text="First Name", anchor=CENTER)
        self.tree.column("#1", minwidth=0, width=100, stretch=NO)
        self.tree.heading("#2", text="Middle Name", anchor=CENTER)
        self.tree.column("#2", minwidth=0, width=100, stretch=NO)
        self.tree.heading("#3", text="Last Name", anchor=CENTER)
        self.tree.column("#3", minwidth=0, width=100, stretch=NO)
        self.tree.heading('#4', text="Address List", anchor=CENTER)
        self.tree.column("#4", minwidth=0, width=350, stretch=NO)
        self.tree.heading('#5', text="Phone List", anchor=CENTER)
        self.tree.column("#5", minwidth=0, width=250, stretch=NO)
        self.tree.heading('#6', text="Date List", anchor=CENTER)
        self.tree.column("#6", minwidth=0, width=350, stretch=NO)

        # Buttons
        ttk.Button(text="ADD", command=self.insert_contact).grid(row=6, column=0, sticky=W + E)
        ttk.Button(text="MODIFY", command=self.modify_contact).grid(row=6, column=1, sticky=W + E)
        ttk.Button(text="DELETE", command=self.delete_contact).grid(row=6, column=2, sticky=W + E)

        # Filling the GUI
        self.get_contacts()

    def run_query(self, query, command):
        result = str()
        if command == "GET":
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.execute("commit")
        if command == "INSERT":
            cursor = self.connection.cursor()
            cursor.execute(query)
            cursor.execute("commit")
        if command == "DELETE":
            cursor = self.connection.cursor()
            cursor.execute(query)
            cursor.execute("commit")
        if command == "UPDATE":
            cursor = self.connection.cursor()
            cursor.execute(query)
            cursor.execute("commit")
        return result

    def search_contact(self):

        query =  "SELECT c.Contact_id, c.Fname, c.Mname, c.Lname FROM CONTACT c, ADDRESS a, PHONE p, DATE d WHERE c.Contact_id = a.Contact_id and a.Contact_id = p.Contact_id and p.Contact_id = d.Contact_id and CONCAT(c.Contact_id, '', c.Fname, '', c.Mname, '', c.Lname, '', a.Address_id, '', a.Address_type, '', a.Address, '', a.City, '', a.State, '', a.Zip, '', p.Phone_id, p.Phone_type, p.Area_code, p.Number, d.Date_id, d.Date_type, d.Date) LIKE '%{}%'".format(self.search_string.get())
        rows = self.run_query(query, "GET")

        # Cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Filling Data in GUI
        for row in rows:
            self.tree.insert('', 0, text=row[0], values=(row[1], row[2], row[3]))

        self.message['text'] = "Search Complete"



    def get_contacts(self):
        # Cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Obtaining Data
        query1 = "SELECT * FROM CONTACT"
        rows1 = self.run_query(query1, "GET")

        # Filling Data in GUI
        for row in rows1:
            query2 = "SELECT * FROM ADDRESS WHERE Contact_id='" + str(row[0]) + "'"
            result2 = self.run_query(query2, "GET")
            val2 = str()
            for res in result2:
                val2 = val2 + str(res) + "\n"
            query3 = "SELECT * FROM PHONE WHERE Contact_id='" + str(row[0]) + "'"
            result3 = self.run_query(query3, "GET")
            val3 = str()
            for res in result3:
                val3 = val3 + str(res) + "\n"
            query4 = "SELECT * FROM DATE WHERE Contact_id='" + str(row[0]) + "'"
            result4 = self.run_query(query4, "GET")
            val4 = str()
            for res in result4:
                val4 = val4 + str(res) + "\n"
            result4 = self.run_query(query4, "GET")

            self.tree.insert('', 0, text=row[0], values=(row[1], row[2], row[3], val2, val3, val4))

    def validation(self):
        return len(self.fname.get()) != 0 and len(self.lname.get()) != 0

    def add_contact(self):
        if self.validation():
            fname_str = self.fname.get()
            mname_str = self.mname.get()
            lname_str = self.lname.get()
            query = "INSERT INTO CONTACT(Fname, Mname, Lname) VALUES('" + fname_str + "','" + mname_str + "','" + lname_str + "')"
            self.run_query(query, "INSERT")
            self.message['text'] = "Contact {} {} {} has been added successfully".format(fname_str, mname_str,
                                                                                         lname_str)
            self.fname.delete(0, END)
            self.mname.delete(0, END)
            self.lname.delete(0, END)
        else:
            self.message['text'] = "First name and Last name cannot be left empty"
        # Filling the GUI
        self.get_contacts()

    def delete_contact(self):
        self.message['text'] = ""
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text'] = "Please select a Record"
            return
        self.message['text'] = ""
        Contact_id_str = self.tree.item(self.tree.selection())['text']

        query1 = "DELETE FROM ADDRESS WHERE Contact_id='{}'".format(Contact_id_str)
        self.run_query(query1, "DELETE")

        query2 = "DELETE FROM PHONE WHERE Contact_id='{}'".format(Contact_id_str)
        self.run_query(query2, "DELETE")

        query3 = "DELETE FROM DATE WHERE Contact_id='{}'".format(Contact_id_str)
        self.run_query(query3, "DELETE")

        query = "DELETE FROM CONTACT WHERE Contact_id='{}'".format(Contact_id_str)
        self.run_query(query, "DELETE")

        self.message['text'] = "Contact {} deleted successfully".format(Contact_id_str)

        # Filling the GUI
        self.get_contacts()

    def modify_contact(self):
        self.message['text'] = ""
        try:
            Contact_id_str = self.tree.item(self.tree.selection())['text']
            old_fname_str = self.tree.item(self.tree.selection())['values'][0]
            old_mname_str = self.tree.item(self.tree.selection())['values'][1]
            old_lname_str = self.tree.item(self.tree.selection())['values'][2]
        except IndexError as e:
            self.message['text'] = "Please select a Record"
            return

        self.edit_wind = Toplevel()
        self.edit_wind.title = "Modify Contact"

        # Old Contact_id
        Label(self.edit_wind, text="Old Contact_id: ").grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=Contact_id_str), state="readonly").grid(
            row=0, column=2)

        new_Contact_id_str = str(Contact_id_str)

        Label(self.edit_wind, text="CONTACT TABLE").grid(row=2, column=1)

        # Old First Name
        Label(self.edit_wind, text="Old First Name: ").grid(row=3, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_fname_str), state="readonly").grid(row=3,
                                                                                                                  column=2)
        # New First Name
        Label(self.edit_wind, text="New First Name: ").grid(row=4, column=1)
        new_fname_str = Entry(self.edit_wind)
        new_fname_str.grid(row=4, column=2)

        # Old Middle Name
        Label(self.edit_wind, text="Old Middle Name: ").grid(row=5, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_mname_str), state="readonly").grid(row=5,
                                                                                                                  column=2)
        # New Middle Name
        Label(self.edit_wind, text="New Middle Name: ").grid(row=6, column=1)
        new_mname_str = Entry(self.edit_wind)
        new_mname_str.grid(row=6, column=2)

        # Old Last Name
        Label(self.edit_wind, text="Old Last Name: ").grid(row=7, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_lname_str), state="readonly").grid(row=7,
                                                                                                                  column=2)
        # New Last Name
        Label(self.edit_wind, text="New Last Name: ").grid(row=8, column=1)
        new_lname_str = Entry(self.edit_wind)
        new_lname_str.grid(row=8, column=2)

        Label(self.edit_wind, text="ADDRESS TABLE").grid(row=9, column=1)

        # New Address_Id
        Label(self.edit_wind, text="Address_id: ").grid(row=11, column=1)
        new_address_id_str = Entry(self.edit_wind)
        new_address_id_str.grid(row=11, column=2)

        # New Address Type
        Label(self.edit_wind, text="New Address Type: ").grid(row=13, column=1)
        new_atype_str = Entry(self.edit_wind)
        new_atype_str.grid(row=13, column=2)

        # New Address
        Label(self.edit_wind, text="New Address: ").grid(row=15, column=1)
        new_address_str = Entry(self.edit_wind)
        new_address_str.grid(row=15, column=2)

        # New City
        Label(self.edit_wind, text="New City: ").grid(row=17, column=1)
        new_city_str = Entry(self.edit_wind)
        new_city_str.grid(row=17, column=2)

        # New State
        Label(self.edit_wind, text="New State: ").grid(row=19, column=1)
        new_state_str = Entry(self.edit_wind)
        new_state_str.grid(row=19, column=2)

        # New Zip
        Label(self.edit_wind, text="New Zip: ").grid(row=21, column=1)
        new_zip_str = Entry(self.edit_wind)
        new_zip_str.grid(row=21, column=2)

        Label(self.edit_wind, text="PHONE TABLE").grid(row=22, column=1)

        # New Phone_id
        Label(self.edit_wind, text="Phone_id: ").grid(row=24, column=1)
        new_phone_id_str = Entry(self.edit_wind)
        new_phone_id_str.grid(row=24, column=2)

        # New Phone Type
        Label(self.edit_wind, text="New Phone Type: ").grid(row=26, column=1)
        new_ptype_str = Entry(self.edit_wind)
        new_ptype_str.grid(row=26, column=2)

        # New Area Code
        Label(self.edit_wind, text="New Area Code: ").grid(row=28, column=1)
        new_area_str = Entry(self.edit_wind)
        new_area_str.grid(row=28, column=2)

        # New Number
        Label(self.edit_wind, text="New Number: ").grid(row=30, column=1)
        new_number_str = Entry(self.edit_wind)
        new_number_str.grid(row=30, column=2)

        Label(self.edit_wind, text="DATE TABLE").grid(row=31, column=1)

        # New Date_id
        Label(self.edit_wind, text="Date_id: ").grid(row=33, column=1)
        new_date_id_str = Entry(self.edit_wind)
        new_date_id_str.grid(row=33, column=2)

        # New Date Type
        Label(self.edit_wind, text="New Date Type: ").grid(row=35, column=1)
        new_dtype_str = Entry(self.edit_wind)
        new_dtype_str.grid(row=35, column=2)

        # New Date
        Label(self.edit_wind, text="New Date: ").grid(row=37, column=1)
        new_date_str = Entry(self.edit_wind)
        new_date_str.grid(row=37, column=2)

        Button(self.edit_wind, text="Update",
               command=lambda: self.edit_contacts(new_Contact_id_str, new_fname_str.get(), new_mname_str.get(),
                                                  new_lname_str.get(), Contact_id_str, new_address_id_str.get(),
                                                  new_atype_str.get(), new_address_str.get(), new_city_str.get(), new_state_str.get(),
                                                  new_zip_str.get(), new_phone_id_str.get(), new_ptype_str.get(), new_area_str.get(),
                                                  new_number_str.get(), new_date_id_str.get(), new_dtype_str.get(), new_date_str.get())).grid(
            row=38, column=2, sticky=W)

    def edit_contacts(self, new_Contact_id_str, new_fname_str, new_mname_str, new_lname_str, Contact_id_str,
                      new_address_str, new_atype_str, new_address_id_str, new_city_str, new_state_str, new_zip_str,
                      new_phone_id_str, new_ptype_str, new_area_str, new_number_str, new_date_id_str, new_dtype_str,
                      new_date_str):
        try:
            if new_fname_str != "" and new_lname_str != "":
                print(new_fname_str, new_mname_str)
                query = "UPDATE CONTACT SET Contact_id={}, Fname='{}', Mname='{}', Lname='{}' WHERE Contact_id='{}'".format(
                    new_Contact_id_str, new_fname_str, new_mname_str, new_lname_str, Contact_id_str)
                self.run_query(query, "UPDATE")

            if new_address_id_str != "":
                print(type(new_address_id_str), new_address_id_str, type(new_Contact_id_str), new_Contact_id_str, type(new_atype_str), new_atype_str, type(new_address_str), new_address_str, type(new_city_str),new_city_str, type(new_state_str), new_state_str, type(new_zip_str), new_zip_str)
                query1 = "UPDATE ADDRESS SET Contact_id = {}, Address_type = '{}', Address = '{}', City = '{}', State = '{}', Zip = '{}' WHERE Address_id='{}'".format(new_Contact_id_str, new_atype_str, new_address_id_str, new_city_str, new_state_str, new_zip_str, new_address_str)
                self.run_query(query1, "UPDATE")

            if new_phone_id_str != "":
                query2 = "UPDATE PHONE SET Phone_id={}, Contact_id={}, Phone_type='{}', Area_code='{}', Number='{}' WHERE Phone_id='{}'".format(
                    new_phone_id_str, new_Contact_id_str, new_ptype_str, new_area_str, new_number_str, new_phone_id_str)
                self.run_query(query2, "UPDATE")

            if new_date_id_str != "":
                query3 = "UPDATE DATE SET Date_id={}, Contact_id={}, Date_type='{}', Date='{}' WHERE Date_id='{}'".format(new_date_id_str,
                                                                                                       new_Contact_id_str,
                                                                                                       new_dtype_str,
                                                                                                       new_date_str, new_date_id_str)
                self.run_query(query3, "UPDATE")

            self.edit_wind.destroy()
            self.message['text'] = "Contact {} Updated Successfully".format(Contact_id_str)
        except Exception as e:
            print(e)
            self.message['text'] = "Error in updating Contact {}".format(Contact_id_str)

        # Filling the GUI
        self.get_contacts()


    def insert_contact(self):

        self.add_wind = Toplevel()
        self.add_wind.title = "Add Contact"

        Label(self.add_wind, text="CONTACT TABLE").grid(row=0, column=1)

        Label(self.add_wind, text="Contact_id: ").grid(row=1, column=1)
        Contact_id_str = Entry(self.add_wind)
        Contact_id_str.grid(row=1, column=2)

        # CONTACT TABLE
        Label(self.add_wind, text="First Name: ").grid(row=2, column=1)
        fname_str = Entry(self.add_wind)
        fname_str.grid(row=2, column=2)

        Label(self.add_wind, text="Middle Name: ").grid(row=3, column=1)
        mname_str = Entry(self.add_wind)
        mname_str.grid(row=3, column=2)

        Label(self.add_wind, text="Last Name: ").grid(row=4, column=1)
        lname_str = Entry(self.add_wind)
        lname_str.grid(row=4, column=2)

        Label(self.add_wind, text="ADDRESS TABLE").grid(row=5, column=1)

        # ADDRESS TABLE
        Label(self.add_wind, text="Address Type: ").grid(row=6, column=1)
        addrtype_str = Entry(self.add_wind)
        addrtype_str.grid(row=6, column=2)

        Label(self.add_wind, text="Address: ").grid(row=7, column=1)
        addr_str = Entry(self.add_wind)
        addr_str.grid(row=7, column=2)

        Label(self.add_wind, text="City: ").grid(row=8, column=1)
        city_str = Entry(self.add_wind)
        city_str.grid(row=8, column=2)

        Label(self.add_wind, text="State: ").grid(row=9, column=1)
        state_str = Entry(self.add_wind)
        state_str.grid(row=9, column=2)

        Label(self.add_wind, text="Zip: ").grid(row=10, column=1)
        zip_str = Entry(self.add_wind)
        zip_str.grid(row=10, column=2)

        Label(self.add_wind, text="Zip: ").grid(row=11, column=1)

        # PHONE TABLE

        Label(self.add_wind, text="PHONE TABLE").grid(row=12, column=1)

        Label(self.add_wind, text="Phone Type: ").grid(row=13, column=1)
        ptype_str = Entry(self.add_wind)
        ptype_str.grid(row=13, column=2)

        Label(self.add_wind, text="Area Code: ").grid(row=14, column=1)
        areacode_str = Entry(self.add_wind)
        areacode_str.grid(row=14, column=2)

        Label(self.add_wind, text="Phone Number: ").grid(row=15, column=1)
        number_str = Entry(self.add_wind)
        number_str.grid(row=15, column=2)

        # DATE TABLE

        Label(self.add_wind, text="DATE TABLE").grid(row=16, column=1)

        Label(self.add_wind, text="Date Type: ").grid(row=17, column=1)
        dtype_str = Entry(self.add_wind)
        dtype_str.grid(row=17, column=2)

        Label(self.add_wind, text="Date (yyyy-mm-dd): ").grid(row=18, column=1)
        date_str = Entry(self.add_wind)
        date_str.grid(row=18, column=2)

        try:
            Button(self.add_wind, text="Confirm",
                   command=lambda: self.insert_contact_db(Contact_id_str.get(), fname_str.get(), mname_str.get(),
                                                          lname_str.get(), addrtype_str.get(), addr_str.get(),
                                                          city_str.get(), state_str.get(), zip_str.get(),
                                                          ptype_str.get(), areacode_str.get(), number_str.get(),
                                                          dtype_str.get(), date_str.get())).grid(row=19, column=2,
                                                                                                 sticky=W)
        except:
            self.message['text'] = "Incorrect Entry"

    def insert_contact_db(self, Contact_id_str, fname_str, mname_str, lname_str, addrtype_str, addr_str, city_str,
                          state_str, zip_str, ptype_str, areacode_str, number_str, dtype_str, date_str):

        if Contact_id_str != "":
            if fname_str != "" and lname_str != "":
                query = "INSERT INTO CONTACT(Contact_id, Fname, Mname, Lname) VALUES('" + Contact_id_str + "','" + fname_str + "','" + mname_str + "','" + lname_str + "')"
                self.run_query(query, "INSERT")

            if addrtype_str != "" and addr_str != "":
                query1 = "INSERT INTO ADDRESS(Contact_id, Address_type, Address, City, State, Zip) VALUES('" + Contact_id_str + "','" + addrtype_str + "','" + addr_str + "','" + city_str + "','" + state_str + "','" + zip_str + "')"
                self.run_query(query1, "INSERT")

            if ptype_str != "" and number_str != "":
                query2 = "INSERT INTO PHONE(Contact_id, Phone_type, Area_code, Number) VALUES('" + Contact_id_str + "','" + ptype_str + "','" + areacode_str + "','" + number_str + "')"
                self.run_query(query2, "INSERT")

            if dtype_str != "" and date_str != "":
                query3 = "INSERT INTO DATE(Contact_id, Date_type, Date) VALUES('" + Contact_id_str + "','" + dtype_str + "','" + date_str + "')"
                self.run_query(query3, "INSERT")

        else:
            if fname_str != "" and lname_str != "":
                query = "INSERT INTO CONTACT(Fname, Mname, Lname) VALUES('" + fname_str + "','" + mname_str + "','" + lname_str + "')"
                self.run_query(query, "INSERT")

                get_query = "SELECT Contact_id FROM CONTACT WHERE Fname = '" + fname_str + "' and Mname = '" + mname_str + "' and Lname = '" + lname_str + "'"
                val = self.run_query(get_query, "GET")
                Contact_id_val = str(val[0][0])

                if addrtype_str != "" and addr_str != "":
                    query1 = "INSERT INTO ADDRESS(Contact_id, Address_type, Address, City, State, Zip) VALUES('" + Contact_id_val + "','" + addrtype_str + "','" + addr_str + "','" + city_str + "','" + state_str + "','" + zip_str + "')"
                    self.run_query(query1, "INSERT")

                if ptype_str != "" and number_str != "":
                    query2 = "INSERT INTO PHONE(Contact_id, Phone_type, Area_code, Number) VALUES('" + Contact_id_val + "','" + ptype_str + "','" + areacode_str + "','" + number_str + "')"
                    self.run_query(query2, "INSERT")

                if dtype_str != "" and date_str != "":
                    query3 = "INSERT INTO DATE(Contact_id, Date_type, Date) VALUES('" + Contact_id_val + "','" + dtype_str + "','" + date_str + "')"
                    self.run_query(query3, "INSERT")
            else:
                self.message['text'] = "The (Contact_id) or (First Name and Last Name) cannot be empty"

        self.add_wind.destroy()
        self.message['text'] = "Contact {} {} {} Added Successfully".format(fname_str, mname_str, lname_str)

        # Filling the GUI
        self.get_contacts()


if __name__ == "__main__":
    window = Tk()
    # window.geometry("600x300")
    application = ContactApp(window)
    window.mainloop()
