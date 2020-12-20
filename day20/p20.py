#!/usr/bin/env python
"""Tedious and lots of painful indexing typos but pretty fun. Super thankful for numpy."""

from math import sqrt
import re
import numpy as np
from collections import deque, defaultdict
from itertools import product
import sys

try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans

# Bunch of ugly globals not worth cleaning up
TILE_SIZE = None
IMG_SIZE_TILES = None


# Get list of integers in a string
def gan(s):
    return [int(i) for i in re.findall(r"-?\d+", s)]


## Part 1

# Check if a vector is equal to another, allowing flipping
def is_edge_eq(edge1, edge2):
    return np.array_equal(edge1, edge2) or np.array_equal(edge1, np.flip(edge2))


# Check if a vector matches any edge of a given tile, allowing flipping
def does_edge_match_tile(edge, tile):
    if is_edge_eq(edge, tile[0, :]):
        return True
    if is_edge_eq(edge, tile[-1, :]):
        return True
    if is_edge_eq(edge, tile[:, 0]):
        return True
    if is_edge_eq(edge, tile[:, -1]):
        return True
    return False


# Key insight: corners have only two neighbors
def p1(lines):
    global TILE_SIZE
    TILE_SIZE = len(lines[1].strip())

    # Build dict mapping each tile number to a numpy array of the tile
    all_tiles = {}
    i = 0
    while i < len(lines):
        tile_id = gan(lines[i])[0]
        i += 1
        img = lines[i : i + TILE_SIZE]
        for j in range(len(img)):
            img[j] = [int(k) for k in img[j].translate(maketrans("#.", "10"))]
        all_tiles[tile_id] = np.array(img)
        i += TILE_SIZE + 1

    # Count potential neighbors of each tile
    corners = []
    for i, tile in all_tiles.items():
        n_neighbors = 0
        for j, other_tile in all_tiles.items():
            if i == j:
                continue
            if does_edge_match_tile(tile[0, :], other_tile):
                n_neighbors += 1
                continue
            if does_edge_match_tile(tile[-1, :], other_tile):
                n_neighbors += 1
                continue
            if does_edge_match_tile(tile[:, 0], other_tile):
                n_neighbors += 1
                continue
            if does_edge_match_tile(tile[:, -1], other_tile):
                n_neighbors += 1
                continue
        assert n_neighbors >= 2
        if n_neighbors == 2:
            corners.append(i)

    return np.product(corners)


## Part 2


def get_neighbors(i, cache):
    tile = cache[i]
    neighbors = []
    for j, other in cache.items():
        if len(neighbors) == 4:
            break
        if j == i:
            continue
        if does_edge_match_tile(tile[0, :], other):
            neighbors.append(j)
            continue
        if does_edge_match_tile(tile[-1, :], other):
            neighbors.append(j)
            continue
        if does_edge_match_tile(tile[:, 0], other):
            neighbors.append(j)
            continue
        if does_edge_match_tile(tile[:, -1], other):
            neighbors.append(j)
            continue
    return neighbors


def place_tile_in_spot(img, target, tile):
    row, col = target
    img[
        row * TILE_SIZE : row * TILE_SIZE + TILE_SIZE,
        col * TILE_SIZE : col * TILE_SIZE + TILE_SIZE,
    ] = tile
    return img


def get_all_rotations(tile):
    yield tile
    # 90
    tile = np.rot90(tile)
    yield tile
    # 180
    tile = np.rot90(tile)
    yield tile
    # 270
    tile = np.rot90(tile)
    yield tile
    tile = np.rot90(tile)


def get_all_orientations(tile):
    for i in get_all_rotations(tile):
        yield i
    tile = np.flipud(tile)
    for i in get_all_rotations(tile):
        yield i


# spot = Tile coordinates of the tile that the new tile should neighbor
def place_neighbor_in_img(img, spot, tile):
    row, col = spot
    r_idx, c_idx = row * TILE_SIZE, col * TILE_SIZE
    new_spot = None

    # Bottom edge of target
    if row != IMG_SIZE_TILES - 1:
        for rot_tile in get_all_orientations(tile):
            if np.array_equal(
                rot_tile[0, :], img[r_idx + TILE_SIZE - 1, c_idx : c_idx + TILE_SIZE]
            ):
                new_spot = row + 1, col
                img = place_tile_in_spot(img, new_spot, rot_tile)
                return img, new_spot
    # Top edge of target
    if row != 0:
        for rot_tile in get_all_orientations(tile):
            if np.array_equal(rot_tile[-1, :], img[r_idx, c_idx : c_idx + TILE_SIZE]):
                new_spot = row - 1, col
                img = place_tile_in_spot(img, new_spot, rot_tile)
                return img, new_spot
    # Right edge of target
    if col != IMG_SIZE_TILES - 1:
        for rot_tile in get_all_orientations(tile):
            if np.array_equal(
                rot_tile[:, 0], img[r_idx : r_idx + TILE_SIZE, c_idx + TILE_SIZE - 1]
            ):
                new_spot = row, col + 1
                img = place_tile_in_spot(img, new_spot, rot_tile)
                return img, new_spot
    # Left edge of target
    if col != 0:
        for rot_tile in get_all_orientations(tile):
            if np.array_equal(rot_tile[:, -1], img[r_idx : r_idx + TILE_SIZE, c_idx]):
                new_spot = row, col - 1
                img = place_tile_in_spot(img, new_spot, rot_tile)
                return img, new_spot

    raise Exception("Tile wasn't placed")


