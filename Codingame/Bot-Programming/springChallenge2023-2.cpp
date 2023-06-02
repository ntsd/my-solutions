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

double calculate_priority_factor(double my_score, double remaining_crystal,
                                 double opp_score, double total_crystals) {
  const double my_score_weight = 2.0;
  const double remaining_crystal_weight = 1.0;
  const double opp_score_weight = 1.5;

  double max_score = max(my_score + opp_score, total_crystals);
  double weight_sum =
      my_score_weight + remaining_crystal_weight + opp_score_weight;

  double priority_factor = (my_score * my_score_weight +
                            remaining_crystal * remaining_crystal_weight +
                            opp_score * opp_score_weight) /
                           (weight_sum * max_score);
  return priority_factor;
}

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
      cin >> cell.resources >> cell.my_ants >> cell.opp_ants;
      cin.ignore();
    }

    int total_ants = 0;
    double my_score = 0;
    double remaining_crystal = 0;
    for (const Cell &cell : cells) {
      if (cell.type == 2 && cell.resources > 0) {
        if (cell.my_ants > 0) {
          my_score += min(cell.resources, cell.my_ants);
        }
        remaining_crystal += cell.resources;
      }
      total_ants += cell.my_ants;
    }

    double opp_score = total_crystals - my_score - remaining_crystal;

    double priority_factor = calculate_priority_factor(
        my_score, remaining_crystal, opp_score, total_crystals);

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

      int strength;
      // Send ants to high-priority targets
      for (const auto &[index, score] : targets) {
        if (resource_type == 1) {
          // Ants (type 1); adjust strength with the priority_factor
          strength =
              min(total_ants, static_cast<int>(20 * (1.0 - priority_factor)));
        } else {
          // Crystals (type 2); adjust strength with the priority_factor
          strength = min(total_ants, static_cast<int>(20 * priority_factor));
        }

        if (total_ants - strength < 0)
          break;
        cout << "BEACON " << index << " " << strength << ";";
        total_ants -= strength;
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
