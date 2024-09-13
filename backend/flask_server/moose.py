from muselsl import stream, record, list_muses, record_direct
import csv
import os
from time import time, strftime, gmtime
from os import listdir
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import scipy
import mne
import pickle
array = np.array
from scipy import signal
from flask import Flask, send_file, render_template
from PIL import Image, ImageDraw
import csv
import os
from time import time, strftime, gmtime
app = Flask(__name__)

k = ""
    
def _print_muse_list(muses):
    if not muses:
        print('No Muses found.')
    else:
        for m in muses:
            print(f'Found device {m["name"]}, MAC Address {m["address"]}')
    

#Found device MuseS-6453, MAC Address 00:55:DA:B9:5D:E7
def butter_delta(eeg_data): #0.5-4 --> check whether low delta is necessary or not
    l_freq = 0.5
    h_freq = 4.0
    return mne.filter.filter_data(eeg_data, 512, l_freq, h_freq, picks=None, filter_length='auto',
                           l_trans_bandwidth='auto', h_trans_bandwidth='auto', n_jobs=1,
                           method='fir', iir_params=None, copy=True, phase='zero', fir_window='hamming',
                           fir_design='firwin', pad='reflect_limited', verbose=None)
def butter_theta(eeg_data): #IMPORTANT: 4-8
    l_freq = 4.0
    h_freq = 8.0
    return mne.filter.filter_data(eeg_data, 512, l_freq, h_freq, picks=None, filter_length='auto',
                           l_trans_bandwidth='auto', h_trans_bandwidth='auto', n_jobs=1,
                           method='fir', iir_params=None, copy=True, phase='zero', fir_window='hamming',
                           fir_design='firwin', pad='reflect_limited', verbose=None)
def butter_alpha(eeg_data): #IMPORTANT: 8-12
    l_freq = 8.0
    h_freq = 12.0
    return mne.filter.filter_data(eeg_data, 512, l_freq, h_freq, picks=None, filter_length='auto',
                           l_trans_bandwidth='auto', h_trans_bandwidth='auto', n_jobs=1,
                           method='fir', iir_params=None, copy=True, phase='zero', fir_window='hamming',
                           fir_design='firwin', pad='reflect_limited', verbose=None)
def butter_beta(eeg_data):  #IMPORTANT: 12-35
    l_freq = 12.0
    h_freq = 35.0
    return mne.filter.filter_data(eeg_data, 512, l_freq, h_freq, picks=None, filter_length='auto',
                           l_trans_bandwidth='auto', h_trans_bandwidth='auto', n_jobs=1,
                           method='fir', iir_params=None, copy=True, phase='zero', fir_window='hamming',
                           fir_design='firwin', pad='reflect_limited', verbose=None)
def butter_gamma(eeg_data): #35-60 --> check whether high gamma is necessary or not
    l_freq = 35.0
    h_freq = 60.0
    return mne.filter.filter_data(eeg_data, 512, l_freq, h_freq, picks=None, filter_length='auto',
                           l_trans_bandwidth='auto', h_trans_bandwidth='auto', n_jobs=1,
                           method='fir', iir_params=None, copy=True, phase='zero', fir_window='hamming',
                           fir_design='firwin', pad='reflect_limited', verbose=None)
def eeg_wavelet_parser(filename):
    with open(filename, "r") as f:
        q1a = f.read(1000)
    eeg_demo = pd.read_csv(filename,sep=",",engine='python')[:]
    #make an mne info object
    mne_info = mne.create_info(list(eeg_demo.columns[1:5]), 256, ch_types=['eeg']*len(eeg_demo.columns[1:5]))
    mne_raw = mne.io.RawArray(eeg_demo.iloc[:,1:5].values.T, mne_info)
    standard_1020 = mne.channels.make_standard_montage('standard_1020')
    mne_raw.set_montage(standard_1020)
    lower_bound = 0
    upper_bound = 50
    freqNotch = 60
    mne_raw.filter(lower_bound, upper_bound, fir_design='firwin')
    mne_raw.notch_filter(freqNotch, fir_design='firwin')
    ica_obj = mne.preprocessing.ICA(n_components = 0.95, method='infomax', max_iter="auto", random_state=1, fit_params=dict(extended=True)).fit(mne_raw)
    ica = ica_obj.get_sources(mne_raw).get_data()
    filtered_wavelets = {}
    channels = ["TP9","TP10","AF7","AF8"]
    for i in range(3):
        filtered_wavelets[channels[i]]= []
        filtered_wavelets[channels[i]].append(butter_delta(ica[i]))
        filtered_wavelets[channels[i]].append(butter_theta(ica[i]))
        filtered_wavelets[channels[i]].append(butter_beta(ica[i]))
        filtered_wavelets[channels[i]].append(butter_alpha(ica[i]))
        filtered_wavelets[channels[i]].append(butter_gamma(ica[i]))
    return filtered_wavelets

def eeg2CSV(recording_duration):
    # Duration for which data will gitbe recorded (in seconds)
    #recording_duration = 30  # 30 seconds
    # Initialize the Muse headset and start the LSL stream
    #Found device MuseS-5DE7, MAC Address 00:55:DA:B9:5D:E7
    if __name__ == "__main__":
        i = 0
        muses = list_muses()
        print(muses[0]['name'])
        j = 0
        for j in range(len(muses)):
            if muses[j]['name'] == 'MuseS-6453':
                i = j
        print("Initializing Muse headset...")
        print(muses[i]['name'])
        if muses[i] == None:
            print("NO HEADSET FOUND")
            exit
        try:
            wowcool = os.path.join(
            os.getcwd(),("recording_%s.csv" % strftime("%Y-%m-%d-%H.%M.%S", gmtime())))
            # Start recording the data
            print(f"Recording data for {recording_duration / 60} minutes...")
            print("Muse List")
            print(muses)
            print(muses[i]['address'])
        # writeCSV('outputCSV')
            record_direct(recording_duration, muses[i]['address'], filename = wowcool)
            # The data is recorded into a CSV file in the current directory. The filename is automatically generated.
        # print(f"Data has been recorded. Output file: {'owens.csv'}")
        finally:
            # Stop the LSL stream
            print("Successful Extraction to CSV")

            k = wowcool
        return wowcool

@app.route('/')
def baseFunc():
    return display_image()

@app.route('/image/')
def display_image():
    return render_template('display_image.html')

@app.route('/getdata/')
def passCSV():
   # wowcool = 'C:/Users/Computer/Desktop/ntab-hack/recording_2024-03-02-23.50.50.csv'
    #csv_path = os.path.join(
     #       os.getcwd(),("recording_%s.csv" % strftime("%Y-%m-%d-%H.%M.%S", gmtime())))
    #print(type(wowcool))

    directory = '.'
    files = os.listdir(directory)
    files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)
    most_recent_file = files[0]
    print(most_recent_file)

    return send_file(most_recent_file, as_attachment=True, mimetype='text/csv')
    # Path to your CSV file
    #csv_path = 'C:/Users/Computer/Desktop/ntab-hack/recording_2024-03-02-23.50.50.csv'
    csv_path = os.path.join(
            os.getcwd(),("recording_%s.csv" % strftime("%Y-%m-%d-%H.%M.%S", gmtime())))
    # Read the CSV file and parse its contents
    csv_data = []
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_data.append(row)

    # Render the HTML template and pass the CSV data
    return render_template('display_csv.html', csv_data=csv_data)


rec = input("Enter Desired Recording Length in seconds: ")
#print(list(eeg_wavelet_parser(eeg2CSV(int(rec))).keys()))
eeg_wavelet_parser(eeg2CSV(int(rec)))

#call model

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)