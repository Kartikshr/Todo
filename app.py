from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class database(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    desc=db.Column(db.String(200),nullable=False)
    # password=db.Column(db.String(100),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
   

    def __repr__(self):
        return f"{self.sno} - {self.title}"
with app.app_context():
    db.create_all()
    
@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        print(request.form)
        title=request.form.get('title')
        desc=request.form.get('desc')
        # password=request.form.get('password')
        user=database(title=title,desc=desc)
        db.session.add(user)
        db.session.commit()
    alldata=database.query.all()
    return render_template('boot.html',alldata=alldata)
    # return "<p>Hello, World!</p>"
    
@app.route("/show")
def showing():
    alldata=database.query.all()
    print(alldata)
    return 'this is data page'
@app.route("/delete/<int:sno>")
def delete(sno):
    todo=database.query.filter_by(sno=sno).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    else:
        
        return redirect('/')

    return redirect("/")
@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        
        todo=database.query.filter_by(sno=sno).first()
        title=request.form.get('title')
        desc=request.form.get('desc')
        # password=request.form.get('password')
        todo.title=title
        todo.desc=desc
        db.session.commit()
        return redirect("/")
    todo=database.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
if __name__=="__main__":
    app.run(debug=False,host='0.0.0.0')
