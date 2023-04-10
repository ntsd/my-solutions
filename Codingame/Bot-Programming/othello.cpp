#include <chrono>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <vector>

using namespace std;

const int MAX_TIME_MS = 100; // 150

class State {
public:
  State(int boardSize, int playerID, const vector<string> &board)
      : boardSize(boardSize), playerID(playerID), board(board),
        last_move(-1, -1) {}

  void apply_move(int x, int y) {
    board[x][y] = '0' + playerID;
    for (int dx = -1; dx <= 1; dx++) {
      for (int dy = -1; dy <= 1; dy++) {
        if (dx == 0 && dy == 0)
          continue;
        int nx = x + dx, ny = y + dy;
        while (nx >= 0 && nx < boardSize && ny >= 0 && ny < boardSize &&
               board[nx][ny] != '.') {
          if (board[nx][ny] == '0' + playerID) {
            int px = x + dx, py = y + dy;
            while (px != nx || py != ny) {
              board[px][py] = '0' + playerID;
              px += dx, py += dy;
            }
            break;
          }
          nx += dx, ny += dy;
        }
      }
    }
    last_move = make_pair(x, y);
    playerID = 1 - playerID;
  }

  int get_winner() const {
    int cnt0 = 0, cnt1 = 0;
    for (int i = 0; i < boardSize; i++) {
      for (int j = 0; j < boardSize; j++) {
        if (board[i][j] == '0')
          cnt0++;
        else if (board[i][j] == '1')
          cnt1++;
      }
    }
    if (cnt0 > cnt1)
      return 0;
    else if (cnt0 < cnt1)
      return 1;
    else
      return -1;
  }

  vector<pair<int, int>> get_legal_moves() const {
    vector<pair<int, int>> legal_moves;
    for (int i = 0; i < boardSize; i++) {
      for (int j = 0; j < boardSize; j++) {
        if (board[i][j] != '.')
          continue;
        bool valid = false;
        for (int dx = -1; dx <= 1; dx++) {
          for (int dy = -1; dy <= 1; dy++) {
            if (dx == 0 && dy == 0)
              continue;
            int nx = i + dx, ny = j + dy;
            while (nx >= 0 && nx < boardSize && ny >= 0 && ny < boardSize &&
                   board[nx][ny] != '.') {
              if (board[nx][ny] == '0' + playerID) {
                valid = true;
                break;
              }
              nx += dx, ny += dy;
            }
            if (valid)
              break;
          }
          if (valid)
            break;
        }
        if (valid)
          legal_moves.emplace_back(i, j);
      }
    }
    return legal_moves;
  }

  bool game_over() const { return get_legal_moves().empty(); }

  bool equal(State &b) {
    return (boardSize == b.boardSize && playerID == b.playerID &&
            board == b.board && last_move == b.last_move);
  };

  State copy() const { return *this; }

  int playerID;
  vector<string> board;
  int boardSize;
  pair<int, int> last_move;
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
  MCTS() : root(nullptr), time_budget(0) {}
  MCTS(int time_budget) : root(nullptr), time_budget(time_budget) {}

  ~MCTS() { delete root; }

  pair<int, int> search(const State &state) {
    root = new Node(state);
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
    pair<int, int> move = {-1, -1};
    for (auto &child : root->get_children()) {
      if (child == best_child) {
        move = child->get_state().last_move;
        break;
      }
    }
    return move;
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

  Node *root;
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
        cout << char('a' + move.second) << move.first + 1 << endl;
    }

    return 0;
}
