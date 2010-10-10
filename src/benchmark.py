from quadtree import QuadTree
from geo import Point
from random import randint as r

tree = QuadTree(Point(0,100), Point(100,0))

def build(x=1):
    for i in xrange(x):
        tree.add(Point(r(0,100), r(0,100)), "test")

def nearest_neighbour():
    tree.get(Point(50,50))
    
def search():
    tree.search(Point(50,50), 20)
    
if __name__ == "__main__":
    import sys
    from timeit import Timer
    t = Timer("build(x=%s)" % sys.argv[1], "from __main__ import build")
    print "building took %fseconds" % t.timeit(number=1)
    
    t = Timer("nearest_neighbour()", "from __main__ import nearest_neighbour")
    print "nearest neighbour took %fseconds" % t.timeit(number=1)
    
    t = Timer("search()", "from __main__ import search")
    print "searching took %fseconds" % t.timeit(number=1)
