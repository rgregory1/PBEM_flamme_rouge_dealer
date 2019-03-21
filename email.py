import time
import yagmail
import credentials

# get timestamp for log
temp_timestamp = str(datetime.datetime.now())
print(2 * "\n")
print(temp_timestamp)

# setup credentials for sending email
gmail_user = credentials.gmail_user
gmail_password = credentials.gmail_password
yag = yagmail.SMTP(gmail_user, gmail_password)


# begin email notifications
contents = "A new staff member, {}, was added to the Staff Exit Process spreadsheet, go and check it out. \n\n".format(
    staff["Staff Member"]
)
html = '<a href="https://docs.google.com/spreadsheets/d/1kgLv2h_TWmb9FzBmDAe6dJDw5mkz-itbCrt69PdxO3c/edit#gid=0">Staff Exit Process spreadsheet</a>'
yag.send(
    [
        "rgregory@fnwsu.org",
        "jlaroche@fnwsu.org",
        "jjennett@fnwsu.org",
        "dstamour@fnwsu.org",
        "dtessier@fnwsu.org",
        "mellis@fnwsu.org",
        "clongway@fnwsu.org",
    ],
    "Notification of Employee Exiting",
    [contents, html],
)
print("sent exit notification emails for {}".format(staff["Staff Member"]))

if is_leaving_staff == False:
    print("No staff exits to report on")
else:
    print("Finished")
