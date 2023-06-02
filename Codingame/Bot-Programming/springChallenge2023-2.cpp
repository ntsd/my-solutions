#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>

using namespace std;

struct Cell {
    int index;
    int type;
    int resources;
    int my_ants;
    int opp_ants;
    vector<int> neighbors;
};

int main() {
    int number_of_cells;
    cin >> number_of_cells; cin.ignore();

    vector<Cell> cells(number_of_cells);

    for (int i = 0; i < number_of_cells; i++) {
        Cell &cell = cells[i];
        cell.index = i;
        cin >> cell.type >> cell.resources;
        cell.neighbors.resize(6);
        for (int j = 0; j < 6; j++) {
            cin >> cell.neighbors[j];
        }
        cin.ignore();
    }

    int number_of_bases;
    cin >> number_of_bases; cin.ignore();

    int my_base_index, opp_base_index;
    cin >> my_base_index; cin.ignore();
    cin >> opp_base_index; cin.ignore();

    auto shortest_paths = [&](const Cell &start) {
        vector<int> dist(cells.size(), -1);
        dist[start.index] = 0;

        queue<int> q;
        q.push(start.index);

        while (!q.empty()) {
            const Cell &current = cells[q.front()];
            q.pop();

            for (int n : current.neighbors) {
                if (n == -1) continue;
                if (dist[n] == -1) {
                    dist[n] = dist[current.index] + 1;
                    q.push(n);
                }
            }
        }

        return dist;
    };

    vector<int> distances_from_my_base = shortest_paths(cells[my_base_index]);

    while (1) {
        for (int i = 0; i < number_of_cells; i++) {
            Cell &cell = cells[i];
            cin >> cell.resources >> cell.my_ants >> cell.opp_ants; cin.ignore();
        }

        vector<pair<int, double>> targets;
        for (const Cell &cell : cells) {
            if (cell.type == 2 && cell.resources > 0 && cell.my_ants == 0) {
                double score = static_cast<double>(cell.resources) / distances_from_my_base[cell.index];
                targets.emplace_back(cell.index, score);
            }
        }

        // Sort targets based on their scores
        sort(targets.begin(), targets.end(), [](const auto &a, const auto &b) {
            return a.second > b.second;
        });

        // Send ants to high-priority targets
        int total_beacons = 100;
        for (const auto &[index, score] : targets) {
            int strength = min(total_beacons, 20);
            if (total_beacons - strength < 0) break;
            cout << "BEACON " << index << " " << strength << ";";
            total_beacons -= strength;
        }

        // Place lines of beacons back to the base to harvest resources
        for (const Cell &cell : cells) {
            if (cell.type == 2 && cell.resources > 0 && cell.my_ants > 0) {
                cout << "LINE " << cell.index << " " << my_base_index << " 100;";
            }
        }

        cout << endl;
    }

    return 0;
}