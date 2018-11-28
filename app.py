
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import session,redirect,request,url_for,render_template
import requests
import json
from bs4 import BeautifulSoup
import pymysql



app = Flask(__name__)

app.config['SECRET_KEY'] = 'xxx'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Andy0102@localhost:3306/pvp?charset=utf8'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class herodata(db.Model):
    __tablename__ = 'hero_data'
    id = db.Column(db.Integer, primary_key=True)
    ename = db.Column(db.Integer, unique=True)
    cname = db.Column(db.String(120), unique=True)
    title = db.Column(db.String(120), unique=True)

    def __init__(self, ename, cname, title):
        self.ename = ename
        self.cname = cname
        self.title = title

class heroskill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_one = db.Column(db.String(120), unique=True)
    detail_one = db.Column(db.String(1000), unique=True)
    skill_two = db.Column(db.String(120), unique=True)
    detail_two = db.Column(db.String(1000), unique=True)
    skill_three = db.Column(db.String(120), unique=True)
    detail_three = db.Column(db.String(1000), unique=True)
    skill_four = db.Column(db.String(120), unique=True)
    detail_four = db.Column(db.String(1000), unique=True)
    skill_five = db.Column(db.String(120), unique=False)
    detail_five = db.Column(db.String(1000), unique=False)
    heroid = db.Column(db.Integer, unique= True)
    
    def __init__(self,skill_one,detail_one,skill_two,detail_two,skill_three,detail_three,skill_four,detail_four,skill_five,detail_five,heroid):
        self.skill_one = skill_one
        self.skill_two = skill_two
        self.skill_three = skill_three
        self.skill_four = skill_four
        self.skill_five = skill_five
        self.detail_one = detail_one
        self.detail_two = detail_two
        self.detail_three = detail_three
        self.detail_four = detail_four
        self.detail_five = detail_five
        self.heroid = heroid
        
    
db.create_all()


def get_herolist(url):
    response = requests.get(url)
    return response.json()


for i in get_herolist('https://pvp.qq.com/web201605/js/herolist.json'):
    setin = True
    for j in herodata.query.all():
        if j.ename == i['ename']:
            setin = False
    
    if setin :
        hdata = herodata(i['ename'],i['cname'],i['title'])
        db.session.add(hdata)
        db.session.commit()




for heroes in herodata.query.all():
    setin = True
    skilllist = []
    
    for i in heroskill.query.all():
        if i.heroid == heroes.ename:
            setin = False
    if setin :
        url = 'https://pvp.qq.com/web201605/herodetail/' + str(heroes.ename) + '.shtml'
        response = requests.get(url)
        response.encoding = 'gbk'
        soup = BeautifulSoup(response.text,features="html.parser")
        i = soup.find_all('p')
        html = '''
        %s
        '''
        for a in range(10):
            soup = BeautifulSoup(html % i[a], features="html.parser")
            if not soup.b == None:
                if not soup.b.string == None:
                    skilllist.append(str(soup.b.string))
    
            else:
                if not soup.p == None:
                    if not soup.p.string == None:
                        skilllist.append(str(soup.p.string))

        if len(skilllist) == 8:
            skilldata = heroskill(skilllist[0],skilllist[1],skilllist[2],skilllist[3],skilllist[4],skilllist[5],skilllist[6],skilllist[7],'无','无',heroes.ename)
        if len(skilllist) == 10:
            skilldata = heroskill(skilllist[0],skilllist[1],skilllist[2],skilllist[3],skilllist[4],skilllist[5],skilllist[6],skilllist[7],skilllist[8],skilllist[9],heroes.ename)
        
        db.session.add(skilldata)
        db.session.commit()








@app.route('/',methods=['GET','POST'])
def index():
    if not 'username' in session:
        return render_template('index.html')
    else:
        return render_template('herolist.html',imgurl='https://game.gtimg.cn/images/yxzj/img201606/heroimg/',username=session['username'],fuck = herodata.query.all())

@app.route('/login',methods = ['post'])
def login():
    session['username'] = request.form.get('username')
    return redirect('/')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

@app.route('/herodetail',methods = ['post'])
def herodetail():
	if herodata.query.filter_by(ename = request.form.get('heroid')).first() != None:
		return render_template('herodetail.html',imgurl='https://game.gtimg.cn/images/yxzj/img201606/heroimg/',deone =  herodata.query.filter_by(ename = request.form.get('heroid')).first(),detwo = heroskill.query.filter_by(heroid = request.form.get('heroid')).first())
	return 'fuck'

app.run(debug = True)
