from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
    
@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    
    adminEmail = "qwer@qwer.com"
    adminPassword = "12341234"
    
    # 만약 회원가입한 회원이 admin일 경우,
    #   "관리자님 환영합니다."
    # 아닐경우,
    #   만약 아이디만 맞는 경우,
    #       "관리자님 비번이 틀렸습니다. 좀 더 생각해보세요."
    #   아이디도 틀릴 경우
    #       "꺼지셈"
    msg = ""
    if email == adminEmail and password == adminPassword :
        msg = "관리자님 환영합니다."
    else :
        if email == adminEmail :
            msg = "관리자님 비번이 틀렸습니다. 좀 더 생각해보세요."
        else :
            msg = "꺼지셈."
    
    return render_template('signup.html', email=email, msg=msg)