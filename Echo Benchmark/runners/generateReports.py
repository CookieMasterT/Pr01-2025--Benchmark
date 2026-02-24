import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from logger_factory import LoggerFactory

logger = LoggerFactory.get_logger("runners.generateReports")

def parse_measurements(filepath):
    """
    Parses a measurements file.
    Expected format: Algorithm;Size;TimeMs;Success
    Example: BubbleSort;10000;12.5;true
    Returns a list of dictionaries.
    """
    results = []
    if not filepath.exists():
        logger.warning(f"Measurements file not found: {filepath}")
        return results

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(';')
            if len(parts) >= 4:
                results.append({
                    'algorithm': parts[0],
                    'size': int(parts[1]),
                    'time': float(parts[2]),
                    'success': parts[3].lower() == 'true'
                })
    return results

def aggregate_results(measurements):
    """
    Groups measurements by (Algorithm, Size) and calculates avg, min, and max time.
    """
    grouped = defaultdict(list)
    for m in measurements:
        if m['success']:
            grouped[(m['algorithm'], m['size'])].append(m['time'])

    aggregated = {}
    for (algo, size), times in grouped.items():
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            aggregated[(algo, size)] = (avg_time, min_time, max_time)
            
    return aggregated

def generate_report():
    project_dir = Path(__file__).resolve().parents[1]
    results_dir = project_dir / "results"
    reports_dir = project_dir / "reports"
    reports_dir.mkdir(exist_ok=True)

    # 1. Read environment info
    env_info = "Environment information not available."
    env_file = results_dir / "env_info.txt"
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_info = f.read()

    # 2. Parse and aggregate results
    cpp_results = parse_measurements(results_dir / "measurements_cpp.txt")
    py_results = parse_measurements(results_dir / "measurements_python.txt")

    agg_cpp = aggregate_results(cpp_results)
    agg_py = aggregate_results(py_results)

    all_keys = set(agg_cpp.keys()).union(set(agg_py.keys()))
    sorted_keys = sorted(list(all_keys), key=lambda x: (x[0], x[1])) # sort by algo, then size

    # 3. Generate Markdown content
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = reports_dir / f"report_{timestamp}.md"

    md_content = [
        f"# Raport z Benchmarku: C++ vs Python",
        f"Data wygenerowania: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Opis testu",
        "Poniższy raport przedstawia porównanie wydajności algorytmów sortowania zaimplementowanych w C++ i Pythonie.",
        "",
        "## Środowisko testowe",
        "```text",
        env_info.strip(),
        "```",
        "",
        "## Parametry testu",
        "- **Badane algorytmy**: BubbleSort",
        "- **Języki**: C++, Python",
        "- **Precyzja pomiaru**: Mikrosekundy/Milisekundy (przeliczone na ms)",
        "- **Flagi kompilatora C++**: -O2",
        "",
        "## Wyniki",
        "| Język | Algorytm | Rozmiar | Średni czas [ms] | Min-Max [ms] |",
        "|--------|----------|---------|------------------|--------------|"
    ]

    for algo, size in sorted_keys:
        if (algo, size) in agg_cpp:
            avg, mn, mx = agg_cpp[(algo, size)]
            md_content.append(f"| C++ | {algo} | {size} | {avg:.2f} | {mn:.2f} - {mx:.2f} |")
        
        if (algo, size) in agg_py:
            avg, mn, mx = agg_py[(algo, size)]
            md_content.append(f"| Python | {algo} | {size} | {avg:.2f} | {mn:.2f} - {mx:.2f} |")

    md_content.extend([
        "",
        "## Wnioski",
    ])

    logger.info(f"Generating markdown report at {report_path}")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))

if __name__ == "__main__":
    generate_report()
