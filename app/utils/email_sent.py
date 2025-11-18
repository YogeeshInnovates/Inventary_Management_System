from app.database import get_db
from datetime import datetime ,timedelta
import  smtplib
from email.mime.text import MIMEText
from app.models import User_Pick_object,User
def send_email(to_email,subject,body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "yogiemailpractice@gmail.com"
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login("yogiemailpractice@gmail.com","tevmldbyynqbctey")
        server.send_message(msg)

def check_overdue_products():
    db=next(get_db())
    # db=SessionLocal()
    now = datetime.now()
    tweleve_hours_ego = now - timedelta(minutes=3)

    user_info = db.query(User_Pick_object).filter(User_Pick_object.status_of_getting == "Not return",User_Pick_object.picking_date<=tweleve_hours_ego ).all()

    for pick in user_info:
        users=db.query(User).filter(User.id == pick.user_id).first()

        if users:
            send_email(
                users.email,"Return reminder",f"Hi {users.name}, you have not returned the product  within 12 hours. Please return it immediately!,or if you forget to update status in web, please update immidietly"
        
            )
    db.close()