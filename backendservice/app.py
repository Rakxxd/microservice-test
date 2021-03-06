from flask import Flask,request,render_template,redirect
import psycopg2
import os
import time

DB_USER = "rakesh"
DB_PASSWORD = "ranjan"
DB = "user"
DB_HOST = "db"

app = Flask(__name__)

def init_tables():

    CREATE_TABLE = "CREATE TABLE IF NOT EXISTS REVIEWS (name TEXT NOT NULL, review TEXT NOT NULL)"
    conn = psycopg2.connect(host=DB_HOST,database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE)
    conn.commit()
    cursor.close()
    conn.close()

def add_review(name,review):

    ADD_REVIEW = "INSERT INTO REVIEWS (name,review) VALUES (%s,%s)"
    conn = psycopg2.connect(host=DB_HOST,database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(ADD_REVIEW,(name,review))
    conn.commit()
    cursor.close()
    conn.close()

def load_reviews():

    reviews = []

    LOAD_REVIEW = "SELECT * from REVIEWS"
    conn = psycopg2.connect(host=DB_HOST,database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(LOAD_REVIEW)
    results = cursor.fetchall()

    for row in results:
        reviews.append((row[0],row[1]))
    cursor.close()
    conn.close()

    return reviews

@app.route("/",methods=["POST", "GET"])
def homeview():
    return render_template("index.html")

@app.route("/rply",methods=["POST","GET"])
def viewrply():
    return {"success":True}

@app.route("/reviews/add",methods=["POST"])
def addreview():

    
    name = request.form["name"]
    review = request.form["review"]

    add_review(name,review)

    return {"success":True}

@app.route("/reviews/list",methods=["POST"])
def listreviews():

    reviews = load_reviews()

    return {"success":True,"list":reviews}

#Deferred execution by 20 seconds to allow database to initialize
time.sleep(20)
init_tables()
app.run(host="0.0.0.0",port=5000)
