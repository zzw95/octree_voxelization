from octree_1 import *

tree = Octree("data/knot.stl", maxLevel=4, cubic=True)
tree.traverse()
tree.writeBoxes("data/knot_voxel_cube.txt")
# print("backtrack\n")
# tree.backtrack()
# tree.writeBoxes("bstep_voxel_cube1.txt")
