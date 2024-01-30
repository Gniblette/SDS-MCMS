from datetime import datetime
from datetime import date, timedelta
import random
import string

#################################################################################################################
# Patient
#################################################################################################################

class Patient:

    def __init__(self, username, password, name, dateOfBirth, mobile, address):

        self.__name = name
        self.__dateOfBirth = dateOfBirth
        self.__symptoms = []
        self.__mobile = mobile
        self.__address = address
        self.__appointments = []
        self.__username = username
        self.__password = password
        self.__doctor = Doctor
        self.__family = Family

    #converts the patients infomation into a line for the text file
    def MakeLine(self) -> list:

        line = list()
        line.append(self.__username)
        line.append(self.__password)
        line.append(self.__name)
        line.append(self.__dateOfBirth.strftime("%d-%m-%Y"))
        line.append(self.__mobile)
        line.append(self.__address)

        if len(self.__symptoms) > 0 and not self.__symptoms is None:

            symptoms = []

            for symptom in self.__symptoms:

                symptoms.append(symptom)

            #joins the patients with ; and adds it to the line
            separator = ';'
            symptomsAsString = separator.join(symptoms)
            line.append(symptomsAsString)

        return line
    
    #turns the list of symptoms into a format to be displayed
    def MakeSymptomsLine(self) -> string:

        NO_SYMPTOMS_MESSAGE = "No Symptoms"

        line = ""

        for symptom in self.__symptoms:

            line = line + symptom + ", "

        line = line[:-2]

        if line == '':

            return NO_SYMPTOMS_MESSAGE

        return line
    
    def AddAppointment(self, doctorUsername, patientUsername, dateTime, note):

        status = "pending"
        appointments = AppointmentList()
        appointments.Load()
        patientAppointment = appointments.AddNewAppointment(status, dateTime, doctorUsername, patientUsername, note) 
        appointments.Save()
        self.__appointments.append(patientAppointment)

    def GetAppointmentFromID(self, id):

        for appointment in self.__appointments:

            if appointment.GetID() == id:

                return appointment

    def AddCompleteAppointment(self,appointment):

        self.__appointments.append(appointment)
    
    #adds asymptom to a patient
    def AddSymptom(self, symptom):

        self.__symptoms.append(symptom)

    #removes a symptom from a patient
    def RemoveSymptom(self, symptom):

        self.__symptoms.remove(symptom)

    #gets the patients name
    def GetName(self) -> string:

        return self.__name

    #gets the patients age
    def GetDateOfBirth(self) -> datetime:

        return self.__dateOfBirth

    #gets the patients mobile
    def GetMobile(self) -> string:

        return self.__mobile

    #gets the patients address
    def GetAddress(self) -> string:

        return self.__address

    #gets the patients symptons
    def GetSymptoms(self) -> list:

        return self.__symptoms

    #gets the patients username
    def GetUsername(self) -> string:

        return self.__username
    
    def GetPassword(self) -> string:

        return self.__password
    
    #sets the patients password
    def SetPassword(self, password):

        self.__password = password

    #sets the doctor of the patient
    def SetDoctor(self, doctor):

        self.__doctor = doctor

    def SetFamily(self, family):

        self.__family = family

    def SetAppointment(self, appointment):

        self.__appointments.append(appointment)

    def GetAppointment(self):

        return self.__appointments

    def GetDoctor(self):

        if not self.__doctor is None:

            return self.__doctor
        
        else:

            return "No Assigned Doctor"
    
    def GetAppointmentFromId(self, Id):

        for appointment in self.__appointments:

            if appointment.GetID() == Id:

                return appointment
            
    def GetAppointmentIds(self):

        ids =[]

        for appointment in self.__appointments:

            ids.append(appointment.GetID())

        return ids

#################################################################################################################
# Doctor
#################################################################################################################