## Create dragon mask as numpy array
dragon = """
00000000000000000010
10000110000110000111
01001001001001001000
""".strip().split(
    "\n"
)
DRAGON = np.array([[int(j) for j in list(i)] for i in dragon])

# Check if there's a dragon in the given tile
def dragon_equals(tile):
    return np.array_equal(tile & DRAGON, DRAGON)


# Mask out the dragon at the given location in the image
def clear_dragon(img, row, col):
    img[row : row + DRAGON.shape[0], col : col + DRAGON.shape[1]] = (
        img[row : row + DRAGON.shape[0], col : col + DRAGON.shape[1]] & ~DRAGON
    )
    return img


# Clear all dragons
def clear_all_dragons(img):
    count = 0
    for row, col in product(
        range(img.shape[0] - DRAGON.shape[0] + 1),
        range(img.shape[1] - DRAGON.shape[1] + 1),
    ):
        if dragon_equals(img[row : row + DRAGON.shape[0], col : col + DRAGON.shape[1]]):
            img = clear_dragon(img, row, col)
            count += 1
    return count, img


def p2(lines):
    global TILE_SIZE
    TILE_SIZE = len(lines[1].strip())

    all_tiles = {}

    i = 0
    while i < len(lines):
        tile_id = gan(lines[i])[0]
        i += 1
        img = lines[i : i + TILE_SIZE]
        for j in range(len(img)):
            img[j] = [int(i) for i in img[j].translate(maketrans("#.", "10"))]
        all_tiles[tile_id] = np.array(img)
        i += TILE_SIZE + 1

    # Build up dictionary mapping a tile id to it's neighbording tile id's
    corners = set()
    neighbors = defaultdict(list)
    for i, tile in all_tiles.items():
        n_neighbors = 0
        for j, other_tile in all_tiles.items():
            if i == j:
                continue
            if does_edge_match_tile(tile[0, :], other_tile):
                n_neighbors += 1
                neighbors[i].append(j)
                continue
            if does_edge_match_tile(tile[-1, :], other_tile):
                n_neighbors += 1
                neighbors[i].append(j)
                continue
            if does_edge_match_tile(tile[:, 0], other_tile):
                n_neighbors += 1
                neighbors[i].append(j)
                continue
            if does_edge_match_tile(tile[:, -1], other_tile):
                n_neighbors += 1
                neighbors[i].append(j)
                continue
        assert n_neighbors >= 2
        if n_neighbors == 2:
            corners.add(i)

    global IMG_SIZE_TILES
    IMG_SIZE_TILES = int(sqrt(len(all_tiles)))
    assert IMG_SIZE_TILES ** 2 == len(all_tiles)

    # Store (row, col) of each placed tile in units of tiles
    # Picked one of the corner pieces and figured out what orientation to place it manually
    placed = {3457: (0, 0)}
    img = np.zeros(
        ((IMG_SIZE_TILES * TILE_SIZE), IMG_SIZE_TILES * TILE_SIZE), dtype=np.int64
    )
    img = place_tile_in_spot(img, placed[3457], all_tiles[3457][:, ::-1])

    # Breadth-first search to place tiles
    queue = deque([3457])
    while queue:
        placed_tile = queue.pop()
        assert placed_tile in placed
        for neigh in neighbors[placed_tile]:
            if neigh in placed:
                continue
            img, new_spot = place_neighbor_in_img(
                img, placed[placed_tile], all_tiles[neigh]
            )
            placed[neigh] = new_spot
            queue.append(neigh)

    ## Don't forget to remove the borders between images!

    # Clear vertical borders
    NEW_TILE_SIZE = TILE_SIZE - 2
    img2 = np.zeros(
        (IMG_SIZE_TILES * TILE_SIZE, IMG_SIZE_TILES * NEW_TILE_SIZE), dtype=np.int64
    )
    src_i = 1
    dst_i = 0
    while src_i < np.shape(img)[0]:
        img2[:, dst_i : dst_i + NEW_TILE_SIZE] = img[:, src_i : src_i + NEW_TILE_SIZE]
        src_i += NEW_TILE_SIZE + 2
        dst_i += NEW_TILE_SIZE

    # Clear horizontal borders
    img3 = np.zeros(
        (IMG_SIZE_TILES * NEW_TILE_SIZE, IMG_SIZE_TILES * NEW_TILE_SIZE), dtype=np.int64
    )
    src_i = 1
    dst_i = 0
    while src_i < np.shape(img2)[0]:
        img3[dst_i : dst_i + NEW_TILE_SIZE, :] = img2[src_i : src_i + NEW_TILE_SIZE, :]
        src_i += NEW_TILE_SIZE + 2
        dst_i += NEW_TILE_SIZE

    # Rotate and flip image until there are dragons
    for rot_img in get_all_orientations(img3):
        n, rot_img = clear_all_dragons(rot_img)
        if n == 0:
            continue
        return np.count_nonzero(rot_img)
    else:
        raise Exception("Where there be dragons?")


def main():
    with open(sys.argv[1]) as fin:
        data = [line.strip() for line in fin]

    print("Part 1: {}".format(p1(data)))
    print("Part 2: {}".format(p2(data)))


if __name__ == "__main__":
    main()
