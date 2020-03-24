#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <array>

using namespace std;

struct Point
{
    int x{-1}, y{-1};

    int distance(const Point &oth)
    {
        return abs(x - oth.x) + abs(y - oth.y);
    }

    ostream &dump(ostream &ioOut) const
    {
        ioOut << x << " " << y;
        return ioOut;
    }
};

ostream &operator<<(ostream &ioOut, const Point &obj)
{
    return obj.dump(ioOut);
}

struct Cell : Point
{
    bool passed{false};
    bool op_passed{false};
    
    
};


int main()
{
    int width;
    int height;
    int myId;
    cin >> width >> height >> myId; cin.ignore();
    for (int i = 0; i < height; i++) {
        string line;
        getline(cin, line);
    }

    // Write an action using cout. DON'T FORGET THE "<< endl"
    // To debug: cerr << "Debug messages..." << endl;

    cout << "7 7" << endl;

    // game loop
    while (1) {
        int x;
        int y;
        int myLife;
        int oppLife;
        int torpedoCooldown;
        int sonarCooldown;
        int silenceCooldown;
        int mineCooldown;
        cin >> x >> y >> myLife >> oppLife >> torpedoCooldown >> sonarCooldown >> silenceCooldown >> mineCooldown; cin.ignore();
        
        string sonarResult;
        cin >> sonarResult; cin.ignore();
        
        string opponentOrders;
        getline(cin, opponentOrders);

        // Write an action using cout. DON'T FORGET THE "<< endl"
        // To debug: cerr << "Debug messages..." << endl;

        cout << "MOVE N TORPEDO" << endl;
    }
}