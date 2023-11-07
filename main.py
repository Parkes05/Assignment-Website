from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, exc
import os, form
from datetime import datetime as dt
import pandas as pd


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///bincomphptest.db')
db = SQLAlchemy(app)

class Agentname(db.Model):
    id = db.Column('name_id', db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(13), nullable=False)
    pollingunit_uniqueid =  db.Column(db.Integer, nullable=False)

class AnnouncedLga(db.Model):
    __tablename__ = 'announced_lga_results'
    id = db.Column('result_id', db.Integer, primary_key=True)
    lga_name = db.Column(db.String(50), nullable=False)
    party_abbreviation = db.Column(db.String(4), nullable=False)
    party_score =  db.Column(db.Integer, nullable=False)
    entered_by_user = db.Column(db.String(50), nullable=False)
    date_entered = db.Column(db.String(50), nullable=False)
    user_ip_address =  db.Column(db.String(50), nullable=False)

class AnnouncedPu(db.Model):
    __tablename__ = 'announced_pu_results'
    id = db.Column('result_id', db.Integer, primary_key=True)
    polling_unit_uniqueid =  db.Column(db.String(50), nullable=False)
    party_abbreviation = db.Column(db.String(4), nullable=False)
    party_score =  db.Column(db.Integer, nullable=False)
    entered_by_user = db.Column(db.String(50), nullable=False)
    date_entered = db.Column(db.String(50), nullable=False)
    user_ip_address =  db.Column(db.String(50), nullable=False)

class AnnouncedState(db.Model):
    __tablename__ = 'announced_state_results'
    id = db.Column('result_id', db.Integer, primary_key=True)
    state_name =  db.Column(db.String(50), nullable=False)
    party_abbreviation = db.Column(db.String(4), nullable=False)
    party_score =  db.Column(db.Integer, nullable=False)
    entered_by_user = db.Column(db.String(50), nullable=False)
    date_entered = db.Column(db.String(50), nullable=False)
    user_ip_address =  db.Column(db.String(50), nullable=False)

class AnnouncedWard(db.Model):
    __tablename__ = 'announced_ward_results'
    id = db.Column('result_id', db.Integer, primary_key=True)
    ward_name =  db.Column(db.String(50), nullable=False)
    party_abbreviation = db.Column(db.String(4), nullable=False)
    party_score =  db.Column(db.Integer, nullable=False)
    entered_by_user = db.Column(db.String(50), nullable=False)
    date_entered = db.Column(db.String(50), nullable=False)
    user_ip_address =  db.Column(db.String(50), nullable=False)

class Lga(db.Model):
    id = db.Column('uniqueid', db.Integer, primary_key=True)
    lga_id = db.Column(db.Integer, nullable=False)
    lga_name = db.Column(db.String(50), nullable=False)
    state_id = db.Column(db.Integer, nullable=False)
    lga_description = db.Column(db.Text)
    entered_by_user = db.Column(db.String(50), nullable=False)
    date_entered = db.Column(db.String(50), nullable=False)
    user_ip_address = db.Column(db.String(50), nullable=False)

class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partyid = db.Column(db.String(11), nullable=False)
    partyname = db.Column(db.String(11), nullable=False)

class PollingUnit(db.Model):
    __tablename__ = 'polling_unit'
    id = db.Column('uniqueid', db.Integer, primary_key=True)
    polling_unit_id = db.Column(db.Integer, nullable=False)
    ward_id = db.Column(db.Integer, nullable=False)
    lga_id = db.Column(db.Integer, nullable=False)
    uniquewardid = db.Column(db.Integer, nullable=True)
    polling_unit_number = db.Column(db.String(50), nullable=False)
    polling_unit_name = db.Column(db.String(50), nullable=False)
    polling_unit_description = db.Column(db.Text)
    lat = db.Column(db.String(255), nullable=True)
    long = db.Column(db.String(255), nullable=True)
    entered_by_user = db.Column(db.String(50), nullable=True)
    date_entered = db.Column(db.String(50), nullable=True)
    user_ip_address = db.Column(db.String(50), nullable=True)

