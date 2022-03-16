import json
import os
import time
import pyautogui
from dataclasses import dataclass
from typing import List, Literal, Optional, Tuple, Dict

from PIL import Image, ImageGrab


def is_background(colour: Tuple[int, int, int]) -> bool:
    red, green, blue = colour
    return red <= 20 and green <= 20 and blue <= 20


@dataclass
class Bounds:
    top_left: Tuple[int, int]
    bot_right: Tuple[int, int]


def get_bounds() -> Bounds:
    print("Position your cursor in the top left corner")
    time.sleep(5)
    top_left = pyautogui.mouseinfo.position()
    print("Position your cursor in the bottom right corner")
    time.sleep(5)
    bot_right = pyautogui.mouseinfo.position()
    return Bounds(top_left, bot_right)


ColourGrid = List[List[Optional[Tuple[int, int, int]]]]


def find_colours(image: Image, bounds: Bounds, size: int) -> ColourGrid:
    result: List[List[Optional[Tuple[int, int, int]]]] = []
    tile_size = (bounds.bot_right[0] - bounds.top_left[0]) // size
    for row in range(0, size):
        result.append([])
        for col in range(0, size):
            middle = (
                bounds.top_left[0] + tile_size * col + tile_size // 2,
                bounds.top_left[1] + tile_size * row + tile_size // 2,
            )
            colour = image.getpixel(middle)
            if is_background(colour):
                result[-1].append(None)
            else:
                result[-1].append(colour)
    return result


try:
    os.mkdir("puzzles")
except FileExistsError:
    pass

collection = input("Collection name: ")
os.mkdir(f"puzzles/{collection}")

ask_size = (
    True if input("Ask for size for each puzzle (y/n): ") == "y" else False
)
if ask_size:
    sizes: Dict[int, Bounds] = {}
    next_button_positions: Dict[int, Tuple[int, int]] = {}
else:
    size = int(input("Size: "))
    bounds = get_bounds()
    print("Position your cursor on the next button")
    time.sleep(3)
    next_button_position = pyautogui.mouseinfo.position()

number_of_puzzles = int(input("Number of puzzles: "))

for i in range(0, number_of_puzzles):
    with open(f"puzzles/{collection}/{i}.json", "w") as file:
        image = ImageGrab.grab()
        if ask_size:
            size = int(input("Size: "))
            if size not in sizes.keys():
                sizes[size] = get_bounds()
                print("Position your cursor on the next button")
                time.sleep(3)
                next_button_positions[size] = pyautogui.mouseinfo.position()
            colour_grid = find_colours(image, sizes[size], size)
        else:
            colour_grid = find_colours(image, bounds, size)
        json.dump(colour_grid, file)
        if i < number_of_puzzles - 1:
            if ask_size:
                pyautogui.click(
                    next_button_positions[size][0],
                    next_button_positions[size][1],
                )
            else:
                pyautogui.click(
                    next_button_position[0], next_button_position[1]
                )
            time.sleep(1.5)
