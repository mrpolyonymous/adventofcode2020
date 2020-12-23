from functools import reduce
import math

class Tile:
    def __init__(self, id, tile_data):
        self.id = id
        self.tile_data = tile_data
        self.top_edge = tile_data[0]
        self.bottom_edge = tile_data[-1]
        self.left_edge = reduce(lambda x, y: x+y, map(lambda l: l[0], tile_data))
        self.right_edge = reduce(lambda x, y: x+y, map(lambda l: l[-1], tile_data))
        self.top_edge_rev = self.top_edge[::-1]
        self.bottom_edge_rev = self.bottom_edge[::-1]
        self.left_edge_rev = self.left_edge[::-1]
        self.right_edge_rev = self.right_edge[::-1]
        self.unmatched_edges = set()

    def all_possible_edges(self):
        return set([self.top_edge, self.top_edge_rev, self.bottom_edge, self.bottom_edge_rev,
            self.left_edge, self.left_edge_rev, self.right_edge, self.right_edge_rev])

    def __str__(self):
        return f"Tile {self.id}: {self.tile_data}"

    def __repr__(self):
        return f"Tile {self.id}: {self.tile_data}"

    def __eq__(self, other): 
        if not isinstance(other, Tile):
            return NotImplemented

        return self.id == other.id

    def set_unmatched_edges(self, unmatched):
        self.unmatched_edges = unmatched

    def orient_top_left(self):
        if len(self.unmatched_edges) != 4:
            raise RuntimeError("Not a corner")
        if self.top_edge in self.unmatched_edges and self.left_edge in self.unmatched_edges:
            raise RuntimeError("Implement me") 
        elif self.top_edge in self.unmatched_edges and self.right_edge in self.unmatched_edges:
            return self.rotated_widdershins()
        elif self.bottom_edge in self.unmatched_edges and self.right_edge in self.unmatched_edges:
            return self.rotated_180()
        elif self.bottom_edge in self.unmatched_edges and self.left_edge in self.unmatched_edges:
            raise RuntimeError("Implement me") 
        else:
            raise RuntimeError("Cannot orient to top-left")            

        return self

    def orient_with_left_edge_matching(self, edge_to_match):
        if edge_to_match == self.left_edge:
            return self
        elif edge_to_match == self.left_edge_rev:
            return self.flipped_top()
        elif edge_to_match == self.right_edge:
            return self.flipped_left()
        elif edge_to_match == self.right_edge_rev:
            return self.rotated_180()
        elif edge_to_match == self.top_edge:
            return self.flipped_left().rotated_widdershins()
        elif edge_to_match == self.top_edge_rev:
            return self.rotated_widdershins()
        elif edge_to_match == self.bottom_edge:
            return self.rotated_clockwise()
        elif edge_to_match == self.bottom_edge_rev:
            return self.flipped_left().rotated_clockwise()
        else:
            raise RuntimeError("Called incorrectly")

    def orient_with_top_edge_matching(self, edge_to_match):
        if edge_to_match == self.left_edge:
            return self.rotated_clockwise().flipped_left()
        elif edge_to_match == self.left_edge_rev:
            return self.rotated_clockwise()
        elif edge_to_match == self.right_edge:
            return self.rotated_widdershins()
        elif edge_to_match == self.right_edge_rev:
            return self.rotated_widdershins().flipped_left()
        elif edge_to_match == self.top_edge:
            return self
        elif edge_to_match == self.top_edge_rev:
            return self.flipped_left()
        elif edge_to_match == self.bottom_edge:
            return self.rotated_180().flipped_left()
        elif edge_to_match == self.bottom_edge_rev:
            return self.rotated_180()
        else:
            raise RuntimeError("Called incorrectly")

    def rotated_180(self):
        new_tile_data = list(map(lambda x: x[::-1], reversed(self.tile_data)))
        return Tile(f"{self.id} (rotated 180)", new_tile_data)

    def rotated_clockwise(self):
        new_tile_data = [ [self.tile_data[-(j+1)][i] for j in range(len(self.tile_data))] for i in range(len(self.tile_data))]
        new_tile_data = list(map(lambda x: reduce(lambda a, b:a+b,x), new_tile_data))
        return Tile(f"{self.id} (rotated 90)", new_tile_data)


    def rotated_widdershins(self):
        new_tile_data = [ [self.tile_data[j][-(i+1)] for j in range(len(self.tile_data))] for i in range(len(self.tile_data)) ]
        new_tile_data = list(map(lambda x: reduce(lambda a, b:a+b,x), new_tile_data))
        return Tile(f"{self.id} (rotated -90)", new_tile_data)

    def flipped_left(self):
        new_tile_data = list(map(lambda r:r[::-1], self.tile_data))
        return Tile(f"{self.id} (flipped left-right)", new_tile_data)

    def flipped_top(self):
        new_tile_data = self.tile_data[::-1]
        return Tile(f"{self.id} (flipped top-bottom)", new_tile_data)

