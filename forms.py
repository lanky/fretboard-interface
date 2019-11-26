from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    RadioField,
    IntegerField,
    SubmitField,
    TextAreaField,
    HiddenField
    )


class ChordForm(FlaskForm):
    title = StringField(label='Chord title', default=None)
    positions = StringField(label='Positions', default='0000')
    fingers = StringField(label='Fingers', default='----')
    label_all = BooleanField(label="Label all frets?", default=False)
    barre = IntegerField(label='Barre override', default=None)
    filename = StringField(label="Save As", default="chord.svg")

    extras = TextAreaField(label='Extra Fingers', default=None)

    render = SubmitField(label='Render diagram')
    # hidden field to hold diagram content
    diagram = HiddenField(label="diagram content", default="No diagram")


class DownloadForm(FlaskForm):
    DL_FORMATS = [
            ('svg', 'svg'),
            ('png_t', 'png (transparent)'),
            ('png', 'png')
            ]
    filename = StringField(label='Name this image file', default='chord')
    format = RadioField(label="File format", choices=DL_FORMATS)
    submit = SubmitField('Download image')

