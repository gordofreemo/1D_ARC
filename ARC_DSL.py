import random, functools,  math
from queue import PriorityQueue
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
    @staticmethod
    def dist_measure(grid_1 : ARC_Grid, grid_2 : ARC_Grid) -> int:
      total_metric = 0
      x = min(len(grid_1), len(grid_2))
      size_diff = abs(len(grid_1) - len(grid_2))
      for i in range(x):
        if grid_1[i] != grid_2[i]:
          total_metric += 1
      return (total_metric + size_diff)
    # Extract all the connected components from the grid 
    def get_connected_objects(self) -> None:
        flag : bool = False
        curr_object = dict()
        objects = []
        grid = self.grid
        for (i,x) in enumerate(self.grid):
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
        self.objects = objects

# Grid operations form a DSL which operate on ARC_Grids and return ARC_Grids
class Grid_Operations:
  Operation = Callable[[ARC_Grid], ARC_Grid]
  @staticmethod
  def generate_all(puzzle : ARC_Test) -> list[tuple[Operation, str]]:
    all_combs = []
    for color in Color:
      for color_prime in Color:
        if color == color_prime: 
          continue
        all_combs.append((Grid_Operations.recolor(color,color_prime), f"RECOLOR {color}->{color_prime}|"))
    return all_combs 
  @overload
  @staticmethod 
  def recolor(clr1 : Color, clr2 : Color) -> Operation:
      ...
  @overload
  @staticmethod
  def recolor(obj : ARC_Object, clr : Color) -> Operation:
      ...
  @staticmethod
  def recolor(obj : Color | ARC_Object, clr : Color) -> Operation:
      if isinstance(obj, Color):
        return (lambda grid : [(x if x != obj else clr) for x in grid])
      else:
        return (lambda grid : grid[0:obj['start']] + ((obj['start']-obj['end'])*[clr]) + grid[obj['end']:])
  @staticmethod
  def iden() -> Operation:
    return (lambda grid: grid)
  @staticmethod
  def compose(op1 : Operation, op2 : Operation) -> Operation:
    return (lambda grid : op2(op1(grid)))


def A_Star(test : ARC_Test) -> tuple[Grid_Operations.Operation, str]:
  all_ops = Grid_Operations.generate_all(test)

  # (Operation Chain, String_Chain, Length) prioritized by heuristic+length
  q = PriorityQueue()
  q.put((math.inf, (Grid_Operations.iden(),'IDEN|',0)))

  #heapq.heappush(frontier, (math.inf, 1, (Grid_Operations.iden(),'IDEN|',0)))
  while not q.empty():
    (_, (curr_op, curr_string, path_len)) = q.get()
    #heapq.heappop(frontier)
    for (op, string) in all_ops:
      new_op = Grid_Operations.compose(curr_op, op)
      measure = sum([ Abstract_Grid.dist_measure(new_op(x), y) for (x,y) in test.demonstrations])
      print(measure)
      if measure == 0:
        return (new_op, curr_string + string)
      q.put((measure+path_len+1, (new_op, curr_string + string, path_len+1)))
      #heapq.heappush(frontier, (measure+path_len+1, 1, (new_op, curr_string + string, path_len+1)))
       

  
### TESTING ###
ARC : ARC_Test = ARC_Test('./1D_Corpus/Recolor/Recolor1.json')
grid : Abstract_Grid = Abstract_Grid(ARC.demonstrations[0][0])
grid.get_connected_objects()
# print((Grid_Operations.recolor(Color.ORANGE, Color.GREEN))(grid.grid))
print(A_Star(ARC))