def read_input(file_name):
    tiles = []
    with open(file_name) as input_file:
        is_id_line = True
        tile_data = []
        for line in input_file:
            line = line.strip()
            if is_id_line:
                tile_id = line[5:-1]
                is_id_line = False
            elif len(line) > 0:
                tile_data.append(line)
            else:
                tiles.append(Tile(tile_id, tile_data))
                is_id_line = True
                tile_data = []
    if len(tile_data) > 0:
        tiles.append(Tile(tile_id, tile_data))
    return tiles

def part1(tiles):
    # Find tiles that have no possible common edges
    corners = []
    edges = []
    for base_tile in tiles:
        unmatched_edges = base_tile.all_possible_edges()
        for other_tile in tiles:
            if len(unmatched_edges) == 0:
                break
            if base_tile == other_tile:
                continue

            other_tile_edges = other_tile.all_possible_edges()
            unmatched_edges = unmatched_edges.difference(other_tile_edges)

        if len(unmatched_edges) > 0:
            base_tile.set_unmatched_edges(unmatched_edges)
            # print(f"Tile {base_tile.id} is special; {len(unmatched_edges)} unmatched edges")
            if len(unmatched_edges) == 4:
                corners.append(base_tile)
            else:
                edges.append(base_tile)

    return (corners, edges)

def part2(tiles, corners, edges):
    # solve picture
    # remove edges from tiles
    # rotate until find sea monsters
    # remove sea monsters
    # count number of # remaining

    tile_grid = solve_tiles(tiles, corners, edges)
    tile_dim = len(tile_grid[0][0].tile_data)
    big_dim = tile_dim * len(tile_grid)
    grid_with_borders = [ "" for i in range(big_dim)]
    row = 0
    base_row = 0
    for grid_row in tile_grid:
        for tile in grid_row:
            for td in tile.tile_data:
                grid_with_borders[row] += td
                row += 1
            row = base_row
        base_row += tile_dim
        row = base_row

    # for l in grid_with_borders:
    #     print(l)

    # validate row borders match
    for i in range(tile_dim, big_dim - tile_dim + 1, tile_dim):
        if grid_with_borders[i - 1] != grid_with_borders[i]:
            raise RuntimeError("Bad solution")

    # validate column borders match
    for col in range(tile_dim, big_dim - tile_dim + 1, tile_dim):
        for row in range(big_dim):
            if grid_with_borders[row][col - 1] != grid_with_borders[row][col]:
                raise RuntimeError("Bad solution")

    tile_dim_no_border = tile_dim - 2
    grid_without_borders = [ "" for i in range(tile_dim_no_border * len(tile_grid))]
    row = 0
    base_row = 0
    for grid_row in tile_grid:
        for tile in grid_row:
            for i in range(tile_dim_no_border):
                grid_without_borders[row] += tile.tile_data[i+1][1:-1]
                row += 1
            row = base_row
        base_row += tile_dim_no_border
        row = base_row

    # for l in grid_without_borders:
    #     print(l)

    num_monsters = count_sea_monsters(grid_without_borders)
    num_hash = 0
    for row in grid_without_borders:
        for c in row:
            if c == "#":
                num_hash += 1

    return num_hash - 15 * num_monsters

