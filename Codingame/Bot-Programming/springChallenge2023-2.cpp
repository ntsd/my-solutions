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

    double total_crystals = 0;
    for (auto &cell : cells) {
        // Calculate total crystals on the map
        if (cell.type == 2 && cell.resources > 0) {
            total_crystals += cell.resources;
        }
    }

    int turn = 0;
    while (1) {
        turn++;

        for (int i = 0; i < number_of_cells; i++) {
            Cell &cell = cells[i];
            cin >> cell.resources >> cell.my_ants >> cell.opp_ants; cin.ignore();
        }

        double current_crystals = 0;
        for (const Cell &cell : cells) {
            if (cell.type == 2 && cell.my_ants > 0) {
                current_crystals += min(cell.resources, cell.my_ants);
            }
        }

        double opp_score = total_crystals - current_crystals;
        double priority = opp_score / total_crystals;
        double ants_priority = 1 - priority;

        if (priority < 0.5 || turn < 100) {
            priority = 0.5;
            ants_priority = 0.5;
        }

        if (opp_score > current_crystals) { // about to lose
            ants_priority = 0;
        }

        int total_beacons = 100;

        for (int resource_type = 1; resource_type <= 2; ++resource_type) {
            vector<pair<int, double>> targets;

            for (const Cell &cell : cells) {
                if (cell.type == resource_type && cell.resources > 0 && cell.my_ants == 0) {
                    double score = static_cast<double>(cell.resources) / distances_from_my_base[cell.index];
                    targets.emplace_back(cell.index, score);
                }
            }

            // Sort targets based on their scores
            sort(targets.begin(), targets.end(), [](const auto &a, const auto &b) {
                return a.second > b.second;
            });

            // Send ants to high-priority targets
            for (const auto &[index, score] : targets) {
                int strength = min(total_beacons, resource_type == 1 ? (int) (20 * ants_priority) : (int) (20 * priority));
                if (total_beacons - strength < 0) break;
                cout << "BEACON " << index << " " << strength << ";";
                total_beacons -= strength;
            }
        }

        // Create lines of beacons back to the base to harvest resources
        for (const Cell &cell : cells) {
            if ((cell.type == 1 || cell.type == 2) && cell.resources > 0 && cell.my_ants > 0) {
                cout << "LINE " << cell.index << " " << my_base_index << " 100;";
            }
        }

        cout << endl;
    }

    return 0;
}