import json
from functools import wraps
import re
from datetime import datetime
from datetime import timedelta

import pytz
from flask import (Flask, abort, jsonify, redirect,url_for, render_template, request, session)
from flask_socketio import SocketIO
import requests
import jwt  # You need to have PyJWT library installed
import string
import random
import datetime
import pytz


from argon2 import PasswordHasher
import argon2.exceptions
JWT_EXPIRATION_MINUTES = 1440

skc = "kousic"
# Function to create a new JWT token
def create_jwt_token(username,sid,client_ip, skc):
    payload = {
        'username': username,
        'ip': client_ip,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXPIRATION_MINUTES),
        'user_agent': request.headers.get('User-Agent'),
        "sid": sid
    }
    
    token = jwt.encode(payload, skc, algorithm='HS256')

    return token


def hash_password(password):
    # Generate a salt
    ph = PasswordHasher()

    hash = ph.hash(password)

    return hash



 

def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def validate_password(password):
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return bool(re.match(pattern, password))



def InputValidation(u, p1, p2):
    rp1 = r'[a-zA-Z]{5,}' # atleast six characters and minimum five characters should be alphabets
    if re.match(rp1, u):
        username=u
        if (p1 == p2):
            if (validate_password(p1) == 1):
                p1 = hash_password(p1)
                InpData = [username, p1]
                return InpData
            else:
                error="Password must contain atleast 8 characters.<br>Atleast one Letter. <br> Atleast one Digit. <br>Atleast one character from @, $, !, %, ?, &."
                return error

                
        else:
            error="Both Passwords should match!"
            return error

    else:
        error=  "Username should have atleast 6 Alphabets"
        return error
    
#================================================================================================================================#


# Function to format current date and time in IST timezone
def format_date_time():
    # Get the current datetime in IST timezone
    ist = pytz.timezone('Asia/Kolkata')
    current_datetime = datetime.datetime.now(ist)

    # Format the datetime as "Mon DD YYYY hh:mmAM/PM"
    formatted_datetime = current_datetime.strftime("%b %d %Y %I:%M%p")
    return formatted_datetime

# Function to generate a random string of specified length
def generate_random_string(length=random.randint(30, 40)):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string



# Function to send sign-up data to the API
def send_sign_up_data_to_db(username, password):
    
    # API endpoint URL
    url = "http://localhost/api/postUserData.php"

    # JWT payload
    payload = {
        "username": username,
        "password": password,
        "datetime": format_date_time(),
        "sid": generate_random_string()
    }

    # Your secret key
    secret_key = 'kousic'

    # Create JWT token
    jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')
    

    # Custom headers including the JWT
    headers = {
        "Authorization": f"Bearer {jwt_token}"
    }

    # Send the POST request with custom headers and JWT token
    response = requests.post(url, headers=headers)

    # Print response content
    # print("Response Content:", response.content)
    return response.status_code
        




#==============for password verification==============#


def verify_password(entered_password, stored_hashed_password):
    ph = PasswordHasher()
    
    try:
        passwords_match = ph.verify(stored_hashed_password, entered_password)
    except argon2.exceptions.VerifyMismatchError:
        # Password verification failed
        return False
    
    return passwords_match

#==============for password verification==============#





#S==============Shit is about to get real==============#
def isPasswordOkay(username, password):
    # API endpoint URL
    secret_key = "kousic"
    url = "http://localhost/api/isPasswordOkay.php"

    # Custom headers including the username and password
    headers = {
        "u": f"{username}",
        "p": "kousic111"
    }

    # Send the GET request with custom headers
    responsetoget = requests.get(url, headers=headers)
    print("========================")
    print(responsetoget)
    print("========================")
    print(responsetoget.status_code)
    print("========================")

    if responsetoget.status_code == 200 :

        try:
            response_json = responsetoget.json()
            jwt_token = response_json['message']
            print("========================")
            print(f"This is the JWT : {jwt_token}" )

        except (json.JSONDecodeError, KeyError):
            print("Failed to extract JWT token from response")
            return False

        # Decode the JWT token
        try:
            decoded_payload = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])
            password_hash = decoded_payload['password']
            if verify_password(password, password_hash):
                client_ip = request.remote_addr


                jwt_token1 = create_jwt_token(decoded_payload['username'], decoded_payload['sid'], client_ip, skc)
    
                # API endpoint URL
                url = "http://localhost/api/uploadToken.php"

                # JWT payload
                payload1 = {
                    "id": decoded_payload['id'],
                    "username": decoded_payload['username'],
                    "token": jwt_token1,
                    "aid": decoded_payload['aid'],
                    "valid": True
                }

                # Create JWT token#####Works because skc and secret_key are same####
                jwt_token11 = jwt.encode(payload1, skc, algorithm='HS256')
                # print("New JWT Token:", jwt_token11)
                # Custom headers including the JWT
                headers = {
                    "token": f"Bearer {jwt_token11}"
                }

                # Send the POST request with custom headers and JWT token
                response1 = requests.post(url, headers=headers)

                # Print response content
                print("Response Content:", response1.content)
                return [response1.status_code, jwt_token1]
            else:
                return False
        except jwt.ExpiredSignatureError:
            print("Token expired")
            return False
        except jwt.InvalidTokenError:
            print("Invalid token")
            return False

    else:
        return False



















            
            ####=======================================####


            


 













#E==============Shit is about to get real==============#



    







# Function to send sign-up data to the API
def get_user_data_from_db(username):
    # API endpoint URL
    url = "http://localhost/api/getUserData.php"


    # Your secret key
    secret_key = 'kousic'


    # Custom headers including the JWT
    headers = {
        "u": f"{username}",
        "p": "kousic111"#Here is where you need to change the key||
    }


    # Send the POST request with custom headers and JWT token
    response = requests.get(url, headers=headers)
    try:
        response_json = json.loads(response.content)
        jwt_token = response_json['message']
    except (json.JSONDecodeError, KeyError):
        print("Failed to extract JWT token from response")
        return
    

     # Decode the JWT token
    try:
        decoded_payload = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])
        
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False



def require_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('authenticated')
        
        if not token:
            return redirect(url_for('LogIn'))

        try:
            payload = jwt.decode(token, skc, algorithms=['HS256'])

            # Verify client IP against the IP in the token payload
            client_ip = request.remote_addr
            token_ip = payload.get('ip')

            if token_ip and token_ip != client_ip:
                return redirect(url_for('LogIn'))

            # Verify user-agent header against the user-agent in the token payload
            client_user_agent = request.headers.get('User-Agent')
            token_user_agent = payload.get('user_agent')

            if token_user_agent and token_user_agent != client_user_agent:
                return redirect(url_for('LogIn'))

            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return redirect(url_for('LogIn'))
        except jwt.InvalidTokenError:
            return redirect(url_for('LogIn'))
    return decorated_function
