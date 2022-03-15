from cProfile import label
import imp
import requests
import json
from flask import Flask, jsonify, request
from typing import List, Dict
import mariadb

app = Flask(__name__)


config = {'host': '172.29.0.2','port': 3306,'user': 'me','password': 'yourSAFEpassword','database': 'auth_details'}

@app.route('/')
def welcome():
    return f'Hello World'





#SignUp
@app.route('/signUpNew', methods = ['POST'])
def signUpNew():
    dict={
        "lead_id": 30,
        "goal": "Weight Loss",
        "diet": "Flexible",
        "name": "nish",
        "email": "nishil@gmai.com",
        "phone": "9821251354",
        "age": 24,
        "height_feet": 5,
        "height_inches": 8,
        "weight": 77,
        "activities": "No Physical Activity",
        "meal_preference": "Eggetarian",
        "egg_in_bread": "Yes",
        "start_date": "28/06/2021",
        "no_of_days": 30,
        "whatsapp_consent": 1,
        "body_fat": "Normal",
        "last_page": "physical-activities",
        "notes": "I want good food only",
        "dont_eat_egg_on": [
            "tue"
        ],
        "doesnt_eat_meat": [
            "mutton"
        ],
        "dont_eat_nonveg_on": [
            "thu"
        ],
        "meals": [
            "lunch"
        ],
        "addresses": {
            "is_evening_address_same": "false",
            "is_weekend_address_same": "false",
            "is_weekend_evening_address_same": "false",
            "default": {
            "street": "This is my Address",
            "street_2": "This is new Address",
            "pincode": "400050",
            "landmark": "Devi Temple",
            "city": "Mumbai",
            "state": "Maharashtra"
            },
            "evening_address": {
            "street": "This is my Address",
            "street_2": "This is new Address",
            "pincode": "400050",
            "landmark": "Devi Temple",
            "city": "Mumbai",
            "state": "Maharashtra"
            },
            "weekend_address": {
            "street": "This is my Address",
            "street_2": "This is new Address",
            "pincode": "400050",
            "landmark": "Devi Temple",
            "city": "Mumbai",
            "state": "Maharashtra"
            },
            "weekend_evening_address": {
            "street": "This is my Address",
            "street_2": "This is new Address",
            "pincode": "400050",
            "landmark": "Devi Temple",
            "city": "Mumbai",
            "state": "Maharashtra"
            }
        }
        }

    headers={
        'Content-Type': 'application/json'
        }

    url= "https://erp-test.fooddarzee.com/api/signUpNew"
    response = requests.post(url, data=json.dumps(dict), headers=headers)

    return response.json()





#Login
@app.route('/login', methods = ['POST'])
def login():
    url="https://erp-test.fooddarzee.com/api/login"
    input={
        "phone": 9920045322
    }
    header= {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(input), headers=header, verify= False)
    return response.json()



@app.route('/resendOtp', methods = ['POST'])
def resendOtp():
    url="https://erp-test.fooddarzee.com/api/resendOtp"
    input={
        "phone": 9920045322
    }
    header= {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(input), headers=header, verify= False)
    return response.json()



