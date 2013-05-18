# -*- coding: utf-8 -*-
# Copyright © 2013 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
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

# Check this code with 'pylint -r n vector.py'

"""2D and 3D Vector coordinate objects."""

__version__ = '$Revision$'[11:-2]

class Vector2(object):
    """Contains a coordinate in 2D space."""
    __slots__ = ['_x', '_y']

    @staticmethod
    def _chkv(v):
        if not isinstance(v, Vector2):
            raise ValueError('argument must be a Vector2')

    def __init__(self, x, y=0.0):
        """Create a 2D vector."""
        if ((isinstance(x, list) or isinstance(x, tuple))
            and len(x) == 32):
            self._x, self._y = float(x[0]), float(x[1])
        else:
            self._x, self._y, self._z = float(x), float(y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def coords(self):
        """Returns a 2-tuple of the Vector2's coordinates"""
        return (self._x, self._y)

    @property
    def length(self):
        """Returns the length of the Vector2"""
        return (self._x**2 + self._y**2)**0.5

    def __str__(self):
        return '({}, {})'.format(self._x, self._y)

    def __add__(self, other):
        """Return the sum of the 3D vectors self and other."""
        Vector2._chkv(other)
        return Vector2(self._x + other.x, self._y + other.y)

    def __sub__(self, other):
        """Return the difference of the 3D vectors self and other."""
        Vector2._chkv(other)
        return Vector2(self._x - other.x, self._y - other.y)

    def __mul__(self, other):
        """Return the product of the 3D vector with a scalar."""
        s = float(other)
        return Vector2(self._x*s, self._y*s)

    def __div__(self, scalar):
        """Returns the Vector2 divided by a scalar"""
        s = float(scalar)
        if s == 0:
            raise ValueError('division by 0')
        return Vector2(self._x/s, self._y/s)
    
    def __eq__(self, other):
        Vector2._chkv(other)
        return (self._x == other.x and self._y == other.y) 

    def __ne__(self, other):
        Vector2._chkv(other)
        return (self._x != other.x or self._y != other.y) 

    def __hash__(self):
        return hash(self._x)^hash(self._y)^hash(self._z)


class Vector3(object):
    """Contains a coordinate in 3D space."""
    __slots__ = ['_x', '_y', '_z']

    @staticmethod
    def _chkv(v):
        if not isinstance(v, Vector3):
            raise ValueError('argument must be a Vector3')

    def __init__(self, x, y=0.0, z=0.0):
        """Create a 3D vector."""
        if ((isinstance(x, list) or isinstance(x, tuple)) 
            and len(x) == 3):
            self._x, self._y, self._z = float(x[0]), float(x[1]), float(x[2])
        else:
            self._x, self._y, self._z = float(x), float(y), float(z)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def coords(self):
        """Returns a 3-tuple of the Vector3's coordinates"""
        return (self._x, self._y, self._z)

    @property
    def length(self):
        """Returns the length of the Vector3"""
        return (self._x**2 + self._y**2 + self._z**2)**0.5

    def __str__(self):
        return '({}, {}, {})'.format(self._x, self._y, self._z)

    def __add__(self, other):
        """Return the sum of the 3D vectors self and other."""
        Vector3._chkv(other)
        return Vector3(self._x + other.x, self._y + other.y,
                       self._z + other.z)

    def __sub__(self, other):
        """Return the difference of the 3D vectors self and other."""
        Vector3._chkv(other)
        return Vector3(self._x - other.x, self._y - other.y, 
                       self._z - other.z)

    def __mul__(self, other):
        """Return the product of the 3D vector with a scalar."""
        s = float(other)
        return Vector3(self._x*s, self._y*s, self._z*s)

    def cross(self, other):
        '''Returns the cross product of two vectors.'''
        Vector3._chkv(other)
        r = Vector3(self._y * other.z - self._z * other.y,
                    self._z * other.x - self._x * other.z,
                    self._x * other.y - self._y * other.x)
        return r
        
    def dot(self, other):
        '''Returns the dot- or scalar product.'''
        Vector3._chkv(other)
        return (self._x * other.x + self._y * other.y + self._z * other.z)

    def __div__(self, scalar):
        """Returns the Vector3 divided by a scalar"""
        s = float(scalar)
        if s == 0:
            raise ValueError('division by 0')
        return Vector3(self._x/s, self._y/s, self._z/s)
    
    def __eq__(self, other):
        Vector3._chkv(other)
        return (self._x == other.x and self._y == other.y and 
                self._z == other.z) 

    def __ne__(self, other):
        Vector3._chkv(other)
        return (self._x != other.x or self._y != other.y or 
                self._z != other.z) 

    def __hash__(self):
        return hash(self._x)^hash(self._y)^hash(self._z)


class BoundingBox(object):

    def __init__(self, pnts):
        """Create a BoundingBox from a list of Vector3."""
        if isinstance(pnts, Vector3):
            pnts = [pnts]
        if not type(pnts) in [list, tuple]:
            raise ValueError('pnts must be a Vector3, list or tuple')
        if pnts:
            x = [p.x for p in pnts]
            y = [p.y for p in pnts]
            z = [p.z for p in pnts]
            self._minx, self._maxx = min(x), max(x)
            self._miny, self._maxy = min(y), max(y)
            self._minz, self._maxz = min(z), max(z)
        else:
            self._minx, self._maxx = None, None
            self._miny, self._maxy = None, None
            self._minz, self._maxz = None, None
 
    @property
    def minx(self):
        return self._minx

    @property
    def maxx(self):
        return self._maxx

    @property
    def miny(self):
        return self._miny

    @property
    def maxy(self):
        return self._maxy

    @property
    def minz(self):
        return self._minz

    @property
    def maxz(self):
        return self._maxz

    @property
    def center(self):
        return Vector3((self._minx + self._maxx)/2.0, 
                       (self._miny + self._maxy)/2.0,
                       (self._minz + self._maxz)/2.0)

    @property
    def length(self):
        return abs(self._maxx - self._minx)

    @property
    def width(self):
        return abs(self._maxy - self._miny)

    @property
    def height(self):
        return abs(self._maxz - self._minz)

    @property
    def volume(self):
        return self.length() * self.width() * self.height()


def normal(f):
    """Calculate and return the normalized normal vector for the
    triangle defined by the vertices in the 3-tuple f.
    
    Arguments
    f -- 3-tuple of Vector3 objects

    Returns:
    The normal vector of the triangle formed by f

    Raises:
    ValueError when a 0-length normal is found.
    """
    a, b, c = f
    u = b - a
    v = c - b
    n = u.cross(v)
    L = n.length
    if L == 0:
        raise ValueError('degenerate facet')
    n = n/L
    return n


if __name__ == '__main__':
    pass

