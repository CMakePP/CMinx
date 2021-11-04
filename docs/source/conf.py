# -*- coding: utf-8 -*-
# Copyright 2021 CMakePP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cminx
import datetime
import os
import sys

#####
#  Gather some metadata about the project
#####

now = datetime.datetime.now()
src_dir  = os.path.abspath(os.path.dirname(__file__))
docs_dir = os.path.abspath(os.path.join(src_dir, ".."))
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
# Run CMinx on itself
################################################################################


cminx_out_dir = os.path.join(src_dir, "developer", "cmake")
cminx_in_dir = os.path.join(root_dir, "cmake")
args = ["-r", "-o", cminx_out_dir, cminx_in_dir]
cminx.main(args)

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
