from flask import * # web应用框架
import os # 检查文件是否存在
from helper_functions import *

app = Flask(__name__) # port端口，起到服务器的作用
UPLOAD_PATH = 'uploads' # 这行什么意思？设定变量，记录上传路径
# create this directory if not exist

app.config['UPLOAD_PATH'] = UPLOAD_PATH # 配置默认的上传地址，全局变量（在任何函数，任何页面都可以获取
app.secret_key = "123456" # 这行什么意思？flask的机制，保证应用安全


@app.route('/', methods=["GET", "POST"]) # 网站路径（默认路径）# 前面的/什么意思？路由
def index():
    if request.method == "POST":
        username = request.form["username"] # 这个form是干啥的？填的表格，将两个输入框包在表格里
        password = request.form["password"]
        print("Get username and password: ", username, password) # debug

        login_result = login(username, password)
        if login_result is not None:
            session["username"] = username
            return render_template('loginsuccess.html', username = session["username"])
            flash("Incorrect Username or Password")

    print(os.getcwd())

    return render_template('mainpage.html') # 渲染模板，以后将mainpage装到这里

@app.route('/signup', methods=["GET", "POST"]) # 每个函数前的这个网址是这个函数本身的网址还是这个函数结束后会跳转到的网址？函数本身
def signup_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirmpassword = request.form["confirmpassword"]
        if confirmpassword != password:
            flash("Enter same password.") # 是做弹窗还是在输入框里写"Enter same password."？做弹窗
            return render_template("signup.html")
        else:
            signup_result = signup(username, password)
            if signup_result is not None:
                return render_template("loginsuccess.html")
            else:
                flash("Username has already exists")
        return render_template("logininsuccess.html")
    else:
        return render_template("signup.html")


@app.route('/upload', methods=['GET','POST']) # 网站路径（upload的页面）
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files: # 检查请求中是否包含文件
            return 'No File'
        print(request.files) # 打印请求中的文件信息
        file = request.files['file'] # 获取上传的文件对象
        if not file.filename: #检查上传的文件是否有文件名
            return "No File Selected" # 并未上传文件
        if file:
            filename = file.filename # 设置文件名
            username = session["username"] # 从会话中获取用户名
            filepath = str(upload_meme(username, filename)) + ".jpg" # 生成文件路径
            filepath = os.path.join(app.config['UPLOAD_PATH'], filepath) # 拼接文件路径          
            file.save(filepath) # 保存文件到指定路径         
            return f'File {filename} uploaded successfully'     
        else:
            return 'File not valid' # 如果文件无效，返回提示信息
    return render_template("upload.html", username = session["username"]) # 如果是GET请求，渲染上传页面并传递用户名


@app.route('/monkey', methods=['GET']) # 网站路径（upload的页面）
def monkey():
    return render_template("monkey.html")

@app.route('/chinese', methods=['GET'])
def chinese():
    return render_template("chinese.html")

@app.route('/panda', methods=['GET'])
def panda():
    return render_template("panda.html")

@app.route('/emotion', methods=['GET'])
def emotion():
    return render_template("emotion.html")

@app.route('/chat', methods=['GET'])
def chat():
    return render_template("chat.html")

@app.route('/cat', methods=['GET'])
def cat():
    return render_template("cat.html")

@app.route('/bear', methods=['GET'])
def bear():
    return render_template("bear.html")

@app.route('/dog', methods=['GET'])
def dog():
    return render_template("dog.html")

@app.route('/trump', methods=['GET'])
def trump():
    return render_template("trump.html")



if __name__ == '__main__':
    app.run(debug=True) # 启动Flask应用，开启调试模式

