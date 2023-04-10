#include <algorithm>
#include <chrono>
#include <iostream>
#include <limits>
#include <set>
#include <string>
#include <vector>

using namespace std;
using namespace std::chrono;

int boardSize;
char playerId;
int playerScore, opponentScore;
int numBoxes;

struct Box {
  string name;
  string sides;
};

struct PlayedSide {
  string boxName;
  char side;

  bool operator<(const PlayedSide &other) const {
    return boxName < other.boxName ||
           (boxName == other.boxName && side < other.side);
  }
};

vector<Box> boxes;
set<PlayedSide> playedSides;

bool isSidePlayed(const string &boxName, char side) {
  return playedSides.count({boxName, side}) > 0;
}

vector<pair<string, char>> getValidMoves() {
    vector<pair<string, char>> validMoves;
    vector<pair<string, char>> priorityMoves;

    for (const Box &box : boxes) {
        for (char side : box.sides) {
            string boxName = box.name;
            if (playedSides.find({boxName, side}) == playedSides.end()) {
                if (box.sides.size() == 1) {
                    priorityMoves.push_back({boxName, side});
                } else {
                    validMoves.push_back({boxName, side});
                }
            }
        }
    }

    if (!priorityMoves.empty()) {
        return priorityMoves;
    }
    return validMoves;
}

int alphabeta(int depth, bool isMax, int alpha, int beta, int playerScore,
              int opponentScore) {
  if (depth == 0) {
    return playerScore - opponentScore;
  }

  vector<pair<string, char>> validMoves = getValidMoves();
  if (validMoves.empty()) {
    return playerScore - opponentScore;
  }

  if (isMax) {
    int bestVal = numeric_limits<int>::min();
    for (const auto &[boxName, side] : validMoves) {
      auto it = find_if(boxes.begin(), boxes.end(), [boxName](const Box &box) {
        return box.name == boxName;
      });
      if (it == boxes.end())
        continue;
      Box &box = *it;

      string prevSides = box.sides;
      box.sides.erase(remove(box.sides.begin(), box.sides.end(), side),
                      box.sides.end());
      int prevScore = playerScore;
      if (box.sides.empty())
        playerScore++;

      int moveVal =
          alphabeta(depth - 1, !isMax, alpha, beta, playerScore, opponentScore);

      box.sides = prevSides;
      playerScore = prevScore;

      bestVal = max(bestVal, moveVal);
      alpha = max(alpha, bestVal);

      if (beta <= alpha) {
        break;
      }
    }
    return bestVal;
  } else {
    int bestVal = numeric_limits<int>::max();
    for (const auto &[boxName, side] : validMoves) {
      auto it = find_if(boxes.begin(), boxes.end(), [boxName](const Box &box) {
        return box.name == boxName;
      });
      if (it == boxes.end())
        continue;
      Box &box = *it;

      string prevSides = box.sides;
      box.sides.erase(remove(box.sides.begin(), box.sides.end(), side),
                      box.sides.end());
      int prevScore = opponentScore;
      if (box.sides.empty())
        opponentScore++;

      int moveVal =
          alphabeta(depth - 1, !isMax, alpha, beta, playerScore, opponentScore);

      box.sides = prevSides;
      opponentScore = prevScore;

      bestVal = min(bestVal, moveVal);
      beta = min(beta, bestVal);

      if (beta <= alpha) {
        break;
      }
    }
    return bestVal;
  }
}

string getNextMove() {
    int bestVal = numeric_limits<int>::min();
    string bestMove = "";
    vector<pair<string, char>> validMoves = getValidMoves();
    int alpha = numeric_limits<int>::min();
    int beta = numeric_limits<int>::max();
    
    auto start = steady_clock::now();

    for (const auto &[boxName, side] : validMoves) {
        // Find the box and try the move
        auto it = find_if(boxes.begin(), boxes.end(), [boxName](const Box &box) {
            return box.name == boxName;
        });
        if (it == boxes.end()) continue;
        Box &box = *it;

        string prevSides = box.sides;
        box.sides.erase(remove(box.sides.begin(), box.sides.end(), side), box.sides.end());
        int prevScore = playerScore;
        if (box.sides.empty()) playerScore++;

        // Add the side to the playedSides set
        playedSides.insert({boxName, side});

        int moveVal = alphabeta(2, false, alpha, beta, playerScore, opponentScore);

        // Undo the move and update the best move
        box.sides = prevSides;
        playerScore = prevScore;

        // Remove the side from the playedSides set
        playedSides.erase({boxName, side});

        if (moveVal > bestVal) {
            bestVal = moveVal;
            bestMove = boxName + " " + side;
        }

        alpha = max(alpha, bestVal);

        auto end = steady_clock::now();
        auto elapsed = duration_cast<milliseconds>(end - start);

        if (elapsed.count() >= 95) {
            break;
        }
    }

    if (bestMove.empty()) {
        // If no best move is found based on Alpha-Beta pruning, play the first available valid side
        const auto &[boxName, side] = validMoves[0];
        bestMove = boxName + " " + side;
    }

    // Add the best move to the playedSides set
    playedSides.insert({bestMove.substr(0, 2), bestMove[3]});
    return bestMove;
}

int main() {
  cin >> boardSize >> playerId;
  while (true) {
    cin >> playerScore >> opponentScore;
    cin >> numBoxes;
    boxes.resize(numBoxes);
    for (int i = 0; i < numBoxes; i++) {
      cin >> boxes[i].name >> boxes[i].sides;
    }
    cout << getNextMove() << endl;
  }
  return 0;
}
