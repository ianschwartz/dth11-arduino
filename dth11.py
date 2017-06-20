# POST :3000/stations/3/readings temp=12 humidity=34 Authorization:'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE0OTcwMjI5Njh9.edJNCTwSH-tckPav46CRdoA9ng1oeP_r7aLZwQoyYTY'
# http POST :3000/auth/login email="ian@schwartz.world" name='hank' password='meatpie123'
import requests
import json
import serial

ser = serial.Serial('/dev/ttyACM1', 19200)
url = "http://localhost:3000"
email = ""
user_id = 0
auth_token = ''
station_id = 0

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

def sign_up():
  name = raw_input('Enter your name -->')
  global email
  email = raw_input('Enter your email -->')
  password = raw_input('Enter your password -->')
  confirmation = raw_input('Confirm your password -->')
  r = requests.post(url + "/signup", data = {'email': email, 'password': password, 'password_confirmation': confirmation, name: 'name'})
  print r
  return

def login():
  global email
  password = ''
  global auth_token

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

def select_station():
  global station_id
  global user_id
  r = requests.get(url + "/user", data = {'email': email})
  user = json.loads(r.text)
  user_id = user['id']
  print "Here are your stations:"
  for s in user['stations']:
    print str(s['id']) + ". " + s['name']
  choice = raw_input("Enter the number of the station you would like to select, or enter 'N' to set up a new station--> ")
  if choice == 'N':
    return add_station()
  else:
    station_id = choice
    return check_readings()

def add_station():
  global station_id
  name = raw_input('What would you like to name the station? --> ')
  zipcode = raw_input('What is the zip code of the station? --> ')
  r = requests.post(url + '/stations/', data = {"name": name, "zipcode": zipcode, 'user_id': user_id}, headers = {"Authorization": auth_token})
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
  reading = ser.readline()

  if reading[:8] == '{"temp":' and len(reading) >= 25 and len(reading) <= 28:
    # return post_readings(reading)
    print reading
    return post_readings(reading)
  else:
    print "nope"
    print reading
    return check_readings()

def post_readings(reading):
  #:3000/stations/3/readings temp=12 humidity=34 Authorization:'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE0OTcwMjI5Njh9.edJNCTwSH-tckPav46CRdoA9ng1oeP_r7aLZwQoyYTY'
  parsed_json = json.loads(reading)
  r = requests.post(url + "/stations/" + str(station_id) + "/readings", data = parsed_json, headers = {"Authorization": auth_token})
  if r.status_code == 201:
    print "Great success! It's " + reading
  else:
    print r.text
    return check_readings()
  return

start_up()


# logs into the API with a post request



# API returns JSON token, variable stores it

# Once per hour, checks temperature reading

# uploads reading to the API using the stored JSON token