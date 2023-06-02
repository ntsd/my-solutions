#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>

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
  cin >> number_of_cells;
  cin.ignore();

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
  cin >> number_of_bases;
  cin.ignore();

  vector<int> my_base_indices, opp_base_indices;
  for (int i = 0; i < number_of_bases; ++i) {
    int my_base_index, opp_base_index;
    cin >> my_base_index;
    cin.ignore();
    cin >> opp_base_index;
    cin.ignore();

    my_base_indices.push_back(my_base_index);
    opp_base_indices.push_back(opp_base_index);
  }

  auto shortest_paths = [&](const Cell &start) {
    vector<int> dist(cells.size(), -1);
    dist[start.index] = 0;

    queue<int> q;
    q.push(start.index);

    while (!q.empty()) {
      const Cell &current = cells[q.front()];
      q.pop();

      for (int n : current.neighbors) {
        if (n == -1)
          continue;
        if (dist[n] == -1) {
          dist[n] = dist[current.index] + 1;
          q.push(n);
        }
      }
    }

    return dist;
  };

  vector<vector<int>> distances_from_my_bases;
  for (int my_base_index : my_base_indices) {
    distances_from_my_bases.push_back(shortest_paths(cells[my_base_index]));
  }

  while (1) {
    for (int i = 0; i < number_of_cells; i++) {
      Cell &cell = cells[i];
      cin >> cell.resources >> cell.my_ants >> cell.opp_ants;
      cin.ignore();
    }

    int total_beacons = 100;

    for (int resource_type = 1; resource_type <= 2; ++resource_type) {
      vector<pair<int, double>> targets;

      for (const Cell &cell : cells) {
        if (cell.type == resource_type && cell.resources > 0 &&
            cell.my_ants == 0) {
          if (cell.opp_ants > 0) { // Both players have ants in the same cell
            int my_weakest_attack_chain = 1e9;
            int opp_weakest_attack_chain = 1e9;

            for (const auto &dist : distances_from_my_bases) {
              my_weakest_attack_chain =
                  min(my_weakest_attack_chain, dist[cell.index]);
            }

            // Choose one of the opponent's bases as a representative
            opp_weakest_attack_chain =
                shortest_paths(cells[opp_base_indices[0]])[cell.index];

            if (opp_weakest_attack_chain <= my_weakest_attack_chain) {
              // Skip cells where the opponent's attack chain is stronger
              continue;
            }
          }

          // Choose the closest base to prioritize the target cell
          int min_distance = 1e9;
          for (const auto &dist : distances_from_my_bases) {
            min_distance = min(min_distance, dist[cell.index]);
          }

          double score = static_cast<double>(cell.resources) / min_distance;
          targets.emplace_back(cell.index, score);
        }
      }

      // Sort targets based on their scores
      sort(targets.begin(), targets.end(),
           [](const auto &a, const auto &b) { return a.second > b.second; });

      // Send ants to high-priority targets
      for (const auto &[index, score] : targets) {
        int strength = min(total_beacons, resource_type == 1 ? 5 : 20);
        if (total_beacons - strength < 0)
          break;
        cout << "BEACON " << index << " " << strength << ";";
        total_beacons -= strength;
      }
    }

    // Create lines of beacons back to the base to harvest resources
    for (const Cell &cell : cells) {
      if ((cell.type == 1 || cell.type == 2) && cell.resources > 0 &&
          cell.my_ants > 0) {
        // Choose the closest base as the line target
        int closest_base_index = my_base_indices[0];
        int min_distance = distances_from_my_bases[0][cell.index];

        for (size_t i = 1; i < my_base_indices.size(); ++i) {
          if (distances_from_my_bases[i][cell.index] < min_distance) {
            min_distance = distances_from_my_bases[i][cell.index];
            closest_base_index = my_base_indices[i];
          }
        }

        cout << "LINE " << cell.index << " " << closest_base_index << " 100;";
      }
    }

    cout << endl;
  }

  return 0;
}
