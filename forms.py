from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, RadioField, IntegerField, SubmitField, TextAreaField


class ChordForm(FlaskForm):
    title = StringField(label='Chord title', default=None)
    positions = StringField(label='Positions', default='0000')
    fingers = StringField(label='Fingers', default='----')
    label_all = BooleanField(label="Label all frets?", default=False)
    barre = IntegerField(label='Barre override', default=None)
    filename = StringField(label="Save As", default="chord.svg")

    extras = TextAreaField(label='Extra Fingers', default=None)

    render = SubmitField(label='Render diagram')
    # need a field to 'add extra fingers' -


class DownloadForm(FlaskForm):
    name = StringField(label='Name this image file', default='chord')
    submit = SubmitField('Download image')

