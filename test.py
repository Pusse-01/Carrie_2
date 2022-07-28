# import numpy as np
# import pandas as pd
# import ast
import streamlit as st

# from datetime import datetime, timedelta

# dfs = pd.read_excel('doc.xlsx')

# df = pd.DataFrame(dfs)
# # hours = df.iloc[1].work_hours
# data_array = np.array(dfs)
# print()
# doc_id=[]
# doc_appointments = []
# for data in data_array:
#     doc_id.append(data[0])
#     res = [x.strip() for x in data[1].split(',')]
#     # print(res)
#     for result in res:
#         # print(result)
#         result2 = [x.strip() for x in result.split(' - ')]
#         date_time_start = result2[0][4:18]
#         date_time_end = result2[1][3:17]
#         start = datetime.strptime(date_time_start, '%y.%m.%d-%H.%M')
#         end  = datetime.strptime(date_time_end, '%y.%m.%d-%H.%M')
#         doc_appointments.append((start, end))
# print(doc_appointments[0])
# d = data_array[2][1]
# result = [x.strip() for x in d.split(',')]
# # d = d.split(',')

# result2 = [x.strip() for x in result[0].split(' - ')]

# print(result2[1])


# # res = ast.literal_eval(df.appointments[0])

# print (type(d))

# from datetime import datetime

# date_time_start = result2[0][4:18]
# date_time_end = result2[1][3:17]
# # '18/09/19 01:55:19'

# start = datetime.strptime(date_time_start, '%y.%m.%d-%H.%M')
# end  = datetime.strptime(date_time_end, '%y.%m.%d-%H.%M')

# doc_appointments = []
# doc_appointments.append((start, end))

# print ("The type of the date is now",  type(start))
# print ("The date is", start)
# print ("The type of the date is now",  type(end))
# print ("The date is", end)
# print(doc_appointments)



# Using above second method to create a 
# 2D array
# rows, cols = (5, 2)
# arr=[]
# for i in range(rows):
#     col= []
#     # for j in range(cols):
#     #     col.append(0)
#     col.append(i) 
#     col.append(i) 
#     arr.append(col)
# print(arr)

number = st.number_input('Insert a number', step = 1)
st.write('The current number is ', number)

import datetime
from datetime import datetime, date, time
# from datetime import time
appointment = st.slider(
     "Schedule your appointment:",
     value=(time(11, 30), time(12, 45)))
# duration = appointment[1] - appointment[0]
# print(datetime.combine(date.min, appointment[1]) - datetime.combine(date.min, appointment[0]))


duration = datetime.combine(date.min, appointment[1]) - datetime.combine(date.min, appointment[0])
seconds = duration.total_seconds()
hours = seconds // 3600
minutes = (seconds % 3600) // 60
if minutes>0:
    hours = hours +1
print(hours, minutes)
appointment = "{:%H:%M} - {:%H:%M}".format(appointment[0], appointment[1])
st.write("You're scheduled for:", appointment)