@app.route('/verifyOtp', methods = ['POST'])
def verifyOtp():
    url="https://erp-test.fooddarzee.com/api/verifyOtp"
    input={
        "phone": 9920045322,
        "otp": 9999
    }
    header= {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(input), headers=header, verify= False)
    if (request.method=='POST'):
        response_data=response.json()


        phonenumber=response_data['data']['user']['phone']
        tokenid=response_data['data']['token']
        firstname=response_data['data']['user']['first_name']
        lastname=response_data['data']['user']['last_name']
        emailid=response_data['data']['user']['email']
        dateofbirth=response_data['data']['user']['birth_date']

        customerid=response_data['data']['user']['customer_id']
        gender=response_data['data']['user']['gender']
        heightfeet=response_data['data']['user']['height_feet']
        heightinch=response_data['data']['user']['height_inches']
        heighttext=response_data['data']['user']['height_text']
        nextsub=response_data['data']['user']['next_subscription']
        subs=response_data['data']['user']['subscription']
        targetweight=response_data['data']['user']['target_weight']
        weight=response_data['data']['user']['weight']
        whatsappconcent=response_data['data']['user']['whatsapp_consent']
        cityname=response_data['data']['user']['city']


        conn = mariadb.connect(**config)
        cur = conn.cursor()
        cur.execute ("INSERT INTO tokendetails (token_id, phone_number) VALUES(%s, %s)",  (tokenid, phonenumber))
        cur.execute("INSERT INTO Customerdetails (phone_number, first_name, last_name, email, customer_id, gender, height_feet, height_inches, height_text, next_subscription, subscription, target_weight, weight, whatsapp_consent, city) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (phonenumber, firstname, lastname, emailid, customerid, gender, heightfeet, heightinch, heighttext, nextsub, subs, targetweight, weight, whatsappconcent, cityname))
        cur.connection.commit()
        conn.close()

    return response.json()

    
    



#Address
@app.route('/v1/address', methods= ['GET'])
def v1addressget():
    url ="https://erp-test.fooddarzee.com/api/v1/address"

    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql= "SELECT token_id FROM tokendetails WHERE phone_number = 9920045322"
    cur.execute (sql)
    res = cur.fetchall()
    res1=res[0]
    auth_token=res1[0]
  
    header= {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + auth_token
    }
    response = requests.get(url, headers=header, verify= False)
    return response.json()



@app.route('/v1/address', methods= ['POST'])
def v1addresspost():
    url ="https://erp-test.fooddarzee.com/api/v1/address"
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql= "SELECT token_id FROM tokendetails WHERE phone_number = 9920045322"
    cur.execute (sql)
    res = cur.fetchall()
    res1=res[0]
    auth_token=res1[0]
    input={
        "label": "A nice Address",
        "street_1": "This is my Address",
        "street_2": "This is new Address",
        "pincode": "400050",
        "area": "Bandra West",
        "city": "Mumbai",
        "state": "Maharashtra"
    }
    header= {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + auth_token
    }
    response = requests.post(url, data=json.dumps(input), headers=header, verify= False)
    if (request.method=='POST'):
        phonenumber='9920045322'
        area=input['area']
        city=input['city']
        label=input['label']
        pincode=input['pincode']
        state=input['state']
        street1=input['street_1']
        street2=input['street_2']

        conn = mariadb.connect(**config)
        cur = conn.cursor()
        cur.execute("INSERT INTO addressdetails (area, phone_number, city, label, pincode, state, street_1, street_2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (area, phonenumber, city, label, pincode, state, street1, street2))
        cur.connection.commit()
        conn.close()

    return response.json()



@app.route('/v1/address/<string:num>', methods=['PUT'])
def v1addressput(num):
    url = "https://erp-test.fooddarzee.com/api/v1/address/"
    base_url=url+num
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql= "SELECT token_id FROM tokendetails WHERE phone_number = 9920045322"
    cur.execute (sql)
    res = cur.fetchall()
    res1=res[0]
    auth_token=res1[0]
    input={
        "label": "A nice Address",
        "street_1": "This is my Address",
        "street_2": "This is new Address",
        "pincode": "400050",
        "area": "Bandra West",
        "city": "Mumbai",
        "state": "Maharashtra"
    }
    header= {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + auth_token
    }
    response = requests.put(url=base_url, data=json.dumps(input), headers=header, verify= False)
    return response.json()



@app.route('/v1/address/<string:num>', methods=['DELETE'])
def v1addressdelete(num):
    url = "https://erp-test.fooddarzee.com/api/v1/address/"
    base_url=url+num
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql= "SELECT token_id FROM tokendetails WHERE phone_number = 9920045322"
    cur.execute (sql)
    res = cur.fetchall()
    res1=res[0]
    auth_token=res1[0]
    header= {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + auth_token
    }
    response = requests.delete(url=base_url, headers=header, verify= False)
    return response.json()





#Customer
@app.route('/v1/customer', methods=['GET'])
def v1customer():
    url = "https://erp-test.fooddarzee.com/api/v1/customer"
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql= "SELECT token_id FROM tokendetails WHERE phone_number = 9920045322"
    cur.execute (sql)
    res = cur.fetchall()
    res1=res[0]
    auth_token=res1[0]
    header={
        'Authorization': 'Bearer ' + auth_token,
        'accept': 'application/json'
    }
    
    response = requests.get(url, headers=header, verify= False)
    return response.json()



@app.route('/v1/customer/changePhone', methods=['POST'])
def v1customerchangePhone():
    url = "https://erp-test.fooddarzee.com/api/v1/customer/changePhone"
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql= "SELECT token_id FROM tokendetails WHERE phone_number = 9920045322"
    cur.execute (sql)
    res = cur.fetchall()
    res1=res[0]
    auth_token=res1[0]
    input={
        "phone": 9920045322,
        "otp": 9999
    }
    header= {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + auth_token
    }
    response = requests.post(url, data=json.dumps(input), headers=header, verify= False)
    return response.json()





#Dish
@app.route('/v1/getAvailableDishes', methods=['GET'])
def v1getAvailableDishes():
    date= request.args.get('date', None)
    dish_id=request.args.get('dish_id', None)
    meal_type=request.args.get('meal_type', None)
    url = "https://erp-test.fooddarzee.com/api/v1/getAvailableDishes"
    base_url= url+"?date="+str(date)+'&dish_id='+str(dish_id)+'&meal_type='+str(meal_type)
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql= "SELECT token_id FROM tokendetails WHERE phone_number = 9920045322"
    cur.execute (sql)
    res = cur.fetchall()
    res1=res[0]
    auth_token=res1[0]
    header={
        'Authorization': 'Bearer ' + auth_token,
        'accept': 'application/json'
    }
    
    response = requests.get(url=base_url, headers=header, verify= False)
    return response.json()




@app.route('/v1/replaceDish', methods = ['POST'])
def v1replaceDish():
    url="https://erp-test.fooddarzee.com/api/v1/replaceDish"
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql= "SELECT token_id FROM tokendetails WHERE phone_number = 9920045322"
    cur.execute (sql)
    res = cur.fetchall()
    res1=res[0]
    auth_token=res1[0]
    input={
        "date": "09/06/2021",
        "dish_id": 617,
        "meal_type": 2
    }
    header= {
        'Authorization': 'Bearer ' + auth_token,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(input), headers=header, verify= False)
    return response.json()


@app.route('/v1/rateDish', methods = ['POST'])
def v1rateDish():
    url="https://erp-test.fooddarzee.com/api/v1/rateDish"
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql= "SELECT token_id FROM tokendetails WHERE phone_number = 9920045322"
    cur.execute (sql)
    res = cur.fetchall()
    res1=res[0]
    auth_token=res1[0]
    input={
        "date": "09/06/2021",
        "dish_id": 617,
        "stars": "4",
        "reasons": [
            "Good one"
        ]
    }
    header= {
        'Authorization': 'Bearer ' + auth_token,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(input), headers=header, verify= False)
    return response.json()



@app.route('/v1/getOrderBags', methods = ['POST'])
def v1getOrderBags():
    url="https://erp-test.fooddarzee.com/api/v1/getOrderBags"
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql= "SELECT token_id FROM tokendetails WHERE phone_number = 9920045322"
    cur.execute (sql)
    res = cur.fetchall()
    res1=res[0]
    auth_token=res1[0]
    input={
        "date": "07/02/2020"
    }
    header= {
        'Authorization': 'Bearer ' + auth_token,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(input), headers=header, verify= False)
    return response.json()





#General
@app.route('/checkUpdate', methods = ['POST'])
def checkUpdate():
    url="https://erp-test.fooddarzee.com/api/checkUpdate"
    input={
        "platform": "ios",
        "version": "1.0.1"
    }

    header= {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(input), headers=header, verify= False)
    return response.json()



@app.route('/v1/getDeadline', methods=['GET'])
def v1getDeadline():
    url = "https://erp-test.fooddarzee.com/api/v1/getDeadline"
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql= "SELECT token_id FROM tokendetails WHERE phone_number = 9920045322"
    cur.execute (sql)
    res = cur.fetchall()
    res1=res[0]
    auth_token=res1[0] 
    header={
        'Authorization': 'Bearer ' + auth_token,
        'accept': 'application/json'
    }
    
    response = requests.get(url, headers=header, verify= False)
    return response.json()



@app.route('/v1/getAddressDeadline', methods=['GET'])
def v1getAddressDeadline():
    url = "https://erp-test.fooddarzee.com/api/v1/getAddressDeadline"
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    sql= "SELECT token_id FROM tokendetails WHERE phone_number = 9920045322"
    cur.execute (sql)
    res = cur.fetchall()
    res1=res[0]
    auth_token=res1[0] 
    header={
        'Authorization': 'Bearer ' + auth_token,
        'accept': 'application/json'
    }
    
    response = requests.get(url, headers=header, verify= False)
    return response.json()



@app.route('/v1/getPricing', methods = ['POST'])
def v1getPricing():
    url="https://erp-test.fooddarzee.com/api/v1/getPricing"
    input={
        "days": 30,
        "type": 4
    }
    header= {
        'accept': 'application/json'
    }
    response = requests.post(url, data=json.dumps(input), headers=header, verify= False)

    return response.json()



if __name__ == '__main__':
    app.run(host ='0.0.0.0', debug=True)