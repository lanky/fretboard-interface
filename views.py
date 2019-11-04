from flask import render_template, request, url_for, Blueprint, current_app

from diagram import UkuleleChord, GuitarChord, MultiFingerChord

from forms import ChordForm, DownloadForm
import yaml
import json


my_view = Blueprint('my_view', __name__)

chord_style = yaml.safe_load(open('chord_diagram.yml'))


@my_view.route('/', methods=['GET', 'POST'])
def home():
    def create_diagram(chord_form):
        """Create chord diagram and return filename."""
        extras = [
                dict(
                    zip(['string', 'fret', 'finger'], x.split(',')[:3])
                )
                for x in chord_form.extras.data.splitlines()
        ]

        chord_style['drawing']['label_all_frets'] = chord_form.label_all.data
        print(chord_style)


        diagram = MultiFingerChord(
            positions=chord_form.positions.data,
            fingers=chord_form.fingers.data,
            barre=chord_form.barre.data,
            title=chord_form.title.data,
            style=chord_style,
            extras=extras
        )

        # This is obviously dumb, but works for now
        filename = 'static/ukulele/{title}_{pos}_{fin}_{bar}.svg'.format(
            title=chord_form.title.data,
            pos=chord_form.positions.data,
            fin=chord_form.fingers.data,
            bar=chord_form.barre.data,
        )
        diagram.save(filename)

        return filename

    chord_form = ChordForm(request.form)
    # download_form = DownloadForm(request.form)

    if request.method == 'POST':
        # Diagram
        if chord_form.validate_on_submit():
            return render_template(
                'index.html',
                diagram=create_diagram(chord_form),
                chord_form=chord_form,
                # download_form=download_form
            )

    return render_template(
                'index.html',
                diagram=create_diagram(chord_form),
                chord_form=chord_form,
                # download_form=download_form
            )



