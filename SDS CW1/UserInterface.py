import tkinter 
import sys
from tkinter import *
from datetime import datetime
from datetime import date
from warnings import catch_warnings
from Logic import Admin
from Logic import Login
from Logic import PatientList
from Logic import Patient

#################################################################################################################
# GUI
#################################################################################################################

class GUI:

    ADMIN_FILE = "Admins.txt"
    DOCTOR_FILE = "Doctors.txt"
    PATIENT_FILE = "Patients.txt"
    
    def __init__(self):
        
        self.__role = ""

        self.__my_widget = tkinter.Tk()
        self.__my_widget.geometry("1000x700")

    #allows the user to select their role
    def SelectRole(self):

        self.ClearWidgets()

        button_width = 6

        select_role_prompt = tkinter.Label(self.__my_widget, text = "Are you an admin doctor or patient?")
        select_role_prompt.pack(side = 'top')

        admin_button = tkinter.Button(self.__my_widget, text = "Admin", width = button_width, command = lambda : self.DoLogin("admin"))
        admin_button.pack(side = 'top')

        doctor_button = tkinter.Button(self.__my_widget, text = "Doctor", width = button_width, command = lambda : self.DoLogin("doctor"))
        doctor_button.pack(side = 'top')

        patient_button = tkinter.Button(self.__my_widget, text = "Patient", width = button_width, command = lambda : self.DoLogin("patient"))
        patient_button.pack(side = 'top')

        enroll_button = tkinter.Button(self.__my_widget, text = "Enroll", width = button_width, command = lambda : self.Enroll())
        enroll_button.pack(side = 'top')

        tkinter.mainloop()

    #sets the role of the user
    def DoLogin(self, roleID):

        self.__role = roleID

        login = Login()

        if self.__role == "admin":

            login.LoadLogins(self.ADMIN_FILE)

        elif self.__role == "doctor":

                login.LoadLogins(self.DOCTOR_FILE)

        elif self.__role == "patient":

            login.LoadLogins(self.PATIENT_FILE)

        self.Login(login) 

    #allows the user to login
    def Login(self, login):

        self.ClearWidgets()

        entry_width = 20
      
        username_label = tkinter.Label(self.__my_widget, text = "Username:")
        username_label.pack(side = 'top')

        username_entry = tkinter.Entry(self.__my_widget, width = entry_width)
        username_entry.pack(side = 'top')

        password_label = tkinter.Label(self.__my_widget, text = "Password:")
        password_label.pack(side = 'top') 

        password_entry = tkinter.Entry(self.__my_widget, show = '*', width = entry_width)
        password_entry.pack(side = 'top')

        login_button = tkinter.Button(self.__my_widget, text = "Login", command = lambda : self.LoginAs(username_entry.get(), password_entry.get(), login))
        login_button.pack(side = 'top')

        go_back_button = tkinter.Button(self.__my_widget, text = "Go Back", command = lambda : self.SelectRole())
        go_back_button.pack(side = 'top')

        tkinter.mainloop()

    #attempts to login
    def LoginAs(self, username, password, login):

        self.ClearWidgets()

        person = login.Login(username, password, self.__role)

        #the correct combination is entered
        if person is not None:

            self.OpenCorrectDashBoard(self.__role, person)

        #an incorrect combination is entered
        else:

            login.IncreaseAttempts()

            if login.GetAttemptsRemaining() == 0:
            
                  self.FailedLogin()

            else:

                self.InncorrectLogin(login)

    #shows the remianing attempts and allows the user to retry
    def InncorrectLogin(self, login):

        self.ClearWidgets()

        incorrect_label = tkinter.Label(self.__my_widget, text = "Incorrect Username Or Password")
        incorrect_label.pack(side = 'top')

        attempts_label = tkinter.Label(self.__my_widget, text = "Attempts Remaining: {0}".format(login.GetAttemptsRemaining()))
        attempts_label.pack(side = 'top')

        retry_button = tkinter.Button(self.__my_widget, text = "Retry", command = lambda : self.Login(login))
        retry_button.pack(side = 'top')

        tkinter.mainloop()

    #when the user has run out of login attempts tells them and ends the program
    def FailedLogin(self):

        self.ClearWidgets()

        incorrect_label = tkinter.Label(self.__my_widget, text = "Out Of Login Attempts")
        incorrect_label.pack(side = 'top')

        #exit no need to save
        quit_button = tkinter.Button(self.__my_widget, text = "Quit", command = lambda : self.Quit())
        quit_button.pack(side = 'top')

        tkinter.mainloop()

    #allows patient to enter their infomation to apply to enroll in the system
    def Enroll(self):

        self.ClearWidgets()

        entry_width = 20

        title_label = tkinter.Label(self.__my_widget, text = "Application To Enroll")
        title_label.pack(side = 'top')

        firstname_label = tkinter.Label(self.__my_widget, text = "Firstname:")
        firstname_label.pack(side = 'top')

        firstname_entry = tkinter.Entry(self.__my_widget, width = entry_width)
        firstname_entry.pack(side = 'top')

        surname_label = tkinter.Label(self.__my_widget, text = "Surname:")
        surname_label.pack(side = 'top')

        surname_entry = tkinter.Entry(self.__my_widget, width = entry_width)
        surname_entry.pack(side = 'top')

        date_of_birth_label = tkinter.Label(self.__my_widget, text = "Date of birth:")
        date_of_birth_label.pack(side = 'top')

        year_label = tkinter.Label(self.__my_widget, text = "Year:")
        year_label.pack(side = 'top')

        #gets a list of previous 1000 years from current year
        year = datetime.today().year
        yearOptions = list(range(year, year - 101, -1))
        
        selectedYear = StringVar(self.__my_widget, datetime.today().year)

        year_drop = OptionMenu(self.__my_widget, selectedYear, *yearOptions )
        year_drop.pack()

        month_label = tkinter.Label(self.__my_widget, text = "Month:")
        month_label.pack(side = 'top')

        # Dropdown month menu options for months 
        monthOptions = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

        selectedMonth = StringVar(self.__my_widget, "1")

        month_drop = OptionMenu(self.__my_widget, selectedMonth, *monthOptions)
        month_drop.pack()

        day_label = tkinter.Label(self.__my_widget, text = "Day:")
        day_label.pack(side = 'top')
        
        dayOptions = []
        #gets a list of days between 1 and the selected months number of days theoretically
        selectedMonth.trace_add("unset", self.UpdateDayOptions(selectedMonth.get(), dayOptions))
        #dayOptions = list(range(1, int(self.GetNumberOfDays(selectedMonth.get()))))

        selectedDay = StringVar(self.__my_widget, "1" )

        #stupid problem hererererer
        day_drop = OptionMenu(self.__my_widget, selectedDay, *dayOptions)
        day_drop.pack()

        mobile_label = tkinter.Label(self.__my_widget, text = "Mobile:")
        mobile_label.pack(side = 'top')

        mobile_entry = tkinter.Entry(self.__my_widget, width = entry_width)
        mobile_entry.pack(side = 'top')

        address_label = tkinter.Label(self.__my_widget, text = "Address:")
        address_label.pack(side = 'top')

        address_entry = tkinter.Entry(self.__my_widget, width = entry_width)
        address_entry.pack(side = 'top')

        # symptoms_label = tkinter.Label(self.__my_widget, text = "Symptoms:")
        # symptoms_label.pack(side = 'top')

        # symptoms_entry = tkinter.Entry(self.__my_widget, width = entry_width)
        # symptoms_entry.pack(side = 'top')

        # username_label = tkinter.Label(self.__my_widget, text = "Username:")
        # username_label.pack(side = 'top')

        # username_entry = tkinter.Entry(self.__my_widget, width = entry_width)
        # username_entry.pack(side = 'top')

        # password_label = tkinter.Label(self.__my_widget, text = "Password:")
        # password_label.pack(side = 'top')

        # password_entry = tkinter.Entry(self.__my_widget, show = '*', width = entry_width)
        # password_entry.pack(side = 'top')

        apply_button = tkinter.Button(self.__my_widget, text = "Apply", command = lambda : self.DoEnroll(firstname_entry.get() + " " + surname_entry.get(), selectedYear.get(), selectedMonth.get(), selectedDay.get(), mobile_entry.get(), address_entry.get()))
        apply_button.pack(side = 'top')

        cancel_button = tkinter.Button(self.__my_widget, text = "Cancel", command = lambda : self.SelectRole())
        cancel_button.pack(side = 'top')

        tkinter.mainloop()

    #FIX
    #tries to pass dayOptions byref
    def UpdateDayOptions(self, month, dayOptions):

        tempDayOptions = []
        tempDayOptions = list(range(1, int(self.GetNumberOfDays(month)) + 1))

        for day in tempDayOptions:

            dayOptions.append(day)

    #returns the number of days in the month
    def GetNumberOfDays(self, month):

        days = 0

        if month == "2":
        
            days = "29"

        elif month == "1" or month == "3" or month == "5" or month == "7" or month == "7" or month == "8" or month == "10" or month == "12":

            days = "31"

        elif month == "4" or month == "6" or month == "9" or month == "11":

            days = "30"

        return days

    #addds the patient infomation to the list of applied patients to be reviewed
    def DoEnroll(self, name, year, month, day, mobile, address):

        valid = True

        #FIX
        #tries to convert the entered infomation into the correct date format
        try:

            #dateOfBirth = day + '-' + month + '-' + year
            dateTimeOfBirth = date(int(year), int(month), int(day))
            #dateTimeOfBirth = datetime.strptime(dateOfBirth, '%d-%m-%Y').date

        except Exception as e:

            print(f"error: {str(e)}")
            valid = False
            self.InvalidDate()

        #only if valid date entered
        if valid == True:

            #checks the entered username against the existing usernames
            currentPatients = PatientList("Patients.txt")
            currentPatients.Load()

            #existingUsernames = currentPatients.GetAllPatientUsernames()

            #to check against treated and applied usernames
            #currentPatients = PatientList("Patients.txt")
            #currentPatients.Load()
            #existingUsernames = currentPatients.GetAllPatientUsernames()

            #currentPatients = PatientList("Patients.txt")
            #currentPatients.Load()
            #existingUsernames = currentPatients.GetAllPatientUsernames()

            #if there are already existing usernames in the system
            #if not existingUsernames is None:

                #for existingUsername in existingUsernames:

                    #if username == existingUsername:

                        #self.UsernameAlreadyExists()
                        #valid = False

            #only if username is unique
            if valid == True:

                appliedPatients = PatientList("AppliedPatients.txt")

                #scuffed admin bascically just database 
                admin = Admin("computer", "system", "shhhhh", "you cant see this")

                admin.Load()
                username = admin.GeneratePatientUsername(name)
                password = admin.GeneratePassword()

                appliedPatients.Load()
                appliedPatients.AddPatient(username, password, name, dateTimeOfBirth, mobile, address)
                appliedPatients.Save()

                #returns to start screen
                self.SelectRole()

    #outputs an error if the entered date is not valid
    def InvalidDate(self):

        error_label = tkinter.Label(self.__my_widget, text = "This Is Not A Valid Date")
        error_label.pack(side = 'top')

        tkinter.mainloop()

    #outputs that the username already exists onto the screen
    def UsernameAlreadyExists(self):

        error_label = tkinter.Label(self.__my_widget, text = "This Username Already Exits")
        error_label.pack(side = 'top')

        tkinter.mainloop()

    #opens the correct dashboard for the role
    def OpenCorrectDashBoard(self, role , person):

        if role == "admin":

            adminGUI = AdminGUI(person, self.__my_widget)
            adminGUI.LoadAll()

        elif role == "doctor":

            doctorGUI = DoctorGUI(person, self.__my_widget)
            doctorGUI.Load()

        elif role == "patient":

            patientGUI = PatientGUI(person, self.__my_widget)
            patientGUI.DashBoard()

    #clears previous widgets from the window
    def ClearWidgets(self):

        self.__my_widget.destroy()
        self.__my_widget = tkinter.Tk()
        self.__my_widget.geometry("1000x700")

    #quits the program
    def Quit(self):

        sys.exit()