class Doctor:

    SYMPTOMS_FILE = "Symptoms.txt"
    PATIENT_FILE = "Patients.txt"

    def __init__(self, username, password, name):

        self.__name = name
        self.__patients = []
        self.__appointments  = []
        self.__username = username
        self.__password = password
        self.__allPatients = PatientList(self.PATIENT_FILE)

    #adds a patient to the doctors patient list
    def AddPatient(self , patient):

        self.__patients.append(patient)

    #takes the doctors infomation and puts it into a line to be stored
    def MakeLine(self) -> list:

        line = list()
        line.append(self.__username)
        line.append(self.__password)
        line.append(self.__name)   

        if len(self.__patients) > 0:

            patientsUsernames = []

            #makes a list of the doctors patients usernames
            for patient in self.__patients:

                patientsUsernames.append(patient.GetUsername())

            #joins the patients with ; and adds it to the line
            separator = ';'
            patientUsernamesAsString = separator.join(patientsUsernames)
            line.append(patientUsernamesAsString)

        return line
    
    #formats the patients line for display
    def MakePatientsLine(self) -> list:

        line = ""

        for patient in self.__patients:

            line = line + patient.GetUsername() + ", "

        line = line[:-2]

        return line
    
    #removes a patient with a specific username
    def RemovePatient(self, patientUsername):

        for patient in self.__patients:

            if patient.GetUsername() == patientUsername:

                self.__patients.remove(patient)

    #gets a patient from its username
    def GetPatientFromUsername(self, patientUsername) -> Patient:

        for patient in self.__patients:

            if patient.GetUsername() == patientUsername:

                return patient
            
    #returns all the usernames of theh patients assigned to the doctor
    def GetAllPatientUsernames(self) -> list:

        patients = []

        for patient in self.__patients:

            patients.append(patient.GetUsername())

        return patients
    
    #loads in the list of possible symptoms from the file
    def LoadSymptoms(self) -> list:

        fileLoader = FileLoader()
        listSymptoms =  fileLoader.ReadFile(self.SYMPTOMS_FILE)    

        symptoms = []

        for item in listSymptoms:

            symptoms.append(item[0])

        return symptoms
    
    #saves the changes that the doctor makes
    def Save(self):

        self.__allPatients.Load()

        allPatients = self.__allPatients.GetPatients()
        
        patients = []

        for patient in allPatients:

            found = False

            for doctorPatient in self.__patients:

                if doctorPatient.GetUsername() == patient.GetUsername():

                        patients.append(doctorPatient)
                        found = True

            if found == False:

                patients.append(patient)

        self.__allPatients.SetPatients(patients)
        self.__allPatients.Save()

    def GetAvailableAppointments(self):

        allAppointmentSlots = self.GetAllAppointmentSlots()

        appointments = AppointmentList()
        appointments.Load()
        #gets the times the doctor already has an appointment
        dateTimes = appointments.GetAllDateTimesOfDoctor(self.__username)

        for slot in allAppointmentSlots:

            if slot in dateTimes:

                allAppointmentSlots.remove(slot)

        return allAppointmentSlots
    
    def GetAppointmentFromID(self, id):

        for appointment in self.__appointments:

            if appointment.GetID() == id:

                return appointment
            
    def GetAppointmentFromId(self, Id):

        for appointment in self.__appointments:

            if appointment.GetID() == Id:

                return appointment
            
    def GetAppointmentIds(self):

        ids =[]

        for appointment in self.__appointments:

            ids.append(appointment.GetID())

    def AddCompleteAppointment(self,appointment):

        self.__appointments.append(appointment)

    def GetAllAppointmentSlots(self) -> list:

        slots = []

        previousDay = datetime.today()
        previousDay = previousDay.replace(hour = 0, minute = 0,second = 0, microsecond = 0)

        timeSlotLength = timedelta(hours = 1)

        for i in range (1, 10):

            nextDay = previousDay + timedelta(days = 1)

            timeChange = timedelta(hours = 10)

            for i in range (1,7):

                timeSlot = nextDay + timeChange
                timeSlot = timeSlot.isoformat()
                slots.append(timeSlot)
                timeChange = timeChange + timeSlotLength

        return slots

    #returns the doctors nane
    def GetName(self) -> string:

        return self.__name

    #changes the doctors name
    def SetName(self, name):

        self.__name = name

    #gets the list of doctors patients
    def GetPatients(self) -> list:

        return self.__patients
    
    #gets a specific patient
    def GetPatient(self):

        pass

    #gets the doctors username
    def GetUsername(self):

        return self.__username
    
    #sets the doctors username
    def SetUsername(self, username):

        self.__username = username

    #sets the doctors password
    def SetPassword(self, password):

        self.__password = password

#################################################################################################################
# Appointment
#################################################################################################################
    
