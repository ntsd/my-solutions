for([x,y,a,b]=readline().split` `;;){s="";if(y>+b)s+="S";b++;if(x>+a)s+="E";if(x<+a)s+="W";print(s)}

for([x,y,a,b]=readline().split` `;;){s="";if(y>+b++)s+="S";if(x>+a)s+="E";if(x<+a)s+="W";print(s)}

for([x,y,a,b]=readline().split` `;;)s="",y>+b++&&(s+="S"),x>+a&&(s+="E"),x<+a&&(s+="W"),print(s)

for([x,y,a,b]=readline().split` `;;)print((y>+b++&&'S'||'')+(x!=a&&'WE'[+(x>+a)]||''))
