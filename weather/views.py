from django.shortcuts import render
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Create your views here.

def index(request):
    api_key = os.getenv('API_KEY')  # Ensure the API key is defined here
    weather = {}
    if request.method == 'POST':
        city = request.POST['city']
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url).json()
        
        if response.get('cod') != 200:
            weather = {'error': response.get('message', 'City not found or invalid API response')}
        else:
            weather = {
                'country_code': response['sys']['country'],
                'coordinate': f"{response['coord']['lon']}, {response['coord']['lat']}",
                'temperature': f"{response['main']['temp']} °C",
                'pressure': response['main']['pressure'],
                'humidity': response['main']['humidity'],
                'main': response['weather'][0]['main'],
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
            }

    return render(request, 'main/index.html', {'weather': weather})
