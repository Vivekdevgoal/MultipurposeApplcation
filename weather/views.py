import requests
from django.shortcuts import render
import datetime

def home(request):
    city = request.GET.get('city')
    result = {}

    if city:
        try:
            api_key = '284671d8d92977ebbebaaee5a4b4254b'
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
            response = requests.get(url)
            data = response.json()

            if data.get('cod') == 200:
                result['region'] = data['name']
                result['country'] = data['sys']['country']
                result['lat'] = data['coord']['lat']
                result['lon'] = data['coord']['lon']
                result['temp'] = f"{data['main']['temp']} °C"
                result['feels_like'] = f"{data['main']['feels_like']} °C"
                result['temp_min'] = f"{data['main']['temp_min']} °C"
                result['temp_max'] = f"{data['main']['temp_max']} °C"
                result['sky'] = data['weather'][0]['description'].title()
                result['humidity'] = f"{data['main']['humidity']}%"
                result['wind_speed'] = f"{data['wind']['speed']} m/s"
                result['pressure'] = f"{data['main']['pressure']} hPa"
                result['visibility'] = f"{data.get('visibility', 0) / 1000} km"
                result['clouds'] = f"{data['clouds']['all']}%"
                result['timezone'] = data['timezone']  # in seconds

                sunrise_ts = data['sys']['sunrise'] + data['timezone']
                sunset_ts = data['sys']['sunset'] + data['timezone']
                now_ts = datetime.datetime.utcnow().timestamp() + data['timezone']

                result['sunrise'] = datetime.datetime.fromtimestamp(sunrise_ts).strftime('%H:%M:%S')
                result['sunset'] = datetime.datetime.fromtimestamp(sunset_ts).strftime('%H:%M:%S')
                result['local_time'] = datetime.datetime.fromtimestamp(now_ts).strftime('%Y-%m-%d %H:%M:%S')

                icon_code = data['weather'][0]['icon']
                result['icon_url'] = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            else:
                result['error'] = data.get('message', 'City not found.')

        except Exception as e:
            result = {"error": f"Could not retrieve weather data: {str(e)}"}

    return render(request, 'weather/index.html', {'result': result})
