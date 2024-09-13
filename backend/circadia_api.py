from flask import Flask, render_template, send_file, request, jsonify
from PIL import Image, ImageDraw
import sleep_utils.schedule as schedule 
import sleep_utils.pipeline as pipeline 
from sleep_utils.schedule import Sleeper, Optimal
# from models import db
import numpy as np
import pandas as pd
import yasa
import mne
import csv
import os
from time import time, strftime, gmtime
import json
import matplotlib.pyplot as plt
from yasa import Hypnogram
app = Flask(__name__)


## HELPER FUNCTIONS ##

def remove_leading(arr, target_element):
    first_diff_index = np.argmax(arr != target_element)
    return arr[first_diff_index:]
    
def remove_trailing(arr, target_element):
    # Reverse the array to find the index of the last non-target element
    reversed_arr = arr[::-1]
    
    # Find the first index in the reversed array that is not the target_element
    first_non_target_index = np.argmax(reversed_arr != target_element)

    return arr[:-first_non_target_index] if first_non_target_index > 0 else arr

def convert_csv_to_stages(input_csv):
    sample_data = pd.read_csv(input_csv)
    sample_data =sample_data.fillna(0)
    sampling_rate = 256
    ch_names = ['TP9', 'AF7', 'AF8', 'TP10']
    time_series = []
    time_series.append(np.array(sample_data['ch1']))
    time_series.append(np.array(sample_data['ch2']))
    time_series.append(np.array(sample_data['ch3']))
    time_series.append(np.array(sample_data['ch4']))
    time_series = np.array(time_series)
    info = mne.create_info(ch_names,sampling_rate)
    raw = mne.io.RawArray(time_series, info)
    sls = yasa.SleepStaging(raw, eeg_name="TP10", metadata=dict(age=21, male=False))
    y_pred = sls.predict()
    df_pred = pd.DataFrame({'Stage': y_pred})
    sleep_cycles = list(df_pred["Stage"])
    return sleep_cycles

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


@app.route("/get_hypnogram_image", methods=['POST'])
def get_hypnogram_image():
    data = request.get_json()  # We assume this includes necessary data to generate the hypnogram
    image_path = generate_hypnogram(data)
    image_url = f"{request.host_url}static/{os.path.basename(image_path)}"
    return jsonify({'image_url': image_url})


def generate_hypnogram(filename):
    # Call the hypnogram generation logic from your Jupyter notebook
    sleep_stages = convert_csv_to_stages(filename)
    sleep_stages = np.array(sleep_stages)
    sleep_stages = remove_leading(sleep_stages, 'W')
    sleep_stages = remove_trailing(sleep_stages, 'W')
    hyp = Hypnogram(sleep_stages, freq="30s")
    plt.savefig("hypnogram.png")
    plt.close()
    image_path = os.path.basename("hypnogram.png")
    # You need to implement the actual generation and saving logic here
    # Example: plt.savefig(image_path)
    return image_path

@app.route("/generate_hypnogram", methods=['GET'])
def getSleepInfo():
    return "77"

@app.route("/get_schedule", methods=['GET', 'POST'])
def getSchedule():
    if request.method == 'POST':
       
        data = request.get_json()
     

        sleep_score = pipeline.calculate_sleep_score("sleep_eeg.csv")
        bedtimes = []
        waketimes = []
        days = []
        for day, times in data.items():
            days.append(day)
            bedtimes.append(times['bedtime'])
            waketimes.append(times['waketime'])
        bedtimes = list(map(schedule.standard_to_military,bedtimes))
        waketimes = list(map(schedule.standard_to_military,waketimes))
        curr_person = Sleeper(3,sleep_score,bedtimes,waketimes)
        optimal = Optimal()

        print("Adjusting my sleep schedule")

        adjusted_bedtime, adjusted_waketime = schedule.adjust(curr_person, optimal)
        adjusted_bedtime = list(map(schedule.d_to_s,adjusted_bedtime))
        adjusted_waketime = list(map(schedule.d_to_s,adjusted_waketime))

        print("Printing my new sleep schedule")

        new_schedule = {}
        for i in range(len(days)):
            print(i)
            new_schedule[days[i]] = {}
            new_schedule[days[i]]["bedtime"] = adjusted_bedtime[i]
            new_schedule[days[i]]["waketime"] = adjusted_waketime[i]
    

        print(new_schedule)
        # db.session.commit()  # Commit changes to the database
        return jsonify(new_schedule)
        
    
    #User inputs:
    #Their bedtimes, waketimes, mtwtf

    #Json object, you guys need to parse that
    #create a sleeper object
    #write a function that takes in a sleeper ob
    else:
        temp = "Went through, but was not POST!"
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
    app.run(host='0.0.0.0', port=8080, debug=True)