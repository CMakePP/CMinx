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
    corresponding: true # (This is how to denote the corresponding author)
    affiliation: "1, 2"
affiliations:
 - name: Ames National Laboratory, Ames, IA, USA
   index: 1
 - name: Iowa State University, Ames, IA, USA
   index: 2
date: XX August 2022
bibliography: paper.bib
---

# Summary

This manuscript introduces CMinx, a program for generating
application programming interface (API) documentation for CMake modules
(code written in the CMake language). Since most of CMinx's intended audience
is comprised of C/C++ developers, CMinx is designed to operate similar to
Doxygen [@doxygen] (the *de facto* C/C++ API documentation tool).
Specifically, developers annotate their CMake source with documentation
comments (traditional CMake block comments, starting with an extra "["
character). Running CMinx on the annotated source code generates
restructured text (reST) files containing the API documentation. Unlike other
solutions for documenting CMake modules, CMinx knows the CMake language's
grammar. In turn, CMinx can automatically extract function/macro signatures
(even when functions are not documented). CMinx is also aware of extensions to
the CMake programming language, such as the object-oriented CMakePP language
[@cmakepp], and the CMake unit testing framework [@cmaketest]. CMinx's output is
easily controlled via a YAML (YAML ain't Markup Language) configuration file.
The CMakePP organization manages a substantial CMake code base and has found
CMinx to be an invaluable productivity tool. As more and more scientific
software projects treat their software infrastructure as code, we anticipate
CMinx will prove invaluable to these other projects as well.

# Statement of need

The exascale-era of high-performance scientific computing arguably started when
the Frontier supercomputer achieved a performance of more than 1.1 exaFLOPs
(10$^{18}$ floating-point operations per second) on the High-Performance
Linpack Benchmark [@frontier]. With the breakdown of Dennard scaling
(*i.e.*, power density remains constant as transistors get smaller),
achieving exascale performance is presently only possible by relying
on heterogeneous hardware. Unfortunately, hardware heterogeneity significantly
complicates the process of developing high-performance scientific software.
For many high performance software packages, these complications start in the
build system.

As build systems for scientific software become more complicated there is an
increasing desire to treat the build system as code. This means that the
build system should be modularized, and those modules should be documented,
tested, and reusable. With the popularity of C/C++ for high-performance
computing, "build system" is increasingly becoming synonymous with CMake
(*N.B.* CMake is often described as a build system generator; however, since
the typical CMake workflow encapsulates running the build system, the
present manuscript ignores the "generator" distinction). Therefore
there is a need for a robust CMake development ecosystem.

CMake is typically used as a build system for software packages written
in a compiled language (*e.g.*, C or C++, but CMake supports a number of other
languages as well). For generality we refer to the software package being
built as the "target." The CMake ecosystem contains a number of tools that
facilitate the development of the target, but notably absent from the CMake
ecosystem are resources to facilitate the development of the target's
literal build system. From a historical perspective, this is understandable
since CMake-based build systems have tended to be relatively small (*i.e.*,
less than ~1K lines of code) and tightly coupled to the identity of the
target. Modern build systems are increasingly complex and, depending on the
needs of the target, can include: hardware/software introspection, managing
optional dependencies, managing the target's development environment,
supporting multiple programming languages, etc.
While it may be argued that some of these tasks are better handled outside
the build system, the point remains that CMake is actually a very flexible
language which can be used to automate complex development tasks. In all
likelihood, scientific software developers will continue to use
CMake for increasingly complex tasks and it behooves the research community
to grow the CMake ecosystem accordingly.

One of the most basic elements of a software development ecosystem is the
ability to generate API documentation.
Anecdotal evidence [@official_solution] indicates that the developers of the
CMake language (*i.e.*, Kitware) internally write their API documentation
using reST and Sphinx. Following best practices, this reST API
documentation resides next to the CMake code being described. Kitware has
also written a Sphinx plugin that makes it easy to extract the
API documentation as part of a normal Sphinx workflow. This Sphinx plugin
is distributed with the source code for the CMake interpreter, and is
also available in a GitHub repository mirror [@sphinx_plugin].
For completeness, we note that similar Sphinx
plugins [@official_sphinx_domain; @marco_koch] also exist, but they appear
to have been abandoned.

To our knowledge, all of the aforementioned documentation solutions simply
extract the reST API documentation verbatim. Notably this means the
developer is responsible for manually: adding the function/macro signatures
to the documentation, listing the function's parameters, and the overall
formatting (*e.g.*, titles and subtitles, creation of parameter
tables, underline/overline consistency). For build system developers
maintaining one or two CMake modules, these are admittedly pretty minor
inconveniences; however, for organizations which maintaining a substantial
CMake code base, these "minor inconveniences" can impact productivity.
In order to increase the productivity of the CMakePP team, we created CMinx.

Concurrent with the submission of this manuscript, we have also released the
1.0.0 production version of CMinx. The easiest means of obtaining CMinx is from
the Python Packaging Index via `pip install CMinx`. Alternatively, CMinx can
be used as a CMake module via installation via CMake's `FetchContent` command.
Despite only just releasing 1.0.0, the CMinx GitHub organization
has already started to see attention and interest from developers not
affiliated with the CMakePP organization. So while CMinx is not research
software itself, we anticipate CMinx to be a useful productivity tool for
many of the research software developers who use CMake as their build system.

# Acknowledgements

This research was supported by the Exascale Computing Project (17-SC-20-SC),
a collaborative effort of the U.S. Department of Energy Office of Science
and the National Nuclear Security Administration.

The authors would also like to acknowledge GitHub users ni-fgenois,
ni-dschiller, dschiller, and zachcran for discussions, bug-reports, and
bug-fixes.

# References
