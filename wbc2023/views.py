from django.shortcuts import render, redirect  # ,徐尉庭增加 redirect
from django.contrib.auth import update_session_auth_hash  # 徐尉庭增加
from django.contrib.auth.forms import PasswordChangeForm  # 徐尉庭增加
from .crawler import 生辰八字主業  # 徐尉庭增加
# Create your views here.
import re
import pyrebase
from random import randint
from django.core.mail import send_mail
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import db
from django.http import HttpResponse


config = {
     "apiKey": "AIzaSyAZoUH8mJsS9h7u2kff5eSU38Dmckm0olY",
    "authDomain": "wbc2023-8cd43.firebaseapp.com",
    "databaseURL": "https://wbc2023-8cd43-default-rtdb.firebaseio.com",
    "projectId": "wbc2023-8cd43",
    "storageBucket": "wbc2023-8cd43.appspot.com",
    "messagingSenderId": "1057594948984",
    "appId": "1:1057594948984:web:13559062c6c74406c91c8d",


    #   'apiKey': "AIzaSyCE-vHKK0MNrCcy-KAtK__0HW9hrRXM_M4",
    #   'authDomain': "test1-bfab0.firebaseapp.com",
    #   'projectId': "test1-bfab0",
    #   'storageBucket': "test1-bfab0.appspot.com",
    #   'messagingSenderId': "863152004967",
    #   'appId': "1:863152004967:web:85cd44c032569b84d799c2",
    #   'measurementId': "G-8ED4G9L00T",
    #   #URL 路徑為資料庫網址
    #   'databaseURL': "https://test1-bfab0-default-rtdb.firebaseio.com",
}
if not firebase_admin._apps:
    # 設定 Firebase Admin SDK 的認證憑證
    cred = credentials.Certificate(
        "wbc2023-8cd43-firebase-adminsdk-ndv66-5c84199d79.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://wbc2023-8cd43-default-rtdb.firebaseio.com'
    })

firebase = pyrebase.initialize_app(config)
database = firebase.database()
authe = firebase.auth()


def signIn(request):
    return render(request, "firebaseLogin.html")


def home(request):
    email = request.POST.get('email')
    return render(request, "firebaseHome.html", {"email": email})


def inquire(request):
    if request.method == 'POST':
        if 'search_horoscope' in request.POST:
            return redirect('birthday')

    return render(request, 'inquire.html')


def postsignIn(request):
    email = request.POST.get('email')
    pasw = request.POST.get('pass')
    a = email.split(".")
    email_t = a[0]
    # return HttpResponse("{}".format(email_t))
    try:
        # if there is no error then signin the user with given email and password
        user = authe.sign_in_with_email_and_password(email, pasw)
    except:
        message = "Invalid Credentials!!Please Check your Data"
        return render(request, "firebaseLogin.html", {"message": message})
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    request.session['email_t'] = email_t  # 存储 email_t
    request.session['email'] = email
    return render(request, "firebaseHome.html", {"email": email_t})
    # return HttpResponse("{}".format(email_t))


def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request, "firebaseLogin.html")


def signUp(request):
    return render(request, "firebaseRegistration.html")


def postsignUp(request):
    # global globalemail
    email = request.POST.get('email')
    passs = request.POST.get('pass')
    name = request.POST.get('name')
    # globalemail = email
    otp = randint(000000, 999999)
    try:
        user = authe.create_user_with_email_and_password(email, passs)
        uid = user['localId']
        dict1 = {"otp": otp, "email": email}
        a = email.split('.')
        database.child('Humandata').child(a[0]).push(dict1)
        message = "This is your one-time OTP number:"+str(otp)
        send_mail("帳號驗證", message,
                  "yuanhsikung@gmail.com", [email, 'yuanhsikung@gmail.com'])
    except:
        message = "本帳號已存在，請確認！！"
        return render(request, "firebaseLogin.html", {"message": message})
    t_email = a[0]
    return render(request, "verify.html", {"email": t_email})


# def validate(request):
#     email_t = request.POST.get('email')
#     # return HttpResponse("{}".format(email_t))
#     user_otp = request.POST.get('otp')
#     ref = db.reference('Humandata')

