from gui import *
from backend import *
from movement_transform import  *

test_grid = [
 [2, 2, 2, 2, 2, 2, 2, 2],
 [2, 5, 0, 0, 0, 0, 0, 2],
 [2, 3, 0, 2, 2, 0, 0, 2],
 [2, 0, 0, 0, 2, 0, 5, 2],
 [2, 2, 2, 0, 2, 2, 2, 2],
 [2, 0, 0, 1, 0, 0, 0, 4],
 [2, 0, 2, 2, 2, 2, 2, 2],
 [2, 0, 0, 4, 0, 0, 0, 5],
 [2, 2, 2, 2, 2, 2, 2, 2],
]



movements, car_pos= backend(test_grid)

if movements is None:
   movements = ['None']
else:
    print(movements)
    movements = get_movements(movements)  
    movements.append('park')

   
gui(car_pos, movements, test_grid)