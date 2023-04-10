#include <algorithm>
#include <iostream>
#include <limits>
#include <set>
#include <string>
#include <vector>

using namespace std;

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
  for (const Box &box : boxes) {
    for (char side : box.sides) {
      if (!isSidePlayed(box.name, side)) {
        validMoves.push_back({box.name, side});
      }
    }
  }
  return validMoves;
}

int minimax(int depth, bool isMax, int playerScore, int opponentScore) {
  if (depth == 0 || numBoxes == playerScore + opponentScore) {
    return playerScore - opponentScore;
  }

  if (isMax) {
    int best = numeric_limits<int>::min();
    for (Box &box : boxes) {
      if (box.sides.size() == 1) {
        playerScore++;
        box.sides = "";
        best =
            max(best, minimax(depth - 1, !isMax, playerScore, opponentScore));
        playerScore--;
        box.sides = "L";
      }
    }
    return best;
  } else {
    int best = numeric_limits<int>::max();
    for (Box &box : boxes) {
      if (box.sides.size() == 1) {
        opponentScore++;
        box.sides = "";
        best =
            min(best, minimax(depth - 1, !isMax, playerScore, opponentScore));
        opponentScore--;
        box.sides = "L";
      }
    }
    return best;
  }
}

string getNextMove() {
  int bestVal = numeric_limits<int>::min();
  string bestMove = "";
  vector<pair<string, char>> validMoves = getValidMoves();

  for (const auto &[boxName, side] : validMoves) {
    // Find the corresponding box
    auto it = find_if(boxes.begin(), boxes.end(), [boxName](const Box &box) {
      return box.name == boxName;
    });
    if (it == boxes.end())
      continue;
    Box &box = *it;

    // Try the move
    string prevSides = box.sides;
    box.sides.erase(remove(box.sides.begin(), box.sides.end(), side),
                    box.sides.end());
    int prevScore = playerScore;
    if (box.sides.empty())
      playerScore++;

    // Perform Minimax and find the best move
    int moveVal = minimax(1000, false, playerScore, opponentScore);

    // Undo the move
    box.sides = prevSides;
    playerScore = prevScore;

    // Update the best move
    if (moveVal > bestVal) {
      bestVal = moveVal;
      bestMove = boxName + " " + side;
    }
  }

  if (bestMove.empty()) {
    // If no best move is found based on Minimax, play the first available valid
    // side
    const auto &[boxName, side] = validMoves[0];
    bestMove = boxName + " " + side;
  }

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
