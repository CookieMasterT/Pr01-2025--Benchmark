#include <vector>
#include <utility>

using namespace std;
// Bubble sort implementation
void bubble_sort(vector<int>& arr) {
    bool swapped;
    size_t n = arr.size();

    for (size_t i = 0; i < n - 1; ++i) {
        swapped = false;

        for (size_t j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }

        // Optimization: stop if already sorted
        if (!swapped)
            break;
    }
}