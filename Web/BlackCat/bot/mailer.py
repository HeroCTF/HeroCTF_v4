import smtplib, ssl, mysql.connector, datetime, time

pwd = ":J2.bmF4.q/'=2T^gb(["
sender_email = "contactblackcat2k22@gmail.com"
subject = "[Black Cat 2k22]"
content = """We are glad that you participate at this very hidden confenrece !

Conferences will take place at 'blackcatjnhhyaiolppiqnbsvvxgcifuelkzpalsm.onion'

Be sure to proof that you receive this email with this sentence : Hero{y0u_b34t_bl4ckc4t_0rg4n1z3rs!!}

BlackCat.
"""

db = mysql.connector.connect(
    host="blackcatbdd",
    user="evilhackerz",
    password="wjKNQJLSP4X3uPL522Q6",
    database="blackcat"
)


def get_email_address_to_send():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM newsletter")
    res = cursor.fetchall()
    cursor.close()
    return res

def delete(ids):
    for id in ids:
        cursor = db.cursor()
        cursor.execute("DELETE FROM newsletter WHERE id = %s"%(id))
        db.commit()
        cursor.close()

def main():
    id_to_delete=[]
    emails = get_email_address_to_send()
    ssl_context = ssl.create_default_context()
    service = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl_context)
    service.login(sender_email, pwd)
    for email in emails:
        today = datetime.date.today()
        id_to_delete.append(email[0])
        if email[1] - today >= datetime.timedelta(days=3):
            service.sendmail(sender_email,email[2],f"Subject: {subject}\n{content}")
    delete(id_to_delete)

while True:
	main()
	time.sleep(10)
