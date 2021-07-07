# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 18:39:00 2021

@author: Lenovo
"""


import base64
import sqlite3
import streamlit as st
import pandas as pd
from PIL import Image


try:
    con = sqlite3.connect('smiit.db')
except:
    "Database is not connected"
    
try:
    st.title("SMIIT DASHBOARD")
    cursor = con.cursor()
    
    Tables =["Manager","Employee","Attendance"]
    
    Type = ["Insert","Delete","Custom"]
    
    option2 = st.selectbox(
                    'Select Operation',
                     Type)
    
    
    option = st.selectbox(
                    'Select Table',
                     Tables)
    
    "* fields are complusory"
    
    
    if option2 == Type[0]:
       if option == Tables[0]:
           Manager_ID = st.number_input("Enter Manager ID ( Employee_ID for Manager) *",step = 1)
           Department = st.text_input("Enter Department of Manager *")
           Button = st.button("ADD")
           SQL = "Insert INTO Manager (Department, Manager_ID) Values (?,?)"
           if Button:
               cursor.execute(SQL,(Department,Manager_ID))
               "Added Successfully"
               con.commit()
       if option == Tables[1]:
           #st.write("**NOTE** : Before making the entry in Employee Table, Make sure you have added the Employee ID in Admin")
           Employee_ID = st.number_input("Enter Employee ID *",step = 1)
           name = st.text_input("Enter Employee's Name * ")
           Manager_ID = st.number_input("Enter Manager ID of the Employee *",step = 1)
           Role = st.text_input("Enter Role of Employee *")
           Salary = st.number_input("Enter Salary of Employee *",step = 10)
           Qualification = st.text_input("Qualifications of employee *")
           Date_of_joining = st.date_input("Date of Joining *")     
           CONTACT = st.number_input("Contact Information *",step = 1)
           passport_number = st.text_input("Passport Number ")
           Visa_Validity_to = st.date_input("Enter Visa Validity From: ")
           Visa_validity_expiry = st.date_input("Enter Visa Validity To: ")
           NI_number = st.text_input("Enter NI Number ")
           passport_expiry_date = st.date_input("Enter Passport Expiry Date ")
           Button = st.button("ADD")
           SQL = """Insert INTO Employee (NAME, ROLE,EMPLOYEE_SALARY,QUALIFICATION,
           DATE_OF_JOINIING,CONTACT_NO,EMPLOYEE_ID,MANAGER_ID,PASSPORT_NO,VISA_VALIDITY,VISA_EXPIRY,NI_NUMBER,PASSPORT_EXPIRY) Values (?,?,?,?,?,?,?,?,?,?,?,?,?)"""
           SQL2 = "INSERT INTO ADMIN VALUES ({})".format(Employee_ID)
           if Button:
               cursor.execute(SQL,(name,Role,Salary,Qualification,Date_of_joining,CONTACT,Employee_ID,Manager_ID,passport_number,Visa_Validity_to,Visa_validity_expiry
                                   ,NI_number,passport_expiry_date))
               con.commit()
               cursor.execute(SQL2)
               con.commit
               "Added Successfully"
               con.commit()
       if option == Tables[2]:
           Date = st.date_input("Date *")
           Employee_ID = st.number_input("Enter Employee ID *",step = 1)
           Attendance = st.selectbox("Attendance", ("Present *","Absent"))
           if Attendance == "Present":
               Attendance = 1
           else:
               Attendance = 0
           Button = st.button("ADD")
           SQL = "INSERT INTO Attendance VALUES (?,?,?)"
           if Button:
               cursor.execute(SQL,(Date,Attendance,Employee_ID))
               "Added Successfully"
               con.commit()        
    
            
    if option2 == Type[1]:
        if option == Tables[0]:
            st.write(' **NOTE **: The manager access would be revoked but the person is still an employee')
            Manager_ID = st.number_input("Enter Manager ID to delete the employee as manager *",step = 1)
            SQL = "DELETE FROM MANAGER WHERE Manager_ID = ?"
            Button = st.button("Delete")
            if Button:
                cursor.execute(SQL,(Manager_ID,))
                con.commit()
                "Deleted Successfully"
        if option == Tables[1]:
            st.write(' **Note** : that Employee records would be deleted completely')
            Employee_ID = st.number_input("Enter ID to delete the employee *",step = 1)
            SQL2 = "DELETE FROM ADMIN WHERE EMPLOYEE_ID = ?"
            Button = st.button("Delete")
            SQL = "DELETE FROM EMPLOYEE WHERE EMPLOYEE_ID = ?"
            SQL3 = "DELETE FROM MANAGER WHERE MANAGER_ID = ?"
            SQL4 = "Delete from attendance where employee_ID = ?"
            if Button:
                cursor.execute(SQL,(Employee_ID,))
                con.commit()
                con.execute(SQL2,(Employee_ID,))
                con.commit()
                cursor.execute(SQL3,(Employee_ID,))
                con.commit()
                cursor.execute(SQL4,(Employee_ID,))
                con.commit()
                "Deleted Successfully"
        if option == Tables[2]:
            Date = st.date_input("Enter Date *")
            Employee_ID = st.number_input("Enter Employee ID *",step = 1)
            SQL = "DELETE FROM Attendance Where Employee_ID = ? AND Date = ?"
            Button = st.button("Delete")
            if Button :
                cursor.execute(SQL,(Employee_ID,Date))
                con.commit()
                "Deleted Successfully"
    if option2 == Type[2]:
        Query = st.text_input("Write Your Query")
        cursor.execute(Query)
        data = cursor.fetchall()
        for i in data:
            i
            
            
    st.write("## The dataframe for reference ")
    
    data = ["Manager","Employee","Attendance","Admin"]
    
    
    data_option = st.selectbox(
                    'Select Dataframe',
                     data)
    
    
    
    df = pd.read_sql("SELECT * FROM %s" %data_option , con)
    df
    csv = df.to_csv()
    if st.button("Click to download {} Table".format(data_option)):
       'Download Started!'
       b64 = base64.b64encode(csv.encode()).decode()  # some strings
       linko= f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'
       st.markdown(linko, unsafe_allow_html=True)
       
except:
    "Error has occured"
    st.write("Please check inputs or your query")