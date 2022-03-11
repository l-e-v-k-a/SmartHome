import socket
from flask import Flask, render_template, redirect, request, session


class Device():
    def __init__(self, tag, name, pin, status=False):
        self.tag = tag
        self.name = name
        self.pin = pin
        self.status = status

    def setStatus(self, status):
        self.status = status

    def getInfo(self):
        info = {
            'tag': self.tag,
            'name': self.name,
            'pin': self.pin,
            'status': self.status
        }
        return info


light1 = Device('light1', 'Свет 1', 13)
light2 = Device('light2', 'Свет 2', 14)
boiler = Device('boiler', 'Чайник', 15)
devices = [light1, light2, boiler]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
adminData = {"username": "admin", "password": "LetMeIn"}


@app.route('/', methods=['POST', 'GET'])  # Страница авторизации
def login():
    if request.method == 'GET':  # Просто получаем страницу
        if session.get('is_auth'):  # Если мы авторизованы то редирект на страницу пользоавателя
            return redirect("/main")
        return render_template("login.html", error_alert="")
    elif request.method == 'POST':  # Посылаем Логин и Пароль через форму
        username = request.form.get('username')
        password = request.form.get('password')
        # print(username, password)  # Эта строчка использовалась во время разработки и полезна при отладке
        if username == adminData["username"] and password == adminData["password"]:
            session["is_auth"] = True  # Если проверка прошла то говорим что пользователь авторизован
            return redirect("/main")  # Переадресуем уже авторизованого пользователя на главную
        else:  # Если логин и пароль проверку не прошли то загружаем ту же страницу, но с сообщением об ошибке
            return render_template("login.html", error_alert="Неверный логин и/или пароль")

@app.route('/main', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        if not session.get('is_auth'):  # Если ты не авторизован то иди авторизуйся
            return redirect("/")
    elif request.method == 'POST':
        for d in devices:
            status = (request.form.get(d.getInfo()['tag']) == "on")
            d.setStatus(status)
            print(d.getInfo()["status"]*'+' + (not d.getInfo()["status"])*'-')
    return render_template('index.html', devices=devices)


if __name__ == '__main__':
    app.run(host=socket.gethostbyname(socket.gethostname()), port=27015)