class States(db.Model):
    id = db.Column('state_id', db.Integer, primary_key=True)
    state_name = db.Column(db.String(50), nullable=False)

class Ward(db.Model):
    id = db.Column('uniqueid', db.Integer, primary_key=True)
    ward_id = db.Column(db.Integer, nullable=False)
    ward_name = db.Column(db.String(50), nullable=False)
    lga_id = db.Column(db.Integer, nullable=False)
    ward_description = db.Column(db.Text)
    entered_by_user = db.Column(db.String(50), nullable=False)
    date_entered = db.Column(db.String(50), nullable=False)
    user_ip_address = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

datetime = dt.now().strftime('%B, %Y')
databases = ['agentname', 'announced_lga_results', 'announced_pu_results', 'announced_state_results', 'announced_ward_results', 'lga', 'party', 'polling_unit', 'states', 'ward']


@app.route('/')
def home():
    pu = db.session.execute(db.select(PollingUnit)).scalars().all()
    return render_template('index.html', sum=False, date=datetime, pu=pu)

@app.route('/LGA-Result', methods=['GET','POST'])
def sum():
    lga = db.session.execute(db.select(Lga)).scalars().all()
    if request.method == 'POST':
        unique_id = request.form.get('comp_select')
        my_pr = db.session.execute(db.select(PollingUnit).where(PollingUnit.lga_id == unique_id)).scalars().all()
        result = []
        for i in my_pr:
            pr = db.session.execute(db.select(AnnouncedPu).where(AnnouncedPu.polling_unit_uniqueid == i.polling_unit_id)).scalars().all()
            if pr != []:
                result.append(pr)
        party = []
        score = []
        for i in result:
            for j in i:
                party.append(j.party_abbreviation)
                score.append(j.party_score)

        df = pd.DataFrame({'party':party, 'score':score})
        new = df.groupby('party').sum()
        party = []
        score = []
        for index, row in new.iterrows():
            party.append(index)
            score.append(row.score)
        return render_template('index.html', sum=True, date=datetime, lga=lga, party=party, score=score)
    return render_template('index.html', sum=True, date=datetime, lga=lga)

@app.route('/secrets')
def secrets():
    for i in databases:
        with open(f'data/{i}.txt', 'r') as f:
            sql = text(f'{f.read()}') 
            try:
                db.session.execute(sql)
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
    return redirect(url_for('home'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    update_form = form.Form()
    if update_form.validate_on_submit():
        dt_ = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = request.remote_addr
        data = [('pdp',update_form.pdp.data), ('dpp',update_form.dpp.data), ('acn',update_form.acn.data), ('ppa',update_form.ppa.data), ('cdc',update_form.cdc.data), ('jp',update_form.jp.data), ('anpp',update_form.anpp.data), ('labour',update_form.labour.data), ('cpp',update_form.cpp.data)] 
        pu_id = update_form.id.data
        user = update_form.user.data
        for i in data:
            db.session.add(AnnouncedPu(
                polling_unit_uniqueid=pu_id,
                party_abbreviation=i[0].upper(),
                party_score=i[1],
                entered_by_user=user,
                date_entered=dt_,
                user_ip_address=ip
            ))
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('update.html', sum=True, date=datetime, form=update_form)

@app.route("/result", methods=['POST'])
def result():
    id = request.form.get('comp_select')
    pr = db.session.execute(db.select(AnnouncedPu).where(AnnouncedPu.polling_unit_uniqueid == id)).scalars().all()
    party = []
    score = []
    for i in pr:
        party.append(i.party_abbreviation)
        score.append(i.party_score)
    pu = db.session.execute(db.select(PollingUnit)).scalars().all()
    return render_template('index.html', sum=False, date=datetime, pu=pu, party=party, score=score)

    
if __name__ == '__main__':
    app.run(debug=True)
