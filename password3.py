import pymysql.cursors
import hashlib
import uuid

# mMke the salt!
salt = str(uuid.uuid4())

# Get username and password from user
userName = input("Enter new username: ")
password = input("Enter password: ")

# Hash the password
hashed_Password = hashlib.sha256((password + salt).encode())

# print the hashed password
# print("the hashed pw is: ", hashed_Password)


# Connect to the Password database
connection = pymysql.connect(host='mrbartucz.com',
                             user='an8520td',
                             password='Toby2020!',
                             db='an8520td_Password',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


try:
    with connection.cursor() as cursor:
        # Insert New User Into Passwords table using input
        setPW = "INSERT INTO `Password` (`userName`, `salt`, `hash`) VALUES (%s,%s,%s)"

        # execute the SQL command
        cursor.execute(setPW, (userName, salt, hashed_Password.hexdigest()))

        # If you INSERT, UPDATE or CREATE, commit to save your changes.
        connection.commit()

    with connection.cursor() as cursor:
        # get info from Password table using input
        getCredentials = "SELECT * FROM `Password` WHERE userName = %s"

        # execute the SQL command
        cursor.execute(getCredentials, userName)

        # get the results
        for row in cursor:
            SaltFromDataBase = row['salt']
            HashedPasswordFromDataBase = row['hash']
finally:
    connection.close()

# ask user to reenter their password
reEnteredPassword = input("Enter your password again to recheck: ")

# rehash the reEntered password with salt retrieved from DB
reHashedPassword = hashlib.sha256((
    reEnteredPassword + SaltFromDataBase).encode())

# test if hash from DB and hash from reEntered passwords match
if HashedPasswordFromDataBase == reHashedPassword.hexdigest():
    print("Congradulations, your passwords matched!")
else:
    print("I'm sorry Dave. I'm afraid I can't do that.")
