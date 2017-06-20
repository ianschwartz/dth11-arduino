import requests
import json
import serial

# open serial port
ser = serial.Serial('/dev/ttyACM1', 19200)

# establish some variables
url = "https://weathertown-ma.herokuapp.com"
email = ""
user_id = 0
auth_token = ''
station_id = 0

# start up
def start_up():
  print "Welcome to Weathertown!"
  print "Enter 1 to login"
  print "Enter 2 to sign up"
  choice = raw_input('--> ')
  if choice == '1':
    return login()
  elif choice == '2':
    return sign_up()
  else:
    return start_up() 

# If you need a new account
def sign_up():
  # enter your name
  name = raw_input('Enter your name --> ')
  
  # choose your email and password
  global email
  email = raw_input('Enter your email --> ')
  password = raw_input('Enter your password --> ')
  confirmation = raw_input('Confirm your password --> ')
  sign_up_data = {'email': email, 'password': password, 'password_confirmation': confirmation, 'name': name}
  r = requests.post(url + "/signup", data = sign_up_data)
  print
  print sign_up_data
  return start_up()

#if you already have an account
def login():
  global email
  password = ''
  global auth_token

  # input your email and password.
  email = raw_input('What is your email address --> ')
  password = raw_input('What is your password --> ')

  r = requests.post(url + "/auth/login", data = { "email": email, "password": password })
  parsed_json = json.loads(r.text)

  if r.status_code == 401:
    print "Invalid credentials"
    return login()
  elif r.status_code == 200:
    auth_token = parsed_json['auth_token']
    return select_station()

# lists the user's available stations and let's them choose one (or make a new one)
def select_station():
  global station_id

  # gets your data
  global user_id
  r = requests.get(url + "/user", data = {'email': email})
  user = json.loads(r.text)
  user_id = user['id']

  # lists your stations
  print "Here are your stations:"
  for s in user['stations']:
    print str(s['id']) + ". " + s['name']
  choice = raw_input("Enter the number of the station you would like to select, or enter 'N' to set up a new station--> ")
  if choice == 'N':
    return add_station()
  else:
    station_id = choice
    return check_readings()

# add a new station
def add_station():
  global station_id
  name = raw_input('What would you like to name the station? --> ')
  zipcode = raw_input('What is the zip code of the station? --> ')
  r = requests.post(url + '/stations/', data = {"name": name, "zipcode": zipcode, 'user_id': user_id}, headers = {"Authorization": auth_token})

  # checks if station added successfully
  if r.status_code == 201:
    parsed_json = json.loads(r.text)
    station_id = parsed_json['id']
    # station_id = json.loads(
    print "Station created successfully"
    return check_readings()
  else:
    print "Something went wrong, try again"
    return add_station()

def check_readings():
  # gets a reading from the Arduino over Serial
  reading = ser.readline()

  # sometimes the reading gets garbled, this validates it
  if reading[:8] == '{"temp":' and len(reading) >= 25 and len(reading) <= 28:
    print "Reading successful"
    print reading
    return post_readings(reading)
  else:
    # if the reading is invalid, try again
    print "Invalid reading. Trying again."
    print reading
    return check_readings()

def post_readings(reading):
  parsed_json = json.loads(reading)
  r = requests.post(url + "/stations/" + str(station_id) + "/readings", data = parsed_json, headers = {"Authorization": auth_token})
  if r.status_code == 201:
    print "Great success! It's " + reading
  else:
    print r.text
    return check_readings()
  return

start_up()