# -*- coding: utf-8 -*-
import datetime
import os
import sys

#####
#  Gather some metadata about the project
#####

now = datetime.datetime.now()
docs_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
root_dir = os.path.join(docs_dir, "..")

project = 'CMinx'
author = 'CMakePP Team'
version  = ""
release  = ""

# release includes alpha, beta, rc, etc.; version is pure numeric
with open(os.path.join(root_dir, "version.txt")) as f:
    release = f.read()
    pieces = release.split('.')
    version = pieces[0] + '.' + pieces[1] +'.'
    version += ''.join(filter(str.isdigit, pieces[2]))


################################################################################
#             Shouldn't need to modify anything below this point               #
################################################################################

copyright = '{}, {}'.format(now.year, author)

# -- Assemble some paths -------------------------------------------------------
source_path = os.path.dirname(os.path.realpath(__file__))
doc_path = os.path.dirname(source_path)
root_path = os.path.dirname(doc_path)
build_path = os.path.join(doc_path, 'build')
sys.path.insert(0, root_path)

# -- General configuration -----------------------------------------------------
templates_path = ['.templates']
source_suffix = '.rst'
master_doc = 'index'
numfig = True
exclude_patterns = ['build', '.templates']
pygments_style = 'sphinx'
# Required theme setup
html_theme = 'sphinx_rtd_theme'

htmlhelp_basename = project + 'doc'
extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.githubpages',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx_rtd_theme'

]
autosummary_generate = True

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']
