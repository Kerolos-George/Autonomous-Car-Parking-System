#Transform the traversed path to movements instructions
def get_movements(optimal_path):
    movements = []
    for i in range(len(optimal_path)-1):
        curr_cell = optimal_path[i]
        next_cell = optimal_path[i+1]
        
        if curr_cell[0] < next_cell[0]:
            movements.append("down")
        elif curr_cell[0] > next_cell[0]:
            movements.append("up")
        elif curr_cell[1] < next_cell[1]:
            movements.append("right")
        else:
            movements.append("left")
    
    return movements