import os
import json
import secrets
import bcrypt
from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS
from flask import request
# from utils import get_duration, find_timeslot
from datetime import datetime, timedelta, date, time

application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'


# doc_data = [
#     {
#         "id":'01',
#         "appointments":[(datetime(2022, 5, 21, 10), datetime(2022, 5, 21, 10, 30)),
#                 (datetime(2022, 5, 22, 12), datetime(2022, 5, 22, 13)),
#                 (datetime(2022, 5, 22, 15, 30), datetime(2022, 5, 22, 17, 10))],
#         "work_hours":(datetime(2022, 5, 22, 9), datetime(2022, 5, 22, 18)),
#         "distance":8
#     },
#     {
#         "id":'02',
#         "appointments":[(datetime(2022, 5, 22, 10), datetime(2022, 5, 22, 10, 30)),
#                 (datetime(2022, 5, 22, 12), datetime(2022, 5, 22, 13)),
#                 (datetime(2022, 5, 22, 15, 30), datetime(2022, 5, 22, 17, 10))],
#         "work_hours":(datetime(2022, 5, 22, 9), datetime(2022, 5, 22, 18)),
#         "distance":15
#     },
#     {
#         "id":'03',
#         "appointments":[(datetime(2022, 5, 22, 10), datetime(2022, 5, 22, 10, 30)),
#                 (datetime(2022, 5, 22, 12), datetime(2022, 5, 22, 13)),
#                 (datetime(2022, 5, 22, 15, 30), datetime(2022, 5, 22, 17, 10))],
#         "work_hours":(datetime(2022, 5, 22, 9), datetime(2022, 5, 22, 18)),
#         "distance":10
#     }
# ]



client = MongoClient('mongodb+srv://carrie:Carrie123@carrie.vpraptv.mongodb.net/?retryWrites=true&w=majority')
print("Connected successfully!!!")
  
#     print("Could not connect to MongoDB")

db = client['Carrie']
collection = db['users']

def get_duration(start, end):
    duration = datetime.combine(date.min, end) - datetime.combine(date.min, start)
    seconds = duration.total_seconds()
    hours = seconds // 3600
    print(hours)
    minutes = (seconds % 3600) // 60
    if minutes>0:
        appointment_duration = hours +1
    else: appointment_duration = hours
    return appointment_duration


def find_timeslot(doc_data, user_dist, appointment_duration, user_time_slot, dateA):
    arr=[]
    for doc in doc_data:
        doc_id = (doc['id'])
        appointments = doc['appointments']
        print(appointments)
        # work_hours = doc['work_hours']
        dist = doc['distance']
        # print(work_hours)
        work_hours = [datetime.combine(dateA, time(7, 0)), datetime.combine(dateA, time(18,0))]
        print(work_hours)
        available_slots = get_slots(work_hours, appointments,appointment_duration, dateA)
        print(available_slots) 
        col= {
            'id':doc_id,
            'available_slots':available_slots,
            'dist':dist
        }
        arr.append(col)
        # get_daily_appointments(appointments, dateA)
    available_doctors = []
    times_sorted = []
    new_times =[]
    for data in arr:
        if data['dist']<=user_dist:
            # print([0][1])
            for ts in sorted(data['available_slots']):
                # print(ts)
                ts1 = datetime.strptime(ts[:16], '%Y:%m:%d:%H:%M')
                ts2 = datetime.strptime(ts[19:], '%Y:%m:%d:%H:%M')
                times_sorted.append(ts1)
                times_sorted.append(ts2)
                # print(ts1,user_time_slot1 )
                # if ts==user_time_slot:
                #     available_doctors.append(data['id'])
                # else: err = "No doctors available at the selected time slot" 
            # print(times_sorted)
            for i in times_sorted:
                if times_sorted.count(i) > 1:
                    pass
                else:
                    new_times.append(i)
            user_time_slot1 = datetime.strptime(user_time_slot[:16], '%Y:%m:%d:%H:%M')
            user_time_slot2 = datetime.strptime(user_time_slot[19:], '%Y:%m:%d:%H:%M')
            for i in range((len(new_times))-1):
                if (new_times[i] <= user_time_slot1 and new_times[i+1] >= user_time_slot2):
                    available_doctors.append(data['id'])
                else: err = "No doctors available at the selected time slot" 
            print(available_doctors)

        # else: 
        #     err = "No Doctors available in this range. Please increase the distance!"


    # print(err)
    # print(available_doctors)
    return available_doctors


def get_daily_appointments(appointments, dateA):
    # print(dateA)
    appointments_on_the_day = []
    for i in appointments:
        print("App dawasa: " ,str(i[0].date()))
        print(dateA.date())
        if (i[0].date()==dateA.date()):
            x= (i[0],i[1])
            appointments_on_the_day.append(x)
    print("appointments_on_the_day" , str(appointments_on_the_day))
    return((appointments_on_the_day))


