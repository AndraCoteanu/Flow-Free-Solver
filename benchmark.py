import csv
import multiprocessing
import os
from statistics import fmean
from time import time
from typing import Any, Callable, Optional

import heuristic_solver
import sat_solver

sample_size = 5
timeout = 10.0


def benchmark(func: Callable[[], Any]) -> Optional[float]:
    results = []

    for _ in range(0, sample_size):
        start_time = time()

        process = multiprocessing.Process(target=func)
        process.start()
        process.join(timeout)
        if process.exitcode is None:
            process.terminate()
            return -1.0

        results.append(time() - start_time)
    return fmean(results)


if __name__ == "__main__":
    directory = input("Puzzle directory: ")
    with open("benchmark_sat.csv", "w", newline="") as sat_file, open(
        "benchmark_heuristic.csv", "w", newline=""
    ) as heuristic_file:
        sat_writer = csv.writer(sat_file)
        heuristic_writer = csv.writer(heuristic_file)

        for root, _, files in os.walk(directory):
            for file in files:
                path = os.path.join(root, file)
                print(path)

                sat_puzzle = sat_solver.Puzzle.from_file(path)
                heuristic_puzzle = heuristic_solver.parse_json(path)

                for func, writer in (
                    ((lambda: sat_puzzle.solve()), sat_writer),
                    (
                        (lambda: heuristic_solver.solvePuzzle(heuristic_puzzle)),
                        heuristic_writer,
                    ),
                ):
                    benchmark_result = benchmark(func)
                    if benchmark_result is None:
                        benchmark_result = -1
                    writer.writerow([path, benchmark_result, sat_puzzle.grid_size])
