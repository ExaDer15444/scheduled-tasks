import requests
import os
import smtplib
import ssl
from email.mime.text import MIMEText



OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"

api_key = os.environ.get("OWM_API_KEY")
my_email = os.environ.get("WP_EMAIL")
to_email = os.environ.get("TO_EMAIL")
my_password = os.environ.get("WP_PASSWORD")





def analyze_day(codes):
    result = {
        "storm": any(200 <= c <= 232 for c in codes),
        "rain": any(300 <= c <= 531 for c in codes),
        "snow": any(600 <= c <= 622 for c in codes),
        "sun": any(c == 800 for c in codes),
        "clouds": any(801 <= c <= 804 for c in codes),
    }
    return result

def message_for_asia(codes):

    weather = analyze_day(codes)

    if weather["storm"]:
        return (
            "Kochana Asiu ❤️ Dzisiaj może pojawić się burza. "
            "Pamiętaj jednak, że niezależnie od tego, co dzieje się za oknem, "
            "jesteś moim najjaśniejszym promieniem słońca. ☀️"
        )

    if weather["rain"]:
        if weather["sun"]:
            return (
                "Kochana Asiu ❤️ Dzień zapowiada się trochę deszczowo, "
                "ale między chmurami powinno pokazać się też słoneczko. "
                "Mam nadzieję, że Twój uśmiech rozgoni wszystkie chmurki. Kocham Cię! ☀️🥰"
            )

        return (
            "Kochana Asiu ❤️ Dzisiaj może popadać, ale pamiętaj, "
            "że nawet najładniejszy deszcz nie jest tak piękny jak Twój uśmiech. 🌷"
        )

    if weather["sun"] and not weather["clouds"]:
        return (
            "Kochana Asiu ❤️ Zapowiada się piękny, słoneczny dzień. "
            "Mam nadzieję, że będzie dla Ciebie tak ciepły i cudowny jak Ty dla mnie. ☀️😘"
        )

    if weather["sun"] and weather["clouds"]:
        return (
            "Kochana Asiu ❤️ Dzień przyniesie trochę słońca i trochę chmurek, "
            "ale jedno jest pewne: dla mnie zawsze jesteś najpiękniejszą pogodą. ☀️💖"
        )

    return (
        "Kochana Asiu ❤️ Dzień zapowiada się spokojnie. "
        "Życzę Ci mnóstwa powodów do uśmiechu i cudownego nastroju. 🥰"
    )

weather_params = {
    "lat": 54.42880315,
    "lon": 18.798325902846855,
    "appid": API_KEY,
    "cnt": 4,
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

#print(weather_data["list"][0]["weather"][0]["description"])


condition_codes =[]

for hour_data in weather_data["list"]:
    condition_codes.append(hour_data["weather"][0]["id"])
print(condition_codes)

print(message_for_asia(condition_codes))
message_for_asia = message_for_asia(condition_codes)


message = MIMEText(
    message_for_asia,
    "plain",
    "utf-8"
)

message["From"] = my_email
message["To"] = to_email
message["Subject"] = "Specjalna prognoza pogody dla żonki"

context = ssl.create_default_context()

print("1. Łączenie...")
with smtplib.SMTP_SSL("smtp.wp.pl", 465, context=context) as connection:
    print("2. Połączono")

    connection.login(
        user=my_email,
        password=my_password
    )

    print("3. Zalogowano")

    connection.sendmail(
        from_addr=my_email,
        to_addrs=to_email,
        msg=message.as_string()
    )

    print("4. Email wysłany")

