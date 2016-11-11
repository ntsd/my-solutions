#include<iostream>
#include <cmath>
#include <limits>
#include <stdlib.h>
using namespace std;
bool AreDoubleSame(double dFirstVal, double dSecondVal)
{
    return std::fabs(dFirstVal - dSecondVal) < std::numeric_limits<double>::epsilon();
}

int main()
{

    long double a,b,c;
    cin>>a>>b>>c;
    if(AreDoubleSame(a+b, c))
    {
        cout<<"Correct";
    }

    else
    {
        cout<<"Wrong";
    }

}
