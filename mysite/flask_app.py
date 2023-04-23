from flask import Flask, jsonify, request, render_template, redirect, url_for
import pandas as pd
import os
import time
import sys
import re
import numpy as np
import feature_engineering
import requests
import csv
from bs4 import BeautifulSoup
import base64


app = Flask(__name__)

CURRENT_FILE = "No File Loaded"
CURRENT_DATAFRAME = None
@app.route('/player_stats',methods=['GET', 'POST'])
def player_stats():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save('tmp.csv')  # uploaded_file.filename)
            teams = feature_engineering.generate_entry_statistics('tmp.csv')

            filename_1 = 'static/images/team_1.jpg'
            filename_2 = 'static/images/team_2.jpg'
            return render_template('index.html', team_1=filename_1, team_2=filename_2)
    elif request.method == 'GET':
        return render_template('index.html')
@app.route('/',methods=['GET', 'POST'])
def index():
    global CURRENT_FILE, CURRENT_DATAFRAME
    team_1_url = ""
    team_2_url = ""
    if request.method == 'POST':
        #uploaded_file = request.files['file']
        if request.form.get('process') == "Submit":
            uploaded_file = request.files['file']
            if uploaded_file.filename != "":
                uploaded_file.save(uploaded_file.filename) #'tmp.csv')  # uploaded_file.filename)
                CURRENT_FILE=uploaded_file.filename
                CURRENT_DATAFRAME = pd.read_csv(CURRENT_FILE)
        #elif uploaded_file.filename != '':
        #   uploaded_file.save('tmp.csv')  # uploaded_file.filename)
        #    teams = feature_engineering.generate_entry_statistics('tmp.csv')
        elif request.form.get('process') == "Compute Entry Statistics":
            teams, teams_bytes = feature_engineering.generate_entry_statistics(df=CURRENT_DATAFRAME)
            if teams is None or teams_bytes is None:
                print("Error: Nothing computed")
            else:
                teams_bytes[0].seek(0)
                plot_url = base64.b64encode(teams_bytes[0].getvalue()).decode()
                team_1_url = "data:image/png;base64,{}".format(plot_url)
                teams_bytes[1].seek(0)
                plot_url = base64.b64encode(teams_bytes[1].getvalue()).decode()
                team_2_url = "data:image/png;base64,{}".format(plot_url)

        elif request.form.get('process') == "Compute Player Stats (Sean 2.0)":
            team_1, team_2 = feature_engineering.generate_summary(df=CURRENT_DATAFRAME)
            t1 = create_table(df=team_1)
            t2 = create_table(df=team_2)
            return render_template('index.html', t1=t1, t2=t2)

    #img = cv2.imread('static/images/entrystats_team_1.png')
    #_, im_bytes_np = cv2.imencode('.png', byte_img)
    #bytes_str = im_bytes_np.tobytes()



    entrystats_team_1 = 'static/images/entrystats_team_1.png'
    entrystats_team_2 = 'static/images/entrystats_team_2.png'
    return render_template('index.html', team_1=team_1_url, team_2=team_2_url, current_file=CURRENT_FILE)
    #return render_template('index.html', entrystats_team_1=entrystats_team_1, entrystats_team_2=entrystats_team_2)
    #return render_template('index.html', entrystats_team_1=entrystats_team_1, entrystats_team_2=entrystats_team_2)
    #return render_template('index.html')

@app.route('/entry_statistics', methods=['GET'])
def entry_statistics():
    entrystats_team_1 = 'static/images/entrystats_team_1.png'
    entrystats_team_2 = 'images/entrystats_team_2.png'
    return render_template('entrystats.html', entrystats_team_1=entrystats_team_1, entrystats_team_2=entrystats_team_2)


@app.route('/show_entry', methods=['GET', 'POST'])
def show_entry():
    filename_1 = 'static/images/team_1.jpg'
    filename_2 = 'static/images/team_2.jpg'
    return render_template('entrystats.html', team_1=filename_1, team_2=filename_2)

def create_table(df=None):
    print('Request for index page received')
    fragment = df.style.set_table_styles([{'selector': '',
                               'props': [('border',
                                          '10px solid yellow')]}]).render()
    fragment2 = df.style.set_table_styles([{"selector": "tbody tr:nth-child(even)", "props": [("background-color", "lightgrey")]}]).hide_index().render()

    return fragment2
@app.route('/show_table')
def show():
    print('Request for index page received')
    df = pd.read_csv('team_1.csv')
    res = df.to_html('templates/apa2.html', border=3)
    res = df.to_html('templates/apa2.html',
                     bold_rows = False, border =1,
                     index = False,
                     justify = 'left',
                     na_rep =' ')
    df = df.drop("Unnamed: 0", axis=1)
    # making a yellow border
    fragment = df.style.set_table_styles([{'selector': '',
                               'props': [('border',
                                          '10px solid yellow')]}]).render()
    fragment2 = df.style.set_table_styles([{"selector": "tbody tr:nth-child(even)", "props": [("background-color", "lightgrey")]}]).hide_index().render()

    return render_template('stats.html', pp=fragment2)

def print_csv(filename):
    df = pd.read_csv(filename)
    print(df)

@app.route('/generate_summary', methods=['GET', 'POST'])

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        print(uploaded_file.filename)
        uploaded_file.save('tmp.csv')#uploaded_file.filename)

        team_1, team_2 = feature_engineering.generate_summary(filename='tmp.csv')
        team_1.to_csv('team_1.csv')
        team_2.to_csv('team_2.csv')

        #feature_engineering.generate_entry_statistics('tmp.csv')

        #print(redirect(url_for('index')))
        #df = pd.read_csv('tmp.csv')
        #text = df.columns.values[0]
    df = pd.read_csv('team_1.csv')
    #return render_template(df.to_html('test.html'), name=text)
    #html = df.to_html('apa.html')
    #p = team_1.to_html(classes='data')

    # df = df.set_properties(
    #     **{'border': '1px black solid !important'}).set_table_styles([{
    #     'selector': '.col_heading',
    #     'props': 'background-color: green; color: black;'
    # }])

    render_template('stats.html', pp=df.to_html('apa.html', border=3))
    #return render_template('stats.html', pp=df.to_html('apa.html'))
    # with open("team_1.csv") as file:
    #     return render_template('stats.html', pp=df.to_html(border="2"))  # , titles=team_1.columns.values)
    # reader = csv.reader(file)
    # return df.to_html()

    return team_1.to_html(header="true", table_id="fo", index="false")
    #return render_template('stats.html', table=df.to_html(classes='data'), titles=df.columns.values)
    #return redirect(url_for('test'))


if __name__ == '__main__':
    #feature_engineering.generate_summary(filename='Swe_Sui.csv', team='Sweden Sweden')
    #teams = feature_engineering.generate_entry_statistics(filename='Swe_Sui.csv', team='Sweden Sweden')
    #sql.create_table()
    app.run(debug=True)