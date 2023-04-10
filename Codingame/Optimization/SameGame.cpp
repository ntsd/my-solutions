#include <algorithm>
#include <chrono>
#include <iostream>
#include <queue>
#include <vector>

using namespace std;
using namespace chrono;

constexpr int ROWS = 15;
constexpr int COLS = 15;

vector<vector<int>> board(ROWS, vector<int>(COLS));
vector<vector<bool>> visited(ROWS, vector<bool>(COLS));
queue<pair<int, int>> moves;

int dx[] = {-1, 0, 1, 0};
int dy[] = {0, 1, 0, -1};

bool is_valid(int x, int y) { return x >= 0 && x < COLS && y >= 0 && y < ROWS; }

int floodfill(int x, int y, int color, bool remove = false) {
  if (!is_valid(x, y) || visited[y][x] || board[y][x] != color)
    return 0;

  visited[y][x] = true;
  int cnt = 1;
  for (int i = 0; i < 4; ++i)
    cnt += floodfill(x + dx[i], y + dy[i], color);

  if (remove)
    board[y][x] = -1;

  return cnt;
}

void simulate() {
  for (int x = 0; x < COLS; ++x) {
    int insert_pos = 0;
    for (int y = 0; y < ROWS; ++y) {
      if (board[y][x] != -1) {
        board[insert_pos][x] = board[y][x];
        if (insert_pos != y)
          board[y][x] = -1;
        insert_pos++;
      }
    }
  }

  int insert_col = 0;
  for (int x = 0; x < COLS; ++x) {
    if (board[0][x] != -1) {
      if (insert_col != x) {
        for (int y = 0; y < ROWS; ++y) {
          board[y][insert_col] = board[y][x];
          board[y][x] = -1;
        }
      }
      insert_col++;
    }
  }
}

void calculate_best_moves() {
  auto start = high_resolution_clock::now();
  auto end = high_resolution_clock::now();
  auto duration = duration_cast<milliseconds>(end - start);

  while (duration.count() < 20000) {
    int best_x = -1, best_y = -1, best_score = -1;

    for (int y = 0; y < ROWS; ++y) {
      for (int x = 0; x < COLS; ++x) {
        if (board[y][x] == -1 || visited[y][x])
          continue;

        int cnt = floodfill(x, y, board[y][x]);
        if (cnt > 2) { // Ensure selected region has at least 2 cells
          int score = (cnt - 2) * (cnt - 2);
          if (score > best_score) {
            best_score = score;
            best_x = x;
            best_y = y;
          }
        }
      }
    }

    if (best_score == -1)
      break;

    for (auto &row : visited)
      fill(row.begin(), row.end(), false);

    floodfill(best_x, best_y, board[best_y][best_x], true);
    moves.push({best_x, best_y});
    for (auto &row : visited)
      fill(row.begin(), row.end(), false);

    simulate();

    end = high_resolution_clock::now();
    duration = duration_cast<milliseconds>(end - start);
  }
}

int main() {
  for (int i = 0; i < ROWS; ++i)
    for (int j = 0; j < COLS; ++j)
      cin >> board[ROWS - 1 - i][j];
  calculate_best_moves();

  while (!moves.empty()) {
    auto move = moves.front();
    moves.pop();
    cout << move.first << " " << move.second << endl;

    for (int i = 0; i < ROWS; ++i)
      for (int j = 0; j < COLS; ++j)
        cin >> board[ROWS - 1 - i][j];
  }

  return 0;
}
