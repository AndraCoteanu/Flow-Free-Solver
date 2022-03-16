import json
from typing import Any, List
from colorama import init
from termcolor import colored
import time

def print_matrix(matrix):
    """
    Printez matricea cu numerele culorilor
    :param matrix: matricea
    :return:
    """
    solution = ""
    for r in range(1, len(matrix) - 1):
        for c in range(1, len(matrix[0]) - 1):
            solution += str(matrix[r][c]) + " "
        print(solution)
        solution = ""


def pretty_print_matrix(matrix):
    """
    Afisam solutia
    :param matrix: matricea
    :return:
    """
    solution = ""
    for r in range(1, len(matrix) - 1):
        for c in range(1, len(matrix[0]) - 1):
            if matrix[r][c] == 0:
                solution += "   "
            else:
                solution += colored(" ■ ", colors[matrix[r][c]], background[matrix[r][c]])
        print(solution)
        solution = ""


def parse_json(file_name1):
    """
    Parsam puzzle-urile pentru rezolvarea problemei si construiesc matricea cu care vom lucra
    :param file_name1: numele jsonului
    :return: matricea creata
    """
    grid1: List[List[int]] = []
    with open(file_name1) as file:
        seen: List[Any] = []
        contents = json.load(file)
        grid1.append([1] * (len(contents) + 2))
        for row in contents:
            grid1.append([1])
            for cell in row:
                if cell is None:
                    grid1[-1].append(0)
                else:
                    try:
                        grid1[-1].append(seen.index(cell) + 2)
                    except ValueError:
                        seen.append(cell)
                        grid1[-1].append(len(seen) + 1)
            grid1[-1].append(1)
        grid1.append([1] * (len(contents) + 2))
    return grid1


# grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         [1, 0, 0, 2, 0, 0, 0, 0, 0, 1],
#         [1, 0, 0, 3, 4, 5, 0, 0, 0, 1],
#         [1, 0, 0, 6, 0, 0, 0, 0, 0, 1],
#         [1, 0, 0, 0, 0, 0, 6, 0, 4, 1], x1 5    x2 7         y1 4    y2 4
#         [1, 0, 0, 0, 2, 0, 3, 0, 0, 1], |x1-y1| + |x2-y2| distanta manhattan sau taxicab
#         [1, 5, 0, 7, 0, 0, 7, 8, 0, 1],
#         [1, 9, 0, 0, 0, 8, 0, 0, 0, 1],
#         [1, 0, 0, 9, 0, 0, 0, 0, 0, 1],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

def identify_nodes(grid1):
    """
    Identifica pozitia nodurilor de start si cele terminale, distantele dintre culorile de acelasi fel
    :param grid1: matrix
    :return: Dictionare cu nodurile initiale, cu nodurile finale, cu nodurile corespunzatoare culorile lor si distanta
    """

    init_nodes1 = {}
    final_nodes1 = {}
    endpoints1 = []
    distances1 = {}
    for row in range(1, len(grid1) - 1):
        for column in range(1, len(grid1[0]) - 1):
            color = grid1[row][column]
            if color > 0:
                if color in init_nodes1:
                    final_nodes1[color] = [row, column]
                    distances1[color] = abs(row - init_nodes1[color][0]) + abs(column - init_nodes1[color][1])
                else:
                    init_nodes1[color] = [row, column]
                endpoints1.append([row, column, color])
    # print(distances)
    return init_nodes1, final_nodes1, endpoints1, distances1


def checkGrid(matrix):
    """
    Functie pentru verificarea validitatii matricii. Daca matricea are un punct(culoare) inconjurata de alte culori,
    adica nu pot pleca din acel punct( forma de T-uri sau + uri)
    :param matrix: matricea pe care lucram
    :return: True daca este in regula, pot pleca din fiecare punct din matrice, False altfel
    """
    for r in range(1, len(matrix) - 1):
        for c in range(1, len(matrix) - 1):
            if matrix[r][c] > 0:
                color = matrix[r][c]

                if (
                        matrix[r + 1][c] > 0 and matrix[r + 1][c] != color
                        and matrix[r - 1][c] > 0 and matrix[r - 1][c] != color
                        and matrix[r][c + 1] > 0 and matrix[r][c + 1] != color
                        and matrix[r][c - 1] > 0 and matrix[r][c - 1] != color
                ):
                    return False

                if (
                        matrix[r + 1][c] == color and matrix[r - 1][c] == color and matrix[r][c + 1] == color
                        or matrix[r + 1][c] == color and matrix[r - 1][c] == color and matrix[r][c - 1] == color
                        or matrix[r + 1][c] == color and matrix[r][c + 1] == color and matrix[r][c - 1] == color
                        or matrix[r - 1][c] == color and matrix[r][c + 1] == color and matrix[r][c - 1] == color
                ):
                    return False
    return True


