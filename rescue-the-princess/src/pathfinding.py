from heapq import heappush, heappop

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def neighbors(node, tile_map):
    x, y = node
    results = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    valid = []
    for nx, ny in results:
        if 0 <= nx < tile_map.width and 0 <= ny < tile_map.height:
            valid.append((nx, ny))
    return valid

def a_star_search(start, goal, tile_map):
    frontier = []
    heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heappop(frontier)
        if current == goal:
            break
        for next in neighbors(current, tile_map):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                heappush(frontier, (priority, next))
                came_from[next] = current

    path = []
    cur = goal
    while cur != start:
        path.append(cur)
        cur = came_from.get(cur)
        if cur is None:
            return []
    path.reverse()
    return path