#################################################################################################################
# AdminGUI
#################################################################################################################

class AdminGUI(object):

    def __init__(self, admin, widget):

        self.__my_widget = widget
        self.__admin = admin

    #loads all the file infomation into the admin
    def LoadAll(self):

        self.__admin.Load()
        self.DashBoard()

    #saves all the files
    def SaveAll(self):

        self.__admin.Save()

    #shows the admins dashboard
    def DashBoard(self):

        button_width = 25

        admin_dashboard_label = tkinter.Label(self.__my_widget, width = button_width, text = "Admin Dashboard")
        admin_dashboard_label.pack(side = 'top')

        manage_doctors_button = tkinter.Button(self.__my_widget, width = button_width, text = "Manage Doctors", command = lambda : self.ManageDoctors())
        manage_doctors_button.pack(side = 'top')

        manage_patients_button = tkinter.Button(self.__my_widget, width = button_width, text = "Manage Patients", command = lambda : self.ManagePatients())
        manage_patients_button.pack(side = 'top')

        manage_appointments_button = tkinter.Button(self.__my_widget, width = button_width, text = "Manage Appointments", command = lambda : self.ManageAppointments())
        manage_appointments_button.pack(side = 'top')

        update_own_infomation_button = tkinter.Button(self.__my_widget, width = button_width, text = "Update Own Infomation", command = lambda : self.UpdateOwnInfomation())
        update_own_infomation_button.pack(side = 'top')

        request_management_report_button = tkinter.Button(self.__my_widget, width = button_width, text = "Request Management Report", command = lambda : self.RequestManagementReport())
        request_management_report_button.pack(side = 'top')

        quit_button = tkinter.Button(self.__my_widget, width = button_width, text = "Quit", command = lambda : self.Quit())
        quit_button.pack(side = 'top')

        tkinter.mainloop()

    def ManageDoctors(self):

        self.ClearWidgets()
        button_width = 25

        manage_doctors_label = tkinter.Label(self.__my_widget, width = button_width, text = "Manage Doctors")
        manage_doctors_label.pack(side = 'top')

        register_doctor_button = tkinter.Button(self.__my_widget, width = button_width, text = "Register Doctor", command = lambda : self.RegisterDoctor())
        register_doctor_button.pack(side = 'top')

        view_doctor_button = tkinter.Button(self.__my_widget, width = button_width, text = "View Doctor", command = lambda : self.ViewDoctor())
        view_doctor_button.pack(side = 'top')

        update_doctor_button = tkinter.Button(self.__my_widget, width = button_width, text = "Update Doctor", command = lambda : self.UpdateDoctor())
        update_doctor_button.pack(side = 'top')
   
        delete_doctor_button = tkinter.Button(self.__my_widget, width = button_width, text = "Delete Doctor", command = lambda : self.DeleteDoctor())
        delete_doctor_button.pack(side = 'top')

        return_to_dashboard_button = tkinter.Button(self.__my_widget, text = "Return To Dashboard", command = lambda : self.ClearAndReturn())
        return_to_dashboard_button.pack(side = 'top')

    def ManagePatients(self):

        self.ClearWidgets()
        button_width = 25

        manage_patients_label = tkinter.Label(self.__my_widget, width = button_width, text = "Manage Patients")
        manage_patients_label.pack(side = 'top')

        view_applied_patients_button = tkinter.Button(self.__my_widget, width = button_width, text = "View Applied Patients", command = lambda : self.ViewAppliedPatients())
        view_applied_patients_button.pack(side = 'top')

        assign_patient_button = tkinter.Button(self.__my_widget, width = button_width, text = "Assign Patient", command = lambda : self.AssignPatient())
        assign_patient_button.pack(side = 'top')

        view_patient_record_button = tkinter.Button(self.__my_widget, width = button_width, text = "View Patient Record", command = lambda : self.ViewPatientRecord())
        view_patient_record_button.pack(side = 'top')

        discharge_patient_button = tkinter.Button(self.__my_widget, width = button_width, text = "Discharge Patient", command = lambda : self.DischargePatient())
        discharge_patient_button.pack(side = 'top')

        view_treated_patients_button = tkinter.Button(self.__my_widget, width = button_width, text = "View Treated Patients", command = lambda : self.ViewTreatedPatientsList())
        view_treated_patients_button.pack(side = 'top')

        manage_families_button = tkinter.Button(self.__my_widget, width = button_width, text = "Manage Families", command = lambda : self.ManageFamilies())
        manage_families_button.pack(side = 'top')

        return_to_dashboard_button = tkinter.Button(self.__my_widget, text = "Return To Dashboard", command = lambda : self.ClearAndReturn())
        return_to_dashboard_button.pack(side = 'top')

    def ManageAppointments(self):

        self.ClearWidgets()
        button_width = 25

        manage_appointments_label = tkinter.Label(self.__my_widget, width = button_width, text = "Manage Appointments")
        manage_appointments_label.pack(side = 'top')

        approve_appointments_button = tkinter.Button(self.__my_widget, text = "Approve Appointments", command = lambda : self.ApproveAppointment())
        approve_appointments_button.pack(side = 'top')

        return_to_dashboard_button = tkinter.Button(self.__my_widget, text = "Return To Dashboard", command = lambda : self.ClearAndReturn())
        return_to_dashboard_button.pack(side = 'top')

    #allows the user to register a doctor by entering a name and username
    def RegisterDoctor(self):

        self.ClearWidgets()

        register_doctor_label = tkinter.Label(self.__my_widget, text = "Register Doctor")
        register_doctor_label.pack(side = 'top')

        name_label = tkinter.Label(self.__my_widget, text = "Name:")
        name_label.pack(side = 'top')

        name_entry = tkinter.Entry(self.__my_widget, width = 20)
        name_entry.pack(side = 'top')

        username_label = tkinter.Label(self.__my_widget, text = "Username:")
        username_label.pack(side = 'top')

        username_entry = tkinter.Entry(self.__my_widget, width = 20)
        username_entry.pack(side = 'top')

        register_button = tkinter.Button(self.__my_widget, text = "Register", command = lambda : self.TryRegisterDoctor(username_entry.get(), name_entry.get()))
        register_button.pack(side = 'top')

        return_to_manage_doctors_button = tkinter.Button(self.__my_widget, text = "Return To Manage Doctors", command = lambda : self.ManageDoctors())
        return_to_manage_doctors_button.pack(side = 'top')

    #checks that the doctors username is unique
    def TryRegisterDoctor(self, newUsername, name):

        usernames = []
        usernames = self.__admin.GetAllDoctorUsernames()

        valid = True

        for username in usernames:

            #if not unique clear and go to the error screen
            if username == newUsername:

                self.ClearWidgets
                self.RepeatedDoctorUsername()
                valid = False

        #unique add doctor to system
        if valid == True: 

            self.__admin.RegisterDoctor(newUsername, name)
            self.RegisterDoctor()

    #allows the admin to view a doctors infomation
    def ViewDoctor(self):

        self.ClearWidgets()

        view_doctor_label = tkinter.Label(self.__my_widget, text = "View Doctor")
        view_doctor_label.pack(side = 'top')

        doctorOptions = self.__admin.GetAllDoctorUsernames()

        #if there are doctors in the system
        if not doctorOptions is None and len(doctorOptions) > 0:

            #drop down menu of doctors
            selectedDoctor = StringVar(self.__my_widget, doctorOptions[0])
            doctor_drop = OptionMenu(self.__my_widget, selectedDoctor, *doctorOptions)
            doctor_drop.pack()  

            select_button = tkinter.Button(self.__my_widget, text = "Select", command = lambda : self.DoViewDoctor(selectedDoctor.get()))
            select_button.pack(side = 'top')

        else:

            no_doctor_label = tkinter.Label(self.__my_widget, text = "No Doctors")
            no_doctor_label.pack(side = 'top')
        
        return_to_manage_doctors_button = tkinter.Button(self.__my_widget, text = "Return To Manage Doctors", command = lambda : self.ManageDoctors())
        return_to_manage_doctors_button.pack(side = 'top')

    #allows the admin to view a doctor infomation
    def DoViewDoctor(self, username):

        self.ClearWidgets()

        doctor = self.__admin.GetDoctorFromUsername(username)

        name_label = tkinter.Label(self.__my_widget, text = "Current Name: {0}".format(doctor.GetName()))
        name_label.pack(side = 'top')  

        username_label = tkinter.Label(self.__my_widget, text = "Current Username: {0}".format(doctor.GetUsername()))
        username_label.pack(side = 'top')  

        patients = doctor.GetPatients()

        if len(patients) > 0:

            patients_label = tkinter.Label(self.__my_widget, text = "Current Patients: {0}".format(doctor.MakePatientsLine()))
            patients_label.pack(side = 'top')  

        else:

            patients_label = tkinter.Label(self.__my_widget, text = "Current Patients: None")

        #appointments

        go_back_button = tkinter.Button(self.__my_widget, text = "Go Back", command = lambda : self.ViewDoctor())
        go_back_button.pack(side = 'top')          

    #allows the admin to update the doctors name and username
    def UpdateDoctor(self):

        self.ClearWidgets()

        update_doctor_label = tkinter.Label(self.__my_widget, text = "Update Doctor")
        update_doctor_label.pack(side = 'top')

        doctorOptions = self.__admin.GetAllDoctorUsernames()

        #if there are doctors in the system
        if not doctorOptions is None and len(doctorOptions) > 0:

            #drop down menu of doctors
            selectedDoctor = StringVar(self.__my_widget, doctorOptions[0])
            doctor_drop = OptionMenu(self.__my_widget, selectedDoctor, *doctorOptions)
            doctor_drop.pack()  

            select_button = tkinter.Button(self.__my_widget, text = "Select", command = lambda : self.DoUpdateDoctor(selectedDoctor.get()))
            select_button.pack(side = 'top')

        else:

            no_doctor_label = tkinter.Label(self.__my_widget, text = "No Doctors")
            no_doctor_label.pack(side = 'top')

        return_to_manage_doctors_button = tkinter.Button(self.__my_widget, text = "Return To Manage Doctors", command = lambda : self.ManageDoctors())
        return_to_manage_doctors_button.pack(side = 'top')

        tkinter.mainloop()

    #where the admin enteres the new username and name
    def DoUpdateDoctor(self, doctorUsername):
            
            self.ClearWidgets()

            current_name_label = tkinter.Label(self.__my_widget, text = "Current Name: {0}".format(self.__admin.GetDoctorFromUsername(doctorUsername).GetName()))
            current_name_label.pack(side = 'top')   

            name_entry = tkinter.Entry(self.__my_widget, width = 20)
            name_entry.pack(side = 'top')     

            update_name_button = tkinter.Button(self.__my_widget, text = "Update Name", command = lambda : self.DoUpdateName(doctorUsername, name_entry.get()))
            update_name_button.pack(side = 'top')  

            current_username_label = tkinter.Label(self.__my_widget, text = "Current Username: {0}".format(doctorUsername))
            current_username_label.pack(side = 'top')   

            username_entry = tkinter.Entry(self.__my_widget, width = 20)
            username_entry.pack(side = 'top')     

            update_username_button = tkinter.Button(self.__my_widget, text = "Update Username", command = lambda : self.DoUpdateUsername(doctorUsername, username_entry.get()))
            update_username_button.pack(side = 'top') 

            return_button = tkinter.Button(self.__my_widget, text = "Go Back", command = lambda : self.UpdateDoctor())
            return_button.pack(side = 'top') 

            tkinter.mainloop()

    #updates the doctors name and saves it then returns to update screen
    def DoUpdateName(self, username, name):

        self.__admin.GetDoctorFromUsername(username).SetName(name)
        self.__admin.save()
        self.DoUpdateDoctor(username)

    #updates the doctors username if the username does not already exist saves it and returns to update screen
    def DoUpdateUsername(self, usernameToUpdate, newUsername):

        usernames = []
        usernames = self.__admin.GetAllDoctorUsernames()

        valid = True

        for username in usernames:

            #if not unique clear and go to the error screen
            if username == newUsername:

                self.ClearWidgets
                self.RepeatedDoctorUsername()
                valid = False

        #unique then change the username and save the file, return to update page
        if valid == True: 

            self.__admin.GetDoctorFromUsername(usernameToUpdate).SetUsername(newUsername)
            self.__admin.Save()
            self.DoUpdateDoctor(newUsername)

    #allows the admin to select and delete a doctor from the system
    def DeleteDoctor(self):

        self.ClearWidgets()

        delete_doctor_label = tkinter.Label(self.__my_widget, text = "Delete Doctor")
        delete_doctor_label.pack(side = 'top')

        doctorOptions = self.__admin.GetAllDoctorUsernames()

        if not doctorOptions is None and len(doctorOptions) > 0:

            #drop down menu of doctors
            selectedDoctor = StringVar(self.__my_widget, doctorOptions[0])
            doctor_drop = OptionMenu(self.__my_widget, selectedDoctor, *doctorOptions)
            doctor_drop.pack()          

            delete_button = tkinter.Button(self.__my_widget, text = "Delete", command = lambda : self.DoDeleteDoctor(selectedDoctor.get()))
            delete_button.pack(side = 'top')  

        else:

            no_doctor_label = tkinter.Label(self.__my_widget, text = "No Doctors")
            no_doctor_label.pack(side = 'top')

        return_to_manage_doctors_button = tkinter.Button(self.__my_widget, text = "Return To Manage Doctors", command = lambda : self.ManageDoctors())
        return_to_manage_doctors_button.pack(side = 'top')

        tkinter.mainloop()

    #deletes the doctor
    def DoDeleteDoctor(self, doctor):

        self.__admin.DeleteDoctor(doctor)
        self.SaveAll()
        self.DeleteDoctor()

    def ApproveAppointment(self):

        self.ClearWidgets()

        approve_appointments_label = tkinter.Label(self.__my_widget, text = "Approve Appointments")
        approve_appointments_label.pack(side = 'top')

        appointments = self.__admin.GetUnapprovedAppointmentIDs()

        if not appointments is None and len(appointments) > 0:

            #drop down menu of doctors
            selectedAppointment = StringVar(self.__my_widget, appointments[0])
            appointment_drop = OptionMenu(self.__my_widget, selectedAppointment, *appointments)
            appointment_drop.pack()          

            view_appointment_button = tkinter.Button(self.__my_widget, text = "View Appiontment", command = lambda : self.DoApproveAppointment(selectedAppointment.get()))
            view_appointment_button.pack(side = 'top')  

        else:

            no_unapproved_appointments_label = tkinter.Label(self.__my_widget, text = "No Unapproved Appointments")
            no_unapproved_appointments_label.pack(side = 'top')

        return_to_manage_appointments_button = tkinter.Button(self.__my_widget, text = "Return To Manage Appointments", command = lambda : self.ManageAppointments())
        return_to_manage_appointments_button.pack(side = 'top')

    def DoApproveAppointment(self, AppointmentID):

        self.ClearWidgets()

        appointment = self.__admin.GetAppointmentFromID()

        appointments_label = tkinter.Label(self.__my_widget, text = "Appointment")
        appointments_label.pack(side = 'top')

        appointment_id_label = tkinter.Label(self.__my_widget, text = "Appointment ID: {0}".format(str(AppointmentID)))
        appointment_id_label.pack(side = 'top')

        doctor_label = tkinter.Label(self.__my_widget, text = "Doctor: {0}".format(appointment.GetDoctor()))
        doctor_label.pack(side = 'top')

        approve_appointments_label = tkinter.Label(self.__my_widget, text = "Patient: {0}".format(appointment.GetPatient()))
        approve_appointments_label.pack(side = 'top')

        approve_appointments_label = tkinter.Label(self.__my_widget, text = "Date Time: ")
        approve_appointments_label.pack(side = 'top')

        approve_button = tkinter.Button(self.__my_widget, text = "Approve", command = lambda : self.ClearAndReturn())
        approve_button.pack(side = 'top')

        decline_button = tkinter.Button(self.__my_widget, text = "Decline", command = lambda : self.ClearAndReturn())
        decline_button.pack(side = 'top')

        go_back_button = tkinter.Button(self.__my_widget, text = "Go Back", command = lambda : self.ApproveAppointment())
        go_back_button.pack(side = 'top')

    def DoApprove(self, appointment):

        appointment.ChangeSatus("Approved")
        self.SaveAll()
        self.ApproveAppointment()

    def DoDecline(self, appointment):

        appointment.ChangeSatus("Declined")
        self.SaveAll()
        self.ApproveAppointment()

    #allows the user to select an applied patient to view
    def ViewAppliedPatients(self):

        self.ClearWidgets()
        self.SaveAll()

        view_applied_patients_label = tkinter.Label(self.__my_widget, text = "View Applied Patients")
        view_applied_patients_label.pack(side = 'top')

        patientOptions = self.__admin.GetAllAppliedPatientUsernames()

        if not patientOptions is None and len(patientOptions) > 0:

            selectPatient = StringVar(self.__my_widget, patientOptions[0])
            patient_drop = OptionMenu(self.__my_widget, selectPatient, *patientOptions)
            patient_drop.pack()

            view_button = tkinter.Button(self.__my_widget, text = "View Applied Patient", command = lambda : self.EnrollPatient(selectPatient.get()))
            view_button.pack(side = 'top') 
      
        else:

            error_label = tkinter.Label(self.__my_widget, text = "No Applied Patients")
            error_label.pack(side = 'top')

        return_to_manage_patients_button = tkinter.Button(self.__my_widget, text = "Return To Manage Patients", command = lambda : self.ManagePatients())
        return_to_manage_patients_button.pack(side = 'top')

    #allows the admin to select a patient to enroll into the system
    def EnrollPatient(self, patientUsername):

        self.ClearWidgets()
     
        patient = self.__admin.GetAppliedPatientFromUsername(patientUsername)

        applied_patient_label = tkinter.Label(self.__my_widget, text = "Applied Patient")
        applied_patient_label.pack(side = 'top')

        name_label = tkinter.Label(self.__my_widget, text = "Name: {0}".format(patient.GetName()))
        name_label.pack(side = 'top')

        #FIX datetimeness
        date_of_birth_label = tkinter.Label(self.__my_widget, text = "Date of birth: {0}".format(patient.GetDateOfBirth()))
        date_of_birth_label.pack(side = 'top')

        mobile_label = tkinter.Label(self.__my_widget, text = "Mobile: {0}".format(patient.GetMobile()))
        mobile_label.pack(side = 'top')

        address_label = tkinter.Label(self.__my_widget, text = "Address: {0}".format(patient.GetAddress()))
        address_label.pack(side = 'top')

        username_label = tkinter.Label(self.__my_widget, text = "Username: {0}".format(patient.GetUsername()))
        username_label.pack(side = 'top')

        enroll_patient_button = tkinter.Button(self.__my_widget, text = "Enroll", command = lambda : self.DoPatientEnroll(patient))
        enroll_patient_button.pack(side = 'top')

        go_back_button = tkinter.Button(self.__my_widget, text = "Go Back", command = lambda : self.ViewAppliedPatients())
        go_back_button.pack(side = 'top')

    def DoPatientEnroll(self, patient):

        self.__admin.EnrollPatient(patient)
        self.ViewAppliedPatients()

    def ViewPatientRecord(self):

        self.ClearWidgets()

        view_patient_record_label = tkinter.Label(self.__my_widget, text = "View Patient Record")
        view_patient_record_label.pack(side = 'top')

        patientOptions = self.__admin.GetAllPatientUsernames()

        if not patientOptions is None and len(patientOptions) > 0:

            selectPatient = StringVar(self.__my_widget, patientOptions[0])
            patient_drop = OptionMenu(self.__my_widget, selectPatient, *patientOptions)
            patient_drop.pack()

            view_button = tkinter.Button(self.__my_widget, text = "View Record", command = lambda : self.DoViewPatientRecord(selectPatient.get()))
            view_button.pack(side = 'top') 
      
        else:

            error_label = tkinter.Label(self.__my_widget, text = "No Patients")
            error_label.pack(side = 'top')

        return_to_manage_patients_button = tkinter.Button(self.__my_widget, text = "Return To Manage Patients", command = lambda : self.ManagePatients())
        return_to_manage_patients_button.pack(side = 'top')

        tkinter.mainloop()

    #outputs the 
    def DoViewPatientRecord(self, patientUsername):

        self.ClearWidgets()
            
        patient = self.__admin.GetPatientFromUsername(patientUsername)

        patient_record_label = tkinter.Label(self.__my_widget, text = "Patient Record")
        patient_record_label.pack(side = 'top')

        name_label = tkinter.Label(self.__my_widget, text = "Name: {0}".format(patient.GetName()))
        name_label.pack(side = 'top')

        #FIX datetimeness
        date_of_birth_label = tkinter.Label(self.__my_widget, text = "Date of birth: {0}".format(patient.GetDateOfBirth()))
        date_of_birth_label.pack(side = 'top')

        mobile_label = tkinter.Label(self.__my_widget, text = "Mobile: {0}".format(patient.GetMobile()))
        mobile_label.pack(side = 'top')

        address_label = tkinter.Label(self.__my_widget, text = "Address: {0}".format(patient.GetAddress()))
        address_label.pack(side = 'top')

        #FIX symptomsness
        symptoms_label = tkinter.Label(self.__my_widget, text = "Symptoms: {0}".format(patient.MakeSymptomsLine()))
        symptoms_label.pack(side = 'top')

        username_label = tkinter.Label(self.__my_widget, text = "Username: {0}".format(patient.GetUsername()))
        username_label.pack(side = 'top')

        go_back_button = tkinter.Button(self.__my_widget, text = "Go Back", command = lambda : self.ViewPatientRecord())
        go_back_button.pack(side = 'top')

        tkinter.mainloop()

    #allows the admin to 
    def AssignPatient(self):
        #maybe make patient only assigned to one doctor? #extra

        self.ClearWidgets()

        assign_patient_label = tkinter.Label(self.__my_widget, text = "Assign Patient")
        assign_patient_label.pack(side = 'top')

        #FIX
        #gets the patients and doctors usernames

        doctorOptions = self.__admin.GetAllDoctorUsernames()
        patientOptions = self.__admin.GetDoctorList().GetAllPatientUsernamesWithoutDoctors()

        #if there are both patients and doctors in the system
        if not patientOptions is None and not doctorOptions is None and not len(patientOptions) == 0 and not len(doctorOptions) == 0:

            select_patient_label = tkinter.Label(self.__my_widget, text = "Select Patient:")
            select_patient_label.pack(side = 'top')

            #makes a patients drop down menu
            selectedPatient =  StringVar(self.__my_widget, patientOptions[0])
            patient_drop = OptionMenu(self.__my_widget, selectedPatient, *patientOptions)
            patient_drop.pack()

            select_doctor_label = tkinter.Label(self.__my_widget, text = "Select Doctor:")
            select_doctor_label.pack(side = 'top')

            #makes a doctors drop down menu
            selectedDoctor =  StringVar(self.__my_widget, doctorOptions[0])
            doctor_drop = OptionMenu(self.__my_widget, selectedDoctor, *doctorOptions)
            doctor_drop.pack()

            assign_button = tkinter.Button(self.__my_widget, text = "Asssign Patient", command = lambda : self.DoAssignPatient(selectedPatient.get(), selectedDoctor.get()))
            assign_button.pack(side = 'top')

        #if there are no patients
        if patientOptions is None or len(patientOptions) == 0:

            error_label = tkinter.Label(self.__my_widget, text = "No Unassigned Patients")
            error_label.pack(side = 'top')

        #if there are no doctors
        if doctorOptions is None or len(doctorOptions) == 0:

            error_label = tkinter.Label(self.__my_widget, text = "No Doctors")
            error_label.pack(side = 'top')

        return_to_manage_patients_button = tkinter.Button(self.__my_widget, text = "Return To Manage Patients", command = lambda : self.ManagePatients())
        return_to_manage_patients_button.pack(side = 'top')

        tkinter.mainloop()

    def DoAssignPatient(self, patient, doctor):

        self.__admin.AssignPatient(patient, doctor)
        self.AssignPatient()

    #allows the admin to select a patient to discharge
    def DischargePatient(self):

        self.ClearWidgets()

        discharge_patient_label = tkinter.Label(self.__my_widget, text = "Disharge Patient")
        discharge_patient_label.pack(side = 'top')

        #makes a patients drop down menu
        patientOptions = self.__admin.GetAllPatientUsernames()

        #if there are patients in the system
        if not patientOptions is None and not patientOptions is None:

            selectedPatient =  StringVar(self.__my_widget, patientOptions[0])

            patient_drop = OptionMenu(self.__my_widget, selectedPatient, *patientOptions)
            patient_drop.pack()

            discharge_button = tkinter.Button(self.__my_widget, text = "Discharge", command = lambda : self.DoDischarge(selectedPatient.get()))
            discharge_button.pack(side = 'top')

        else:

            error_label = tkinter.Label(self.__my_widget, text = "No Patients")
            error_label.pack(side = 'top')

        return_to_manage_patients_button = tkinter.Button(self.__my_widget, text = "Return To Manage Patients", command = lambda : self.ClearAndReturnManagePatients())
        return_to_manage_patients_button.pack(side = 'top')

        tkinter.mainloop()

    #discharges the selected patient
    def DoDischarge(self, dischargedPatient):

        self.__admin.DischargePatient(dischargedPatient)
        self.DischargePatient()

    #shows a drop of the treated patients
    def ViewTreatedPatientsList(self):

        self.ClearWidgets()

        view_treated_patients_label = tkinter.Label(self.__my_widget, text = "View Treated Patients")
        view_treated_patients_label.pack(side = 'top')

        #makes a patients drop down menu
        patientOptions = self.__admin.GetAllTreatedPatientUsernames()

        #if there are patients in the system
        if not patientOptions is None and not patientOptions is None:

            selectedPatient =  StringVar(self.__my_widget, patientOptions[0])

            patient_drop = OptionMenu(self.__my_widget, selectedPatient, *patientOptions)
            patient_drop.pack()

            discharge_button = tkinter.Button(self.__my_widget, text = "Select", command = lambda : self.DoViewTreatedPatientRecord(selectedPatient.get()))
            discharge_button.pack(side = 'top')

        else:

            error_label = tkinter.Label(self.__my_widget, text = "No Patients")
            error_label.pack(side = 'top')

        return_to_manage_patients_button = tkinter.Button(self.__my_widget, text = "Return To Manage Patients", command = lambda : self.ManagePatients())
        return_to_manage_patients_button.pack(side = 'top')

    #allows the admin to view treated patients
    def DoViewTreatedPatientRecord(self, patientUsername):

        self.ClearWidgets()
            
        patient = self.__admin.GetTreatedPatientFromUsername(patientUsername)

        patient_record_label = tkinter.Label(self.__my_widget, text = "Treated Patient Record")
        patient_record_label.pack(side = 'top')

        name_label = tkinter.Label(self.__my_widget, text = "Name: {0}".format(patient.GetName()))
        name_label.pack(side = 'top')

        date_of_birth_label = tkinter.Label(self.__my_widget, text = "Date of birth: {0}".format(patient.GetDateOfBirth()))
        date_of_birth_label.pack(side = 'top')

        mobile_label = tkinter.Label(self.__my_widget, text = "Mobile: {0}".format(patient.GetMobile()))
        mobile_label.pack(side = 'top')

        address_label = tkinter.Label(self.__my_widget, text = "Address: {0}".format(patient.GetAddress()))
        address_label.pack(side = 'top')

        symptoms_label = tkinter.Label(self.__my_widget, text = "Symptoms: {0}".format(patient.MakeSymptomsLine()))
        symptoms_label.pack(side = 'top')

        username_label = tkinter.Label(self.__my_widget, text = "Username: {0}".format(patient.GetUsername()))
        username_label.pack(side = 'top')

        go_back_button = tkinter.Button(self.__my_widget, text = "Go Back", command = lambda : self.ViewTreatedPatientsList())
        go_back_button.pack(side = 'top')

        tkinter.mainloop()

    #allows the admin to edit view and create families
    def ManageFamilies(self):

        self.ClearWidgets()

        manage_families_label = tkinter.Label(self.__my_widget, text = "Manage Families")
        manage_families_label.pack(side = 'top')

        view_families_button = tkinter.Button(self.__my_widget, text = "View Family", command = lambda : self.ViewFamily())
        view_families_button.pack(side = 'top')

        create_family_button = tkinter.Button(self.__my_widget, text = "Create New Family", command = lambda : self.CreateFamily())
        create_family_button.pack(side = 'top')

        return_to_dashboard_button = tkinter.Button(self.__my_widget, text = "Return To Dashboard", command = lambda : self.ClearAndReturn())
        return_to_dashboard_button.pack(side = 'top')

    def ViewFamily(self):

        self.ClearWidgets()

        familyOptions = self.__admin.GetAllFamilyNames()

        #if there are families in the system
        if not familyOptions is None and not familyOptions is None:

            selectedFamily =  StringVar(self.__my_widget, familyOptions[0])

            family_drop = OptionMenu(self.__my_widget, selectedFamily, *familyOptions)
            family_drop.pack()

            discharge_button = tkinter.Button(self.__my_widget, text = "Select", command = lambda : self.DoViewFamily(selectedFamily.get()))
            discharge_button.pack(side = 'top')

        else:

            error_label = tkinter.Label(self.__my_widget, text = "No Families")
            error_label.pack(side = 'top')

        return_to_manage_families_button = tkinter.Button(self.__my_widget, text = "Return To Manage Families", command = lambda : self.ClearAndReturnManageFamilies())
        return_to_manage_families_button.pack(side = 'top')

    def DoViewFamily(self, familyName):

        self.ClearWidgets()
        self.SaveAll()

        family = self.__admin.GetFamilyFromFamilyName(familyName)

        family_name_label = tkinter.Label(self.__my_widget, text = "Family Name: {0}".format(family.GetName()))
        family_name_label.pack(side = 'top')

        patients_label = tkinter.Label(self.__my_widget, text = "Patients: {0}".format(family.MakePatientsLine()))
        patients_label.pack(side = 'top')

        if len(family.GetAllPatientsInFamily()) > 0 and not family.GetAllPatientsInFamily() is None:

            remove_patient_button = tkinter.Button(self.__my_widget, text = "Remove Patient", command = lambda : self.RemovePatient(family))
            remove_patient_button.pack(side = 'top')

        add_patient_button = tkinter.Button(self.__my_widget, text = "Add Patient", command = lambda : self.AddPatient(family))
        add_patient_button.pack(side = 'top')

        go_back_button = tkinter.Button(self.__my_widget, text = "Go Back", command = lambda : self.ViewFamily())
        go_back_button.pack(side = 'top')

    def AddPatient(self, family):

        self.ClearWidgets()

        family_name_label = tkinter.Label(self.__my_widget, text = "Family Name: {0}".format(family.GetName()))
        family_name_label.pack(side = 'top')

        patients_label = tkinter.Label(self.__my_widget, text = "Patients: {0}".format(family.MakePatientsLine()))
        patients_label.pack(side = 'top')

        patientOptions = self.__admin.GetAllPatientUsernames()

        #if there are patients in the system
        if not patientOptions is None and not patientOptions is None:

            selectedPatient =  StringVar(self.__my_widget, patientOptions[0])

            patient_drop = OptionMenu(self.__my_widget, selectedPatient, *patientOptions)
            patient_drop.pack()

            add_patient_button = tkinter.Button(self.__my_widget, text = "Add Patient", command = lambda : self.DoAddPatient(selectedPatient.get(), family.GetName()))
            add_patient_button.pack(side = 'top')

        else:

            error_label = tkinter.Label(self.__my_widget, text = "No Patients")
            error_label.pack(side = 'top')

        go_back_button = tkinter.Button(self.__my_widget, text = "Go Back", command = lambda : self.DoViewFamily(family.GetName()))
        go_back_button.pack(side = 'top')

    def DoAddPatient(self, patientUsername, familyName):

        self.__admin.AddPatientToFamily(patientUsername, familyName)
        self.__admin.Save()
        self.AddPatient(self.__admin.GetFamilyFromFamilyName(familyName))

    def RemovePatient(self, family):

        self.ClearWidgets()

        patientOptions = family.GetAllPatientsInFamily()
        
        selectedPatient =  StringVar(self.__my_widget, patientOptions[0])

        patient_drop = OptionMenu(self.__my_widget, selectedPatient, *patientOptions)
        patient_drop.pack()

        add_patient_button = tkinter.Button(self.__my_widget, text = "Remove Patient", command = lambda : self.DoRemovePatient(selectedPatient.get(), family.GetName()))
        add_patient_button.pack(side = 'top')

        go_back_button = tkinter.Button(self.__my_widget, text = "Go Back", command = lambda : self.DoViewFamily(family.GetName()))
        go_back_button.pack(side = 'top')

    def DoRemovePatient(self, patientUsername, familyName):

        self.__admin.RemovePatient(patientUsername, familyName)
        self.__admin.Save()
        self.RemovePatient(self.__admin.GetFamilyFromFamilyName(familyName))

    def CreateFamily(self):

        self.ClearWidgets()

        create_family_label = tkinter.Label(self.__my_widget, text = "Create Familly")
        create_family_label.pack(side = 'top')

        family_name_label = tkinter.Label(self.__my_widget, text = "Family Name:")
        family_name_label.pack(side = 'top')

        new_name_entry = tkinter.Entry(self.__my_widget, width = 20)
        new_name_entry.pack(side = 'top')

        create_button = tkinter.Button(self.__my_widget, text = "Create", command = lambda : self.DoCreateFamily(new_name_entry.get()))
        create_button.pack(side = 'top')

    def DoCreateFamily(self, familyName):

        names = self.__admin.GetAllFamilyNames()

        if not familyName in names:
            
            self.__admin.CreateFamily(familyName)
            self.ClearAndReturnManageFamilies()

        repeated_family_name_label = tkinter.Label(self.__my_widget, text = "Family Name Already Exists")
        repeated_family_name_label.pack(side = 'top')

    #allows the admin to change their name or address
    def UpdateOwnInfomation(self):

        self.ClearWidgets()

        update_own_infomation_label = tkinter.Label(self.__my_widget, text = "Update Own Infomation")
        update_own_infomation_label.pack(side = 'top')

        update_name_label = tkinter.Label(self.__my_widget, text = "Current Name: {0}".format(self.__admin.GetName()))
        update_name_label.pack(side = 'top')

        new_name_entry = tkinter.Entry(self.__my_widget, width = 20)
        new_name_entry.pack(side = 'top')

        update_name_button = tkinter.Button(self.__my_widget, text = "Update Name", command = lambda : self.UpdateName(new_name_entry.get()))
        update_name_button.pack(side = 'top')

        update_address_label = tkinter.Label(self.__my_widget, text = "Current Address: {0}".format(self.__admin.GetAddress()))
        update_address_label.pack(side = 'top')

        new_address_entry = tkinter.Entry(self.__my_widget, width = 20)
        new_address_entry.pack(side = 'top')

        update_address_button = tkinter.Button(self.__my_widget, text = "Update Address", command = lambda : self.__admin.SetAddress(new_address_entry.get()))
        update_address_button.pack(side = 'top')

        return_to_dashboard_button = tkinter.Button(self.__my_widget, text = "Return To Dashboard", command = lambda : self.ClearAndReturn())
        return_to_dashboard_button.pack(side = 'top')

        tkinter.mainloop()

    #udates the namme
    def UpdateName(self, name):

        self.__admin.SetName(name)
        self.UpdateOwnInfomation()

    #udates the adress
    def UpdateAdress(self, address):

        self.__admin.SetName(address)
        self.UpdateOwnInfomation()

    def RequestManagementReport(self):

        self.ClearWidgets()

        management_report_label = tkinter.Label(self.__my_widget, text = "Management Report")
        management_report_label.pack(side = 'top')

        #outputs the number of doctors
        number_of_doctors_label = tkinter.Label(self.__my_widget, text = "Number Of Doctors: {0}".format(str(len(self.__admin.GetAllDoctorUsernames()))))
        number_of_doctors_label.pack(side = 'top')

        #outputs the number of patients
        number_of_patients_label = tkinter.Label(self.__my_widget, text = "Number Of Patients: {0}".format(str(len(self.__admin.GetAllPatientUsernames()))))
        number_of_patients_label.pack(side = 'top')

        #outputs the number of applied patients
        number_of_applied_patients_label = tkinter.Label(self.__my_widget, text = "Number Of Applied Patients: {0}".format(str(len(self.__admin.GetAllAppliedPatientUsernames()))))
        number_of_applied_patients_label.pack(side = 'top')

        #outputs the number of treated patients
        number_of_treated_patients_label = tkinter.Label(self.__my_widget, text = "Number Of Treated Patients: {0}".format(str(len(self.__admin.GetAllTreatedPatientUsernames()))))
        number_of_treated_patients_label.pack(side = 'top')

        #outputs the total number of patients
        total_number_of_patients_label = tkinter.Label(self.__my_widget, text = "Total Number Of Patients: {0}".format(str(len(self.__admin.GetAllTreatedPatientUsernames()) + len(self.__admin.GetAllAppliedPatientUsernames()) + len(self.__admin.GetAllPatientUsernames()))))
        total_number_of_patients_label.pack(side = 'top')

        doctors = self.__admin.GetAllDoctorUsernames()

        for doctor in doctors:

            #outputs the total number of patients
            patients_per_doctor_label = tkinter.Label(self.__my_widget, text = "{0} : {1} Patients".format(doctor, self.__admin.GetPatientsPerDoctor(doctor)))
            patients_per_doctor_label.pack(side = 'top')

        symptoms = self.__admin.GetSymptomNames()

        for symptom in symptoms:
    
            #outputs the total number of patients
            patients_per_doctor_label = tkinter.Label(self.__my_widget, text = "{0} : {1} Patients".format(symptom, self.__admin.GetSymptomFrequency(symptom)))
            patients_per_doctor_label.pack(side = 'top')

        return_to_dashboard_button = tkinter.Button(self.__my_widget, text = "Return To Dashboard", command = lambda : self.ClearAndReturn())
        return_to_dashboard_button.pack(side = 'top')

        tkinter.mainloop()

    #displays an error if the entered username already exists
    def RepeatedDoctorUsername(self):

        error_label = tkinter.Label(self.__my_widget, text = "This Usename Already Exists")
        error_label.pack(side = 'top')

        #figure out cammand or make them all separately whoop whoop
        #go_back_button = tkinter.Button(self.__my_widget, text = "Go Back", command = lambda : self.RegisterDoctor())
        #go_back_button.pack(side = 'top')

        tkinter.mainloop()

    #clears previous widgets from the window
    def ClearWidgets(self):

        self.__my_widget.destroy()
        self.__my_widget = tkinter.Tk()

        self.__my_widget.geometry("1000x700")

    def ClearAndReturnManageDoctors(self):

        self.ClearWidgets()
        self.SaveAll()
        self.ManageDoctors()

    def ClearAndReturnManagePatients(self):

        self.ClearWidgets()
        self.SaveAll()
        self.ManagePatients()

    def ClearAndReturnManageAppointments(self):

        self.ClearWidgets()
        self.SaveAll()
        self.ManageAppointments()

    def ClearAndReturnManageFamilies(self):

        self.ClearWidgets()
        self.SaveAll()
        self.ManageFamilies()

    #clears and returns to the dashboard
    def ClearAndReturn(self):

        self.ClearWidgets()
        self.SaveAll()
        self.DashBoard()

    #saves to files then quits the program
    def Quit(self):

        self.SaveAll()
        sys.exit()