def get_slots(hours, appointments, appointment_duration, dateA ):
    print("Appointments comming", str(appointments))
    appointments = get_daily_appointments(appointments, dateA)
    print(appointments)
    duration=timedelta(hours=appointment_duration)
    available_slots = []
    # print("Appointments", str(appointments))
    if appointments != []:
        slots = sorted([(hours[0], hours[0])] + appointments + [(hours[1], hours[1])])
    else: slots = [(hours[0], hours[0])] + [(hours[1], hours[1])]
    print(slots)
    for start, end in ((slots[i][1], slots[i+1][0]) for i in range(len(slots)-1)):
        # print(start, end)
        # assert start <= end, "Cannot attend all appointments"
        while start + duration <= end:
            # print(start, start + duration)
            time_slot = "{:%Y:%m:%d:%H:%M} - {:%Y:%m:%d:%H:%M}".format(start, start + duration)
            available_slots.append(time_slot)
            # print ()
            start += duration
    print("hello")
    # print(available_slots)       

    return available_slots


def pwHash(password):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode('utf8'), salt)
    return hash

def make_token():
    """
    Creates a cryptographically-secure, URL-safe string
    """
    return secrets.token_urlsafe(16) 

@application.route("/", methods=['GET'])
def home_view():
        return "Hello Carrie"

@application.route("/signup", methods=['POST'])
def register():
    name = json.loads(request.data)['name']
    email = json.loads(request.data)['email']
    role = json.loads(request.data)['role']
    password = json.loads(request.data)['password']
    distance = json.loads(request.data)['distance']
    res = (collection.find({'email':email}))
    for doc in res:
        if doc['email'] == email:
            return("User already exist!")
        
    hash = pwHash(password)
    res = {"name":name, "email":email, "role":role, "password":hash}
    x = collection.insert_one(res)
    token = make_token()
    y = {"name":name ,"email":email, "role": role, "token":token, "distance": distance}
    return (json.dumps(y))

@application.route("/login", methods=['POST'])
def login():
    # hash = []
    email = json.loads(request.data)['email']
    password = json.loads(request.data)['password']
    res = (collection.find({'email':email}))
    for doc in res:
        hash = (doc['password'])
        if bcrypt.checkpw(password.encode('utf8'), hash):
            token = make_token()
            
            y = {"name":doc['name'] ,"email":doc['email'], "role": doc['role'] , "token":token}
            # print(y)
            return (json.dumps(y))
        else:
            return ("Login Failed!")

@application.route("/getClinicians", methods=['POST'])
def get_clinicians():
    doc_data = []
    appointments = []
    start = json.loads(request.data)['start']
    end = json.loads(request.data)['end']
    date = json.loads(request.data)['date']
    distance = json.loads(request.data)['distance']
    start = datetime.strptime(start, '%H:%M:%S').time()
    end = datetime.strptime(end, '%H:%M:%S').time()
    date = datetime.strptime(date, '%Y:%m:%d')
    appointment_duration = get_duration(start, end)
    appointment = "{:%Y:%m:%d:%H:%M} - {:%Y:%m:%d:%H:%M}".format(datetime.combine(date, start), datetime.combine(date, end))
    res = (collection.find({"role":"Doctor"}))
    for data in res:
        for dates in data["appointments"]:
            # start = dates[0][0][0]
            # end = dates[0][0][1]
            print("Dates", str(dates[0]))
            appointments.append(dates[0])
        entry = {"id":data["name"],"appointments": appointments,"distance": data["distance"], "work_hours":(datetime(2022, 5, 22, 9), datetime(2022, 5, 22, 18)) }
        doc_data.append(entry)
        print(doc_data)
    available_clinicians = find_timeslot(doc_data, distance, appointment_duration,appointment, date)
    # print(available_clinicians)
    response = {"available_clinicians":available_clinicians}
    return (json.dumps(response))


@application.route("/addAppointments", methods=['POST'])
def add_appointments():
    start = json.loads(request.data)['start']
    end = json.loads(request.data)['end']
    date = json.loads(request.data)['date']
    email = json.loads(request.data)['email']
    distance = json.loads(request.data)['distance']
    start = datetime.strptime(start, '%H:%M:%S').time()
    end = datetime.strptime(end, '%H:%M:%S').time()
    date = datetime.strptime(date, '%Y:%m:%d')
    appointment_duration = get_duration(start, end)
    appointment = [(datetime.combine(date, start), datetime.combine(date, end))]
    res = (collection.find({'email':email}))
    for data in res:
        if email==data['email']:
            result = collection.update_many(
                {"email":email},
                {'$push':
                    {'appointments': appointment}
                }
            )
    msg = "Appointment added succesfully!"
    return (json.dumps(msg))


if __name__ == "__main__":
    application.run()