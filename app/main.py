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

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


client = MongoClient('mongodb+srv://carrie:Carrie123@carrie.vpraptv.mongodb.net/?retryWrites=true&w=majority')
print("Connected successfully!!!")
  
#     print("Could not connect to MongoDB")

db = client['Carrie']
collection = db['users']

def get_duration(start, end):
    duration = datetime.combine(date.min, end) - datetime.combine(date.min, start)
    seconds = duration.total_seconds()
    hours = seconds // 3600
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
        dist = doc['distance']
        work_hours = [datetime.combine(dateA, time(7, 0)), datetime.combine(dateA, time(18,0))]
        available_slots = get_slots(work_hours, appointments,appointment_duration, dateA)
        col= {
            'id':doc_id,
            'available_slots':available_slots,
            'dist':dist
        }
        arr.append(col)
    available_doctors = []
    times_sorted = []
    new_times =[]
    for data in arr:
        if data['dist']<=user_dist:
            for ts in sorted(data['available_slots']):
                ts1 = datetime.strptime(ts[:16], '%Y:%m:%d:%H:%M')
                ts2 = datetime.strptime(ts[19:], '%Y:%m:%d:%H:%M')
                times_sorted.append(ts1)
                times_sorted.append(ts2)
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
    return available_doctors


def get_daily_appointments(appointments, dateA):
    appointments_on_the_day = []
    for i in appointments:
        if (i[0].date()==dateA.date()):
            x= (i[0],i[1])
            appointments_on_the_day.append(x)
    return((appointments_on_the_day))


def get_slots(hours, appointments, appointment_duration, dateA ):
    appointments = get_daily_appointments(appointments, dateA)
    duration=timedelta(hours=appointment_duration)
    available_slots = []
    if appointments != []:
        slots = sorted([(hours[0], hours[0])] + appointments + [(hours[1], hours[1])])
    else: slots = [(hours[0], hours[0])] + [(hours[1], hours[1])]
    for start, end in ((slots[i][1], slots[i+1][0]) for i in range(len(slots)-1)):
        while start + duration <= end:
            time_slot = "{:%Y:%m:%d:%H:%M} - {:%Y:%m:%d:%H:%M}".format(start, start + duration)
            available_slots.append(time_slot)
            start += duration
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

def checkPw(password, hash):
    salt = bcrypt.gensalt()
    hash_gen = bcrypt.hashpw(password.encode('utf8'), salt)
    print(hash_gen)
    print(hash)
    if hash_gen == hash:
        return True
    else: return False

@app.route("/", methods=['GET'])
def home_view():
        return "Hello Carrie"

@app.route("/signup", methods=['POST'])
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

@app.route("/login", methods=['POST'])
def login():
    # hash = []
    email = json.loads(request.data)['email']
    password = json.loads(request.data)['password']
    res = (collection.find({'email':email}))
    for doc in res:
        hash = (doc['password'])
        if bcrypt.checkpw(password.encode('utf8'), hash.encode('utf8')):
            token = make_token()
            y = {"name":doc['name'] ,"email":doc['email'], "role": doc['role'] , "token":token}
            # print(y)
            return (json.dumps(y))
        else:
            return ("Login Failed!")

@app.route("/getClinicians", methods=['POST'])
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


@app.route("/addAppointments", methods=['POST'])
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