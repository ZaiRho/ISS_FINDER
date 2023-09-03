import requests
from datetime import datetime
import smtplib

MY_EMAIL = "PUT_YOUR_EMAIL_HERE"
MY_PASSWORD = "PUT_YOUR_APP_PASS_HERE"
MY_LATITUDE = 14.604077
MY_LONGITUDE = 120.986134

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

data = response.json()

longitude = float(data["iss_position"]["longitude"])
latitude = float(data["iss_position"]["latitude"])
iss_position = (longitude, latitude)
print(iss_position)

# ----------------------SUNRISE & SUNSET -------------------------------#
parameters ={
    "lat": MY_LATITUDE,
    "lang": MY_LONGITUDE,
    "formatted": 0,
}

response2 = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response2.raise_for_status()
data2 = response2.json()

sunrise = int(data2["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data2["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now().hour
long_diff = longitude - MY_LONGITUDE
lat_diff = latitude - MY_LATITUDE
is_dark = time_now > sunset
is_above = 5 > long_diff > -5 and 5 > lat_diff > -5

if is_above and is_dark:
    with smtplib.SMTP("smtp.gmail.com",port=587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:ISS Finder\n\nHey! the ISS is above you now!"
        )
    print("email has been sent")
    print(is_dark)
    print(is_above)

