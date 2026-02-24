#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <string>
#include <filesystem>
#include <chrono>
#include <algorithm>

using namespace std;

void bubble_sort(vector<int>& arr);

bool is_sorted(const vector<int>& arr) {
    for (size_t i = 1; i < arr.size(); ++i) {
        if (arr[i - 1] > arr[i])
            return false;
    }
    return true;
}

vector<int> load_csv(const string& filepath) {
    vector<int> numbers;
    ifstream file(filepath);

    if (!file.is_open()) {
        cerr << "Cannot open file: " << filepath << endl;
        return numbers;
    }

    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        string value;

        while (getline(ss, value, ';')) {
            numbers.push_back(stoi(value));
        }
    }

    return numbers;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " <optimization_flag>" << endl;
        return 1;
    }
    string opt_flag = argv[1];

    int repetitions = 5;

    string data_folder = "./data";
    string results_file = "./results/measurements_cpp.txt";

    ofstream results(results_file, ios::app);
    if (!results.is_open()) {
        cerr << "Cannot open results file. attempted at: " << filesystem::absolute(results_file) << endl;
        return 1;
    }

    for (const auto& entry : filesystem::directory_iterator(data_folder)) {
        if (entry.path().extension() == ".csv") {
            for (size_t i = 0; i < repetitions; i++)
            {
                string filepath = entry.path().string();

                vector<int> original = load_csv(filepath);

                if (original.empty()) {
                    cerr << "Skipping empty file: " << filepath << endl;
                    continue;
                }

                string filename = entry.path().stem().string();
                size_t sizeOfArray = stoul(filename);

                // --- Bubble Sort ---
                vector<int> to_sort = original;
                auto start = chrono::high_resolution_clock::now();
                bubble_sort(to_sort);
                auto end = chrono::high_resolution_clock::now();

                double duration = chrono::duration_cast<chrono::nanoseconds>(end - start).count();
                duration /= 1000000.0;

                bool success = is_sorted(to_sort);

                results << "BubbleSort;"
                    << sizeOfArray << ";"
                    << duration << ";"
                    << (success ? "true" : "false") << ";"
                    << opt_flag
                    << "\n";

                // --- Library Sort (std::sort) ---
                vector<int> to_sort_lib = original;
                auto start_lib = chrono::high_resolution_clock::now();
                sort(to_sort_lib.begin(), to_sort_lib.end());
                auto end_lib = chrono::high_resolution_clock::now();

                double duration_lib = chrono::duration_cast<chrono::nanoseconds>(end_lib - start_lib).count();
                duration_lib /= 1000000.0;

                bool success_lib = is_sorted(to_sort_lib);

                results << "LibrarySort;"
                    << sizeOfArray << ";"
                    << duration_lib << ";"
                    << (success_lib ? "true" : "false") << ";"
                    << opt_flag
                    << "\n";

            }
        }
    }

    results.close();
    return 0;
}
