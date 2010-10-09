import math

class Point(object):
    """ 
       Class to represent a point
       
       >>> p = Point(10,0)
       >>> p.x()
       10
       >>> p.y()
       0
       >>> p.distance_from(Point(10,0))
       0.0
       >>> p.distance_from(Point(5,0))
       5.0
       >>> p2 = Point(10,-5)
       >>> p2.y()
       -5
       >>> p.distance_from(p2)
       5.0
       >>> p
       (10, 0)
    """
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def x(self):
        return self._x

    def y(self):
        return self._y

    def distance_from(self, point):
        return distance(self, point)

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "(%d, %d)" % (self._x, self._y)


def distance(p1, p2):
    side_one = p2.x() - p1.x()
    side_two = p2.y() - p1.y()
    d = math.sqrt(math.pow(side_one, 2) + math.pow(side_two, 2))
    return d


class BoundingBox(object):
    """ 
       Class to represent a bounding box where north is assumed to be 
       a value greater than south and west a value less than east - this
       means a bounding box which spans the edge of a parent box is not 
       currently supported (e.g):
       
           -------------------
           |   |             |
           |--- sw           |
           |         ne -----|
           |           |     |
           -------------------           
       
       TODO: support this by optional accepting a parent bounding box 
             which is then factored into the contains_point method
              
       >>> b = BoundingBox(Point(0,10), Point(10,0))
       >>> b.north
       10
       >>> b.west
       0
       >>> b.south
       0
       >>> b.east
       10
       >>> b.contains_point(Point(5,5))
       True
       >>> b.contains_point(Point(11,10))
       False
       >>> b.contains_point(Point(0,0))
       True
       >>> b.distance_from_point(Point(10,20))
       10.0
       >>> b.distance_from_point(Point(5,5))
       0.0
       >>> b.distance_from_point(Point(0,20))
       10.0
       >>> b = BoundingBox(Point(-90,90), Point(90,-90))
       >>> b.contains_point(Point(0,0))
       True
       >>> b.distance_from_point(Point(-100,90))
       10.0
    """
    def __init__(self, nw, se):
        self.north = nw.y()
        self.west = nw.x()
        self.south = se.y()
        self.east = se.x()
                
    def contains_point(self, point):
        if (point.x() >= self.west and point.x() <= self.east and 
           point.y() >= self.south and point.y() <= self.north):
            return True
        return False

    def distance_from_point(self, point):
        if self.south <= point.y() and point.y() <= self.north:
            ns_distance = 0
        else:
            ns_distance = min(math.fabs(point.y() - self.north), 
                                   math.fabs(point.y() - self.south))
        
        if self.west <= point.x() and point.x() <= self.east:
            ew_distance = 0
        else:
            ew_distance = min(math.fabs(point.x() - self.west),
                                   math.fabs(point.x() - self.east))
        
        return math.sqrt(ns_distance * ns_distance + ew_distance * ew_distance)

    def __str__(self):
        return "((%d,%d),(%d,%d))" % (self.north, self.west, self.south, self.east)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