#     # 讀取資料
#     data = ref.get()
#     for m_t in data.keys():
#         if m_t == email_t:
#             # return HttpResponse("成功")
#             for d_t in data[email_t].keys():
#                 otp = int(data[email_t][d_t]["otp"])
#                 temp_otp = int(user_otp)
#                 if otp != temp_otp:
#                     return render(request, "verifyE.html", {"email": email_t})
#                 else:
#                     return render(request, "birthday.html", {"email": email_t})

#         else:
#             continue
def validate(request):
    email_t = request.POST.get('email')
    user_otp = request.POST.get('otp')
    ref = db.reference('Humandata')

    data = ref.get()
    for m_t in data.keys():
        if m_t == email_t:
            for d_t in data[email_t].keys():
                otp = int(data[email_t][d_t]["otp"])
                temp_otp = int(user_otp)
                if otp != temp_otp:
                    return render(request, "verifyE.html", {"email": email_t, "invalid": True})
                else:
                    return render(request, "birthday.html", {"email": email_t})

    # 如果找不到电子邮件，或者循环结束后仍未找到匹配项，则显示错误消息。
    return render(request, "verifyE.html", {"email": email_t, "invalid": True})
    


def words82(request):
    email_t = request.session.get('email_t')
    # return HttpResponse("{}".format(email_t))
    ref = db.reference('Humandata/')
    # database.child('Humandata').child(email_t)
    data = ref.get()
    # return HttpResponse("{}".format(data))
    Year = data[email_t]["year"]
    Month = data[email_t]["month"]
    Day = data[email_t]["day"]
    Hour = data[email_t]["time"]
    sex = data[email_t]["gender"]
    horoscope, nativityAnaly, godOfJoy = words8(Year, Month, Day, Hour, sex)
    # b = str(nativityAnaly)
    # return HttpResponse(b)
    # return render(request, "birthday_result.html", {"email": email_t})
    return render(request, "birth_result.html", {"email": email_t, "horoscope": horoscope, "nativityAnaly": nativityAnaly})


def table(request):
    email_t = request.session.get('email_t')
    # return HttpResponse("{}".format(email_t))
    ref = db.reference('完整公司資料_2')
    data = ref.get()
    ref2 = db.reference('Humandata/{}/godOfJoy'.format(email_t))
    reference_list = ref2.get()
    company_data = []
    for key1 in reference_list:
        if key1 in data:
            for value in data[key1].keys():
                company_data.append({
                    '屬性': data[key1][value]['屬性'],
                    '股票代碼': data[key1][value]['股票代碼'],
                    '公司名稱': data[key1][value]['公司名稱'],
                    '所屬產業': data[key1][value]['所屬產業'],
                    'New_ROE': data[key1][value]['New_ROE'],
                    'Next_ROE': data[key1][value]['Next_ROE'],
                    'statuses': data[key1][value]['statuses']
                })
    return render(request, 'table.html', {'data': company_data, "email": email_t})




def words8(Year, Month, Day, Hour, sex):
    import re
    import requests
    from bs4 import BeautifulSoup

    session = requests.session()
    myHeaders = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

    payload1 = {
        "_Year": Year,
        "_Month": Month,
        "_Day": Day,
        "_Hour": Hour,
        "_sex": sex,
        "_earth": "N",
        "_method": "A",
        "txt_eight": "",
        "txt_twelve": "",
        "txt_sun_date": "",
        "txt_moon_date": "",
        "txt_act": "",
        "job_kind": "A1",
    }

    a = session.post("https://www.dearmoney.com.tw/eightwords/result_eight_words_page",
                     data=payload1, headers=myHeaders)
    a.encoding = 'utf-8'
    soup1 = BeautifulSoup(a.text, 'html.parser')

    if a.status_code == 200:
        main = soup1.select_one("div.ResultContent")
        main_str = str(main)
        pattern = re.compile(r'<tr align="center"><td bgcolor="#FFFFFF" height="30"><span style="font-size: 13px"><font color="#660033">劍靈命理網<\/font><\/span> <span style="font-size: 13px"><font color="#330066">https:\/\/www\.dearmoney\.com\.tw\/<\/font><\/span><\/td><\/tr>')
        main_str = pattern.sub('', main_str)
        pattern1 = re.compile(r'劍靈八字命盤批算結果</span>\n</div>')
        main_list = pattern1.split(main_str)
        main_str = main_list[-1]
        pattern2 = re.compile(
            r'<div class="row justify-content-center m-0 p-0 my-3">')
        main_list = pattern2.split(main_str)
        horoscope = "{}\n</div>\n</div>".format(main_list[0])
        pattern3 = re.compile(
            r'<div class="row m-0 justify-content-center mt-5 mb-3">')
        main_list2 = pattern3.split(main_list[1])
        nativityAnalysis = '<div class="row m-0 justify-content-center mt-5 mb-3">{}'.format(
            main_list2[1])
        pattern4 = re.compile(r'</font>運，忌')
        main_list3 = pattern4.split(main_list2[2])
        pattern5 = re.compile(r'行運喜<font color="#FF3300">')
        main_list4 = pattern5.split(main_list3[0])
        tmepGod = main_list4[1]
        godOfJoy = []
        for i in tmepGod:
            godOfJoy.append(i)

        return horoscope, nativityAnalysis, godOfJoy


