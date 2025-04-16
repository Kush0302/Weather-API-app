import sys #handles system variables for python interpretor
import requests #to import request module is useful to make request to an api
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt #QT is used for alignment
from dotenv import load_dotenv  # import dotenv
import os  # to access the environment variable

class WeatherApp(QWidget):
    def __init__(self):  #making constructor
        super().__init__()
        self.city_label=QLabel("Enter city name:",self) #adding city_label to waether_app object
        self.city_input=QLineEdit(self) #making textbox usin line edit
        self.get_weather_button=QPushButton("Get Weather",self) #making a button and adding it to our weather_app object
        self.temprature_label=QLabel(self)
        self.emoji_label=QLabel(self)
        self.description_label=QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox=QVBoxLayout()  #using vertical layout manager to handel all the widgets
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temprature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temprature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temprature_label.setObjectName("temprature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QpushButton{
                font-family:calibri;
            }
            QLabel#city_label
            {
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight:bold;               
            }
            QLabel#temprature_label{
                font-size: 75px;               
            }
            QLabel#emoji_label{
                font-size: 100px;   
                font-family:Segoe UI emoji;            
            }
            QLabel#description_label{
                font-size: 50px;               
            }             

        """)

        self.get_weather_button.clicked.connect(self.get_weather) #connect signal to a slot i.e: when we click on a button we will connect a slot of get_weather

    def get_weather(self):
        # Load the API key securely from the .env file
        load_dotenv()  # Load environment variables from .env file
        api_key = os.getenv("api_key")  # Get the API key from the environment

        city = self.city_input.text()  # this local variable city helps in accessing text from line edit widget city input..
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"  # for making API request

        try:
            response = requests.get(url)  # response object used to access module of requests by calling get method
            response.raise_for_status()  #THis method will raise an exception if there is an HTTP errors "normally Try block doesn't do this so we have to manually type this"
            data = response.json()  # we have to convert our response object into json format
            print(data)

            if data["cod"]==200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error: # HTTP exception is founded within requests module that we have imported so we can't directly say Except HTTPError
              match response.status_code:
                  case 400:
                      print("Bad Request\nPlease check your input")
                  case 401:
                      print("Unauthorized\nInvalid API key")
                  case 403:
                      print("Forbidden\nAccess is denied")
                  case 404:
                      print("Not Found\nCity not found")
                  case 500:
                      print("Internal Server Error\nPlease try again later")
                  case 502:
                      print("Bad Gateway\nInvalid response from the server")
                  case 503:
                      print("Service Unavailable\nServer is down")
                  case 504:
                      print("Gateway Timeout\nNo response from the server")
                  case _:
                      print(f"HTTP error occured\n{http_error}")
        except requests.exceptions.ConnectionError:
            print("Connection Error\nCheck your internet connection")
        except requests.exceptions.Timeout:
            print("Timeout Error\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects\nCheck the URL")
        except requests.exceptions.RequestException as req_error: #for network problems invalid URL
            print(f"Request Error\n{req_error}")
        

    def display_error(self, message): 
        pass

    def display_weather(self, data):
        print(data)

if __name__=="__main__":
    app=QApplication(sys.argv)  #sys.argv helps to send command line arguments to application
    weather_app=WeatherApp() #costructed a waetherapp object
    weather_app.show()
    sys.exit(app.exec_()) #exec_() method handels events within our application e.g:closing the window
 