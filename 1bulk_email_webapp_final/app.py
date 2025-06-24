from flask import Flask, request, render_template
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
UPLOAD_FOLDER = "."

@app.route('/', methods=['GET', 'POST'])
def index():
    status_log = []
    if request.method == 'POST':
        sender_email = request.form['sender_email']
        sender_password = request.form['sender_password']
        subject = request.form['subject']
        message_body = request.form['message']
        file = request.files['email_file']

        if file:
            filepath = os.path.join(UPLOAD_FOLDER, "emails.txt")
            file.save(filepath)

            with open(filepath, 'r') as f:
                recipients = [line.strip() for line in f.readlines()]

            smtp_server = "smtp.gmail.com"
            smtp_port = 587

            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)

                for recipient in recipients:
                    msg = MIMEMultipart()
                    msg["From"] = sender_email
                    msg["To"] = recipient
                    msg["Subject"] = subject
                    msg.attach(MIMEText(message_body, 'plain'))
                    server.sendmail(sender_email, recipient, msg.as_string())
                    status_log.append(f"✅ Sent to {recipient}")
                    time.sleep(2)

                server.quit()
                return render_template('index.html', message="All emails sent successfully!", status_log=status_log)

            except Exception as e:
                return render_template('index.html', message=f"❌ Error: {str(e)}", status_log=[])

    return render_template('index.html', status_log=[])

if __name__ == "__main__":
    app.run(debug=True)
