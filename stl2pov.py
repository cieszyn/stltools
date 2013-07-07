#! /usr/bin/env python
# -*- python coding: utf-8 -*-
# Copyright © 2012,2013 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# $Date$
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

"""Program for converting an STL file into a POV-ray mesh or mesh2."""

import argparse
import sys
import time
from brep import stl, utils

ver = ('stl2pov [ver. ' + '$Revision$'[11:-2] + 
       '] ('+'$Date$'[7:17]+')')


def mesh1(name, ifacets, points):
    """Creates a POV-ray mesh description from facet data.
    
    :name: The name of the object.
    :ifacets: List of facets. Each facet is a 3-tuple of indices into the
    points list.
    :points: List of points. Each point is a 3-tuple of numbers.
    :returns: a string representation of a POV-ray mesh object.
    """
    lines = ["# declare m_{} = mesh {{".format(name.replace(' ', '_'))]
    sot = "  triangle {"
    fc = "    <{1}, {0}, {2}>," # POV-ray has a different coordinate system.
    for (a, b, c) in ifacets:
        lines += [sot, fc.format(*points[a]), fc.format(*points[b]), 
                  fc.format(*points[c])[:-1], "  }"]
    lines += ['}']
    return '\n'.join(lines)


def mesh2(name, ifacets, points):
    """Creates a POV-ray mesh2 object from facet data.

    :name: The name of the object.
    :ifacets: List of facets. Each facet is a 3-tuple of indices into the
    points list.
    :points: List of points. Each point is a 3-tuple of numbers.
    :returns: a string representation of a POV-ray mesh2 object.
    """
    lines = ["# declare m_{} = mesh2 {{".format(name), 
             '  vertex_vectors {', '    {},'.format(len(points))]
    lines += ['    <{1}, {0}, {2}>,'.format(*p) for p in points]
    lines[-1] = lines[-1][:-1]
    lines += ['  face_indices {', '    {},'.format(len(ifacets))]
    lines += ['    <{}, {}, {}>,'.format(*f) for f in ifacets]
    lines[-1] = lines[-1][:-1]
    lines += ['  }', '}']
    return '\n'.join(lines)


def main(argv):
    """Main program.

    :argv: command line arguments (without program name!)
    """
    parser = argparse.ArgumentParser(description=__doc__)
    argtxt = 'generate a mesh2 object (slow on big files)'
    parser.add_argument('-2,' '--mesh2', action='store_true', 
                        help=argtxt, dest='mesh2')
    parser.add_argument('file', nargs='*', help='one or more file names')
    args = parser.parse_args(argv)
    if not args.file:
        parser.print_help()
        sys.exit(0)
    for fn in args.file:
        if not fn.lower().endswith('.stl'):
            w = 'The file "{}" is probably not an STL file, skipping.'
            print w.format(fn)
            continue
        try:
            facets, points, name = stl.readstl(fn)
            outfn = utils.outname(fn, '.inc')
        except ValueError as e:
            print fn + ':', e
            continue
        outs = "// Generated by {}\n// on {}.\n".format(ver, time.asctime())
        outs += "// Source file name: '{}'\n".format(fn)
        if args.mesh2:
            outs += mesh2(name, facets, points)
        else:
            outs += mesh1(name, facets, points)
        try:
            with open(outfn, 'w+') as of:
                of.write(outs)
        except:
            print "Cannot write output file '{}'".format(outfn)
            sys.exit(2)


if __name__ == '__main__':
    main(sys.argv[1:])