class Appointment:

    def __init__(self, ID, status, dateTime, doctor, patient, note):

        self.__ID = ID 
        self.__status = status
        self.__dateTime = dateTime
        self.__doctorUsername = doctor
        self.__patientUsername = patient
        self.__note = note

    #changes the appointments status
    def ChangeSatus(self, status):

        self.__status = status

    #returns the status of the appointment
    def GetStatus(self) -> string:

        return self.__status

    #sets the date and time of the appointment
    def SetDateTime(self, dateTime):

        self.__dateTime = dateTime

    #returns the date and time of the appointment                                       
    def GetDateTime(self) -> string:                                       

        return self.__dateTime                                       

    #sets the doctor for the appointment                                       
    def SetDoctor(self, doctor):                                       

        self.__doctorUsername = doctor                                       

    #returns the doctor for the appointment
    def GetDoctor(self) -> Doctor:

        return self.__doctorUsername

    #assigns a patient to 
    def SetPatient(self, patient):

        self.__patientUsername = patient

    #returns the patient who has the appointment
    def GetPatient(self) -> Patient:

        return self.__patientUsername
    
    def GetID(self):

        return self.__ID
    
    def GetNote(self):

        return self.__note

    #turns the appointment infomation into a line to be stored
    def MakeLine(self) -> list:

        line = list()
        line.append(self.__ID)
        line.append(self.__status)
        line.append(self.__dateTime)
        line.append(self.__doctorUsername)
        line.append(self.__patientUsername)
        line.append(self.__note)

        return line
    
#################################################################################################################
# Appointment List
#################################################################################################################

class AppointmentList:

    APPOINTMENTS_FILE = "Appointments.txt"

    def __init__(self):

        self.__appointments = []

    #loads the appointments from the file and adds them to the list of patients
    def Load(self):

        #reads file
        fileLoader = FileLoader()
        lines = fileLoader.ReadFile(self.APPOINTMENTS_FILE)

        if len(lines) > 0:

            #adds patients to list
            for item in lines:

                #dateList = []
                #dateList = item[2].split("-")
                #dateTimeOfBirth = date(day = int(dateList[0]), month = int(dateList[1]), year = int(dateList[2]))
            
                                    #Id, staus, datetime, doctor, patient, note
                self.AddAppointment(item[0],item[1],item[2],item[3],item[4],item[5])

    #saves the patient infomation to the file
    def Save(self):

        fileSaver = FileSaver()

        #goes through each appointment
        for appointment in self.__appointments:

            #turns the appointment infomation into a line and adds it to the file
            line = appointment.MakeLine()
            fileSaver.AddLine(line)
       
        #writes to the file
        fileSaver.WriteFile(self.APPOINTMENTS_FILE)

    #adds a new appointment to the appointment 
    def AddNewAppointment(self, status, dateTime, doctor, patient, note) -> Appointment:

        Id = self.GenerateId()

        appointment = Appointment(Id, status, dateTime, doctor, patient, note)
        self.__appointments.append(appointment)
        return appointment
    
    #adds a new appointment to the appointment 
    def AddAppointment(self, Id,  status, dateTime, doctor, patient, note) -> Appointment:

        appointment = Appointment(Id, status, dateTime, doctor, patient, note)
        self.__appointments.append(appointment)
        return appointment
    
    def GenerateId(self):

        #if there are no previous appointments in the system
        if  self.__appointments == None:

            return "1"
        
        else:
            
            return str(len(self.__appointments) + 1)
    
    def GetAppointmentFromPatient(self, patientUsername):

        appointments = []

        for appointment in self.__appointments:

            if appointment.GetPatient() == patientUsername:

                appointments.append(appointment)

        return appointments
    
    def GetAppointmentFromDoctor(self, doctorUsername):

        appointments = []

        for appointment in self.__appointments:

            if appointment.GetDoctor() == doctorUsername:

                appointments.append(appointment)

        return appointments
    
    def GetUnapprovedAppointmentIDs(self) -> list:

        appointmentList = []

        for appointment in self.__appointments:

            if appointment.GetStatus == "pending":

                appointmentList.append(appointment.GetID())

        return appointmentList
    
    def GetAllDateTimesOfDoctor(self, doctorUsername):

        times = []

        for appointment in self.__appointments:

            if appointment.GetUsername() == doctorUsername:

                times.append(appointment.GetDateTime())

        return times
    

#################################################################################################################
# Admin
#################################################################################################################

