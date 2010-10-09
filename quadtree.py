from geo import Point, BoundingBox
import math

class QuadTree(object):
    """ 
        Quad tree data structure for spacial search operations
        
        >>> import random
        >>> good_result = "FIND ME"
        >>> bad_result = "BOGUS"
        >>> tree = QuadTree(Point(0,100), Point(100,0))
        >>> tree.add(Point(50,49), good_result)
        >>> tree.add(Point(59,39), bad_result)
        >>> tree.get(Point(50,50))
        'FIND ME'
        >>> tree = QuadTree(Point(0,50), Point(50,0))
        >>> tree.add(Point(30,8), bad_result)
        >>> tree.add(Point(25,9), bad_result)
        >>> tree.add(Point(26,9), good_result)
        >>> tree.get(Point(27,10))
        'FIND ME'
        >>> tree = QuadTree(Point(0,50), Point(50,0))
        >>> for i in xrange(100):
        ...  point = Point(random.randint(0,48), random.randint(0,48)) 
        ...  tree.add(point, bad_result)
        ...
        >>> tree.add(Point(49,49), good_result)
        >>> tree.get(Point(50,50))
        'FIND ME'
    """
    def __init__(self, nw, se, **kwargs):
        """
           nw is the north west boundary of the grid
           and se is the south east boundary of the grid
        """
        self.root = QuadTreeNode(nw, se, **kwargs)

    def add(self, point, obj):
        """
           adds an object to the tree with a reference
           object
        """
        self.root.add(point, obj)
                
    def get(self, point):
        """
           Returns the object stored in the tree closest to point
        """
        leaf = self.root.get(point)
        if leaf:
             return leaf.object()
        return None
 
    def __str__(self):
        return "%s" % self.root


