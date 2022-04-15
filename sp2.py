from flask import Flask, redirect, url_for, render_template, request, session
import datetime
from datetime import datetime
from datetime import timedelta
import mysql.connector
import requests
from mysql.connector import Error
app = Flask(__name__)
app.secret_key = "zineb_laouzi_hello"
#giving the oportunity to be remembered for 60 minutes in the same device
app.permanent_session_lifetime = timedelta(minutes=60)


@app.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        print("i am here")
        return redirect(url_for("login"))
    #a welcome screen together with a button which directs to the login page
    return render_template("welcome_screen.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        #getting data from the form in the html file
        session.permanent = True
        user = request.form["username"]
        passw = request.form["password"]
        #connecting with the database
        connection = mysql.connector.connect(host='localhost',
                                         database='group3',
                                         user='group3',
                                         password='cSHhKD')
        if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
        if "user" in session:
            return redirect(url_for("user"))
        #deciding on the type of user
        #a lot if statements are associated to this function 
        #ech of the redirects to the proper html based on the type of user
        mySql_insert_query = """SELECT EXISTS(SELECT * FROM Visitors WHERE visitor_name=%s AND visitor_password=%s);"""
        mySql_insert_query_1 = """SELECT EXISTS(SELECT * FROM Places WHERE place_name=%s AND place_password=%s);"""
        mySql_insert_query_2 = """SELECT EXISTS(SELECT * FROM Hospitals WHERE hospital_name=%s AND hospital_password=%s);"""
        mySql_insert_query_3 = """SELECT EXISTS(SELECT * FROM Agents WHERE agent_name=%s AND agent_password=%s);"""
        record = (user, passw)
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query, record)
        result = cursor.fetchall()
        if(result[0][0] == 1):
            cursor.close()
            connection.commit()
            session["user"] = user
            return redirect(url_for("user"))
        cursor.execute(mySql_insert_query_1, record)
        result = cursor.fetchall()
        if(result[0][0] == 1):
            cursor.close()
            connection.commit()
            return redirect(url_for("place", place_name=user))
        cursor.execute(mySql_insert_query_2, record)
        result = cursor.fetchall()
        if(result[0][0] == 1):
            cursor.close()
            connection.commit()
            return redirect(url_for("hospital", hospital_name=user))
        cursor.execute(mySql_insert_query_3, record)
        result = cursor.fetchall()
        if(result[0][0] == 1):
            cursor.close()
            connection.commit()
            return redirect(url_for("agent", agent_name=user))
        connection.commit()
        cursor.close()
        #if the user was not found in any of the tables => a USER_NOT_FOUND.HTML will open
        return render_template("user_not_found.html")
    return render_template("log_in.html")


@app.route("/sign_up_visitor", methods=["POST", "GET"])
def sign_up_as_visitor():
    if request.method == "POST":
        #getting the data from the form in the html file
        user = request.form["visitor_name"]
        passw = request.form["visitor_password"]
        ip_adr = request.remote_addr
        adr = request.form["visitor_address"]
        phone_nr = request.form["phone_number"]
        mail = request.form["email"]
        sick = "negative"
        #connecting to the database
        connection = mysql.connector.connect(host='localhost',
                database='group3',
                user='group3',
                password='cSHhKD')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
        #finding out if the user already exists
        mySql_insert_query = "SELECT EXISTS(SELECT * FROM Visitors WHERE visitor_name=%s);"
        cursor = connection.cursor()
        record = (user,)
        cursor.execute(mySql_insert_query, record)
        result = cursor.fetchall()
        print(result)
        print(result[0][0])
        if result[0][0] == 1:
            return render_template("user_already_exists.html")
        #if the user does not exists, we insert him into the table
        mySql_insert_query = """INSERT INTO Visitors (visitor_name,visitor_password,ip_address,visitor_address,phone_number,email,infect_status)
                                    VALUES (%s,%s,%s,%s,%s,%s,%s);"""
        record = (user, passw, ip_adr, adr, phone_nr, mail, sick)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        cursor.close()
        return redirect(url_for("user"))
    return render_template("sign_up_visitor.html")


