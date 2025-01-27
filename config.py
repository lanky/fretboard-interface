import yaml
SECRET_KEY = 'unguessable-secret'
DEFAULT_STYLE = yaml.safe_load(
"""
drawing:
  background_color:
  font_color: black
  font_family: Verdana
  # font-size for markers and labels
  font_size: 16
  height: 400
  width: 250
  spacing: 30
  label_all_frets: true

nut:
  color: black
  size: 10

fret:
  color: black
  size: 4
  label_all: true

inlays:
  color: black
  radius: 2

string:
  # style for string lines
  color: black
  size: 4
  # colour of markers for open and muted/unplayed strings
  muted_font_color: black
  open_font_color: black
  # things we could support
  # label_font_family
  # label_font_size
  equal_weight: true

marker:
  border_color: black
  color: black
  font_color: white
  radius: 14
  stroke_width: 2
  extra_color: red

title:
  font_color: black
  font_family: Verdana
  font_size: 24

fret_label:
  width: 28
  font_size: 24
  font_style: normal
""")
