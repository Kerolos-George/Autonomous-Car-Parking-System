def backend(test_grid):
    import heapq
    # heuristic fucntion h(x)
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) # using manhattenn distance as our heuristc for this problem 


    # linear function for mulitple goals per each successor ( modified version of A* / multiple candidate goals )
    def z(position,targets):
        mn_heuristic_value = float('inf') # init with infinity for minimization 
        for target in targets: # investigate all possible targets  
            heuristic_value = heuristic(position,target) # calcualte heuristic from this cell to this target 
            mn_heuristic_value = min(mn_heuristic_value,heuristic_value) # minimize heuristic value 
        return mn_heuristic_value 



    # extract candidate targets ( all possible / valid targets )
    def get_targets(grid,target_label):
        targets = []
        for i in range(len(grid)):
            for j in range(len(grid[i])): # travse all grid cells 
                if grid[i][j] == target_label : # check cell of having label of target / goal cells 
                    targets.append((i,j))
        return targets # retun all possible targets 
    
     # extract inital point
    def get_init(grid,init_label):
        for i in range(len(grid)):
            for j in range(len(grid[i])): # travse all grid cells 
                if grid[i][j] == init_label : # check cell of having label of init
                    return (i,j)
        return None 
    
    # extract optimal path 
    def optimal_path(target,parent):
        if target is None:
            return None
        path = [] # memo for store path 
        node = target 
        while True:
            path.append(node)
            if node == parent[node]:
                break 
            node = parent[node] # backtrack to previous ancestor 
        path.reverse()
        return path
    



    # Modified version of A star algorithm [ multiple candidate goals /targets ]
    def astar(src,targets,grid,encoding):
        n = len(grid)    # number of rows 
        m = len(grid[0]) # number of columns

        cost   = {} # f(x) : total path cost g(x) + heuristic h(x) , f(x) = g(x) + h(x)
        depth  = {} # g(x) : defined as the depth of the node / number of levels until reach this position 
        parent = {} # stores the parent of each node ( node from which each node is discoverd )

        # directions 
        dx = [-1,0,1,0] # row
        dy = [0,1,0,-1] # column 

        q = [] # priority queue , we sort our candidate cells on the value of f(x) , total cost => always pick minimum possible 
        heapq.heappush(q, (0, src)) # each element of priority queue if a tuple as : t( f(position) value , position )  
        
        cost[src]   = 0   # f( initial position ) = 0 
        depth[src]  = 0   # g( source ) = 0 
        parent[src] = src # base case 
        
        
        # discovering and expanding untill reach goal 
        # discover untill queue ends / become empty 
        while q :
            cur = heapq.heappop(q) # extract tuple of minimum possible f(x) / cost 

            # base case : you reach a cell that already defined as one of our targets 
            if cur[1] in targets : 
                return cur[1] , parent
            
            # skip element of queue 
            if cur[0] != cost[cur[1]]:
                continue

            # iterate on succsessors ( in this case our successors are 4 direction neighbour cells / that share a side with current cell )
            for i,j in zip(dx,dy):
                
                # construct succsessor/child position tuple 
                child = (cur[1][0] + i , cur[1][1] + j )

                # check it's validity 
                if child[0] >= n or child[1] >= m or child[0] < 0 or child[1] < 0 or grid[ child[0] ][ child[1] ] == encoding['OBSTACLE_CELL'] or grid[ child[0] ][ child[1] ] == encoding['RESERVED_SLOT_CELL'] or  grid[ child[0] ][ child[1] ] == encoding['WALL_CELL'] : 
                    continue

                # calculate h(x) , g(x) , f(x)
                heuristic_value = z(child,targets)  # h(x)
                path_value = depth[ cur[1] ] + 1    # g(x)
                cost_value = heuristic_value + path_value # cost f(x) = g(x) + h(x)

                # minimize if we have got before 
                if (child not in cost) or (cost_value < cost[child])  :
                    
                    depth[ child ] = path_value # update depth 
                    cost[ child ] = cost_value  # 
                    parent[ child ] = cur[1]    # set parent of this sucessor to the currnet node that discovr it   

                    heapq.heappush(q, (cost_value,child)) # set to priority queue 

        # if no path reached / infeasible testcase       
        return None , None


    # main function to operate algorithm
    def pathFinding(grid,init_position,targets,encoding):
        selected_target,parent = astar(init_position,targets,grid,encoding) # apply a star search 
        return optimal_path(selected_target,parent) # extract and return optimal path 

    ###############################
    ############ Testcase 
    ###############################

    grid = test_grid
    encoding = {
        'ROAD_CELL' : 0,
        'STARTING_CELL': 1,
        'WALL_CELL' :2,
        'OBSTACLE_CELL' : 3,
        'RESERVED_SLOT_CELL' : 4,
        'FREE_SLOT_CELL' : 5,
    }
    
    init_position = get_init(grid,encoding['STARTING_CELL'])
    targets = get_targets(grid,encoding['FREE_SLOT_CELL'])
    path = pathFinding(grid,init_position,targets,encoding)
    return path,init_position