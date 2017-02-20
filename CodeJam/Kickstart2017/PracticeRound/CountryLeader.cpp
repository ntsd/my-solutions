#include <iostream>  // includes cin to read from stdin and cout to write to stdout
#include <set>
#include <string>
#include <cstring>


using namespace std;  // since cin and cout are both in namespace std, this saves some text

string input;
string str;
string leader;
int maxAlpha, newAlpha;
int t, num;

int countUnique(string str) {
   int ch[30];
   memset(ch, 0, sizeof ch);
   for (int i = 0; i < str.size(); i++) {
      if (str[i] != ' ')ch[str[i]-'A']++;
   }
   int ret = 0;
   for (int i = 0; i < 26; i++) {
      if (ch[i] > 0) ret++;
   }
   return ret;
}

string countryLeader(int num){
    getline(cin, input);
    leader = input;
    maxAlpha = 0;
    for(int n = 0; n < num; n++){
        getline(cin, input);
        newAlpha = countUnique(input);
        if (newAlpha == maxAlpha) {
            if (input < leader) leader = input;
        }
        else if(newAlpha > maxAlpha){
            maxAlpha = newAlpha;
            leader = input;
        }
    }
    return leader;
}

int main() {
  cin >> t;  // read t. cin knows that t is an int, so it reads it as such.
  for (int i = 1; i <= t; ++i) {
    cin >> num;  // read n and then m.
    cout << "Case #" << i << ": " << countryLeader(num) << endl;
    // cout knows that n + m and n * m are ints, and prints them accordingly.
    // It also knows "Case #", ": ", and " " are strings and that endl ends the line.
  }
}
