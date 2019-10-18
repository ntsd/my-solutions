a='Two Turtle Doves, and'
b='Three French Hens,'
c='Four Calling Birds,'
d='Five Gold Rings,'
e='Six Geese-a-Laying,'
f='Seven Swans-a-Swimming,'
g='Eight Maids-a-Milking,'
h='Nine Ladies Dancing,'
i='Ten Lords-a-Leaping,'
j='Eleven Pipers Piping,'
k=lambda x:f'On the {x} day of Christmas'
x="My true love sent to me"
y="A Partridge in a Pear Tree.\n"
z=f"""{b}
{a}
{y}
"""
print(*[k('First'),x,y,k('Second'),x,a,y,k('Third'),x,z+k('Fourth'),x,c,z+k('Fifth'),x,d,c,z+k('Sixth'),x,e,d,c,z+k('Seventh'),x,f,e,d,c,z+k('Eighth'),x,g,f,e,d,c,z+k('Ninth'),x,h,g,f,e,d,c,z+k('Tenth'),x,i,h,g,f,e,d,c,z+k('Eleventh'),x,j,i,h,g,f,e,d,c,z+k('Twelfth'),x,'Twelve Drummers Drumming,',j,i,h,g,f,e,d,c,b,a,y],sep='\n')