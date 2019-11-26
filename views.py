from flask import (
    render_template,
    request,
    Blueprint,
    make_response
    )

from diagram import MultiFingerChord
from .forms import ChordForm, DownloadForm

import cairosvg
from wand.image import Image

import yaml

from .config import DEFAULT_STYLE

my_view = Blueprint('my_view', __name__)

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

        chord_style = DEFAULT_STYLE

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
    dl_form = DownloadForm(request.form)

    if request.method == 'POST':
        # Diagram
        if chord_form.validate_on_submit():
            return render_template(
                'index.html',
                diagram=create_diagram(chord_form),
                chord_form=chord_form,
                dl_form=dl_form
            )

    return render_template(
                'index.html',
                diagram=create_diagram(chord_form),
                chord_form=chord_form,
                dl_form=dl_form
            )

@my_view.route('/download', methods=['POST'])
def download_as():
    if request.method == 'POST':
        if format == 'png_t':
            # convert using cairosvg
            result = cairosvg.svg2png(imgdata)
        elif format == 'png':
            i = wand.image.Image(blob=imgdata)
            result = i.convert('png').make_blob()
        else:
            result = imgdata

        return send_file(io.BytesIO(imgdata), as_attachment=True, filename='chord.svg')

@my_view.route('/api/v1/chord/', methods=['POST'])
def generate_chord():
    """
    process the request body and return SVG content (no XML header)
    """
    content = request.get_json(silent=True)
    chordobj = MultiFingerChord(
            positions=content.get('positions', '0000'),
            fingers=content.get('fingers','----'),
            barre=content.get('barre', None),
            title=content.get('title', 'Am7'),
            extras=content.get('extras', None),
            style=chord_style
            ).render()
    chordobj.seek(0)
    header, data = chordobj.read().splitlines()

    # export type
    fmt = content.get('format', 'svg')

    if fmt != 'svg':
        content_type = 'image/png'
        ext = 'png'
    else:
        content_type = 'image/svg+xml'
        ext = 'svg'

    # OK, we have a chord object, let's return it
    if fmt == 'png_t':
        # do cairo stuff
        data = cairosvg.svg2png(bytestring=data.encode('utf-8'))

    if fmt == 'png':
        with Image(blob=data.encode('utf-8')) as i:
            data = i.convert('png').make_blob()

    response = make_response(data)
    response.headers.set('Content-Type', content_type)
    response.headers.set('Content-Disposition', 'attachment', filename="{}.{}".format(content.get('title'), ext))

    return response

