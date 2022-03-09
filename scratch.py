import socket
from flask import Flask, render_template, redirect, request, session

adminData = {"username": "admin", "password": "LetMeIn"}
# devicesInfo = [["Свет 1", False], ["Свет 2", False]]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'

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
        light1 = (request.form.get("light1") == "on")
        print(light1)
        status1 = "" + "checked"*light1
    return render_template('index.html', status1=status1)


if __name__ == '__main__':
    app.run(host=socket.gethostbyname(socket.gethostname()), port=27015)