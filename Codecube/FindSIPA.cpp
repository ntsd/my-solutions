#include <iostream>
#include <cmath>
#include <string>
using namespace std;

int main() {

	string f = "sipa";

	string s;
	getline (cin, s);
	int len = s.length();

	int flag[len + (int)ceil(len / 2)];

	int count_ = 0, j, k = 0;

	for (int i = 0; i < len - 3; i++) {
		for (j = i; j <= i + 3; j++) {
			if (tolower(s[j]) != f[j - i])
				break;
		}
		if (j > i + 3) {
			count_++;
			flag[k] = i;
			flag[k + 1] = i + 4;
			k += 2;
		}
	}

	k = 0;
	int i;
	for (i = 0; i < len; i++) {
		while (i == flag[k] && len >3) {
			cout << "\"";
			k++;
		}
		cout << s[i];
	}
	if (i == flag[k])
		cout << "\"";

	cout << "\n" << count_;

	return 0;
}
