# POST :3000/stations/3/readings temp=12 humidity=34 Authorization:'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE0OTcwMjI5Njh9.edJNCTwSH-tckPav46CRdoA9ng1oeP_r7aLZwQoyYTY'
# http POST :3000/auth/login email="ian@schwartz.world" name='hank' password='meatpie123'
import requests
import json

email = ""
password = ""
auth_token = ''
station_id = 0

def login():
  global email
  global password
  global auth_token

  email = raw_input('What is your email address --> ')
  password = raw_input('What is your password --> ')
  r = requests.post("http://localhost:3000/auth/login", data = { "email": email, "password": password })
  parsed_json = json.loads(r.text)
  if r.status_code == 401:
    print "Invalid credentials"
    return login()
  elif r.status_code == 200:
    auth_token = parsed_json['auth_token']
    return select_station()

def select_station():
  global station_id
  r = requests.get("http://localhost:3000/user", data = {'email': email})
  stations = json.loads(r.text)
  print "Here are your stations:"
  for s in stations:
    print str(s['id']) + ". " + s['name']
  station_id = raw_input("--> ")
  return check_readings()

def check_readings():
  temp = '89'
  humidity = '54'
  return post_readings(temp, humidity)

def post_readings(temp, humidity):
  #:3000/stations/3/readings temp=12 humidity=34 Authorization:'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE0OTcwMjI5Njh9.edJNCTwSH-tckPav46CRdoA9ng1oeP_r7aLZwQoyYTY'
  r = requests.post("http://localhost:3000/stations/" + station_id + "/readings", data = {"temp": temp, "humidity": humidity}, headers = {"Authorization": auth_token})
  print r

login()

# logs into the API with a post request



# API returns JSON token, variable stores it

# Once per hour, checks temperature reading

# uploads reading to the API using the stored JSON token