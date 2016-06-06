import os
from util import chart_renderer


BASEDIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
FLATPAGES_HTML_RENDERER = chart_renderer
