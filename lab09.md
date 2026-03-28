# Assignment 9
## A polygon editor

In this assignment, you will build some of the underpinnings of a graphics
editing system. Your system will allow a user to create and modify a scene
consisting of a collection of polygons. The user will also be able to query the
system about his scene.

For our purposes, a scene will be described by a list of polygons. Each polygon
will be described by a list of vertices. The operations which must be supported
are grouped into three categories - creating, modifying and querying. In an
actual graphics system, the user would also be able to draw all or a portion of
the scene.

Your task in this assignment is to implement a program which allows the user to
interact with this system and supports the user operations described below.

The underlying data structures you want to consider for this exercise are:
* A point will consist of two floating point coordinates.
* A polygon will consist of an integer giving its number of vertices and a
  pointer to its first vertex.
* A scene will consist of an integer giving its number of polygons and a pointer
  to its first polygon.

You may want to maintain (singly or doubly) linked lists of points and polygons
within your data structure to allow for insertion and deletion.

You will be asked to consider two definitions of the distance from a point to a
polygon during this assignment. In both, the distance between points is their
Euclidian distance (i.e. distance from (x1,y1) to (x2,y2) is
sqrt((x1-x2)^2 + (yl-y2)^2). The distance from a point to a whole line is
defined as the perpendicular distance from the point to the line. The distance
from a point to a line segment (i.e. edge of polygon) is defined as the
perpendicular distance from the point to the whole line if the perpendicular
from the point intersects the segment. If the perpendicular does not intersect
the segment, the distance is the shorter of the distances to the two endpoints
of the segment.

The two distance measures are then defined as follows. For the first, the
distance from a point to a polygon is taken as the minimum of the distances
from the point to any vertex of the polygon. In the second, a polygon is viewed
as an ordered list of vertices so that we can think of edges joining adjacent
vertices. In this case, the distance is the minimum of the distances from the
point to any edge of the polygon. You may note that in the first case, a polygon
is defined to be its vertices, in the second a polygon is given by its boundary.
Hot shots may want to consider the situation when a polygon also has an interior
(see below).

Your program should allow the user to execute the following commands:

### Polygon editing

<dl>
<dt>A n x1 y1 x2 y2 ... xn yn</dt>
<dd>add a polygon of n points, the points being (x1,y 1),(x2,y2),....(xn,yn).</dd>
<dt>D x1 y1</dt>
<dd>delete the polygon closest to the point (x1,y1) (see F below). If this is
the only polygon in the scene, your program should print a suitable warning
message.</dd>
</dl>

### Point editing

<dl>
<dt>a x1 y1</dt>
<dd>add the point (x1,y1) to the polygon of its nearest neighbor (see f below)</dd>
<dt>d x1 y1</dt>
<dd>delete the point nearest (x1,y1) from its polygon (see f below). If this
causes that polygon to have fewer than 3 vertices, delete the polygon.</dd>
</dl>

### Querying

<dl>
<dt>F x1 y1</dt>
<dd>find the polygon closest to the point (x1,y1)</dd>
<dt>f x1 y1</dt>
<dd>find the point closest to the point (x1,y1)</dd>
<dt>L n</dt>
<dd>list all polygons of n vertices</dd>
<dt>L *</dt>
<dd>list all polygons</dd>
<dt>C n</dt>
<dd>list all polygons of n vertices and their vertices</dd>
<dt>C *</dt>
<dd>list all polygons and their vertices</dd>
<dt>l</dt>
<dd>list all vertices</dd>
</dl>

### User friendliness

<dl>
<dt>h</dt>
<dd>print a list of commands</dd>
<dt>q</dt>
<dd>exit</dd>
</dl>

## Part 1 (80%)

Begin by creating a working program with the functionality given above. For this
version, you may use the first definition of distance given above. Thus, the
polygon nearest a point is the polygon having the vertex closest to that point.

You may find it helpful for your program to begin with one polygon - a large
rectangle which defines the screen on which the picture would be drawn.

## Part 2 (20%)

Add more user "friendliness" to your program. That is, make no assumptions about
the input being in the right form. On invalid input, give the user another try.
If you can, try to guess what the user wanted and provide helpful diagnostic
messages.

Also, modify your program to use the second definition of distance.

## For hot-shots

Be more clever in your calculation of distances. If a point lies within the area
of a polygon, it will be said to be at distance 0 from the polygon. Otherwise,
it will be at the distance given by the second definition above.

## Turning in your assignment

Leave your program (which performs all parts) in file lab9.p. Run this program
on input file /cc1/e119/data/lab9. Turn in a copy of the output and a listing.
