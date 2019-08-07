import time
import urllib
import requests
from flask import Flask
from flask_testing import TestCase

url = 'http://localhost:5000'

time.sleep(5)

class MyTest(TestCase):

    def create_app(self): 
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_server_is_up_and_running(self):
        print ("Test Started")
        response = (urllib.request.urlopen(url))
        self.assertEqual(response.code, 200)
    
    def test_server_correct(self):
        print ("Test Started")
        response = urllib.request.urlopen(url)
        source = str(response.read()).split("\\n")
        self.assertEqual(source[0][2:], "<!-- LOGINPAGE ALIVE TEST -->")
    
    def test_login(self):
        print ("Test Started")
        r = requests.post(url, data={"username":"travisci", "password":"travisci"})
        self.assertEqual(r.text, '{"status": "Login successful"}')