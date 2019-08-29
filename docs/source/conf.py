# -*- coding: utf-8 -*-
import datetime
import os
import sys
now = datetime.datetime.now()

project = 'CMakeDoc'
author = 'Ryan M. Richard'
version = '1.0.0'  # The short X.Y version
release = '1.0.0alpha'  # The full version, including alpha/beta/rc tags

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
exclude_patterns = ['build', '.templates']
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_static_path = []
htmlhelp_basename = project + 'doc'
extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.githubpages',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary'
]
autosummary_generate = True

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']