class Admin:

    ADMIN_FILE = "Admins.txt"
    PATIENT_FILE = "Patients.txt"
    APPLIED_PATIENT_FILE = "AppliedPatients.txt"
    TREATED_PATIENTS_FILE = "TreatedPatients.txt"
    
    def __init__(self, username, password, name, address):

        self.__doctors = DoctorList()
        self.__appointments = AppointmentList()
        self.__patients = PatientList(self.PATIENT_FILE)
        self.__treatedPatients = PatientList(self.TREATED_PATIENTS_FILE)
        self.__appliedPatients = PatientList(self.APPLIED_PATIENT_FILE)
        self.__families = Familylist()
        self.__username = username
        self.__password = password
        self.__name = name
        self.__address = address

    #adds a doctor to the list of doctors
    def RegisterDoctor(self, username, name):

        #self.__doctors.Load()

        password = self.GeneratePassword()
     
        self.__doctors.AddDoctor(username, password, name)

        #self.__doctors.Save()

    #returns a list of all the usernames in the system
    def GetAllUsernames(self) -> list:

        usernames = []

        #patient usernames
        usernames = self.__patients.GetAllPatientUsernames()

        #doctor usernames
        usernames = usernames + self.__doctors.GetAllDoctorUsernames()

        #applied patient usernames
        usernames = usernames + self.__appliedPatients.GetAllPatientUsernames()

        #treated patient usernames
        usernames = usernames + self.__treatedPatients.GetAllPatientUsernames()

        #admin usernames
        usernames.append(self.__username)

        return usernames
    
    #returns all the patient usernames
    def GetAllPatientUsernames(self) -> list:

        return self.__patients.GetAllPatientUsernames()
    
    #returns all the treated patient usernames
    def GetAllTreatedPatientUsernames(self) -> list:

        return self.__treatedPatients.GetAllPatientUsernames()
    
    #returns all the applied patient usernames
    def GetAllAppliedPatientUsernames(self) -> list:

        return self.__appliedPatients.GetAllPatientUsernames()
    
    #returns all the doctor usernames
    def GetAllDoctorUsernames(self) -> list:

        return self.__doctors.GetAllDoctorUsernames()
    
    #generates a random password of capitals lower case and digits of length 8
    def GeneratePassword(self) -> string:

        password = ""

        for i in range(0,7,1):

            password = password + random.choice(string.ascii_letters + string.digits)

        return password
    
    #genereates a unique username in the form FirstnameSurnameNumber
    def GeneratePatientUsername(self, name):

        #removes the spaces from the name
        #name = name.replace(" ", "")
        tempName = name
        valid = False
        valid = self.CheckUnique(tempName)
        counter = 1

        while valid == False:

            tempName = "{0} {1}".format(name, str(counter))
            valid = self.CheckUnique(tempName)

        name = tempName
        return name
    
    def GenerateDoctorUsername(self, name):

        #removes the spaces from the name
        name = ''.join(name)
        name = "Dr" + name
        tempName = name
        valid = False
        valid = self.CheckUnique(tempName)
        counter = 1

        while valid == False:

            tempname = name + str(counter)
            self.CheckUnique(tempName)

        name = tempName
        return name
    
    #checks if a username is unique to the system
    def CheckUnique(self, tryUsername) -> bool:

        usernames = self.GetAllUsernames()

        for username in usernames:

            if tryUsername == username:

                return False
        
        return True

    #updates the doctors name
    def UpdateDoctorName(self, doctorToUpdate, name):

        doctor = self.__doctors.GetDoctorFromUsername(doctorToUpdate)
        doctor.SetName(name)

    #updates the doctors username
    def UpdateDoctorUsername(self, doctorToUpdate, username):

        doctor = self.__doctors.GetDoctorFromUsername(doctorToUpdate)
        doctor.SetUsername(username)

    #removes the specified doctor from the list of doctors
    def DeleteDoctor(self, doctorToRemove):

        doctor = self.__doctors.GetDoctorFromUsername(doctorToRemove)
        self.__doctors.RemoveDoctor(doctorToRemove)

    #adds a patient to the list of patients
    def RegisterPatient(self,username, password, name, address, dateOfBirth, mobile) -> Patient:

        self.__patients.AddPatient(username, password, name, dateOfBirth,  mobile, address)

    #adds an applied patient to the list of applied patients
    def AddAppliedPatient(self, username, password, name, dateOfBirth,  mobile, address):

        self.__appliedPatients.AddPatient(username, password, name, dateOfBirth, mobile, address)

    #removes a patient from the applied patients list and adds them to the patients list
    def EnrollPatient(self, patient):

        self.__appliedPatients.RemovePatient(patient)
        self.__patients.AddCompletePatient(patient)

    #assigns a patient to a doctor
    def AssignPatient(self, patientUsername, doctorUsername):

        #gets the doctor and patient from their usernames
        patient = self.__patients.GetPatientFromUsername(patientUsername)
        doctor = self.__doctors.GetDoctorFromUsername(doctorUsername)
        doctor.AddPatient(patient)

    #unassigns a patient from a doctor
    def DeassignPatient(self, patientUsername, doctorUsername):

        doctor = self.__doctors.GetDoctorFromUsername(doctorUsername)
        doctor.RemovePatient(patientUsername)

    #removes apatient from the list of patients and adds it to the list of patients
    def DischargePatient(self, patientUsername):

        patient = self.__patients.GetPatientFromUsername(patientUsername)

        self.__patients.RemovePatient(patient)
        self.__treatedPatients.AddCompletePatient(patient)
        
        self.__doctors.RemovePatient(patient)

        #patients  = []

        #goes through all the doctors and gets their patients
        #for doctor in self.__doctors:

            #patients = doctor.GetPatients()

            #if the doctor has the discharged patient remove it
            #for doctorPatient in patients:

                #if patient == doctorPatient:

                    #doctor.RemovePatient(patient)

        #can patients have two doctors?
        ####get docor assigned to patient and remove
        #remove appointments tooooooo

    #turns the admin into a file
    def MakeLine(self) -> list:

        line = []
        line.append(self.__username)
        line.append(self.__password)
        line.append(self.__name)
        line.append(self.__address)
        return line
    
    #gets the number of patients a doctor has
    def GetPatientsPerDoctor(self, doctorUsername):

        doctor = self.GetDoctorFromUsername(doctorUsername)
        return str(len(doctor.GetPatients()))

    #gets the list of unique symptoms names
    def GetSymptomNames(self):

        symptoms = self.__patients.GetAllSymptomInstances()
        symptomFrequencies = []

        for symptom in symptoms:

            if symptom not in symptomFrequencies:

                symptomFrequencies.append(symptom)

        return symptomFrequencies

    #gets the frequency of the symptom
    def GetSymptomFrequency(self, symptom):

        symptoms = self.__patients.GetAllSymptomInstances()

        return symptoms.count(symptom)
    
    #adds a patient to a family
    def AddPatientToFamily(self, patientUsername, familyName):

         self.__families.AddPatient(familyName, patientUsername)

    def RemovePatient(self, patientUsername, familyName):

        self.__families.RemovePatient(patientUsername, familyName)

    #adds a family to the list of familys
    def CreateFamily(self, familyName):

        self.__families.AddFamily(familyName)

    def GetAllFamilyNames(self) -> list:

        return self.__families.GetAllFamilyNames()
    
    def GetFamilyFromFamilyName(self, familyName):

        return self.__families.GetFamilyFromFamilyName(familyName)
    
    #gets the patients family
    def GetPatientFamily(self, patientUsername):

        family = self.__families.GetPatientFamily(patientUsername)

        if family is None or family == "":

            return "No Family"
    
    #returns the list 
    def GetDoctorList(self):

        return self.__doctors

    #adds a appointment to the list of appointments
    def RegisterAppointment(self, status, dateTime, doctor, patient, note) -> Appointment:
      
        return self.__appointments.AddAppointment(status, dateTime, doctor, patient, note)
    
    def GetUnapprovedAppointmentIDs(self) -> list:

        return self.__appointments.GetUnapprovedAppointmentIDs()
    
    #gets a doctor object from its username
    def GetDoctorFromUsername(self, username) -> Doctor:

        return self.__doctors.GetDoctorFromUsername(username)
    
    #gets a patient object from its username
    def GetPatientFromUsername(self, username) -> Patient:

        return self.__patients.GetPatientFromUsername(username)
    
    #gets an applied patient object from its username
    def GetAppliedPatientFromUsername(self, username) -> Patient:

        return self.__appliedPatients.GetPatientFromUsername(username)
    
    #gets a treated patient object from its username
    def GetTreatedPatientFromUsername(self, username) -> Patient:

        return self.__treatedPatients.GetPatientFromUsername(username)
    
    #gets the appointment from its id
    def GetAppointmentFromID(self, appointmentID):

        return self.__appointments.GetAppointmentFromID(appointmentID)

    #gets the name of the admin
    def GetName(self) -> string:

        return self.__name

    #sets the name of the admin
    def SetName(self, name):

        self.__name = name

    #gets the address of the admin
    def GetAddress(self) -> string:

        return self.__address

    #sets the address of the admin
    def SetAddress(self, address):

        self.__address = address

    #saves all the infomation files
    def Save(self):

        self.__doctors.Save()
        self.__patients.Save()
        self.__appointments.Save()
        self.__treatedPatients.Save()
        self.__appliedPatients.Save()
        self.__appointments.Save()
        self.__families.Save()

        fileSaver = FileSaver()
        fileSaver.AddLine(self.MakeLine())
        fileSaver.WriteFile(self.ADMIN_FILE)

    #loads all the infomation files
    def Load(self):

        self.__doctors.Load()
        self.__patients.Load()
        self.__appointments.Load()
        self.__treatedPatients.Load()
        self.__appliedPatients.Load()  
        self.__appointments.Load()
        self.__families.Load()


