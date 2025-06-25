import os
import smtplib
from flask import Flask, request, render_template
from email.message import EmailMessage

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sender_email = request.form.get("sender_email")
        sender_password = request.form.get("sender_password")
        subject = request.form.get("subject")
        message_body = request.form.get("message")

        email_file = request.files.get("email_file")
        attachment = request.files.get("attachment")

        if not email_file:
            return "⚠️ Please upload a file containing recipient emails."

        recipients = email_file.read().decode("utf-8").splitlines()

        for recipient in recipients:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = recipient
            msg.set_content(message_body)

            # If an attachment is uploaded
            if attachment:
                filename = attachment.filename
                file_data = attachment.read()
                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=filename)

            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(sender_email, sender_password)
                    smtp.send_message(msg)
                    print(f"✅ Email sent to {recipient}")
            except Exception as e:
                print(f"❌ Failed to send to {recipient}: {e}")

        return "✅ All emails have been processed!"

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
