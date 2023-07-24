from typing import Generic,TypeVar
import math

T = TypeVar('T')

class Priority_Queue(Generic[T]):
  __bin_heap : list[tuple[int, T]]
  __size : int
  __max_size : int
  
  def insert(self, key : int, elem : T) -> None:
    self.__size += 1
    if (self.__size ==  self.__max_size):
      self.__expand_heap()
    self.__bin_heap[self.__size-1] = (key, elem)
    self.__percolate_up(self.__size-1)
  
  def extract_min(self) -> tuple[int, T]:
    elem = self.__bin_heap[0]
    self.__swap(0,self.__size)
    self.__size -= 1
    if (self.__size <= (self.__max_size//4)):
      self.__shrink_heap()
    self.__percolate_down(0)
    return elem
  
  def is_empty(self) -> bool:
    return (True if self.__size == 0 else False)

  def get_queue(self) -> list[tuple[int, T]]:
    return self.__bin_heap

  def __init__(self, max_size: int = 8) -> None:
    self.__size = 0
    self.__bin_heap = [(0,None) for x in range(max_size)] 
    self.__max_size = max_size
    
  def __percolate_down(self, i : int) -> None:
    (key, _) = self.__bin_heap[i]
    size = self.__size
    while True:
      j = self.__left(i)
      k = self.__right(i)
      if (j > size):
        return
      index = j if (k > size) else (j if (self.__bin_heap[j][0] < self.__bin_heap[k][0]) else k)
      (key_prime, _) = self.__bin_heap[index] 
      if key > key_prime:
        self.__swap(i,index)
      else:
        return
      i = index
    
  def __percolate_up(self, i : int) -> None:
    (key, _) = self.__bin_heap[i]
    while (i != 0):
      j = self.__parent(i)
      (key_prime, _) = self.__bin_heap[j]
      if key_prime > key:
        self.__swap(i,j)
      else:
        return
      i = self.__parent(i)
      
  def __expand_heap(self) -> None:
    self.__bin_heap = self.__bin_heap.copy() + [(math.inf,None) for x in range(self.__size)]
    self.__max_size *= 2 
    
  def __shrink_heap(self) -> None:
    self.__bin_heap = self.__bin_heap[0:len(self.__bin_heap)//2]
    self.__max_size //= 2 

  def __swap(self, i : int, j : int) -> None:
    temp = self.__bin_heap[i]
    self.__bin_heap[i] = self.__bin_heap[j]
    self.__bin_heap[j] = temp

  def __parent(self, i : int) -> int:
    if i % 2 == 0:
      return (i-1)//2
    return i//2
  def __left(self, i : int) -> int:
    return (i*2)+1;
  def __right(self, i : int) -> int:
    return (i+1)*2

### TESTING ###

#x = Priority_Queue()
#for k in range(10):
  #x.insert(10-k,k)
#for k in range(10):
  #x.insert(10-k,k)

#while (not x.is_empty()):
  #print(x.extract_min())