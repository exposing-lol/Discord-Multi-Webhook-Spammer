import os
import time
import requests
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor

from modules.logs1 import *
from modules.helper import *  

def validate():
    if not os.path.exists('webhooks.txt') or os.stat('webhooks.txt').st_size == 0:
        log('ERROR', 'No webhooks.txt or it is empty, please add webhooks or create webhooks.txt!')
        return []
    valid = []
    with open('webhooks.txt') as f:
        for line in f:
            hooks = line.strip()
            try:
                response = requests.get(hooks)
                if response.status_code // 100 == 2:
                    valid.append(hooks)
            except requests.RequestException:
                pass
    invalid = sum(1 for _ in open('webhooks.txt')) - len(valid)
    if invalid > 0:
        log('ERROR', f'Removing {invalid} invalid webhook{"s" if invalid > 1 else ""}!')
        with open('webhooks.txt', 'w') as f:
            for line in valid:
                f.write(line + '\n')
    return valid

def spam():
    typing(Fore.WHITE + "[ " + Fore.LIGHTBLUE_EX + "INPUT" + Fore.WHITE + " ] Enter the delay in ms (1000ms default): ", 0.01)
    delayi = input(Fore.WHITE + "[ " + Fore.LIGHTBLUE_EX + "INPUT" + Fore.WHITE + " ] " + Fore.WHITE)
    delay = float(delayi) / 1000 if delayi else 1  
    typing(Fore.WHITE + "[ " + Fore.LIGHTBLUE_EX + "INPUT" + Fore.WHITE + " ] Enter the name to use (Enter to use random names): ", 0.01)
    namei = input(Fore.WHITE + "[ " + Fore.LIGHTBLUE_EX + "INPUT" + Fore.WHITE + " ] " + Fore.WHITE)
    name = namei if namei else None
    message = input(Fore.WHITE + "[ " + Fore.LIGHTBLUE_EX + "INPUT" + Fore.WHITE + " ] Enter the message to send: ")
    webhooks = validate()
    if not webhooks:
        log('ERROR', 'No valid webhooks found!')
        return
    typing(f"{Fore.WHITE}[ {Fore.LIGHTBLUE_EX}STARTING{Fore.WHITE} ] Spamming with a {delay * 1000}ms delay!")
    with ThreadPoolExecutor() as speed:
        while True:
            try:
                user = name if name else names()
                for url in webhooks:
                    speed.submit(lambda url=url, user=user, message=message, delay=delay: send(url, user, message, delay))
                time.sleep(delay)
            except KeyboardInterrupt:
                log('ERROR', 'Closing!')
                break

def send(url, user, message, delay):
    x = {
        "content": message,
        "username": user
    }
    try:
        exposing = requests.post(url, json=x)
        if exposing.status_code // 100 == 2:
            log('SUCCESS', f'{user} sent message successfully!', exposing.status_code) 
        elif exposing.status_code == 429:
            ughratelimits = int(exposing.headers.get('ughratelimits', 1)) / 1000
            log('RATELIMIT', f'Retrying in {ughratelimits} seconds!', exposing.status_code) 
            time.sleep(ughratelimits)
        else:
            log('ERROR', f'{user} message not sent!', exposing.status_code)
    except requests.RequestException as e:
        log('ERROR', f'Error sending message to {url}: {str(e)}')

spam()
