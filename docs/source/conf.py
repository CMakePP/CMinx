# -*- coding: utf-8 -*-
import datetime
import os
import sys
now = datetime.datetime.now()

project = 'CMinx'
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
numfig = True
exclude_patterns = ['build', '.templates']
pygments_style = 'sphinx'
# Required theme setup
html_theme = 'sphinx_rtd_theme'

# html_theme_options = {
#     'analytics_id': 'G-XXXXXXXXXX',  #  Provided by Google in your dashboard
#     'analytics_anonymize_ip': False,
#     'logo_only': False,
#     'display_version': True,
#     'prev_next_buttons_location': 'bottom',
#     'style_external_links': True,
#     'vcs_pageview_mode': 'blob',
#     #'style_nav_header_background': 'white',
#     # Toc options
#     'collapse_navigation': True,
#     'sticky_navigation': True,
#     'navigation_depth': 4,
#     'includehidden': True,
#     'titles_only': False,

# }

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
