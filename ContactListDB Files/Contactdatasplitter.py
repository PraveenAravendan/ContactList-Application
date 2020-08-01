filereader = open("C:\\Users\\prave\\Desktop\\UTD Spring 2020 Classes\\Database Design\\Projects and Homeworks\\Contacts.csv",'r')
filewriter = open("C:\\Users\\prave\\Desktop\\UTD Spring 2020 Classes\\Database Design\\Projects and Homeworks\\ContactDBInsert.sql",'w+')

sql1 = str()
sql2 = str()
sql3 = str()
sql4 = str()
sql5 = str()
for line in filereader:
    data = line.strip().split(',')
    if 'contact_id' not in data:
        Contact_id = data[0]
        Fname = data[1].strip()
        Mname = data[2].strip()
        Lname = data[3].strip()
        sql1 = "INSERT INTO CONTACT (Contact_id, Fname, Mname, Lname) VALUES ({0}, \"{1}\", \"{2}\", \"{3}\");".format(Contact_id, Fname, Mname, Lname)

        home_phone = data[4].strip()
        cell_phone = data[5].strip()
        home_address = data[6].strip()
        home_city = data[7].strip()
        home_state = data[8].strip()
        home_zip = data[9].strip()
        if home_phone:
            sql2 = "INSERT INTO PHONE (Contact_id, Phone_type, Area_code, Number) VALUES ({0}, \"{1}\", \"{2}\", \"{3}\");".format(Contact_id, 'Home', home_phone[:3], home_phone )
        if cell_phone:
            sql3 = "INSERT INTO PHONE (Contact_id, Phone_type, Area_code, Number) VALUES ({0}, \"{1}\", \"{2}\", \"{3}\");".format(Contact_id, 'Cell', cell_phone[:3], cell_phone)
        if home_address:
            sql4 = "INSERT INTO ADDRESS (Contact_id, Address_type, Address, City, State, Zip) VALUES ({0}, \"{1}\", \"{2}\", \"{3}\", \"{4}\", \"{5}\");".format(Contact_id, 'Home', home_address, home_city, home_state, home_zip)

        work_phone = data[10].strip()
        work_address = data[11].strip()
        work_city = data[12].strip()
        work_state = data[13].strip()
        work_zip = data[14].strip()
        birth_date = data[15].strip()
        if work_phone:
            sql2 = "INSERT INTO PHONE (Contact_id, Phone_type, Area_code, Number) VALUES ({0}, \"{1}\", \"{2}\", \"{3}\");".format(Contact_id, 'Work', work_phone[:3], work_phone)
        if work_address:
            sql4 = "INSERT INTO ADDRESS (Contact_id, Address_type, Address, City, State, Zip) VALUES ({0}, \"{1}\", \"{2}\", \"{3}\", \"{4}\", \"{5}\");".format(Contact_id, 'Work', work_address, work_city, work_state, work_zip)
        if birth_date:
            sql5 = "INSERT INTO DATE (Contact_id, Date_type, Date) VALUES ({0}, \"{1}\", \"{2}\");".format(Contact_id, 'BirthDate', birth_date)

        print('SQL 1', sql1)
        print('SQL 2', sql2)
        print('SQL 3', sql3)
        print('SQL 4', sql4)
        print('SQL 5', sql5)

        if sql1:
            filewriter.write(sql1+'\n')
        if sql2:
            filewriter.write(sql2+'\n')
        if sql3:
            filewriter.write(sql3+'\n')
        if sql4:
            filewriter.write(sql4+'\n')
        if sql5:
            filewriter.write(sql5+'\n')

filereader.close()
filewriter.close()




