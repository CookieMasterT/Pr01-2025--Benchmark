import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from logger_factory import LoggerFactory

logger = LoggerFactory.get_logger("runners.generateReports")

def parse_measurements(filepath):
    """
    Parses a measurements file.
    Expected format: Algorithm;Size;TimeMs;Success;OptFlag
    Example: BubbleSort;10000;12.5;true;O2
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
            if len(parts) >= 5:
                results.append({
                    'algorithm': parts[0],
                    'size': int(parts[1]),
                    'time': float(parts[2]),
                    'success': parts[3].lower() == 'true',
                    'opt_flag': parts[4]
                })
    return results

def aggregate_results(measurements):
    """
    Groups measurements by (Algorithm, OptFlag, Size) and calculates avg, min, and max time.
    """
    grouped = defaultdict(list)
    for m in measurements:
        if m['success']:
            grouped[(m['algorithm'], m['opt_flag'], m['size'])].append(m['time'])

    aggregated = {}
    for (algo, opt_flag, size), times in grouped.items():
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            aggregated[(algo, opt_flag, size)] = (avg_time, min_time, max_time)
            
    return aggregated

def export_to_csv(agg_cpp, agg_py, filepath):
    logger.info(f"Exporting combined CSV to {filepath}")
    with open(filepath, 'w') as f:
        f.write("Language,Algorithm,OptFlag,Size,AvgTime,MinTime,MaxTime\n")
        
        for (algo, opt_flag, size), (avg, mn, mx) in agg_cpp.items():
            f.write(f"C++,{algo},{opt_flag},{size},{avg:.4f},{mn:.4f},{mx:.4f}\n")
            
        for (algo, opt_flag, size), (avg, mn, mx) in agg_py.items():
            f.write(f"Python,{algo},{opt_flag},{size},{avg:.4f},{mn:.4f},{mx:.4f}\n")

def generate_charts(agg_cpp, agg_py, reports_dir):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        logger.warning("matplotlib not found, skipping chart generation")
        return []

    logger.info("Generating charts...")
    
    # Organize data for plotting
    plot_data = defaultdict(lambda: {'sizes': [], 'times': []})
    
    for (algo, opt_flag, size), (avg, _, _) in agg_cpp.items():
        label = f"C++ {algo} ({opt_flag})"
        plot_data[label]['sizes'].append(size)
        plot_data[label]['times'].append(avg)
        
    for (algo, opt_flag, size), (avg, _, _) in agg_py.items():
        label = f"Python {algo}"
        plot_data[label]['sizes'].append(size)
        plot_data[label]['times'].append(avg)

    # Sort data by size for proper line plotting
    for label in plot_data:
        combined = sorted(zip(plot_data[label]['sizes'], plot_data[label]['times']))
        plot_data[label]['sizes'], plot_data[label]['times'] = zip(*combined)

    charts = []

    # 1. Bubble Sort Comparison (Python vs C++ O0 vs C++ O2)
    plt.figure(figsize=(10, 6))
    for label, data in plot_data.items():
        if "BubbleSort" in label:
            plt.plot(data['sizes'], data['times'], marker='o', label=label)
    
    plt.title('Bubble Sort Performance Comparison')
    plt.xlabel('Array Size')
    plt.ylabel('Average Time (ms)')
    plt.legend()
    plt.grid(True)
    bubble_chart = reports_dir / 'chart_bubble_sort.png'
    plt.savefig(bubble_chart)
    plt.close()
    charts.append("chart_bubble_sort.png")

    # 2. Library Sort Comparison (Python vs C++ O0 vs C++ O2)
    plt.figure(figsize=(10, 6))
    for label, data in plot_data.items():
        if "LibrarySort" in label:
            plt.plot(data['sizes'], data['times'], marker='s', label=label)
            
    plt.title('Library Sort Performance Comparison')
    plt.xlabel('Array Size')
    plt.ylabel('Average Time (ms)')
    plt.legend()
    plt.grid(True)
    lib_chart = reports_dir / 'chart_library_sort.png'
    plt.savefig(lib_chart)
    plt.close()
    charts.append("chart_library_sort.png")
    
    # 3. All Algorithms Plot
    plt.figure(figsize=(12, 8))
    for label, data in plot_data.items():
        plt.plot(data['sizes'], data['times'], marker='.', label=label)
            
    plt.title('All Algorithms Performance')
    plt.xlabel('Array Size')
    plt.ylabel('Average Time (ms)')
    plt.legend()
    plt.grid(True)
    all_chart = reports_dir / 'chart_all_linear.png'
    plt.savefig(all_chart)
    plt.close()
    charts.append("chart_all_linear.png")

    return charts

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
    # Generate timestamp for both CSV and MD
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create specific directory for this report execution
    current_report_dir = reports_dir / f"report_{timestamp}"
    current_report_dir.mkdir(exist_ok=True)

    # Export CSV alongside markdown
    csv_path = current_report_dir / f"report_{timestamp}.csv"
    export_to_csv(agg_cpp, agg_py, csv_path)
    
    # Generate Charts
    chart_files = generate_charts(agg_cpp, agg_py, current_report_dir)

    all_keys = set(agg_cpp.keys()).union(set(agg_py.keys()))
    sorted_keys = sorted(list(all_keys), key=lambda x: (x[0], x[1], x[2])) # sort by algo, flag, size

    # 3. Generate Markdown content
    report_path = current_report_dir / f"report_{timestamp}.md"

    md_content = [
        f"# Raport z Benchmarku: C++ vs Python",
        f"Data wygenerowania: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Opis testu",
        "Poniższy raport przedstawia porównanie wydajności algorytmów sortowania zaimplementowanych w C++ i Pythonie.",
        "Uwzględniono dwa algorytmy (**Bubble Sort** oraz domyślne \u0060std::sort\u0060 / \u0060list.sort()\u0060) oraz wpływ flag kompilacji C++.",
        "",
        "## Środowisko testowe",
        "```text",
        env_info.strip(),
        "```",
        "",
        "## Wyniki w formie Wykresów",
    ]
    
    for chart in chart_files:
        md_content.append(f"![Wykres](./{chart})")
        
    md_content.extend([
        "",
        "## Tabele Wyników",
        "",
        "### Wyniki: Bubble Sort",
        "| Język | Flaga | Rozmiar | Średni czas [ms] | Min-Max [ms] |",
        "|--------|-------|---------|------------------|--------------|"
    ])

    for algo, opt_flag, size in sorted_keys:
        if algo == "BubbleSort":
            if (algo, opt_flag, size) in agg_cpp:
                avg, mn, mx = agg_cpp[(algo, opt_flag, size)]
                md_content.append(f"| C++ | {opt_flag} | {size} | {avg:.2f} | {mn:.2f} - {mx:.2f} |")
            if (algo, opt_flag, size) in agg_py:
                avg, mn, mx = agg_py[(algo, opt_flag, size)]
                md_content.append(f"| Python | - | {size} | {avg:.2f} | {mn:.2f} - {mx:.2f} |")

    md_content.extend([
        "",
        "### Wyniki: Library Sort",
        "| Język | Flaga | Rozmiar | Średni czas [ms] | Min-Max [ms] |",
        "|--------|-------|---------|------------------|--------------|"
    ])

    for algo, opt_flag, size in sorted_keys:
        if algo == "LibrarySort":
            if (algo, opt_flag, size) in agg_cpp:
                avg, mn, mx = agg_cpp[(algo, opt_flag, size)]
                md_content.append(f"| C++ | {opt_flag} | {size} | {avg:.2f} | {mn:.2f} - {mx:.2f} |")
            if (algo, opt_flag, size) in agg_py:
                avg, mn, mx = agg_py[(algo, opt_flag, size)]
                md_content.append(f"| Python | - | {size} | {avg:.2f} | {mn:.2f} - {mx:.2f} |")

    md_content.extend([
        "",
        "## Zapis Wyników do CSV",
        f"Pośrednie wyniki ze wszystkich pomiarów można znaleźć w dołączonym pliku [{csv_path.name}](./{csv_path.name}).",
        "",
        "## Wnioski",
    ])

    logger.info(f"Generating markdown report at {report_path}")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))

if __name__ == "__main__":
    generate_report()
