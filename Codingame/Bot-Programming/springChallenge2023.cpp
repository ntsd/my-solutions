#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <random>
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

struct Game {
  vector<Cell> cells;
};

struct Node {
  int visits;
  int wins;
};

mt19937 rng(42);

auto roll_dice(int min, int max) {
  uniform_int_distribution<mt19937::result_type> dist(min, max);
  return dist(rng);
}

int get_random_action(Game &game) {
  int targets = 0;
  for (const auto &cell : game.cells) {
    if (cell.type == 2 && cell.resources > 0 && cell.my_ants == 0) {
      targets++;
    }
  }

  return roll_dice(0, targets - 1);
}

vector<int> available_actions(Game &game) {
  vector<int> actions;
  for (const auto &cell : game.cells) {
    if (cell.type == 2 && cell.resources > 0 && cell.my_ants == 0) {
      actions.push_back(cell.index);
    }
  }
  return actions;
}

void update_game(Game &game, int action) {
  game.cells[action].resources -= game.cells[action].my_ants;
  if (game.cells[action].resources < 0) {
    game.cells[action].resources = 0;
  }
}

double uct(int total_games, int node_visits, int node_wins) {
  if (node_visits == 0) {
    return numeric_limits<double>::max();
  }

  double exploitation = (double)node_wins / node_visits;
  double exploration = 2.0 * log((double)total_games) / node_visits;
  return exploitation + sqrt(exploration);
}

int select_action(Game &game, const vector<Node> &tree, int total_games) {
  vector<int> actions = available_actions(game);
  int best_id = -1;
  double best_value = -1;

  for (const auto &action : actions) {
    double uct_val = uct(total_games, tree[action].visits, tree[action].wins);
    if (uct_val > best_value) {
      best_value = uct_val;
      best_id = action;
    }
  }
  return best_id;
}

int mcts(Game &game, int simulations, int max_steps) {
  vector<Node> tree(game.cells.size(), {0, 0});

  for (int i = 0; i < simulations; ++i) {
    int steps = roll_dice(1, max_steps);
    Game current_game = game;

    for (int step = 0; step < steps; ++step) {
      int random_action = get_random_action(current_game);
      update_game(current_game, random_action);
    }

    int best_id = select_action(game, tree, i + 1);
    tree[best_id].visits++;
    tree[best_id].wins++;
  }

  int best_action = select_action(game, tree, simulations);
  return best_action;
}

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

  while (1) {
    for (int i = 0; i < number_of_cells; i++) {
      Cell &cell = cells[i];
      cin >> cell.resources >> cell.my_ants >> cell.opp_ants; cin.ignore();
    }

    Game game;
    game.cells = cells;

    int best_action = mcts(game, 1000, 30);

    if (best_action != -1) {
      cout << "BEACON " << best_action << " 100" << endl;
    } else {
      cout << "WAIT" << endl;
    }
  }

  return 0;
}