@app.route("/sign_up_place", methods=["POST", "GET"])
def sign_up_as_place():
    if request.method == "POST":
        name = request.form["place_name"]
        adr = request.form["place_address"]
        passw = request.form["place_password"]
        qr_str = "https://10.72.1.14:8080/timer"+name
        connection = mysql.connector.connect(host='localhost',
                database='group3',
                user='group3',
                password='cSHhKD')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
        #finding out if the place exists
        mySql_select_query = """SELECT EXISTS(SELECT * FROM Places WHERE place_name=%s);"""
        record = (name,)
        cursor = connection.cursor()
        cursor.execute(mySql_select_query, record)
        result = cursor.fetchall()
        if result[0][0] == 1:
            return render_template("user_already_exists.html")
        #if the place does not exists, than we enter that place into the database
        mySql_insert_query = """INSERT INTO Places (place_name,place_address,place_password,qr_code_string)
                                    VALUES (%s,%s,%s,%s);"""
        record = (name, adr, passw, qr_str)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        cursor.close()
        return redirect(url_for("place", place_name=name))
    return render_template("sign_up_place.html")


@app.route("/agent/sign_up_hospital", methods=["POST", "GET"])
def sign_up_as_hospital():
    if request.method == "POST":
        name = request.form["hospital_name"]
        passw = request.form["hospital_password"]
        connection = mysql.connector.connect(host='localhost',
                database='group3',
                user='group3',
                password='cSHhKD')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
        #finding out if the hospital is in the database
        mySql_select_query = """SELECT EXISTS(SELECT * FROM Visitors WHERE visitor_name=%s);"""
        record = (name,)
        cursor = connection.cursor()
        cursor.execute(mySql_select_query, record)
        result = cursor.fetchall()
        if result[0][0] == 1:
            return render_template("user_already_exists.html")
        #if the place does not exists, than we enter that place into the database
        mySql_insert_query = """INSERT INTO Hospitals (hospital_name,hospital_password)
                                    VALUES (%s,%s);"""
        record = (name, passw)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        cursor.close()
        return render_template("new_hospital.html", data=name)
    return render_template("sign_up_hospital.html")

#the visitor default page(scanning)
#is checked if a session exists and if not the user has to log in again
@app.route("/user", methods=["POST", "GET"])
def user():
    if "user" in session:
        user = session["user"]
    else:
        return redirect(url_for("login"))
    if request.method == "POST":
        next_webpage = request.form["final_result"]
        print(next_webpage)
        return redirect(next_webpage)
    return render_template("scanning.html", data=user)

#the default webpage for the place containing place_name and qr_code
@app.route("/place/<place_name>", methods=["POST", "GET"])
def place(place_name):
    return render_template("place.html", data=place_name)


@app.route("/hospital/<hospital_name>", methods=["POST", "GET"])
def hospital(hospital_name):
    connection = mysql.connector.connect(host='localhost',
                                         database='group3',
                                         user='group3',
                                         password='cSHhKD')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
    #getting access to all the users in the database 
    cursor = connection.cursor()
    mySql_insert_query = """SELECT visitor_name,infect_status FROM Visitors;"""
    cursor.execute(mySql_insert_query)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    if request.method == "POST":
        user = request.form["user_name"]
        inf_stat = request.form["infect_status"]
        cursor = connection.cursor()
        #updating the infection status of the person
        mySql_insert_query = """UPDATE Visitors SET infect_status=%s WHERE visitor_name=%s"""
        record = (inf_stat, user)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        cursor.close()
        return render_template("user_updated.html", data_1=user, data_2=inf_stat)
    return render_template("hospital.html", data=result)


@app.route("/agent/<agent_name>", methods=["POST", "GET"])
def agent(agent_name):
    connection = mysql.connector.connect(host='localhost',
                                         database='group3',
                                         user='group3',
                                         password='cSHhKD')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
    cursor = connection.cursor()
    #getting the data of all the users, since that is a property of the agent
    mySql_insert_query = """SELECT visitor_name,infect_status,visitor_address,phone_number,email FROM Visitors;"""
    cursor.execute(mySql_insert_query)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template("agent.html", data=result, data_1=agent_name)


