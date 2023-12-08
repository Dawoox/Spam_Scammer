import contextlib
import os
from os import devnull

import requests
import time
from faker import Faker
import threading
import sys

running, paused = True, False


def send_request(user, password):
    base_url = "https://instagramphotoo2024.wixsite.com/website"
    params = {
        "-nom d'utilisateurs,": user,
        "-mot,de passe": password
    }
    response = requests.get(base_url, params=params)
    return response


def generate_username():
    fake = Faker('fr_FR')
    return fake.user_name()


def generate_password():
    fake = Faker('fr_FR')
    length = fake.random_int(min=6, max=22)
    return fake.password(length=length)


def listen_for_quit_command():
    global running, paused
    while True:
        command = input()
        if command == 'quit' or command == 'exit' or command == 'stop':
            running = False
            sys.exit()
        elif command == 'pause':
            print("Pause sending requests, type 'resume' to resume")
            paused = True
            with contextlib.redirect_stdout(open(os.devnull, 'w')):
                time.sleep(2)
        elif command == 'resume':
            print("Resume sending requests...")
            paused = False


def process_request():
    password = generate_password()
    username = generate_username()
    print(f"Sending request -> password = {password:<22} | username = {username:<18}, "
          f"response code: {send_request(username, password).status_code}")


# Start the listener thread
listener_thread = threading.Thread(target=listen_for_quit_command)
listener_thread.start()

while running:
    if not paused:
        threads = []
        for _ in range(16):  # Change this number to the number of threads you want to create
            thread = threading.Thread(target=process_request)
            thread.start()
            threads.append(thread)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        time.sleep(0.5)  # Pause before starting the next batch of threads
