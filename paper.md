---
title: 'CMinx: Sphinx Documentation Generator for CMake'
tags:
  - Python
  - CMake
  - Documentation
authors:
  - name: Branden Butler
    equal-contrib: true
    affiliation: "1, 2"
  - name: Ryan M. Richard
    orcid: 0000-0000-0000-0000
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
(code written in the CMake language). Since much of CMinx's intended audience
are C/C++ developers, we designed CMinx to operate similar to 
Doxygen [@doxygen] (the *de facto* C/C++ API documentation tool). 
Specifically, CMinx users add documentation comments to their CMake source
code, and then run CMinx to generate Sphinx-compatible restructrued text (reST)
files containing the API documentation. Unlike other CMake documentation 
solutions, CMinx is aware of the grammar of the CMake language, thus CMinx 
automatically extracts function/macro signatures (even when functions are 
not documented), and is capable of generating documentation for the CMake 
language's more idiosyncratic elements (*e.g.*, targets and generator 
expressions). Furthermore, users can eaisily control almost every aspect 
of the generated reST files via a YAML (YAML ain't Markup Language) 
configuration file. The CMakePP organization manages a substantial CMake code
base and has found CMinx to be invaluable to developer productivity. As more
research software begins to treat infrastructure as code, we anticipate
CMinx proving valueable to other projects as well.

# Statement of need

The exascale-era of high-performance scientific computing arguably started when
the Frontier supercomputer achieved a performance of more than 1.1 exaFLOPs
(10$^{18}$ floating-point operations per second) on the High-Performance
Linpack Benchmark [@frontier]. With the breakdown of Dennard scaling,
achieving exascale performance is presently only possible by relying
on heterogeneous hardware. Unfortunately hardware heterogeneity significantly
complicates high-performance scientific software development.
For many high performance software packages, these complications start in the
build system.

As build systems for scientific software become more complicated there is an
increasing desire to treat the build system as code. This means that the
build system should be modularized, and those modules should be documented,
tested, and reusable. With the popularity of C/C++ for high-performance
computing, "build system" is increasingly becoming synonymous with CMake
(*N.B.* CMake is often described as a build system generator; however, since
the typical CMake workflow encapsulates running the build system, we
ignore the "generator" distinction in our present discussion). Therefore
there is a need for a robust CMake development ecosystem in modern
high-performance scientific software development.

CMake is typically used as a build system for software packages written
in a compiled language (*e.g.*, C or C++, but CMake supports a number of other
languages as well). For brevity we refer to the software package being
built as the "target". The CMake ecosystem contains a number of tools which
facilitate the development of the target, but notably absent from the CMake
ecosystem are resources to facilitate the development of the target's
literal build system. From a historical perspective, this is understandable
since CMake-based build systems have tended to be relatively small (*i.e.*,
less than ~1K lines of code) and tightly coupled to the identity of the
target. Modern build systems are increasingly complex and, depending on the
needs of the target, can include: hardware/software introspection, managing
optional dependencies, managing the target's development environment,
supporting multiple coding languages, coding language introspection, etc.
While it may be argued that some of these tasks are better handled outside
the build system, the point remains that CMake is actually a very flexible
language which can be used to automate complex development tasks. In all
likelihood scientific software developers are going to continue to use
CMake for increasingly complex tasks. Thus it behooves the build system
development community to grow the CMake ecosystem accordingly.

One of the most basic elements of a software development ecosystem is the
ability to generate application programming interface (API) documentation.
Anecdotal evidence [@official_solution] indicates that the CMake developers
internally write API documentation using restructured text (reST) and
Sphinx. Following best practices, this reST API documentation resides
next to the CMake source code being described. The CMake developers have
written a Sphinx plugin which makes it easy to extract the API documentation
as part of a normal Sphinx workflow. This Sphinx plugin is distributed with
the CMake source code, and is available in a mirrored GitHub repository
[@sphinx_plugin]. For completeness, we note that a couple of similar Sphinx
plugins [@official_sphinx_domain; @marco_koch] also exist, but they appear
to have been abandoned.

To our knowledge, all of the aforementioned documentation solutions simply 
extract the reST API documentation verbatim. Notably this means the
developer is responsible for manually: adding the function/macro signatures 
to the documentation, listing the function's parameters, and formatting
(*e.g.*, titles and subtitles, creation of parameter tables, underline/overline
consistency). For build system developers maintaining one or two CMake 
modules, these are admittedly pretty minor inconveniences; however, for 
an organizations which maintain a substational CMake code base, these "minor 
inconveniences" start to impact productivity. Hence, to increase the 
productivity of the CMakePP team, we created CMinx.

Concurrent to submitting this manuscript, we have also created the first public
release of CMinx. Promisingly, we have already started to see attention and 
interest from developers not affiliated with the CMakePP organization. 
So while, CMinx is not research software itself, we anticipate CMinx to be
useful to many research software developers, particularly as more projects 
adopt the "infrastructure as code" philosophy. 
# Acknowledgements

This research was supported by the Exascale Computing Project (17-SC-20-SC),
a collaborative effort of the U.S. Department of Energy Office of Science
and the National Nuclear Security Administration.

The authors would also like to acknowledge GitHub users ni-fgenois,
ni-dschiller, dschiller, and zachcran for discussions, bug-reports, and
bug-fixes.

# References
