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
import subprocess
import sys

######################################
#  Work out paths this script needs  #
######################################

now = datetime.datetime.now()
src_dir  = os.path.abspath(os.path.dirname(__file__))
docs_dir = os.path.abspath(os.path.join(src_dir, ".."))
root_dir = os.path.join(docs_dir, "..")

############################################
#  Gather some metadata about the project  #
############################################

project = 'CMinx'
author = 'CMakePP Team'

# Get the version from the git tag
git_cmd = ['git', 'describe', '--tags', '--abbrev=0']

# N.B. release includes alpha, beta, rc, etc.; version is pure numeric
release = subprocess.check_output(git_cmd).strip().decode()
version = release[1:]

#########################
#  Run CMinx on itself  #
#########################

cminx_out_dir = os.path.join(src_dir, "developer", "cmake")
cminx_in_dir = os.path.join(root_dir, "cmake")
args = ["-r", "-o", cminx_out_dir, cminx_in_dir]
cminx.main(args)

################################################################################
#             Shouldn't need to modify anything below this point               #
################################################################################

copyright = '{}, {}'.format(now.year, author)

# -- General configuration -----------------------------------------------------
templates_path = ['.templates']
source_suffix = '.rst'
master_doc = 'index'
numfig = True
exclude_patterns = ['build', '.templates']
pygments_style = 'sphinx'
# Required theme setup
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'vcs_pageview_mode' : 'edit'
}
html_context = {
    'display_github' : True,
    'github_user' : 'CMakePP',
    'github_repo' : 'CMinx',
    'github_version' : 'master/docs/source/'
}
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