def solve_tiles(tiles, corners, edges):
    dim_in_tiles = int(math.sqrt(len(tiles)))
    tile_grid = [ [None for j in range(dim_in_tiles)] for i in range(dim_in_tiles)]
    remaining_tiles = tiles.copy()
    top_row = tile_grid[0]
    top_left_corner = corners.pop()
    top_row[0] = top_left_corner.orient_top_left()
    remaining_tiles.remove(top_left_corner)

    # solve top row edges
    for i in range(1, dim_in_tiles):
        edge_to_match = top_row[i-1].right_edge
        if i < dim_in_tiles - 1:
            matching_tile = find_tile_matching_edge(edges, edge_to_match)
            edges.remove(matching_tile)
        else:
            matching_tile = find_tile_matching_edge(corners, edge_to_match)
            corners.remove(matching_tile)

        remaining_tiles.remove(matching_tile)
        top_row[i] = matching_tile.orient_with_left_edge_matching(edge_to_match)

    # solve left edge
    for i in range(1, dim_in_tiles):
        edge_to_match = tile_grid[i-1][0].bottom_edge
        if i < dim_in_tiles - 1:
            matching_tile = find_tile_matching_edge(edges, edge_to_match)
            edges.remove(matching_tile)
        else:
            matching_tile = find_tile_matching_edge(corners, edge_to_match)
            corners.remove(matching_tile)

        remaining_tiles.remove(matching_tile)
        tile_grid[i][0] = matching_tile.orient_with_top_edge_matching(edge_to_match)

    # solve bottom row
    bottom_row = tile_grid[-1]
    for i in range(1, dim_in_tiles):
        edge_to_match = bottom_row[i-1].right_edge
        if i < dim_in_tiles - 1:
            matching_tile = find_tile_matching_edge(edges, edge_to_match)
            edges.remove(matching_tile)
        else:
            matching_tile = find_tile_matching_edge(corners, edge_to_match)
            corners.remove(matching_tile)

        remaining_tiles.remove(matching_tile)
        bottom_row[i] = matching_tile.orient_with_left_edge_matching(edge_to_match)

    # solve right edge
    for i in range(1, dim_in_tiles-1):
        edge_to_match = tile_grid[i-1][-1].bottom_edge
        matching_tile = find_tile_matching_edge(edges, edge_to_match)
        edges.remove(matching_tile)
        remaining_tiles.remove(matching_tile)
        tile_grid[i][-1] = matching_tile.orient_with_top_edge_matching(edge_to_match)

    # solve remaining tiles
    for row in range(1, dim_in_tiles - 1):
        for col in range(1, dim_in_tiles - 1):
            right_edge_to_match = tile_grid[row][col-1].right_edge
            bottom_edge_to_match = tile_grid[row-1][col].bottom_edge
            matching_tile = find_tile_matching_edges(remaining_tiles, right_edge_to_match, bottom_edge_to_match)
            remaining_tiles.remove(matching_tile)
            tile_grid[row][col] = matching_tile.orient_with_left_edge_matching(right_edge_to_match).orient_with_top_edge_matching(bottom_edge_to_match)

    return tile_grid

def find_tile_matching_edge(tiles, edge_to_match):
    matching_tile = None
    for tile in tiles:
        if edge_to_match in tile.all_possible_edges():
            if matching_tile != None:
                raise RuntimeError("Can't deal with multiple matches")
            matching_tile = tile
    if matching_tile == None:
        raise RuntimeError("No matching tile")

    return matching_tile

def find_tile_matching_edges(tiles, edge_to_match1, edge_to_match2):
    matching_tile = None
    for tile in tiles:
        if edge_to_match1 in tile.all_possible_edges() and edge_to_match2 in tile.all_possible_edges():
            if matching_tile != None:
                raise RuntimeError("Can't deal with multiple matches")
            matching_tile = tile
    if matching_tile == None:
        raise RuntimeError("No matching tile")

    return matching_tile

def count_sea_monsters(grid):
    grid = grid.copy()
    monster = [[18], [0, 5, 6, 11, 12, 17, 18, 19], [1, 4, 7, 10, 13, 16]]

    max_monsters = 0
    for iter in range(8):
        num_monsters = 0
        # print(f"Iteration {iter}")
        if iter == 4:
            grid = flipped_top(grid)
        # for l in grid: print(l)

        for r in range(len(grid) - 2):
            for c in range(len(grid) - 19):
                num_monster_cells = 0
                r_offset = 0
                for mr_offsets in monster:
                    for c_offset in mr_offsets:
                        if grid[r + r_offset][c+c_offset] == "#":
                            num_monster_cells += 1
                    r_offset += 1
                if num_monster_cells == 15:
                    num_monsters += 1

        max_monsters = max(num_monsters, max_monsters)
        if num_monsters == 0:
            grid = rotated_clockwise(grid)
        else:
            return num_monsters
    return max_monsters

def rotated_clockwise(tile_data):
    new_tile_data = [ [tile_data[-(j+1)][i] for j in range(len(tile_data))] for i in range(len(tile_data))]
    new_tile_data = list(map(lambda x: reduce(lambda a, b:a+b,x), new_tile_data))
    return new_tile_data

def flipped_top(tile_data):
    return tile_data[::-1]

tiles = read_input('day20_input.txt')
# tiles = read_input('day20_example_input.txt')
# for l in tiles: print(l)


(corners, edges) = part1(tiles)
part1_answer = reduce(lambda x,y: x*y, map(lambda tile: int(tile.id), corners))
print(f"Part 1: {part1_answer}")
# My answer to part 1: 8425574315321
part2_answer = part2(tiles, corners, edges)
print(f"Part 2: {part2_answer}")
# My answer to part 2: 1841
