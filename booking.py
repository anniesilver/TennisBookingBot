import requests
import os
from sys import exit
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import hashlib

#print("This program takes a little while to scan all available courts at your specified time with the availabler partner player. please hold tight.....\n when this window is closed, you can view the log.txt to see the result.")
# Check if log gile exists, if not create it with write permissions
log_file_path = "log.txt"
if not os.path.exists(log_file_path):
    with open(log_file_path, 'w', encoding="utf-8") as log_file:
        pass
with open('booking.lic', 'r') as file:
    lic = file.read()
with open('b_config.json', 'r') as f:
    config = json.load(f)
userId = config['userId']
password = config['password']
book_day = config['book_day']
player_list = config['player_list']
book_slot = config['book_slot']
userId="hgglen@gmail.com"
hashed_userId = hashlib.sha256(userId.encode()).hexdigest()
print(userId," authority code: ", hashed_userId)
exit(0)
if hashed_userId != lic:
    with open(log_file_path, 'w', encoding="utf-8") as log_file:
        log_file.write("Sorry. You don't have the authority to use booking.exe\n")
    exit(0)

today = datetime.now().date()
today_weekday = today.weekday()

def days_until_next(target_weekday):
    days_ahead = (target_weekday - today_weekday + 7) % 7
    return days_ahead if days_ahead != 0 else 7

target_weekday = book_day - 1
days_until = days_until_next(target_weekday)
target_date = today + timedelta(days=days_until)

with open(log_file_path, 'a') as log_file:
    log_file.write(f"today {today}, weekday {today_weekday+1}"+'\n')
    log_file.write(f"there is {days_until} days  until next weekday{book_day}" + '\n')

base = 'https://vs2.clubinterconnect.com/wotc/home/'
login_url = base + 'login.do'
viewbooking_url = base + 'calendarDayView.do?id=7&iYear='+target_date.strftime('%Y')+'&iMonth='+str(target_date.month-1)+'&iDate='+target_date.strftime('%d')
booking_handler = base + 'newView.do'

# Login credentials
payload = {
    'userId': userId,
    'password': password
}

# Start a session
session = requests.Session()

# Get the login page to retrieve authenticity tokens or other necessary fields
response = session.get(login_url)
soup = BeautifulSoup(response.text, 'html.parser')


# Post the login credentials to the login URL
login_response = session.post(login_url, data=payload)


# Check if login was successful
if login_response.url == login_url:
    with open(log_file_path, 'a') as log_file:
        log_file.write("Login failed!" + '\n')
else:
    with open(log_file_path, 'a') as log_file:
        log_file.write("Login successful!" + '\n')
        log_file.write("Cookies after login:" + str(session.cookies.get_dict())+'\n')


    bookinglist_response = session.get(viewbooking_url)
    soup = BeautifulSoup(bookinglist_response.text, 'html.parser')

    links = soup.find_all('a', href=True)
    bookable_links = [link['href'] for link in links if 'newView' in link['href']]

    for booking_url in bookable_links:
        booking_url = base + booking_url.replace(" ", "%20")
        booking_page_response = session.get(booking_url)
        booking_payload = {}

        soup = BeautifulSoup(booking_page_response.text, 'html.parser')
        hidden_inputs = soup.find_all("input", type="hidden")
        for hidden_input in hidden_inputs:
            booking_payload[hidden_input['name']] = hidden_input['value']

        booking_payload['Booking Duration'] = '60|1 hour|1 hour'
        if booking_payload["Booking Start Time"] == book_slot:
            for player in player_list:
                booking_payload ['Team_Two_Auto'] = player
                booking_response = session.post(booking_handler, data=booking_payload)
                booking_soup=BeautifulSoup(booking_response.text, 'html.parser')
                h1_err = booking_soup.find('h1', class_='error')
                error = ''
                if h1_err:
                    error = h1_err.text

                if error != '':
                    with open(log_file_path, 'a', encoding="utf-8") as log_file:
                        log_file.write("booking failed，"+ error+'\n')

                    if booking_payload['Team_One_Auto'] in error:
                        with open(log_file_path, 'a',encoding="utf-8") as log_file:
                            log_file.write("Sorry."+ booking_payload['Team_One_Auto']+" has reached same day booking limit or 3 limits in total. Try change your config or cancel other booked court first."+'\n')
                        exit(0)
                    #如果player2 当日已经预定，尝试下一个Player
                    if "already booked a court at the same time" in error:
                        with open(log_file_path, 'a', encoding="utf-8") as log_file:
                            log_file.write("Failed booking court. Either"+ booking_payload['Team_One_Auto']+" or "+booking_payload['Team_Two_Auto']+'has booked on the same day already'+'\n')
                        continue
                    #如果player2已经预定超过三块场地，尝试下一个player
                    if "already booked 3 courts in advance" in error:
                        continue
                    #如果场地已被占用，跳到下一个SLOT
                    if "The court is no longer available" in error:
                        break
                else:
                    #print("sucessfully booked slot",booking_payload["Booking Start Time"],"with player",player)
                    log="sucessfully booked slot "+booking_payload["Booking Start Time"]+" with player "+player+'\n'
                    with open(log_file_path, 'a', encoding="utf-8") as log_file:
                        log_file.write(log)
                    exit(0)
        else:
            with open(log_file_path, 'a', encoding="utf-8") as log_file:
                log_file.write("skip this slot\n")

    with open(log_file_path, 'a', encoding="utf-8") as log_file:
        log_file.write("No court has been booked\n")
