#include <chrono>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <vector>

using namespace std;

const int MAX_TIME_MS = 50; // 150

class State {
public:
  State(int board_size, int player_id, const vector<string> &board)
      : board_size(board_size), player_id(player_id), board(board),
        last_move(-1, -1) {}

  vector<pair<int, int>> get_legal_moves() const {
    vector<pair<int, int>> legal_moves;
    for (int i = 0; i < board_size; i++) {
      for (int j = 0; j < board_size; j++) {
        if (board[i][j] == '.') {
          if (is_legal_move(i, j)) {
            legal_moves.emplace_back(i, j);
          }
        }
      }
    }
    return legal_moves;
  }

  void apply_move(int row, int col) {
    if (!is_legal_move(row, col)) {
      throw runtime_error("Invalid move");
    }
    board[row][col] = player_id == 0 ? '0' : '1';
    flip_pieces(row, col);
    last_move = {row, col};
    player_id = 1 - player_id;
  }

  bool game_over() const { return get_legal_moves().empty(); }

  pair<int, int> get_scores() const {
    int black_count = 0;
    int white_count = 0;
    for (const auto &row : board) {
      for (char c : row) {
        if (c == '0') {
          black_count++;
        } else if (c == '1') {
          white_count++;
        }
      }
    }
    return {black_count, white_count};
  }

  pair<int, int> get_last_move() const { return last_move; }

  int get_winner() const {
    auto scores = get_scores();
    if (scores.first > scores.second) {
      return 0;
    } else if (scores.first < scores.second) {
      return 1;
    } else {
      return -1;
    }
  }

  bool equal(State &b) {
    return (board_size == b.board_size && player_id == b.player_id &&
            board == b.board && last_move == b.last_move);
  };

  State copy() const { return *this; }

private:
  int board_size;
  int player_id;
  vector<string> board;
  pair<int, int> last_move;

  bool is_legal_move(int row, int col) const {
    if (row < 0 || row >= board_size || col < 0 || col >= board_size) {
      return false;
    }
    if (board[row][col] != '.') {
      return false;
    }
    bool legal = false;
    for (int dr = -1; dr <= 1; dr++) {
      for (int dc = -1; dc <= 1; dc++) {
        if (dr == 0 && dc == 0) {
          continue;
        }
        int r = row + dr;
        int c = col + dc;
        while (r >= 0 && r < board_size && c >= 0 && c < board_size) {
          if (board[r][c] == '.') {
            break;
          }
          if (board[r][c] == (player_id == 0 ? '1' : '0')) {
            r += dr;
            c += dc;
          } else {
            legal = true;
            break;
          }
        }
      }
    }
    return legal;
  }

  void flip_pieces(int row, int col) {
    char curr_player = (player_id == 0 ? '0' : '1');
    char other_player = (player_id == 0 ? '1' : '0');
    board[row][col] = curr_player;

    for (int dr = -1; dr <= 1; dr++) {
      for (int dc = -1; dc <= 1; dc++) {
        if (dr == 0 && dc == 0) {
          continue;
        }
        int r = row + dr;
        int c = col + dc;
        bool found_other_player = false;
        while (r >= 0 && r < board_size && c >= 0 && c < board_size) {
          if (board[r][c] == '.') {
            break;
          }
          if (board[r][c] == other_player) {
            r += dr;
            c += dc;
            found_other_player = true;
          } else {
            if (found_other_player) {
              // Flip all the pieces between (row, col) and (r, c)
              while (r != row + dr || c != col + dc) {
                r -= dr;
                c -= dc;
                board[r][c] = curr_player;
              }
            }
            break;
          }
        }
      }
    }
  }
};

class Node {
public:
  Node(const State &state)
      : state(state), parent(nullptr), children(), visits(0), wins(0) {}
  Node(const State &state, Node *parent)
      : state(state), parent(parent), children(), visits(0), wins(0) {}

  ~Node() {
    for (auto &child : children) {
      delete child;
    }
  }

  Node *add_child(const State &state) {
    auto child = new Node(state, this);
    children.push_back(child);
    return child;
  }

  void update(int result) {
    visits++;
    wins += result;
  }

  bool fully_expanded() const {
    return children.size() == state.get_legal_moves().size();
  }

  Node *best_child(double c_param) const {
    double best_score = -1e9;
    Node *best_child = nullptr;
    for (auto &child : children) {
      double exploit = double(child->wins) / child->visits;
      double explore = c_param * sqrt(log(visits) / child->visits);
      double score = exploit + explore;
      if (score > best_score) {
        best_score = score;
        best_child = child;
      }
    }
    return best_child;
  }

  const State &get_state() const { return state; }

  Node *get_parent() const { return parent; }

  const vector<Node *> &get_children() const { return children; }

  int get_visits() const { return visits; }

  int get_wins() const { return wins; }

private:
  State state;
  Node *parent;
  vector<Node *> children;
  int visits, wins;
};

class MCTS {
public:
  MCTS(int time_budget) : time_budget(time_budget) {}

  pair<int, int> search(const State &state) {
    Node *root = new Node(state);
    auto start_time = chrono::high_resolution_clock::now();
    while (true) {
      auto current_time = chrono::high_resolution_clock::now();
      if (chrono::duration_cast<chrono::milliseconds>(current_time - start_time)
              .count() >= time_budget) {
        break;
      }
      Node *node = select(root);
      if (node->get_state().game_over()) {
        backpropagate(node, node->get_state().get_winner());
      } else {
        Node *expanded_node = expand(node);
        if (expanded_node != nullptr) {
          int result = simulate(expanded_node->get_state());
          backpropagate(expanded_node, result);
        }
      }
    }
    Node *best_child = root->best_child(0);
    return best_child->get_state().get_last_move();
  }

private:
  Node *select(Node *node) const {
    while (!node->get_state().game_over()) {
      if (!node->fully_expanded()) {
        return expand(node);
      } else {
        node = node->best_child(1.0 / sqrt(2.0));
      }
    }
    return node;
  }

  Node *expand(Node *node) const {
    auto legal_moves = node->get_state().get_legal_moves();
    for (auto &move : legal_moves) {
      auto new_state = node->get_state().copy();
      new_state.apply_move(move.first, move.second);
      bool already_expanded = false;
      for (auto &child : node->get_children()) {
        State state = child->get_state();
        if (state.equal(new_state)) { // todo
          already_expanded = true;
          break;
        }
      }
      if (!already_expanded) {
        return node->add_child(new_state);
      }
    }
    return nullptr;
  }

  int simulate(State state) const {
    while (!state.game_over()) {
      auto legal_moves = state.get_legal_moves();
      int index = rand() % legal_moves.size();
      auto move = legal_moves[index];
      state.apply_move(move.first, move.second);
    }
    return state.get_winner();
  }

  void backpropagate(Node *node, int result) const {
    while (node != nullptr) {
      node->update(result);
      node = node->get_parent();
    }
  }

  int time_budget;
};

int main() {
  srand(time(NULL));

  int player_id, board_size;
  cin >> player_id >> board_size;

  MCTS mcts(MAX_TIME_MS);

  while (true) {
    vector<string> board(board_size);
    for (int i = 0; i < board_size; i++) {
      cin >> board[i];
    }

    int actionCount;
    cin >> actionCount;
    vector<string> actions(actionCount);
    for (int i = 0; i < actionCount; i++) {
      cin >> actions[i];
    }

    State state = State(board_size, player_id, board);

    auto move = mcts.search(state);

    cout << "EXPERT " << char('a' + move.second) << move.first + 1 << endl;
  }

  return 0;
}