#################################################################################################################
# Database
#################################################################################################################

class Database:
    pass
    
#################################################################################################################
# DoctorList
#################################################################################################################

class DoctorList:

    DOCTOR_FILE = "Doctors.txt"
    PATIENT_FILE = "Patients.txt"

    def __init__(self):

        self.__doctors: list[Doctor] = []
    
    #adds the loaded doctors from the file to the list of doctors
    def Load(self):

        #loads file
        fileLoader = FileLoader()
        lines = fileLoader.ReadFile(self.DOCTOR_FILE)

        #adds to list
        for item in lines:
           
            self.AddDoctor(item[0], item[1], item[2])

            #adds the doctors patients if they have any assigned
            if len(item) == 4:

                #list of the usernames of he doctors assigned patients
                patients =[]
                patients = item[3].split(';')

                #list of all patients in the system
                allPatients = PatientList(self.PATIENT_FILE)
                allPatients.Load()

                #gets this doctors object
                thisDoctor = self.GetDoctorFromUsername(item[0])

                for patient in patients:

                    #gets the correct patient object
                    thisPatient = allPatients.GetPatientFromUsername(patient)
                    #adds the patient to this doctors list of patients
                    thisDoctor.AddPatient(thisPatient)

    #saves the doctor to their file
    def Save(self):

        fileSaver = FileSaver()

        #goes through each doctor
        for doctor in self.__doctors:

            #makes the doctor a line and adds it to the filesavers list of lines
            line = doctor.MakeLine()
            fileSaver.AddLine(line)
       
        #writes to the file
        fileSaver.WriteFile(self.DOCTOR_FILE)

    #adds a doctor to the list
    def AddDoctor(self, username, password, name) -> Doctor:

        doctor = Doctor(username, password, name)
        self.__doctors.append(doctor)
        return doctor

    #removes the specified doctor from the list doctor 
    def RemoveDoctor(self, doctorToRemove):

        doctor = self.GetDoctorFromUsername(doctorToRemove)
        self.__doctors.remove(doctor)

    #removes a patient from a doctor
    def RemovePatient(self, patient):
                
        patients  = []

        #goes through all the doctors and gets their patients
        for doctor in self.__doctors:

            patients = doctor.GetPatients()

            #if the doctor has the discharged patient remove it
            for doctorPatient in patients:

                if patient.GetUsername() == doctorPatient.GetUsername():

                    doctor.RemovePatient(patient.GetUsername())

    #returns a list of all doctor usernames
    def GetAllDoctorUsernames(self) -> list:

        usernames =[]

        for doctor in self.__doctors:

            usernames.append(doctor.GetUsername())

        return usernames
    
    #gets a patient object from its username
    def GetDoctorFromUsername(self, username):

        for doctor in self.__doctors:

            if doctor.GetUsername() == username:

                return doctor
            
        return None
    
    def GetAllPatientUsernamesWithoutDoctors(self) -> list:

        #list of all patients in the system
        allPatients = PatientList(self.PATIENT_FILE)
        allPatients.Load()

        for doctor in self.__doctors:

            doctorPatients = doctor.GetPatients()        

            for doctorPatient in doctorPatients:

                allPatients.RemovePatient(doctorPatient)

        return allPatients.GetAllPatientUsernames()
    

    def GetDoctorFromPatient(self, patientUsername):
        
        for doctor in self.__doctors:

            doctorPatients = doctor.GetPatients()

            for doctorPatient in doctorPatients:

                if patientUsername == doctorPatient.GetUsername():

                    return doctor
            
        return None
    