@app.route("/agent/<agent_name>/search_by_people", methods=["GET", "POST"])
def search_by_people(agent_name):
    connection = mysql.connector.connect(
        host='localhost', database='group3', user='group3', password='cSHhKD')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
    if request.method == "POST":
        visitor_name = request.form["visitor_name"]
        start_time = request.form["start_time"]
        finish_time = request.form["finish_time"]
        #when searching for a specific person , you will get the entire set of datas of that person and the list of all the places visited in the time interval
        mySql_insert_query_1 = """SELECT visitor_name,ip_address,visitor_address,phone_number,email,infect_status FROM Visitors Where Visitors.visitor_name = %s"""
        mySql_insert_query_2 = """SELECT place_name FROM VisitorToPlaces Where VisitorToPlaces.visitor_name = %s AND VisitorToPlaces.enter_time > %s AND VisitorToPlaces.exit_time < %s ;"""
        record_1 = (visitor_name,)
        record_2 = (visitor_name, start_time, finish_time)
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query_1, record_1)
        result_1 = cursor.fetchall()
        cursor.execute(mySql_insert_query_2, record_2)
        result_2 = cursor.fetchall()
        return render_template("search_people_result.html", data_1=result_1, data_2=result_2)
    return render_template("search_people.html")


@app.route("/agent/<agent_name>/search_by_place", methods=["GET", "POST"])
def search_by_place(agent_name):
    connection = mysql.connector.connect(host='localhost',
                                         database='group3',
                                         user='group3',
                                         password='cSHhKD')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
    if request.method=="POST":
        place_name = request.form["place_name"]
        start_time = request.form["start_time"]
        finish_time = request.form["finish_time"]
        #when searching for a specific place, you will get the entire set of datas of that place and the list of all the people that were there in the time interval
        mySql_insert_query_1 = """SELECT place_name,place_address,place_password,qr_code_string FROM Places Where Places.place_name = %s"""
        mySql_insert_query_2 = """SELECT visitor_name FROM VisitorToPlaces Where VisitorToPlaces.place_name = %s AND VisitorToPlaces.enter_time > %s AND VisitorToPlaces.exit_time < %s ;"""
        record_1 = (place_name,)
        record_2 = (place_name, start_time, finish_time)
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query_1,record_1)
        result_1=cursor.fetchall()
        cursor.execute(mySql_insert_query_2,record_2)
        result_2=cursor.fetchall()
        return render_template("search_place_result.html",data_1=result_1,data_2=result_2)
    return render_template("search_place.html")


#after scanning the qr_code , you will get the timer and the button to LOG_OUT
flag=1
formatted_start=None
@app.route("/timer/<place_name>", methods=["POST", "GET"])
def timer(place_name):
    if "user" in session:
        user = session["user"]
    else:
        return redirect(url_for("login"))
    global formatted_start
    global flag
    if flag == 1:
        start_time = datetime.now()
        #getting the starting time
        formatted_start = start_time.strftime('%Y-%m-%d %H:%M:%S')
        flag=0
    if request.method=="POST":
        end_time = datetime.now()
        #getting the ending time
        formatted_end = end_time.strftime('%Y-%m-%d %H:%M:%S')
        flag=1
        connection = mysql.connector.connect(host='localhost',
                database='group3',
                user='group3',
                password='cSHhKD')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
        #adding the meeting and the time interval in the database
        mySql_insert_query = """INSERT INTO VisitorToPlaces (visitor_name,place_name,enter_time,exit_time)
                                    VALUES (%s,%s,%s,%s);"""
        record_1=session["user"]
        record_2=place_name
        cursor = connection.cursor()
        record=(record_1,record_2,formatted_start,formatted_end)
        cursor.execute(mySql_insert_query,record)
        connection.commit()
        cursor.close()
        return redirect(url_for("user"))
    return render_template("timer.html",data=place_name)
@app.route("/logout", methods=["POST", "GET"])
def logout():
    #loging out as a visitor => ending the session
    session.pop("user", None)
    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(host="10.72.1.14", port=8080, debug=True, ssl_context='adhoc')
