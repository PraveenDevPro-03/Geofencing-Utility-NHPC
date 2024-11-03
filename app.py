from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///ProjectAMaster.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
app.app_context().push()

class ProjectMaster(db.Model):
    pid=db.Column(db.Float, primary_key=True)
    pname=db.Column(db.String(500), nullable=False)
    plat=db.Column(db.Float, nullable=False)
    plong=db.Column(db.Float, nullable=False)
    pdetails=db.Column(db.String(1000), nullable=False)

    def __repr__(self) -> str:
        return f'{self.pid}-{self.plat}-{self.plong}'

# add new field in ProjectMaster
@app.route('/new/')
def formdata():
    return render_template('NewProject.html')

# delete rows in ProjectMaster
@app.route('/delete/<float:pid>')
def delete(pid):
    dell=ProjectMaster.query.filter_by(pid=pid).first()
    db.session.delete(dell)
    db.session.commit()
    obj2=ProjectMaster.query.all()
    return render_template('ProjectMaster.html', obj=obj2)

@app.route('/update/<float:pid>',methods=['GET', 'POST'])
def update(pid):
    if request.method=='POST':
        id=request.form['pid']
        name=request.form['pname']
        lat=request.form['plat']
        long=request.form['plong']
        details=request.form['pdetails']

        updt=ProjectMaster.query.filter_by(pid=pid).first()
        updt.pid=id
        updt.pname=name
        updt.plat=lat
        updt.plong=long
        updt.pdetails=details

        db.session.add(updt)
        db.session.commit()
        obj1=ProjectMaster.query.all()
        return render_template('ProjectMaster.html', obj=obj1)
        # return redirect('/')


    updt=ProjectMaster.query.filter_by(pid=pid).first()
    return render_template('Update.html', up=updt)

@app.route('/project/', methods=['GET', 'POST'])
def Check():
    if request.method=='POST':
        pid=request.form['pid']
        name=request.form['pname']
        lat=request.form['plat']
        long=request.form['plong']
        details=request.form['pdetails']

        pm=ProjectMaster(pid=pid, pname=name, plat=lat, plong=long, pdetails=details)
        db.session.add(pm)
        db.session.commit()
    obj=ProjectMaster.query.all()
    return render_template('ProjectMaster.html', obj=obj)

@app.route('/')
def Home():
    loc=ProjectMaster.query.all()
    return render_template('Map.html', locations=loc)

if __name__=='__main__':
    app.run(debug=True)