class QuadTreeNode(object):
    """ 
        A QuadTreeNode which can either contain children (node mode) or
        contain items (leaf mode) 
        
        >>> node = QuadTreeNode(Point(0,10), Point(10,0))
        >>> node.add(Point(5,5), "hello")
        True
        >>> node.add(Point(20,10), "fail")
        Traceback (most recent call last):
            ...
        ValueError: (20, 10) is out of bounds of ((10,0),(0,10))
        >>> result = node.get(Point(0,0))
        >>> result.point()
        (5, 5)
        >>> result.object()
        'hello'
        >>> node.get_node_for_point(Point(1,1))
        ((10,0),(0,10)) -> [hello at (5, 5)]
        >>> node.get_node_for_point(Point(-1,-1))
        >>> node.add(Point(1,10), "let's")
        True
        >>> node.add(Point(5,8), "cause")
        True
        >>> node.add(Point(3,4), "a")
        True
        >>> node.add(Point(7,7), "new level")
        True
        >>> node.get_node_for_point(Point(1,1))
        ((5,0),(0,5)) -> [a at (3, 4)]
        >>> node.add_leaf(QuadTreeLeaf(Point(4,4), "nope"))
        Traceback (most recent call last):
            ...
        Exception: Cannot add an item to a non-leaf node
        >>> node.get(Point(8,6)).object()
        'new level'
        >>> node = QuadTreeNode(Point(0,100), Point(100,0))
        >>> node.add(Point(50,50), "centre")
        True
        >>> node.get(Point(0,0)).object()
        'centre'
        >>> len(node.items)
        1
        >>> node.add_level()
        >>> len(node.children)
        4
        >>> len(node.items)
        0
        >>> node.get_node_for_point(Point(0,70))
        ((100,0),(50,50)) -> [centre at (50, 50)]
        
    """
    min_size = 5 # minimum size of a quadrant
    max_size = 4 # maximum number of leaf items per node
    NORTH_WEST = 0
    NORTH_EAST = 1
    SOUTH_EAST = 2
    SOUTH_WEST = 3

    def __init__(self, nw, se, **kwargs):
        self.children = None
        self.items = []
        self.bounds = BoundingBox(nw, se)

        if kwargs.get('max_size'):
           self.max_size = kwargs.get('max_size')

    def add_leaf(self, leaf):
        if self.children:
            raise Exception("Cannot add an item to a non-leaf node")
            
        self.items.append(leaf)
        
        if len(self.items) > self.max_size:
            self.add_level()
        
        return True
                
    def add(self, point, obj):
        leaf = QuadTreeLeaf(point, obj)
        # get a child to add this item to
        node = self.get_node_for_point(point)
        if node:
            return node.add_leaf(leaf)

        raise ValueError("%s is out of bounds of %s" % (point, self.bounds))
        
    def get(self, point, best_distance=None):
        """
           Get the closest leaf to a given point
        """
        closest = None
        if self.children:
            for child in self.children:
                # calculate how far away this bounding box is from the searched point
                bb_distance = child.bounds.distance_from_point(point)
                
                # if the bounding box is closer than the best match, recurse in and check it
                if not best_distance or (best_distance and bb_distance < best_distance):
                    found = child.get(point, best_distance)
                    # if we have a result, make it our best match
                    if found:
                        distance = point.distance_from(found.point())
                        if not best_distance or (best_distance and distance < best_distance):
                            best_distance = distance
                            closest = found
        else:
            # so we're a leaf node, check each item and it's distance from the point
            for item in self.items:
                # make this the best match if this it beats the best distance so far
                distance = item.point().distance_from(point)
                if not best_distance or (best_distance and distance < best_distance):
                    best_distance = distance
                    closest = item

        return closest
                   
    def add_level(self):
        """
            Splits a tree node into four child nodes
        """
        # don't split if the current node is smaller than the minimum size
        if self.min_size:
            if(math.fabs(self.bounds.north - self.bounds.south) < self.min_size
               and math.fabs(self.bounds.west - self.bounds.east) < self.min_size):
                return None
        
        
        # get the boundary points for the new child nodes 
        ns_half = self.bounds.north - (self.bounds.north - self.bounds.south) / 2
        ew_half = self.bounds.east - (self.bounds.east - self.bounds.west) / 2 
           
        self.children = []
        self.children.append(QuadTreeNode(Point(self.bounds.west, self.bounds.north), Point(ew_half, ns_half)))
        self.children.append(QuadTreeNode(Point(ew_half, self.bounds.north), Point(self.bounds.east, ns_half)))
        self.children.append(QuadTreeNode(Point(self.bounds.west, ns_half), Point(ew_half, self.bounds.south)))
        self.children.append(QuadTreeNode(Point(ew_half, ns_half), Point(self.bounds.east, self.bounds.south)))
    
        # move items to children
        for item in self.items:
            self.add(item.point(), item.object())
        self.items = []
    
    def get_node_for_point(self, point):
        """ 
            Get the deepest child node where a given point lies
            
            For points which live on the borders of child nodes, this algorithm
            will check NW -> NE -> SW -> SE, so a node with bounds of 100,0 -> 0,100
            asked to find the following points:
            
            (50,50) i.e. the centre point - NW
            (100,50) i.e middle eastern edge - NE
            (0,50) i.e. middle western edge - NW
            (50,100) i.e. middle southern edge - SW
        """
        # if the point lies within the bounds of this node, we
        # need to figure out where to store it
        if self.bounds.contains_point(point):
            # if this isn't a leaf node, recursively check for the child
            # we're looking for
            if self.children:
                for child in self.children:
                    if child.bounds.contains_point(point):
                        return child.get_node_for_point(point)
            else:
                # no children, so this is the leaf node we're looking for
                return self
                
        return None

    def __repr__(self):
        return self.__str__()        
        
    def __str__(self):
        if self.children:
            return "%s -> %s" % (self.bounds, self.children)
        return "%s -> %s" % (self.bounds, self.items)

      
class QuadTreeLeaf(object):
    """ 
       Leaf node which is a point -> object pairing
       
       >>> l = QuadTreeLeaf(Point(10,10), "test")
       >>> l.point()
       (10, 10)
       >>> l.object()
       'test'
       >>> l
       test at (10, 10)
    """
    def __init__(self, point, obj):
        self._point = point
        self._object = obj
        
    def point(self):
        return self._point
                    
    def object(self):
        return self._object

    def __repr__(self):
        return self.__str__()
        
    def __str__(self):
        return "%s at %s" % (self._object, self._point)

                   
if __name__ == "__main__":
    import doctest
    doctest.testmod()
