from flask import Flask, render_template, send_file, request, jsonify
from PIL import Image, ImageDraw
import sleep_utils.schedule as schedule 
from sleep_utils.schedule import Sleeper, Optimal
# from models import db
import csv
import os
from time import time, strftime, gmtime
import json
app = Flask(__name__)

@app.route('/')
def baseFunc():
    html_content = """
    <h1>Welcome to Circadia!</h1>
    <p>This is a subtitle.</p>
    <ul>
        <li>/get_schedule/  -  get altered schedule generated from user sleep score and current schedule CSV</li>
    </ul>
    """
    
    # Return the HTML content
    return html_content

@app.route("/get_schedule", methods=['GET', 'POST'])
def getSchedule():
    
    
    if request.method == 'POST':
        data = request.get_json()
        
        print(data)

        bedtimes = []
        waketimes = []
        days = []
        for day, times in data.items():
            days.append(day)
            bedtimes.append(times['bedtime'])
            waketimes.append(times['waketime'])
        bedtimes = list(map(schedule.standard_to_military,bedtimes))
        waketimes = list(map(schedule.standard_to_military,waketimes))
        curr_person = Sleeper(3,90,bedtimes,waketimes)
        optimal = Optimal()
        adjusted_bedtime, adjusted_waketime = schedule.adjust(curr_person, optimal)
        adjusted_bedtime = list(map(schedule.d_to_s,adjusted_bedtime))
        adjusted_waketime = list(map(schedule.d_to_s,adjusted_waketime))

        new_schedule = {}
        for i in range(len(days)):
            print(i)
            new_schedule[days[i]] = {}
            new_schedule[days[i]]["bedtime"] = adjusted_bedtime[i]
            new_schedule[days[i]]["waketime"] = adjusted_waketime[i]
        # db.session.commit()  # Commit changes to the database
        return jsonify(new_schedule)
        
    
    #User inputs:
    #Their bedtimes, waketimes, mtwtf

    #Json object, you guys need to parse that
    #create a sleeper object
    #write a function that takes in a sleeper ob
    else:
        temp = "Request was a success!"
        return temp
    
def process_sleep_schedule(data):
    # Example logic to adjust bedtime and waketime
    new_schedule = {}

    for day, times in data.items():
        # Example of dramatic shift for demonstration:
        # If the original waketime is later than 10 AM, shift it to 8 AM
        bedtime = times['bedtime']
        waketime = times['waketime']
       
        # Parse times assuming they are in "%I:%M %p" format
        from datetime import datetime, timedelta
        fmt = "%I:%M %p"
        bedtime_dt = datetime.strptime(bedtime, fmt)
        waketime_dt = datetime.strptime(waketime, fmt)

        # Implement a dramatic shift if needed
        if waketime_dt.hour > 10:
            waketime_dt = waketime_dt.replace(hour=8, minute=0)

        # Format back to string
        new_bedtime = datetime.strftime(bedtime_dt, fmt)
        new_waketime = datetime.strftime(waketime_dt, fmt)

        new_schedule[day] = {
            "bedtime": new_bedtime,
            "waketime": new_waketime
        }

    return new_schedule


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)