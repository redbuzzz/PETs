import json

from django.core.mail import send_mail

from api.models import User
from freelance.celery import app


@app.task
def save_info_users():
    users = User.objects.all()
    email_list = [user.email for user in users]
    with open('api/services/user_data/info.json', 'w') as file:
        json.dump(email_list, file, indent=4)


@app.task
def send_messages():
    recipient_list = []
    with open('api/services/user_data/info.json', 'r') as file:
        data = json.load(file)
    for item in data:
        recipient_list.append(item)
    print(recipient_list)
    subject = 'Freelance'
    message = 'Здравствуйте! Вы давно у нас не были. Заходите!'
    from_email = 'redbuzzzzzz@gmail.com'
    # time.sleep(50)
    send_mail(subject, message, from_email, recipient_list)
