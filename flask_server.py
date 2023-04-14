from flask import Flask, render_template
import mysql.connector
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib

import pandas as pd
matplotlib.use('agg')
app = Flask(__name__)

mydb= mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'dudfuf123',
    port= '3306',
    database = 'db_hknu'
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generic')
def generic():
    cur = mydb.cursor()
    cur.execute("SELECT id, label, timee, COUNT(*) FROM db_car GROUP BY id, label, timee ORDER BY id DESC LIMIT 1000")
    fetchdata = cur.fetchall()
    cur.close()
    times = [datetime.strptime(str(row[2]), '%H:%M:%S').hour for row in fetchdata]
    values = [row[1] for row in fetchdata]
    plt.plot(times, values)
    plt.title('Data by hour')
    plt.xlabel('Hour')
    plt.ylabel('Count')

    # Save the plot to a file
    plt.savefig('static/images/plot.png')

    return render_template('generic.html', plot_url='static/images/plot.png',data=fetchdata)

@app.route('/elements')
def elements():
    cur = mydb.cursor()
    cur.execute("SELECT id, label, timee, COUNT(*) FROM db_person GROUP BY id, label, timee ORDER BY id DESC LIMIT 1000")
    fetchdata = cur.fetchall()
    cur.close()
    times = [datetime.strptime(str(row[2]), '%H:%M:%S').hour for row in fetchdata]
    values = [row[1] for row in fetchdata]
    plt.plot(times, values)
    plt.title('Data by hour')
    plt.xlabel('Hour')
    plt.ylabel('Count')

    # Save the plot to a file
    plt.savefig('static/images/plot.png')

    return render_template('elements.html', plot_url='static/images/plot.png', data=fetchdata)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