#################################################################################################################
# DoctorGUI
#################################################################################################################

class DoctorGUI(object):

    def __init__(self, doctor, widget):

        self.__my_widget = widget
        self.__doctor = doctor

    def Load(self):
        
        self.DashBoard()

    #displays the doctors dashboard
    def DashBoard(self):

        self.ClearWidgets()

        doctor_dashboard_label = tkinter.Label(self.__my_widget, text = "Doctor Dashboard: {0}".format(self.__doctor.GetName()))
        doctor_dashboard_label.pack(side = 'top')

        view_patient_records_button = tkinter.Button(self.__my_widget, text = "View Patient Records", command = lambda : self.ViewPatientRecords())
        view_patient_records_button.pack(side = 'top')

        view_appointments_button = tkinter.Button(self.__my_widget, text = "View Appointments", command = lambda : self.ViewAppointments())
        view_appointments_button.pack(side = 'top')

        change_password_button = tkinter.Button(self.__my_widget, text = "Change Password", command = lambda : self.ChangePassword())
        change_password_button.pack(side = 'top')

        quit_button = tkinter.Button(self.__my_widget, text = "Quit", command = lambda : self.SaveAndExit())
        quit_button.pack(side = 'top')

        tkinter.mainloop()

    def SaveAndExit(self):

        self.__doctor.Save()
        sys.exit()

    #allows the doctor to view the records of the patients assigned to them
    def ViewPatientRecords(self):

        self.ClearWidgets()
        
        #makes a patients drop down menu
        patientOptions = self.__doctor.GetAllPatientUsernames()

        if not patientOptions is None and len(patientOptions) > 0:

            selectedPatient =  StringVar(self.__my_widget, patientOptions[0])

            patient_drop = OptionMenu(self.__my_widget, selectedPatient, *patientOptions)
            patient_drop.pack()

            select_patient_button = tkinter.Button(self.__my_widget, text = "Select Patient", command = lambda : self.DoViewPatientRecord(selectedPatient.get()))
            select_patient_button.pack(side = 'top')

        else:

            error_label = tkinter.Label(self.__my_widget, text = "No Assigned Patients")
            error_label.pack(side = 'top')

        return_to_dashboard_button = tkinter.Button(self.__my_widget, text = "Return To Dashboard", command = lambda : self.DashBoard())
        return_to_dashboard_button.pack(side = 'top')

        tkinter.mainloop()

    #shows the selected patients records
    def DoViewPatientRecord(self, patientUsername):

        self.ClearWidgets()

        patient = self.__doctor.GetPatientFromUsername(patientUsername)

        patient_record_label = tkinter.Label(self.__my_widget, text = "Patient Record")
        patient_record_label.pack(side = 'top')

        name_label = tkinter.Label(self.__my_widget, text = "Name: {0}".format(patient.GetName()))
        name_label.pack(side = 'top')
        
        username_label = tkinter.Label(self.__my_widget, text = "Username: {0}".format(patient.GetUsername()))
        username_label.pack(side = 'top')

        date_of_birth_label = tkinter.Label(self.__my_widget, text = "Date of birth: {0}".format(patient.GetDateOfBirth()))
        date_of_birth_label.pack(side = 'top')

        mobile_label = tkinter.Label(self.__my_widget, text = "Mobile: {0}".format(patient.GetMobile()))
        mobile_label.pack(side = 'top')

        address_label = tkinter.Label(self.__my_widget, text = "Address: {0}".format(patient.GetAddress()))
        address_label.pack(side = 'top')

        symptoms_label = tkinter.Label(self.__my_widget, text = "Symptoms: {0}".format(patient.MakeSymptomsLine()))
        symptoms_label.pack(side = 'top')

        add_symptom_button = tkinter.Button(self.__my_widget, text = "Add Symptom", command = lambda : self.AddSymptom(patient))
        add_symptom_button.pack(side = 'top')

        if len(patient.GetSymptoms()) > 0:
          
            remove_symptom_button = tkinter.Button(self.__my_widget, text = "Remove Symptom", command = lambda : self.RemoveSymptom(patient))
            remove_symptom_button.pack(side = 'top')

        return_to_dashboard_button = tkinter.Button(self.__my_widget, text = "Return To Dashboard", command = lambda : self.DashBoard())
        return_to_dashboard_button.pack(side = 'top')

        tkinter.mainloop()

    #where the doctor adds the symptom
    def AddSymptom(self, patient):

        self.ClearWidgets()

        symptoms_label = tkinter.Label(self.__my_widget, text = "Symptoms: {0}".format(patient.MakeSymptomsLine()))
        symptoms_label.pack(side = 'top')

        symptomOptions = self.__doctor.LoadSymptoms()

        if not symptomOptions is None and len(symptomOptions) > 0:

            selectedSymptom =  StringVar(self.__my_widget, symptomOptions[0])

            symptom_drop = OptionMenu(self.__my_widget, selectedSymptom, *symptomOptions)
            symptom_drop.pack()

            add_symptom_button = tkinter.Button(self.__my_widget, text = "Add Symptom", command = lambda : self.DoAddSymptom(patient, selectedSymptom.get()))
            add_symptom_button.pack(side = 'top')

        else:

            error_label = tkinter.Label(self.__my_widget, text = "No Symptoms Loaded Check Files")
            error_label.pack(side = 'top')

        go_back_button = tkinter.Button(self.__my_widget, text = "Go Back", command = lambda : self.DoViewPatientRecord(patient.GetUsername()))
        go_back_button.pack(side = 'top')

        tkinter.mainloop()

    #adds the symptom to the patient
    def DoAddSymptom(self, patient, symptom):

        patient.AddSymptom(symptom)
        self.AddSymptom(patient)

    #selects a symptom to be removed from the patient
    def RemoveSymptom(self,patient):

        symptomOptions = patient.GetSymptoms()

        selectedSymptom = StringVar(self.__my_widget, symptomOptions[0])
        symptom_drop = OptionMenu(self.__my_widget, selectedSymptom, *symptomOptions)
        symptom_drop.pack()

        remove_symptom_button = tkinter.Button(self.__my_widget, text = "Remove Symptom", command = lambda : self.DoRemoveSymptom(patient, selectedSymptom.get()))
        remove_symptom_button.pack(side = 'top')

    #actually removes the symptom
    def DoRemoveSymptom(self, patient, symptom):

        patient.RemoveSymptom(symptom)
        self.ViewPatientRecords()

    def ViewAppointments(self):

        self.ClearWidgets()

        appointmentOptions = self.__doctor.GetAppointmentIds()

        if not appointmentOptions is None and len(appointmentOptions) > 0:

            selectedAppointment = StringVar(self.__my_widget, appointmentOptions[0])
            appointments_drop = OptionMenu(self.__my_widget, selectedAppointment, *appointmentOptions)
            appointments_drop.pack()

            view_appointment_button = tkinter.Button(self.__my_widget, text = "View Appointment", command = lambda : self.DoViewAppointment(selectedAppointment.get()))
            view_appointment_button.pack(side = 'top')

        else:

            error_label = tkinter.Label(self.__my_widget, text = "No Appointments")
            error_label.pack(side = 'top')

        go_back_button = tkinter.Button(self.__my_widget, text = "Go Back", command = lambda : self.DashBoard())
        go_back_button.pack(side = 'top')

    def DoViewAppointment(self, appointmentID):

        self.ClearWidgets()

        appointment = self.__doctor.GetAppointmentFromID(appointmentID)

        appointment_id_label = tkinter.Label(self.__my_widget, text = "Appointment Id: {0}".format(appointment.GetID()))
        appointment_id_label.pack(side = 'top')
        
        appointment_status_label = tkinter.Label(self.__my_widget, text = "Appointment Status: {0}".format(appointment.GetStatus()))
        appointment_status_label.pack(side = 'top')

        appointment_patient_label = tkinter.Label(self.__my_widget, text = "Appointment Patient: {0}".format(appointment.GetDoctor()))
        appointment_patient_label.pack(side = 'top')

        appointment_dateTime_label = tkinter.Label(self.__my_widget, text = "Appointment Date Time: {0}".format(appointment.GetDateTime()))
        appointment_dateTime_label.pack(side = 'top')

        go_back_button = tkinter.Button(self.__my_widget, text = "Go Back", command = lambda : self.ViewAppointments())
        go_back_button.pack(side = 'top')

    #allows the doctor to change their password
    def ChangePassword(self):

        self.ClearWidgets()

        new_password_label = tkinter.Label(self.__my_widget, text = "New Password: ")
        new_password_label.pack(side = 'top')

        new_password_entry = tkinter.Entry(self.__my_widget, width = 20)
        new_password_entry.pack(side = 'top')

        update_password_button = tkinter.Button(self.__my_widget, text = "Update Password", command = lambda : self.DoChangePassword(new_password_entry.get()))
        update_password_button.pack(side = 'top')

        return_to_dashboard_button = tkinter.Button(self.__my_widget, text = "Return To Dashboard", command = lambda : self.DashBoard())
        return_to_dashboard_button.pack(side = 'top')

        tkinter.mainloop()

    #checks to ensure that the new password is at least 8 characters long and contains uppercas lowercase and digits
    def DoChangePassword(self, newPassword):

        valid = True

        if not len(newPassword) > 8:

            wrong_length_label = tkinter.Label(self.__my_widget, text = "Password Must Be At Leat 8 Characters Long")
            wrong_length_label.pack(side = 'top')
            valid = False

        containsUpper = False
        containsLower = False
        containsNumber = False

        for letter in newPassword:

            if letter.isupper():

                containsUpper = True

            if letter.islower():

                containsLower = True

            if letter.isdigit():

                containsNumber = True

        if containsLower == False:

            no_lower_label = tkinter.Label(self.__my_widget, text = "Password Must Contain At Least One Lowercase Character")
            no_lower_label.pack(side = 'top')
            valid = False

        if containsUpper == False:

            no_upper_label = tkinter.Label(self.__my_widget, text = "Password Must Contain At Least One Uppercase Character")
            no_upper_label.pack(side = 'top')
            valid = False
        
        if containsNumber == False:

            no_number_label = tkinter.Label(self.__my_widget, text = "Password Must Contain At Least One Digit")
            no_number_label.pack(side = 'top')
            valid = False

        #sets the new password
        if valid == True:

            self.__doctor.SetPassword(newPassword)
            sucess_label = tkinter.Label(self.__my_widget, text = "You Have Sucessfully Changed Your Password")
            sucess_label.pack(side = 'top')

            self.__doctor.SetPassword(newPassword)

        tkinter.mainloop()

    #clears previous widgets from the window
    def ClearWidgets(self):

        self.__my_widget.destroy()
        self.__my_widget = tkinter.Tk()
        self.__my_widget.geometry("1000x700")

