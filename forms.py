from flask_wtf import FlaskForm
from wtforms import (
    validators,
    StringField,
    BooleanField,
    RadioField,
    IntegerField,
    SubmitField,
    FormField,
    FieldList,
)


class ExtraFingerForm(FlaskForm):
    class Meta:
        csrf = False

    string = StringField("string", [validators.regexp("[x0-3]")])
    fret = StringField("fret", [validators.regexp("[0-9]+")])
    marker = StringField("label", [validators.length(max=1)])
    removeme = SubmitField("-")


class ChordForm(FlaskForm):
    title = StringField(label="Chord title", default=None)
    positions = FieldList(
        StringField(
            "",
            [
                validators.length(
                    min=1, max=2, message="Positions can be a maximum of 2 characters"
                ),
                validators.regexp("[x0-9]", message=""),
            ],
            default="0",
        ),
        min_entries=4,
        max_entries=4,
    )
    fingers = FieldList(
        StringField(
            "",
            [validators.length(max=1, message="Labels can only be one character")],
            default="-",
        ),
        min_entries=4,
        max_entries=4,
    )

    extras = FieldList(FormField(ExtraFingerForm), min_entries=0)
    addmarker = SubmitField("+")

    label_all = BooleanField(label="Label all frets", default=False)
    barre = BooleanField("Draw Barre", default=False)
    reverse = BooleanField("Make Sinister", default=False)
    filename = StringField(label="Save As", default="chord.svg")

    render = SubmitField("Render diagram")
    getsvg = SubmitField("SVG")
    getpng = SubmitField("PNG")
    # need a field to 'add extra fingers' -


class DownloadForm(FlaskForm):
    name = StringField(label="Name this image file", default="chord")
    submit = SubmitField("Download image")
