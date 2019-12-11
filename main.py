#!/usr/bin/env python
from flask_bootstrap import Bootstrap
from flask import Flask
# from .views import my_view

app = Flask(__name__)
bootstrap = Bootstrap(app)

# app.register_blueprint(my_view)
app.config.from_pyfile('config.py')

# single file version for the moment. makes testing really simple
# form  definitions
from flask_wtf import FlaskForm
from wtforms import (
        StringField,
        BooleanField,
        SubmitField,
        FieldList,
        FormField,
        HiddenField,
        validators
        )

class ExtrasForm(FlaskForm):
    string = StringField('string', [validators.length(max=1)])
    fret   = StringField('fret', [validators.length(max=1)])
    label  = StringField('label', [validators.length(max=1)])


class ChordForm(FlaskForm):
    title = StringField('Chord title',
                        [validators.required(), validators.length(max=15)],
                        default='')

    positions = FieldList(
            StringField('',
                        [validators.required(), validators.length(max=2)],
                        default='0',
                       ),
            max_entries=4,
            min_entries=4)

    fingers  = FieldList(
                   StringField('',
                   [validators.required(), validators.length(max=1)],
                   default='-',
                   ),
               max_entries=4,
               min_entries=4)

    label_all = BooleanField(label="Label all frets?", default=False)

    barre = BooleanField('Draw Barre?', default=None)

    filename = StringField(label="Save As", default="chord.svg")

    extras = FieldList(FormField(ExtrasForm), min_entries=0, max_entries=4)

    render = SubmitField(label='Render diagram')

    # hidden field to hold diagram content
    diagram = HiddenField("diagram content", default="No diagram")

# utility functions

from diagram import MultiFingerChord
from .config import DEFAULT_STYLE

def create_diagram(**kwargs):
    """
    Generate a chord in SVG format using a kwargs dictionary
    """
    chord_style = DEFAULT_STYLE
    chord_style['drawing']['label_all_frets'] = kwargs.get('label_all', False)

    diagram = MultiFingerChord(style=chord_style, **kwargs)
    data = diagram.render()
    data.seek(0)
    return data.read()

def diagram_from_form(chordfm):
    """process a form"""

    barrepos = min([int(x) for x in chordfm.positions.data if x.isdigit()])

    diagram = MultiFingerChord(
            title=chordfm.title.data,
            positions=chordfm.positions.data,
            fingers=chordfm.fingers.data,
            barre=barrepos,
            extras=chord.form.extras0.data
            )

    # we're going to return a rendered version
    data = diagram.render()
    data.seek(0)
    return data.read()


# views
from flask import request, render_template
@app.route('/', methods=['GET', 'POST'])
def home():
    form = ChordForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            return render_template(
                'index.html',
                form=form)
    else:
        print(form.data)
        return render_template(
                    'index.html',
                    form=form,
                    diagram=create_diagram(
                        title='',
                        positions=['0', '0', '0', '0'],
                        fingers=['-', '-', '-', '-'],
                        label_all=False,
                        barre=None,
                        extras=None
                        )
                    )

if __name__ == '__main__':
    # let's run in debug mode for now
    app.run(debug=True)
