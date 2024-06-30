from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
import threading

app = Flask(__name__)

def send_email(sender_email, app_password, receiver_email, subject, body):
    try:
        # Set up the MIME
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Connect to the server and send the email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, app_password)  # Login to the email server
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Email sent successfully")

    except Exception as e:
        print(f"Failed to send email: {e}")

def schedule_email(time_to_send, sender_email, app_password, receiver_email, subject, body):
    schedule.every().day.at(time_to_send).do(send_email, sender_email, app_password, receiver_email, subject, body)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        time_to_send = request.form['time_to_send']
        sender_email = request.form['sender_email']
        app_password = request.form['app_password']
        receiver_email = request.form['receiver_email']
        subject = request.form['subject']
        body = request.form['body']
        
        # Start a new thread to schedule the email
        threading.Thread(target=schedule_email, args=(time_to_send, sender_email, app_password, receiver_email, subject, body)).start()

        return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
