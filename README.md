# SSE-CSP

Mikael Peltoketo 290513

Project is run from main.py, wtih python 3
PyCrypto and AES libraries might have to be installed

## Databse
Download it here:
https://tuni-my.sharepoint.com/:f:/g/personal/mikael_peltoketo_tuni_fi/EuhYjXJY2YxGqdXJ520fEK0BqQyEGHFaV97uedLYoXzyWg?e=nK0f7s

It has to be named SQL\sm_app.sqlite (linux)
Or be in SQL folder and named sm_app.sqlite (Windows)

## Commands
- emptyALL
Removes all SQL data and encrypted files

- emptyCSP
Removes all CSP SQL data and encrypted files

- emptyTa
Removes all TA SQL data

- addDO
Adds DataOwner, input 2 key seed separated with space.
Data bases uses : addDOO a a

- addFolder
Initializes DB with prefixed folder, this can be run only ones

- addFolderEX *foldername*
Adds new folders contents to database, can be run multiple times,
but before it addFolder has to be run

- search *word*
Searches specified word from DB, program asks is files that contain the word
will be decrypted

- q 
Quits the program
