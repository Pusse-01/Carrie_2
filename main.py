from matplotlib.style import available
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta, date, time

# appointment_duration = 1
err = ""

st.title("Project Carrie")

st.write ("You can check available doctors from here")

date = st.date_input(
     "When do you want to meet your doctor",
     date(2022, 5, 6))

appointment = st.slider(
     "Schedule your appointment:",
     value=(time(11, 30), time(12, 45)))
duration = datetime.combine(date.min, appointment[1]) - datetime.combine(date.min, appointment[0])
seconds = duration.total_seconds()
hours = seconds // 3600
minutes = (seconds % 3600) // 60
if minutes>0:
    appointment_duration = hours +1
else: appointment_duration = hours
appointment = "{:%H:%M} - {:%H:%M}".format(appointment[0], appointment[1])
st.write("You're scheduled for:", appointment)
user_time_slot = appointment
user_dist = st.slider('Select the distance', 0, 50, 2)

button = st.button("Check")

doc_data = [
    {
        "id":'01',
        "appointments":[(datetime(2022, 5, 22, 10), datetime(2022, 5, 22, 10, 30)),
                (datetime(2022, 5, 22, 12), datetime(2022, 5, 22, 13)),
                (datetime(2022, 5, 22, 15, 30), datetime(2022, 5, 22, 17, 10))],
        "work_hours":(datetime(2022, 5, 22, 9), datetime(2022, 5, 22, 18)),
        "distance":8
    },
    {
        "id":'02',
        "appointments":[(datetime(2022, 5, 22, 10), datetime(2022, 5, 22, 10, 30)),
                (datetime(2022, 5, 22, 12), datetime(2022, 5, 22, 13)),
                (datetime(2022, 5, 22, 15, 30), datetime(2022, 5, 22, 17, 10))],
        "work_hours":(datetime(2022, 5, 22, 9), datetime(2022, 5, 22, 18)),
        "distance":15
    },
    {
        "id":'03',
        "appointments":[(datetime(2022, 5, 22, 10), datetime(2022, 5, 22, 10, 30)),
                (datetime(2022, 5, 22, 12), datetime(2022, 5, 22, 13)),
                (datetime(2022, 5, 22, 15, 30), datetime(2022, 5, 22, 17, 10))],
        "work_hours":(datetime(2022, 5, 22, 9), datetime(2022, 5, 22, 18)),
        "distance":10
    }
]

def get_slots(hours, appointments, duration=timedelta(hours=appointment_duration)):
    available_slots = []
    # print(hours[0], hours[1])
    slots = sorted([(hours[0], hours[0])] + appointments + [(hours[1], hours[1])])
    # print(slots)
    for start, end in ((slots[i][1], slots[i+1][0]) for i in range(len(slots)-1)):
        assert start <= end, "Cannot attend all appointments"
        while start + duration <= end:
            print(start, start + duration)
            time_slot = "{:%H:%M} - {:%H:%M}".format(start, start + duration)
            available_slots.append(time_slot)
            # print ()
            start += duration
    return available_slots




def find_timeslot():
    arr=[]
    for doc in doc_data:
        doc_id = (doc['id'])
        appointments = doc['appointments']
        work_hours = doc['work_hours']
        dist = doc['distance']
        available_slots = get_slots(work_hours, appointments, duration=timedelta(hours=appointment_duration))
        col= {
            'id':doc_id,
            'available_slots':available_slots,
            'dist':dist
        }
        arr.append(col)
    available_doctors = []
    for data in arr:
        if data['dist']<=user_dist:
            for ts in data['available_slots']:
                if ts==user_time_slot:
                    available_doctors.append(data['id'])
                else: err = "No doctors available at the selected time slot" 
        # else: 
        #     err = "No Doctors available in this range. Please increase the distance!"


    # print(err)
    print(available_doctors)
    return available_doctors

    

# st.write
if button:
    available_doctors =  find_timeslot()
    if len(available_doctors)!=0:
        for ad in available_doctors:
            st.success("The following doctors are available..!")
            st.write(ad)
    else: st.warning("No doctors available...Please try again!")





# hours = df.iloc[1].work_hours[0]
# appointments = [(datetime(2022, 5, 22, 10), datetime(2022, 5, 22, 10, 30)),
#                 (datetime(2022, 5, 22, 12), datetime(2022, 5, 22, 13)),
#                 (datetime(2022, 5, 22, 15, 30), datetime(2022, 5, 22, 17, 10))]

# hours = (datetime(2022, 5, 22, 9), datetime(2022, 5, 22, 18))



# if __name__ == "__main__":
#     get_slots(hours, appointments)
 