#################################################################################################################
# Family
#################################################################################################################
    
class Family:

    def __init__(self, name):

        self.__name = name
        self.__patients = []

    #makes te family into a line to store in the file
    def MakeLine(self) -> string:

        line = []
        line.append(self.__name)

        for patient in self.__patients:

            line.append(patient)

        return line

    #adds a patient to the family
    def AddPatient(self, patientUsername):

        self.__patients.append(patientUsername)

    def RemovePatient(self, patient):

        self.__patients.remove(patient)

    #formats the patients line for display
    def MakePatientsLine(self) -> list:

        line = ""

        for patient in self.__patients:

            line = line + patient+ ", "

        line = line[:-2]

        if line == "":

            return "No Patients"

        return line
    
    def GetAllPatientsInFamily(self):

        return self.__patients

    #gets the name of the family
    def GetName(self) -> string:

        return self.__name
    
#################################################################################################################
# FamilyList
#################################################################################################################
    
class Familylist:

    FAMILIES_FILE = "Families.txt"

    def __init__(self):

        self.__families = []

    #loads in the families
    def Load(self):

        #reads file
        fileLoader = FileLoader()
        lines = fileLoader.ReadFile(self.FAMILIES_FILE)

        if len(lines) > 0:

            #adds patients in the family to a list
            for item in lines:

                self.AddFamily(item[0])

            family = self.GetFamilyFromFamilyName(item[0])
            patients = item[1:]

            if len(patients) > 0:

                for patient in patients:

                    family.AddPatient(patient)

    #saves the family infomation to the file
    def Save(self):

        fileSaver = FileSaver()

        #goes through each family
        for family in self.__families:

            #turns the family infomation into a line and adds it to the 
            line = family.MakeLine()
            fileSaver.AddLine(line)
       
        #writes to the file
        fileSaver.WriteFile(self.FAMILIES_FILE)

    #adds a family to the list of families
    def AddFamily(self, familyName):

        family = Family(familyName)
        self.__families.append(family)

    #gets all the family names in the system
    def GetAllFamilyNames(self) -> list:

        familyNames = []

        for family in self.__families:

                familyNames.append(family.GetName())

        return familyNames

    def AddPatient(self, familyName, patientUsername):

        family = self.GetFamilyFromFamilyName(familyName)
        family.AddPatient(patientUsername)

    #gets a family object from a family name
    def GetFamilyFromFamilyName(self, familyName) -> Family:

        for family in self.__families:

                if family.GetName() == familyName:

                    return family
    
        return None
    
    #gets the family a patient is in
    def GetPatientFamily(self, patientUsername):

        for family in self.__families:

            if patientUsername in family.GetAllPatientsInFamily():

                return family.GetName()

    #removes the patient
    def RemovePatient(self, patientUsername, familyName):

        family = self.GetFamilyFromFamilyName(familyName)
        family.RemovePatient(patientUsername)

    def DeleteFamily(self, familyName):

        family = self.GetFamilyFromFamilyName(familyName)
        self.__families.remove(family)

