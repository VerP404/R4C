from django.core.mail import send_mail


def send_notification_email(email, robot):
    subject = "Робот в наличии"
    message = f"Добрый день!\nНедавно вы интересовались нашим роботом модели {robot.model}, версии {robot.version}.\n" \
              f"Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."
    from_email = "example@example.com"
    recipient_list = [email]
    print(message) # для проверки работоспособности. удалить!
    try:
        send_mail(subject, message, from_email, recipient_list)
    except ConnectionRefusedError:
        print("Почтовый сервер не доступен! Убедитесь в корректной настройке подключения к SMTP-серверу")
