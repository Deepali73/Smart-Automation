import smtplib

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login("xyz@gmail.com", "app password")  # Use app password here

# message to be sent
message = "Hey!! It's a trial for sending messages."

# sending the mail
s.sendmail("xyz@gmail.com", "abc@gmail.com", message)

# terminating the session
s.quit()
