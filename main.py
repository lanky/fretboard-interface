from flask import Flask
from flask_bootstrap import Bootstrap

from diagram import UkuleleChord, GuitarChord, MultiFingerChord

# to strip out that pesky baseprofile
from bs4 import BeautifulSoup as bs

import cairosvg
from wand.image import Image

import yaml


from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

chord_style = app.config["DEFAULT_STYLE"]


from .forms import ChordForm


def create_diagram(**kwargs):
    """
    create a diagram, based on kwargs. Any unsupported args will be ignored
    """
    chord_style["drawing"]["label_all_frets"] = kwargs.get("label_all", False)
    if "barre" in kwargs:
        bpos = min([int(p) for p in kwargs.get("positions", "0000") if p.isdigit()])
        if bpos == 0:
            bpos = None
    else:
        bpos = None

    title = kwargs.get("title", "")

    # extras is now automatically a list of dicts
    valid_extras = [
        e for e in kwargs.get("extras", []) if len(e["string"].strip()) == 1
    ]

    if len(valid_extras):
        extras = valid_extras
        for e in extras:
            e["label"] = e["marker"]
    else:
        extras = None

    # need to swap 'finger' for 'label'

    diag = MultiFingerChord(
        title=title,
        positions=kwargs.get("positions", "0000"),
        fingers=kwargs.get("fingers", "----"),
        barre=bpos,
        style=chord_style,
        extras=extras,
    )

    d = diag.render()
    d.seek(0)
    hdr, data = d.read().splitlines()

    s = bs(data)
    del s.svg["baseprofile"]

    return str(s)


def mkres(fmt, title, data):
    if fmt == "svg":
        content_type = "image/svg+xml"
    else:
        content_type = "image/{}".format(fmt)
    response = make_response(data)
    response.headers.set("Content-Type", content_type)
    response.headers.set(
        "Content-Disposition", "attachment", filename="{}.{}".format(title, fmt)
    )

    return response


# views
from flask import render_template, request, url_for, current_app, make_response


@app.route("/", methods=["GET", "POST"])
def home():
    """Main chord generation page"""
    chord_form = ChordForm(request.form)
    print(chord_form.data)

    if request.method == "POST":
        print(request.method)
        # Diagram

        if chord_form.validate_on_submit():
            print(chord_form.data)
            diag = create_diagram(**chord_form.data)
            print(diag)

            if chord_form.getsvg.data is True:
                soup = bs(diag)
                del soup.svg["baseprofile"]
                return mkres("svg", chord_form.title.data, str(soup))
            elif chord_form.getpng.data is True:
                payload = cairosvg.svg2png(bytestring=diag.encode("utf-8"))
                return mkres("png", chord_form.title.data, payload)

            else:
                return render_template("index.html", diagram=diag, form=chord_form,)
        else:
            print("form not validated")
            print(chord_form.data)
            print(chord_form.errors)

    return render_template(
        "index.html", diagram=create_diagram(title=""), form=chord_form,
    )


@app.route("/add_marker")
def add_marker():
    f = request.form


@app.route("/api/v1/chord/", methods=["POST"])
def generate_chord():
    """
    process the request body and return SVG content (no XML header)
    """
    content = request.get_json(silent=True)
    chordobj = MultiFingerChord(
        positions=content.get("positions", "0000"),
        fingers=content.get("fingers", "----"),
        barre=content.get("barre", None),
        title=content.get("title", "Am7"),
        extras=content.get("extras", None),
        style=chord_style,
    ).render()
    chordobj.seek(0)
    header, data = chordobj.read().splitlines()

    # export type
    fmt = content.get("format", "svg")

    if fmt != "svg":
        content_type = "image/png"
        ext = "png"
    else:
        content_type = "image/svg+xml"
        ext = "svg"

    # OK, we have a chord object, let's return it
    if fmt == "png_t":
        # do cairo stuff
        data = cairosvg.svg2png(bytestring=data.encode("utf-8"))

    if fmt == "png":
        with Image(blob=data.encode("utf-8")) as i:
            data = i.convert("png").make_blob()

    response = make_response(data)
    response.headers.set("Content-Type", content_type)
    response.headers.set(
        "Content-Disposition",
        "attachment",
        filename="{}.{}".format(content.get("title"), ext),
    )

    return response


if __name__ == "__main__":
    app.run()
