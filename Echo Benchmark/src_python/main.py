import os
import time
from pathlib import Path
from bubble_sort import sort_array


def main() -> None:
    repetitions = 5

    data_dir = Path(__file__).parents[1] / 'data'
    results_file = Path(__file__).parents[1] / 'results' / 'measurements_python.txt'

    files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

    for filename in files:
        for x in range(repetitions):
            file_path = os.path.join(data_dir, filename)
            size_label = filename.split('.')[0]

            with open(file_path, 'r') as f:
                content = f.read().strip()
                original_array = [int(x) for x in content.split(';') if x]

            array_to_sort = original_array.copy()

            start_time = time.perf_counter()
            sorted_array = sort_array(array_to_sort)
            end_time = time.perf_counter()

            duration_ms = (end_time - start_time) * 1000

            is_sorted = all(sorted_array[i] <= sorted_array[i + 1] for i in range(len(sorted_array) - 1))
            success_str = "true" if is_sorted else "no"

            log_entry = f"BubbleSort;{size_label};{duration_ms};{success_str}\n"

            with open(results_file, 'a') as f:
                f.write(log_entry)


if __name__ == "__main__":
    main()
