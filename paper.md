---
title: 'CMinx: A CMake Documentation Generator'
tags:
  - Python
  - CMake
  - Documentation
authors:
  - name: Branden Butler
    equal-contrib: true
    affiliation: "1, 2"
  - name: Ryan M. Richard
    orcid: 0000-0003-4235-5179
    equal-contrib: false
    corresponding: true # (This is how to denote the corresponding author)
    affiliation: "1, 2"
affiliations:
 - name: Ames National Laboratory, Ames, IA, USA
   index: 1
 - name: Iowa State University, Ames, IA, USA
   index: 2
date: August 2022
bibliography: paper.bib
---

# Summary

This manuscript introduces CMinx, a program for generating
application programming interface (API) documentation written in the CMake
language, and CMake modules in particular. Since most of CMinx's intended audience
is comprised of C/C++ developers, CMinx is designed to operate similar to
Doxygen [@doxygen], the *de facto* C/C++ API documentation tool.
Specifically, developers annotate their CMake source with "documentation"
comments, which are traditional CMake block comments starting with an extra
"`[`" character. The documentation comments, written in reST [@rest],
describe to the reader how the functions, parameters, and variables should be
used. Running CMinx on the annotated source code generates reST files containing
the API documentation. The reST files can then be converted into static
websites with tools such as Sphinx [@sphinx] or
easily converted to another format via Pandoc [@pandoc].

Unlike other solutions for documenting CMake modules, CMinx knows the CMake
language's grammar. This enables CMinx to automatically extract function/macro
signatures, even when functions are not documented. CMinx also integrates
seamlessly into existing CMake build systems. CMinx's output is highly
customizable and easily controlled via a YAML [@yaml] configuration file.
CMinx has already proved to be an invaluable
productivity tool in the authors' other projects, and, given that other
scientific software projects also rely heavily on source code written in CMake,
we anticipate CMinx will prove invaluable to many additional projects as well.

Concurrent with the submission of this manuscript, we have also released the
first production version of CMinx, version 1.0.0. CMinx can be obtained
from the Python Packaging Index via "`pip install CMinx`". Alternatively, CMinx
can be used as a CMake module via CMake's "`FetchContent`" command.
Despite only just releasing 1.0.0, the CMinx GitHub organization
has already started to see attention and interest from developers not
affiliated with the authors. We anticipate CMinx will be a useful productivity tool for the large
swath of research software that uses CMake as their build system.

# Statement of need

The process of building a software package written in a compiled language
(e.g., C, C++, Fortran) has always been complicated. Over the years, various build
system solutions have evolved to ease the process. Historically, there
has been a propensity to treat each build system as a one-off use case. This is
understandable since build systems have tended to be relatively small
and tightly coupled to the structure and purpose of the package.
With build system complexity at an all-time high [@snir2014; @xSDK], there is an
increasing need to treat the underlying build system infrastructure as code.
This means that the build system should be modularized, and those modules
should be documented, tested, and reusable. With the popularity of C/C++ for
high-performance computing, "build system" is increasingly becoming synonymous
with CMake: there is a desperate
need for a robust CMake development ecosystem.

CMake already contains a number of tools and features that facilitate
development of the target software package. For example, CMake's
`find_package` module simplifies dependency management, and the `CTest` package
eases the process of testing the resulting software. Additional CMake tools
can be created by writing CMake modules. While the CMake language is
flexible and relatively simple, it is not without its pitfalls. Unfortunately,
tools  to facilitate the development of CMake modules are relatively sparse.
Here we introduce CMinx, a tool for generating API documentation for CMake
modules. API documentation is arguably one of the most basic elements of a
software development ecosystem, and it is our hope that CMinx will serve as the
foundation for a robust CMake development ecosystem.

Anecdotal evidence [@official_solution] indicates that Kitware, the developers
of the CMake language, internally write their API documentation
using reST and Sphinx. Following best practices, this reST documentation
resides next to the described CMake code. Kitware has also written a
Sphinx plugin that makes it easy to extract the API documentation as part of a
normal Sphinx workflow. This Sphinx plugin is distributed with the source code
for the CMake interpreter and is also available in a GitHub repository mirror
[@sphinx_plugin]. For completeness, we note that similar Sphinx plugins
[@official_sphinx_domain; @marco_koch] have been independently developed but
appear to now be abandoned.

To our knowledge, all of the aforementioned Sphinx plugins simply extract the
reST API documentation verbatim. Notably, this means the developer is
responsible
for manually adding the function/macro signatures to the documentation, listing
the function's parameters, and the overall formatting. For
build system developers maintaining one or two CMake modules, these are
admittedly pretty minor inconveniences; however, for organizations
maintaining a substantial CMake code base (such as those for exascale programs),
these "minor inconveniences" can
impact productivity, particularly when ensuring consistency. CMinx
differs from previous solutions primarily in three ways. First, CMinx
understands the grammar of the CMake language, meaning CMinx can automatically
generate some of the documentation by "reading" the source code. Second, CMinx
generates static reST files; this decreases the number of stub files developers
need to maintain and makes it easier for the resulting documentation to be
used in workflows that do not rely on Sphinx. Finally, CMinx has a CMake API
to integrate more easily into existing CMake workflows.

# Acknowledgements

This research was supported by the Exascale Computing Project (17-SC-20-SC),
a collaborative effort of the U.S. Department of Energy Office of Science
and the National Nuclear Security Administration.

The authors would also like to acknowledge GitHub users dschiller, ni-dschiller,
ni-fgenois, peanutfun, robertodr, and zachcran for suggestions, discussions,
bug reports, and bug fixes.

# References
