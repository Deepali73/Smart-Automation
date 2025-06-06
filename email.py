import smtplib

def send_email(sender_email: str, receiver_email: str, app_password: str, message: str):
    try:
        # create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # secure the connection

        # login with app password
        server.login(sender_email, app_password)

        # send the email
        server.sendmail(sender_email, receiver_email, message)
        print("Email sent successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        server.quit()