def birthdaysave(request):
    # email = database.child('Humandata').child(globalemail).get().val()
    email_t = request.POST.get('email')
    born = request.POST.get('birthdate')
    born_split = born.split('-')
    year = born_split[0]
    month = born_split[1]
    day = born_split[2]
    time = request.POST.get('time')
    gender = request.POST.get('gender')
    horoscope, nativityAnalysis, godOfJoy = words8(
        year, month, day, time, gender)
    godOfJoy_t = str(godOfJoy)
    # return HttpResponse("{}+{}".format(godOfJoy_t, godOfJoy))
    dict2 = {"year": year, "month": month,
             "day": day, "time": time, "gender": gender, "godOfJoy": godOfJoy_t}
    database.child('Humandata').child(email_t).set(email_t)
    database.child('Humandata').child(email_t).update(dict2)
    return render(request, "firebaseLogin.html")


def modifydatas(request):
    email_t = request.session.get('email_t')
    return render(request, "birthdaysave.html", {"email": email_t})


def modifysave(request):
    email_t = request.session.get('email_t')
    born = request.POST.get('birthdate')
    born_split = born.split('-')
    year = born_split[0]
    month = born_split[1]
    day = born_split[2]
    time = request.POST.get('time')
    gender = request.POST.get('gender')
    horoscope, nativityAnalysis, godOfJoy = words8(
        year, month, day, time, gender)
    godOfJoy_t = str(godOfJoy)
    dict2 = {"year": year, "month": month,
             "day": day, "time": time, "gender": gender, "godOfJoy": godOfJoy_t}
    database.child('Humandata').child(email_t).update(dict2)
    return render(request, "firebaseHome.html", {"email": email_t})


# def modifydatas(request):
#     email_t = request.POST.get('email')
#     born = request.POST.get('birthdate')
#     born_split = born.split('-')
#     year = born_split[0]
#     month = born_split[1]
#     day = born_split[2]
#     time = request.POST.get('time')
#     gender = request.POST.get('gender')
#     horoscope, nativityAnalysis, godOfJoy = words8(
#         year, month, day, time, gender)
#     godOfJoy_t = str(godOfJoy)
#     dict2 = {"year": year, "month": month,
#              "day": day, "time": time, "gender": gender, "godOfJoy": godOfJoy_t}
#     database.child('Humandata').child(email_t).update(dict2)
#     return render(request, "firebaseLogin.html", {"email": email_t})


def postReset(request):
    email = request.session.get('email')
    # return HttpResponse("{}".format(email))
    try:
        authe.send_password_reset_email(email)
        message = "A email to reset password is succesfully sent"
        return render(request, "firebaseReset.html", {"msg": message})
    except:
        message = "Something went wrong, Please check the email you provided is registered or not"
        return render(request, "firebaseReset.html", {"msg": message})


# def table(request):
#     email_t = request.POST.get("email")
#     ref = db.reference('完整公司資料_2')
#     data = ref.get()  # 数据
#     ref2 = db.reference('Humandata/{}/godOfJoy'.format(email_t))
#     reference_list = ref2.get  # 数据
#     return render(request, 'table.html', {'data': data, 'reference_list': reference_list, "email": email_t})

def home(request):
    email_t = request.session.get('email_t')
    return render(request, "firebaseHome.html", {"email": email_t})
