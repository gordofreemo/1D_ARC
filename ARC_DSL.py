import random, functools
from typing import Callable, overload
from enum import Enum
from ARC_Solver import ARC_Test, Color, ARC_Grid, ARC_Object

class Abstract_Grid:
    # (start, end, object list)
    Object = dict[int, int, ARC_Grid]
    objects : list[Object]
    grid : ARC_Grid
    def __init__(self, grid : ARC_Grid) -> None:
        self.grid = grid
    # ARC grid measure function
    def dist_measure(self, grid : ARC_Grid) -> int:
      total_metric = 0
      x = min(len(self.grid), len(grid))
      size_diff = abs(len(self.grid) - len(grid))
      for i in range(x):
        if self.grid[i] != grid[i]:
          total_metric += 1
      return (total_metric + size_diff)
    
    # Extract all the connected components from the grid 
    def get_connected_objects(self, grid : ARC_Grid) -> list[Object]:
        flag : bool = False
        curr_object = dict()
        objects = []
        for (i,x) in enumerate(grid):
            if x != Color.BLACK and (not flag):
                curr_object['start'] = i
                flag = True
            elif x == Color.BLACK and flag:
                curr_object['end'] = i
                curr_object['list'] = grid[curr_object['start']:curr_object['end']]
                objects.append(curr_object)
                curr_object = dict()
                flag = False
        if flag:
            curr_object['end'] = len(grid)
            curr_object['list'] = grid[curr_object['start']:curr_object['end']]
            objects.append(curr_object)
        return objects

# Grid operations form a DSL which operate on ARC_Grids and return ARC_Grids
class Grid_Operations:
  Operation = Callable[[ARC_Grid], ARC_Grid]
  @overload
  def recolor(clr1 : Color, clr2 : Color) -> Operation:
      ...
  @overload
  def recolor(obj : ARC_Object, clr : Color) -> Operation:
      ...
  def recolor(obj : Color | ARC_Object, clr : Color) -> Operation:
      if isinstance(obj, Color):
        return (lambda grid : [(x if x != obj else clr) for x in grid])
      else:
        return (lambda grid : grid[0:obj['start']] + ((obj['start']-obj['end'])*[clr]) + grid[obj['end']:])
  def iden() -> Operation:
    return id
  def compose(op1 : Operation, op2 : Operation) -> Operation:
    return (lambda grid : op2(op1(grid)))

# Implements a silly random search across the state space
def trivial_search(puzzle : ARC_Test):
  demon = puzzle.demonstrations
  inputs = [x[0] for x in demon]
  outputs = [x[1] for x in demon]
  op = Grid_Operations.iden 

  
  
### TESTING ###
ARC : ARC_Test = ARC_Test('./1D_Corpus/Center/Center1.json')
grid : Abstract_Grid = Abstract_Grid(ARC.demonstrations[0])
objects : list[ARC_Object] = grid.get_connected_objects(ARC.demonstrations[0][0])

print((Grid_Operations.recolor(objects[0], Color.RED))(grid.grid[0]))
