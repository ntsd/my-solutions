import java.util.*;
class Player{
    public static int main(String[]b){
        Scanner i=new Scanner(System.in);
        int x=i.nextInt(),y=i.nextInt(),a=i.nextInt(),s=i.nextInt();
        for(;;){
            String S="";
            if(y>s++)S+="S";
            if(x>a++)S+="E";
            if(x<--a)S+="W";
            System.out.println(S);
        }
    }
}