#################################################################################################################
# PatientGUI
#################################################################################################################

class PatientGUI(object):

    def __init__(self, patient, widget):

        self.__my_widget = widget
        self.__patient = patient

    #displays the patients dashboard
    def DashBoard(self):

        self.ClearWidgets()

        patient_dashboard_label = tkinter.Label(self.__my_widget, text = "Patient Dashboard")
        patient_dashboard_label.pack(side = 'top')

        patientDoctor = self.__patient.GetDoctor()

        assigned_doctor_label = tkinter.Label(self.__my_widget, text = "Assigned Doctor: {0}".format(patientDoctor.GetUsername()))
        assigned_doctor_label.pack(side = 'top')
        
        #only allows patients to book an appointment if they have an assigned doctor
        if  not (patientDoctor == "No Assigned Doctor"):
            
            book_appointment_button = tkinter.Button(self.__my_widget, text = "Book Appointment", command = lambda : self.BookAppointment(patientDoctor))
            book_appointment_button.pack(side = 'top')

            view_appointments_button = tkinter.Button(self.__my_widget, text = "View Appointments", command = lambda : self.ViewAppointments())
            view_appointments_button.pack(side = 'top')

        if patientDoctor == "No Assigned Doctor": 

            no_assigned_doctor_label = tkinter.Label(self.__my_widget, text = "Wait To Be Assigned A Doctor Before Booking An Appointment")
            no_assigned_doctor_label.pack(side = 'top')

        change_password_button = tkinter.Button(self.__my_widget, text = "Change Password", command = lambda : self.ChangePassword())
        change_password_button.pack(side = 'top')

        quit_button = tkinter.Button(self.__my_widget, text = "Quit", command = lambda : sys.exit())
        quit_button.pack(side = 'top')

        tkinter.mainloop()

    #allows the patient to book an appointment
    def BookAppointment(self, doctor):

        self.ClearWidgets()

        book_appointment_label = tkinter.Label(self.__my_widget, text = "Book An Appointment")
        book_appointment_label.pack(side = 'top')

        appointmentDateTimeOptions = doctor.GetAllAppointmentSlots()

        selectedSlot = StringVar(self.__my_widget, appointmentDateTimeOptions[0])
        appointment_slot_drop = OptionMenu(self.__my_widget, selectedSlot, *appointmentDateTimeOptions)
        appointment_slot_drop.pack()

        appointment_notes_label = tkinter.Label(self.__my_widget, text = "Appointment Notes:")
        appointment_notes_label.pack(side = 'top')

        note_entry = tkinter.Entry(self.__my_widget, width = 20)
        note_entry.pack(side = 'top')

        book_appointment_button = tkinter.Button(self.__my_widget, text = "Book Appointment", command = lambda : self.DoBookAppointment(doctor, selectedSlot.get(), note_entry.get()))
        book_appointment_button.pack(side = 'top')

        return_to_dashboard_button = tkinter.Button(self.__my_widget, text = "Return To Dashboard", command = lambda : self.DashBoard())
        return_to_dashboard_button.pack(side = 'top')

    def DoBookAppointment(self, doctor, time, note):

        self.__patient.AddAppointment(doctor.GetUsername(), self.__patient.GetUsername() , time, note)
        self.DashBoard()

    def ViewAppointments(self):

        self.ClearWidgets()

        appointmentOptions = self.__patient.GetAppointmentIds()

        if not appointmentOptions is None and len(appointmentOptions) > 0:

            selectedAppointment = StringVar(self.__my_widget, appointmentOptions[0])
            appointments_drop = OptionMenu(self.__my_widget, selectedAppointment, *appointmentOptions)
            appointments_drop.pack()

            view_appointment_button = tkinter.Button(self.__my_widget, text = "View Appointment", command = lambda : self.DoViewAppointment(selectedAppointment.get()))
            view_appointment_button.pack(side = 'top')

        else:

            error_label = tkinter.Label(self.__my_widget, text = "No Appointments")
            error_label.pack(side = 'top')

        go_back_button = tkinter.Button(self.__my_widget, text = "Go Back", command = lambda : self.DashBoard())
        go_back_button.pack(side = 'top')

    def DoViewAppointment(self, appointmentID):

        self.ClearWidgets()

        appointment = self.__patient.GetAppointmentFromID(appointmentID)

        appointment_id_label = tkinter.Label(self.__my_widget, text = "Appointment Id: {0}".format(appointment.GetID()))
        appointment_id_label.pack(side = 'top')
        
        appointment_status_label = tkinter.Label(self.__my_widget, text = "Appointment Status: {0}".format(appointment.GetStatus()))
        appointment_status_label.pack(side = 'top')

        appointment_doctor_label = tkinter.Label(self.__my_widget, text = "Appointment Doctor: {0}".format(appointment.GetDoctor()))
        appointment_doctor_label.pack(side = 'top')

        appointment_dateTime_label = tkinter.Label(self.__my_widget, text = "Appointment Date Time: {0}".format(appointment.GetDateTime()))
        appointment_dateTime_label.pack(side = 'top')

        go_back_button = tkinter.Button(self.__my_widget, text = "Go Back", command = lambda : self.ViewAppointments())
        go_back_button.pack(side = 'top')

    #allows the patient to change their password
    def ChangePassword(self):

        self.ClearWidgets()

        new_password_label = tkinter.Label(self.__my_widget, text = "New Password: ")
        new_password_label.pack(side = 'top')

        new_password_entry = tkinter.Entry(self.__my_widget, width = 20)
        new_password_entry.pack(side = 'top')

        update_password_button = tkinter.Button(self.__my_widget, text = "Update Password", command = lambda : self.DoChangePassword(new_password_entry.get()))
        update_password_button.pack(side = 'top')

        return_to_dashboard_button = tkinter.Button(self.__my_widget, text = "Return To Dashboard", command = lambda : self.DashBoard())
        return_to_dashboard_button.pack(side = 'top')

        tkinter.mainloop()

    #checks to ensure that the new password is at least 8 characters long and contains uppercas lowercase and digits
    def DoChangePassword(self, newPassword):

        valid = True

        if not len(newPassword) >= 8:

            wrong_length_label = tkinter.Label(self.__my_widget, text = "Password Must Be At Leat 8 Characters Long")
            wrong_length_label.pack(side = 'top')
            valid = False

        containsUpper = False
        containsLower = False
        containsNumber = False

        for letter in newPassword:

            if letter.isupper():

                containsUpper = True

            if letter.islower():

                containsLower = True

            if letter.isdigit():

                containsNumber = True

        if containsLower == False:

            no_lower_label = tkinter.Label(self.__my_widget, text = "Password Must Contain At Least One Lowercase Character")
            no_lower_label.pack(side = 'top')
            valid = False

        if containsUpper == False:

            no_upper_label = tkinter.Label(self.__my_widget, text = "Password Must Contain At Least One Uppercase Character")
            no_upper_label.pack(side = 'top')
            valid = False
        
        if containsNumber == False:

            no_number_label = tkinter.Label(self.__my_widget, text = "Password Must Contain At Least One Digit")
            no_number_label.pack(side = 'top')
            valid = False

        #sets the new password
        if valid == True:

            self.__patient.SetPassword(newPassword)
            sucess_label = tkinter.Label(self.__my_widget, text = "You Have Sucessfully Changed Your Password")
            sucess_label.pack(side = 'top')

            self.__patient.SetPassword(newPassword)

            #save to file FIX

        tkinter.mainloop()

    #clears previous widgets from the window
    def ClearWidgets(self):

        self.__my_widget.destroy()
        self.__my_widget = tkinter.Tk()
        self.__my_widget.geometry("1000x700")
