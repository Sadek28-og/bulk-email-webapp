import os
import smtplib
from flask import Flask, request, render_template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sender_email = request.form["sender_email"]
        sender_password = request.form["sender_password"]
        subject = request.form["subject"]
        message_body = request.form["message"]
        file = request.files["email_file"]

        if file:
            recipients = file.read().decode("utf-8").splitlines()

            for recipient in recipients:
                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["To"] = recipient
                msg["Subject"] = subject
                msg.attach(MIMEText(message_body, "plain"))

                try:
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, recipient, msg.as_string())
                    server.quit()
                    print(f"✅ Email sent to {recipient}")
                except Exception as e:
                    print(f"❌ Failed to send to {recipient}: {e}")

            return "✅ All emails processed!"
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
