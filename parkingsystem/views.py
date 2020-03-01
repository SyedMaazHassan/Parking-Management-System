from django.contrib.sessions.backends import db
from django.shortcuts import render
import sqlite3

import os
# Create your views here.
from firstproject import settings

account_holder = None
all_book_cars = None

def main_page(request):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("DELETE FROM AH")
    conn.commit()
    return render(request, 'main_page.html')

def form_login(request):
    return render(request, 'form_login.html')

def form_signup(request):
    return render(request, 'form_signup.html')

def parking_map(request):
    n = [1,3,7,12,35,17,14,26,21,29,32]
    return render(request, 'parking_map.html', {'number':n})

def signup_view(request):
    if(request.POST):
        signup_data = request.POST.dict()
        username = signup_data.get("name")
        email = signup_data.get("email")
        password = signup_data.get("pass1")
        password2 = signup_data.get("pass2")
        if password == password2:
            print(username, email, password)
            registration(username, email, password)
            print('successfully registered')
            return render(request, 'form_login.html')
        else:
            return render(request, 'form_signup.html', {'notsame':1})


def login_view(request):
    if(request.POST):
        login_data = request.POST.dict()
        email = str(login_data.get("email"))
        password = str(login_data.get("pass"))
        mychecking = login_check(email, password)
        if mychecking == 0:
            return render(request, 'form_login.html', {'notFound': 1})
        else:
            account_holder = mychecking
            setAccountHolder(mychecking[0], mychecking[1], mychecking[2])
            print(mychecking)
            all_book_cars = booked_cars()
            print(all_book_cars)

            conn = sqlite3.connect('db.sqlite3')
            c = conn.cursor()
            c.execute("SELECT * FROM BOOK WHERE id='{}'".format(mychecking[0]))
            t = c.fetchall()
            conn.commit()
            if len(t)>0:
                t = t[-1]
                proper_msg = "Dear {}! slot {} has been booked for you.".format(mychecking[1],t[1])
            else:
                proper_msg = "Dear {}! choose any of available slots for your vehicle.".format(mychecking[1])
            context = {'nameP':mychecking[1], 'pm':proper_msg, 'number':all_book_cars, 'notFound':0}
            return render(request, 'parking_map.html', context)

def logout_view(request):
    logout(getAccountholder())
    return render(request, 'form_login.html')

def booking_view(request):
    if(request.POST):
        booking_data = request.POST.dict()
        vehicle_no = str(booking_data.get("vno"))
        pl_number = str(booking_data.get("plno"))
        date = str(booking_data.get("date"))
        st = str(booking_data.get("st"))
        et = str(booking_data.get("et"))
        isBooked = checkBook(pl_number)
        account_holder = getAccountholder()
        if isBooked == 0:
            doBook(pl_number)
            whoBook(account_holder[0], pl_number)
            makeHistory(date, pl_number, account_holder[1], account_holder[0], vehicle_no, st, et)
            proper_msg = "Dear {}! slot {} has been booked for your vehicle ({})".format(account_holder[1],pl_number,vehicle_no)
            all_book_cars = booked_cars()
            print(list(all_book_cars))
            context = {'nameP': account_holder[1], 'pm':proper_msg, 'number':all_book_cars, 'msg':''}
            return render(request, 'parking_map.html', context)
        else:
            proper_msg = "Dear {}! choose any of available slots for your vehicle.".format(account_holder[1])
            all_book_cars = booked_cars()
            context = {'nameP': account_holder[1], 'pm':proper_msg, 'number':all_book_cars, 'msg':"PL already booked or you entered a wrong PL no."}
            return render(request, 'parking_map.html', context)

def bringout_view(request):
    account_holder = getAccountholder()
    which_book = getPLNObyPerson(account_holder[0])

    if which_book:
        unbook(which_book, account_holder[0])

    proper_msg = "Dear {}! choose any of available slots for your vehicle.".format(account_holder[1])
    all_book_cars = booked_cars()
    context = {'nameP': account_holder[1], 'pm': proper_msg, 'number': all_book_cars,
               'msg': "PL already booked or you entered a wrong PL no."}
    return render(request, 'parking_map.html', context)

def feedback_view(request):
    account_holder = getAccountholder()
    fb = request.POST.dict()
    myfeedback = str(fb.get("fbck"))
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO FB(name, feedback) VALUES {}".format(str((account_holder[1], myfeedback))))
    conn.commit()

    proper_msg = "Dear {}! choose any of available slots for your vehicle.".format(account_holder[1])
    all_book_cars = booked_cars()
    context = {'nameP': account_holder[1], 'pm': proper_msg, 'number': all_book_cars,
               'msg': ""}
    return render(request, 'parking_map.html', context)




def registration(name, email, password):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute("INSERT INTO USERS(name,email,password) \
          VALUES {}".format(str((name, email, password))))

    conn.commit()

def login_check(mail, pas):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT * FROM USERS")
    a = c.fetchall()
    conn.commit()
    found = 0
    for i in a:
        if i[2] == mail and i[3] == pas:
            print(i)
            found = i
    return found

def getPLNObyPerson(person_id):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT * FROM BOOK WHERE id='{}'".format(person_id))
    a = c.fetchall()
    if len(a)>0:
        a = a[-1]
        return a[1]
    else:
        return None

def booked_cars():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT pl_no FROM CARS WHERE isBook='1'")
    a = c.fetchall()
    b = []
    for i in a:
        b.append(i[0])
    print("ye he asal b",b)
    conn.commit()
    return b



    # conn = sqlite3.connect('db.sqlite3')
    # c = conn.cursor()
    #
    # for i in range(1, 37):
    #     c.execute("INSERT INTO CARS(pl_no, isBook) \
    #     VALUES {}".format(tuple((i, 0))))
    #
    # conn.commit()
def unbook(id_car, accountant):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("UPDATE CARS SET isBook=0 WHERE pl_no='{}'".format(id_car))
    c.execute("DELETE FROM BOOK WHERE id='{}'".format(accountant))
    conn.commit()

def doBook(id_car):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("UPDATE CARS SET isBook=1 WHERE pl_no={}".format(id_car))
    conn.commit()

def checkBook(id_car):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT * FROM CARS WHERE isBook=1")
    a = c.fetchall()
    conn.commit()
    f = 0
    for i in a:
        if i[0] == id_car:
            f=1
    return f

def whoBook(id_person, pl_no):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO BOOK(id,pl_no) \
              VALUES {}".format(str((id_person, pl_no))))
    conn.commit()

def makeHistory(date,pl_no,book_by,person_ID,vehicle_no,from_time,to_time):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute("INSERT INTO HISTORY(date,pl_no,book_by,person_ID,vehicle_no,from_time,to_time) \
          VALUES {}".format(str((date,pl_no,book_by,person_ID,vehicle_no,from_time,to_time))))

    conn.commit()

def setAccountHolder(id, name, email):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO AH(id,name,email) VALUES {}".format(str((id, name, email))))
    conn.commit()

def getAccountholder():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT * FROM AH")
    a = c.fetchall()
    conn.commit()
    return a[-1]


def logout(account_holder):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("DELETE FROM AH WHERE id='{}'".format(account_holder[0]))
    conn.commit()




