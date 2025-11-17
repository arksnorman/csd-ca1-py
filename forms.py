from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class BloodPressureForm(FlaskForm):
    """Form for Blood Pressure input"""

    systolic = IntegerField(
        "Systolic Value",
        validators=[
            DataRequired(),
            NumberRange(min=70, max=190, message="Invalid Systolic Value"),
        ],
    )
    diastolic = IntegerField(
        "Diastolic Value",
        validators=[
            DataRequired(),
            NumberRange(min=40, max=100, message="Invalid Diastolic Value"),
        ],
    )
    submit = SubmitField("Calculate")
