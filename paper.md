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

The exascale-era of high-performance computing arguably started when the
Frontier supercomputer achieved a speed of more than 1.1 exaFLOPs (10$^{18}$
floating-point operations per second) [@frontier]. With the breakdown of
Dennard scaling, achieving exascale performance was only possible by relying
on heterogeneous hardware. Unfortunately, hardware heterogeneity is likely here
to stay for the foreseeable future, even though it significantly complicates
high-performance scientific software development. For many high performance
software packages, these complications start in the build system.

As build systems for scientific software become more complicated there is an
increasing desire to treat the infrastructure as code. This means that the
build system should be modularized, and those modules should be documented,
tested, reusable, and capable of distribution. With the popularity of C/C++
for high-performance computing, "build system" is increasingly becoming
synonymous with CMake (*N.B.* CMake is often billed as a build system
generator; however, since the typical CMake workflow encapsulates building
the software, the "generator" distinction is immaterial for our present
discussion). Therefore modern high-performance scientific software development
has a need for a robust CMake development ecosystem.

# Statement of need

The CMake ecosystem contains a number of tools which facilitate the development
of software written in C/C++, but notably absent from the CMake ecosystem are
resources to facilitate writing the actual CMake build system. From a
historical perspective this is understandable since CMake-based build systems
have tended to be relatively small (*i.e.*, less than ~1K lines of code) and
tightly coupled to the software package being built. Modern CMake build
systems are increasingly complex and can include: hardware/software
introspection, managing optional dependencies, managing software
development environments, supporting multiple coding languages, coding
language introspection, etc. While some may argue that these tasks are better
handled elsewhere, the point remains that CMake is actually a very flexible
language which can be used to automate complex development tasks. In all
likelihood software developers are going to continue to use CMake for
increasingly complex tasks, and it behooves us to grow the CMake development
ecosystem accordingly.

One of the most basic elements of a software development ecosystem is the
ability to generate application programming interface (API) documentation.
Anecdotal evidence [@official_solution] indicates that the
[official CMake API documentation](https://cmake.org/cmake/help/latest/) is
generated using restructured text markup and Sphinx. The CMake source code
contains a Sphinx plugin capable of extracting ready-to-go restructured text
from CMake source code and rendering it with Sphinx. For simple CMake
modules this solution works fine, but it notably lacks support for a number
of CMake features (*e.g.*, targets and generator expressions) and requires


# Acknowledgements

The authors would also like to acknowledge GitHub users ni-fgenois,
ni-dschiller, dschiller, and zachcran for discussions, bug-reports, and
bug-fixes.

# References