#################################################################################################################
# FileLoader
#################################################################################################################

class FileLoader:

    def __init__(self):

        self.__lines = []
    
    #reads the files splits it into separate commands 
    def ReadFile(self, fileName) -> list:

        #tries to open and read the file
        try:

            fileName = "data/" + fileName
            with open(fileName, "r") as file:

               #gets the file and splits it into separate lines
               lines = file.read().splitlines()

            for line in lines:

                #goes through each line and splits it at each comma
                self.__lines.append(line.split(','))
        
        #gets the specific error and outputs it
        except Exception as e:

            print(f"error: {str(e)}")

        return self.__lines

    #returns the lines of the file
    def GetLines(self) -> list:

        return self.__lines
    
#################################################################################################################
# FileSaver
#################################################################################################################

class FileSaver:

    def __init__(self):

        self.__lines = []
    
    #writes to the file 
    def WriteFile(self, fileName) -> list:

        try:

            fileName = "data/" + fileName
            with open(fileName, 'w') as file:

                #joins all the lines together and wries them
                file.writelines('\n'.join(self.__lines))
        
        #gets the specific error that occured and outpus it
        except Exception as e:

            print(f"error: {str(e)}")

        return self.__lines

    #joins all the items in the list into a line and separates them with a comma
    def AddLine(self, items):

        separator = ','
        line = separator.join(items)

        self.__lines.append(line)

    #returns the lines of the file
    def GetLines(self) -> list:

        return self.__lines

    #sets the lines of the file
    def SetLines(self, items):

        self.__lines = items

#################################################################################################################
# Login
#################################################################################################################

