import time
import sys
import random
import string

def typing(text, yes=0.01):  
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(yes)
    print()

def names(l=8):
    return ''.join(random.choices(string.ascii_letters, k=l))