#include <iostream>
#include <cmath>
#include <string>
using namespace std;

int main() {
    int loop;
	cin>>loop;
	for (int i = 1; i < loop+1; i++) {
	    string str;
	    cin>>str;
        //getline (cin, str);
        string ans;
        int mode = 0;
        for(char& c : str){
            if(c=='X'){
                mode = 3;
                break;
            }
            else if(c=='T'){
                mode = 2;
            }
            else if(c=='-' && mode == 0){
                mode = 1;
            }
        }
        if(mode == 0)ans = "Yes";
        if(mode == 3)ans = "No - Runtime error";
        if(mode == 2)ans = "No - Time limit exceeded";
        if(mode == 1)ans = "No - Wrong answer";
	    cout<<"Case #"<<i<<": "<<ans<<endl;
	}
	return 0;
}

