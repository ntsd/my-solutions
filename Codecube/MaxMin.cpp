#include <iostream>
#include <cmath>
#include <string>
using namespace std;

int main() {
    int loop;
	cin>>loop;
	long long max_=0;
	long long min_=9223372036854775807;
	for (int i = 1; i < loop+1; i++) {
	    long long num;
	    cin>>num;
        if(num > max_){
                max_ = num;
        }if(num < min_){
            min_ = num;
        }

	}
	cout<<max_<<endl;
	cout<<min_<<endl;
	return 0;
}