def solved(matrix):
    """
    Verifica daca toate spatiile goale(0) sunt colorate
    :param matrix: matriceea
    :return: True daca este colorata, False altfel
    """
    for row in matrix:
        for cell in row:
            if cell == 0:
                return False
    return True


def solvePuzzle(matrix, init_nodes=None, final_nodes=None, endpoints=None, distances=None):
    """
    Functie recursiva pentru verificarea tuturor posibililor mutarii si sarim peste matricile care nu duc la o solutie.
    Verifica initial daca este valida matricea(daca nu are doar culori in jurul ei,daca pot pleca din acel punct),
     dupa verifica daca este colorata
    integral matricea, asta insemnand ca am gasit o solutie.
    Altfel merge la urmatoarea mutare:
    -Verifica daca punctele acestei culori sunt conectate, daca nu sunt, atunci verifica in ce directie trebuie sa
     mearga (stanga, dreapta, sus, jos)
    Daca din niciuna dintre directii nu rezulta o solutie va returna False
    :param matrix: matricea
    :return:True daca am gasit o solutie, False altfel
    """
    if init_nodes is None:
        init_nodes, final_nodes, endpoints, distances = identify_nodes(matrix)

    if not checkGrid(matrix):
        return False

    if solved(matrix):
        return True

    for color in distances:
        start_node = init_nodes[color]
        end_node = final_nodes[color]

        # daca este conectata culoarea (daca este <=1 inseamna ca e conectat)
        if abs(end_node[0] - start_node[0]) + abs(end_node[1] - start_node[1]) <= 1:
            continue
        directions = []
        if matrix[start_node[0]][start_node[1] + 1] == 0:
            if end_node[1] > start_node[1]:
                directions.insert(0, "right")  # Prioritate superioara
            else:
                #face ocolire si de asta am prioritate mai mica
                directions.append("right")  # Prioritate inferioara
        if matrix[start_node[0]][start_node[1] - 1] == 0:
            if end_node[1] < start_node[1]:
                directions.insert(0, "left")
            else:
                directions.append("left")
        if matrix[start_node[0] + 1][start_node[1]] == 0:
            if end_node[0] > start_node[0]:
                directions.insert(0, "down")
            else:
                directions.append("down")
        if matrix[start_node[0] - 1][start_node[1]] == 0:
            if end_node[0] < start_node[0]:
                directions.insert(0, "up")
            else:
                directions.append("up")
        #daca nu are unde sa mearga,daca nu intra in niciun if, nodurile fiind ocupate deja cu alte culori
        if len(directions) == 0:
            return False

        # Let's investigate possible moves in different directions...
        for direction in directions:
            row_dir = col_dir = 0
            if direction == "right":
                col_dir = 1
            elif direction == "left":
                col_dir = -1
            elif direction == "up":
                row_dir = -1
            elif direction == "down":
                row_dir = 1
            start_node[0] += row_dir
            start_node[1] += col_dir
            matrix[start_node[0]][start_node[1]] = color
            if solvePuzzle(matrix, init_nodes, final_nodes, endpoints, distances):
                return True
            else:
                # backtrack...
                matrix[start_node[0]][start_node[1]] = 0
                start_node[0] -= row_dir
                start_node[1] -= col_dir

        # aca nicio miscare nu duce la o solutie
        return False




if __name__ == "__main__":
    start_time = time.time()
    init()
    colors = ['', '', 'grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'red', 'grey', 'blue',
              'magenta', 'green', 'white', 'yellow', 'cyan']
    background = ['', '', 'on_grey', 'on_red', 'on_green', 'on_yellow', 'on_blue', 'on_magenta', 'on_cyan', 'on_white',
                  'on_grey', 'on_red', 'on_green', 'on_yellow', 'on_blue', 'on_magenta', 'on_cyan', 'on_white']

    file_name = input("File name: ")

    grid = parse_json(file_name)
    pretty_print_matrix(grid)
    rows = len(grid)
    cols = len(grid[0])
    if solvePuzzle(grid):
        print("Solution: ")
        print_matrix(grid)
        pretty_print_matrix(grid)
    else:
        print("No solution.")
    print("Running Time: "+(" %s seconds " % (time.time() - start_time)))
