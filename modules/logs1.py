from colorama import Fore, Style
from datetime import datetime

def log(stats, text, codes=None, count=[0]):
    time = datetime.now().strftime('%H:%M:%S')
    c = {'INFO': Fore.LIGHTCYAN_EX, 'SUCCESS': Fore.LIGHTGREEN_EX, 'RATELIMIT': Fore.LIGHTYELLOW_EX, 'ERROR': Fore.LIGHTRED_EX}
    if stats != 'RATELIMIT': count[0] += 1
    if codes is not None:
        code = f"{Fore.LIGHTGREEN_EX}{codes}{Style.RESET_ALL}" if 200 <= codes < 300 else f"{Fore.LIGHTRED_EX}{codes}{Style.RESET_ALL}"
    else:
        code = "EXPOSING"
    print(f"{Fore.WHITE}[ {Fore.LIGHTBLACK_EX}{time}{Style.RESET_ALL} ] {Fore.WHITE}[ {c.get(stats, Fore.WHITE)}{stats}{Fore.WHITE} ] {text}{Style.RESET_ALL} {Fore.WHITE}[ {code}{Style.RESET_ALL}{Fore.WHITE} ] [ {Fore.LIGHTBLACK_EX}{count[0]:02}{Style.RESET_ALL}{Fore.WHITE} ]")