from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired


class Form(FlaskForm):
    pdp = IntegerField(label='PDP', validators=[DataRequired()])
    dpp = IntegerField(label='DPP', validators=[DataRequired()])
    acn = IntegerField(label='ACN', validators=[DataRequired()])
    ppa = IntegerField(label='PPA', validators=[DataRequired()])
    cdc = IntegerField(label='CDC', validators=[DataRequired()])
    jp = IntegerField(label='JP', validators=[DataRequired()])
    anpp = IntegerField(label='ANPP', validators=[DataRequired()])
    labour = IntegerField(label='LABOUR', validators=[DataRequired()])
    cpp = IntegerField(label='CPP', validators=[DataRequired()])
    id = IntegerField(label='Polling_unit_uniqueid', validators=[DataRequired()])
    user = StringField(label='Entered_by', validators=[DataRequired()])
    submit = SubmitField(label='Submit')