class Login():

    PATIENT_FILE = "Patients.txt"

    def __init__(self):

        self.__attempts = 0
        self.__logins = []

    #checks entered username and password against the pairs from the file
    def Login(self, username, password, role):
 
        #goes through all the logins
        for item in self.__logins:

            currentUser = item[0]
            currentPass = item[1]

            if currentUser == username and currentPass == password:
               
                if role == "admin":

                    admin = Admin(item[0], item[1], item[2], item[3])
                    return admin

                elif role == "doctor":

                    doctor = Doctor(item[0], item[1], item[2])
                
                    #adds the doctors patients if they have any assigned
                    if len(item) == 4:

                        #list of the usernames of he doctors assigned patients
                        patients =[]
                        patients = item[3].split(';')

                        #list of all patients in the system
                        allPatients = PatientList(self.PATIENT_FILE)
                        allPatients.Load() 

                        for patient in patients:

                            #gets the correct patient object
                            thisPatient = allPatients.GetPatientFromUsername(patient)
                            #adds the patient to this doctors list of patients

                            if not thisPatient is None:

                                doctor.AddPatient(thisPatient)

                    #adds the doctors appointments 
                    appointments = AppointmentList()
                    appointments.Load()
                    appointment = appointments.GetAppointmentFromDoctor(item[0])
                    
                    if not appointment == None:

                        for app in appointment:

                            doctor.AddCompleteAppointment(app)

                    return doctor

                elif role == "patient":

                    patient = Patient(item[0], item[1], item[2], item[3], item[4], item[5])

                    #adds the patients symptom if they have any assigned
                    if len(item) == 7:

                        #list of the usernames of he doctors assigned patients
                        symptoms = []
                        symptoms = item[6].split(';')

                        for symptom in symptoms:

                            patient.AddSymptom(symptom)


                    #adds the patients family
                    family  = Familylist()
                    family.Load()
                    patientFamily = family.GetPatientFamily(item[0])
                    patient.SetFamily(patientFamily)

                    #adds the patients appointments 
                    appointments = AppointmentList()
                    appointments.Load()
                    appointment = appointments.GetAppointmentFromPatient(item[0])
                    
                    if not appointment == None:

                        for app in appointment:

                            patient.AddCompleteAppointment(app)
                    
                    #adds the patients doctor
                    doctors = DoctorList()
                    doctors.Load()
                    patientDoctor = doctors.GetDoctorFromPatient(item[0])
                    patient.SetDoctor(patientDoctor)

                    return patient

        #the username password combination is not in the system
        return None
        
    #loads the logins from the file
    def LoadLogins(self, filename):

        fileLoader = FileLoader()
        fileLoader.ReadFile(filename)

        self.__logins = fileLoader.GetLines()

    #saves the logins to the file
    def SaveLogins(self, fileName):

        fileSaver = FileSaver()
        fileSaver.SetLines(self.__logins)
        fileSaver.WriteFile(fileName)

    #increases the number of login attempts by one
    def IncreaseAttempts(self):

        self.__attempts = self.__attempts + 1

    #returns the amount of attempts remaining
    def GetAttemptsRemaining(self):

        totalNumberOfAttempts = 3
        return totalNumberOfAttempts - self.__attempts

#################################################################################################################
# Patient List
#################################################################################################################
    
class PatientList:

    def __init__(self, fileName):

        self.__patients = []
        self.__fileName = fileName
    
    #loads the patients from the file and adds them to the list of patients
    def Load(self):

        #reads file
        fileLoader = FileLoader()
        lines = fileLoader.ReadFile(self.__fileName)

        if len(lines) > 0:

            #adds patients to list
            for item in lines:

                dateList = []
                dateList = item[3].split("-")
                dateTimeOfBirth = date(day = int(dateList[0]), month = int(dateList[1]), year = int(dateList[2]))
            
                self.AddPatient(item[0],item[1],item[2],dateTimeOfBirth,item[4],item[5])

                #adds the patients symptom if they have any assigned
                if len(item) == 7:

                    #list of the usernames of he doctors assigned patients
                    symptoms = []
                    symptoms = item[6].split(';')

                    #gets this patients object
                    thisPatient = self.GetPatientFromUsername(item[0])

                    for symptom in symptoms:

                        thisPatient.AddSymptom(symptom)

    #saves the patient infomation to the file
    def Save(self):

        fileSaver = FileSaver()

        #goes through each patient
        for patient in self.__patients:

            #turns the patient infomation into a line and adds it to the 
            line = patient.MakeLine()
            fileSaver.AddLine(line)
       
        #writes to the file
        fileSaver.WriteFile(self.__fileName)

    #adds a patient to the patient list
    def AddPatient(self,username, password, name, dateOfBirth, mobile, address) -> Patient:

        patient = Patient(username, password, name, dateOfBirth,  mobile, address)
        self.__patients.append(patient)
        return patient
    
    def AddCompletePatient(self, patient):

        self.__patients.append(patient)

    #removes a patient from the patient list
    def RemovePatient(self, patientToRemove):

        #patientToRemove = self.GetPatientFromUsername(patientToRemoveUsername)

        for patient in self.__patients:

            if patient.GetUsername() == patientToRemove.GetUsername():

                self.__patients.remove(patient)

    #returns a list of all the patients names
    def GetAllPatientUsernames(self) -> list:

        usernames = []

        for patient in self.__patients:

            usernames.append(patient.GetUsername())

        return usernames

    #gets a patient object from its username
    def GetPatientFromUsername(self, username):

        for patient in self.__patients:

            if patient.GetUsername() == username:

                return patient
            
        return None
    
    #gets all the symptoms of all patients
    def GetAllSymptomInstances(self):

        symptoms = []

        for patient in self.__patients:

            patientSymptoms = patient.GetSymptoms()

            for patientSymptom in patientSymptoms:
                
                symptoms.append(patientSymptom)

        return symptoms
    
    #gets the list of patient objects
    def GetPatients(self) -> list:

        return self.__patients
    
    #sets the list of patient objects
    def SetPatients(self, patients):

        self.__patients = patients
