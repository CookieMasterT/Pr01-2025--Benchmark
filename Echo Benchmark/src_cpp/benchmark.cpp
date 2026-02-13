#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <string>
#include <filesystem>
#include <chrono>

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

int main() {
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

                vector<int> to_sort = original;

                auto start = chrono::high_resolution_clock::now();
                bubble_sort(to_sort);
                auto end = chrono::high_resolution_clock::now();

                double duration = chrono::duration_cast<chrono::nanoseconds>(end - start).count();
                duration /= 1000000;

                bool success = is_sorted(to_sort);

                string filename = entry.path().stem().string();
                size_t sizeOfArray = stoul(filename);

                results << "BubbleSort;"
                    << sizeOfArray << ";"
                    << duration << ";"
                    << (success ? "true" : "false")
                    << "\n";
            }
        }
    }

    results.close();
    return 0;
}
