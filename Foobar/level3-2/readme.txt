You're so close to destroying the LAMBCHOP doomsday device you can taste it! 
But in order to do so, you need to deploy special self-replicating bombs designed for you 
by the brightest scientists on Bunny Planet. There are two types: Mach bombs (M) and Facula bombs (F). 
The bombs, once released into the LAMBCHOP's inner workings, 
will automatically deploy to all the strategic points you've identified and destroy them at the same time. 

But there's a few catches. First, the bombs self-replicate via one of two distinct processes: 
Every Mach bomb retrieves a sync unit from a Facula bomb; for every Mach bomb, a Facula bomb is created;
Every Facula bomb spontaneously creates a Mach bomb.

For example, if you had 3 Mach bombs and 2 Facula bombs,
they could either produce 3 Mach bombs and 5 Facula bombs,
or 5 Mach bombs and 2 Facula bombs. The replication process can be changed each cycle. 

Second, you need to ensure that you have exactly the right number of Mach and Facula bombs to destroy the LAMBCHOP device.
Too few, and the device might survive. Too many,
and you might overload the mass capacitors and create a singularity at the heart of the space station - not good! 

And finally, you were only able to smuggle one of each type of bomb - one Mach,
one Facula - aboard the ship when you arrived, so that's all you have to start with.
(Thus it may be impossible to deploy the bombs to destroy the LAMBCHOP, but that's not going to stop you from trying!) 

You need to know how many replication cycles (generations)
it will take to generate the correct amount of bombs to destroy the LAMBCHOP. Write a function solution(M, F)
where M and F are the number of Mach and Facula bombs needed. Return the fewest number of generations (as a string)
that need to pass before you'll have the exact number of bombs necessary to destroy the LAMBCHOP,
or the string "impossible" if this can't be done! M and F will be string representations of positive integers no larger than 10^50
 For example, if M = "2" and F = "1", one generation would need to pass, so the solution would be "1".
 However, if M = "2" and F = "4", it would not be possible.

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution('2', '1')
Output:
    1

1 1
2 1

Input:
Solution.solution('4', '7')
Output:
    4

1 1
2 1
3 1
3 4
4 7

(1, 1)
1 generations: (1, 2) | (2, 1)
2 generations: (3, 2) (1, 3) | (3, 1) (2, 3)
possible M+F: 5
3 generations: (5, 2) (3, 5) (4, 3) (1, 4) | (4, 1) (3, 4) (5, 3) (2, 5)
possible M+F: 7, 8
4 generations: (7, 2) (5, 7) (8, 5) (3, 8) (4, 7) (7, 3) (5, 4) (1, 5) | ...
possible M+F: 9, 10, 11, 12, 13
5 generations: (9, 2) (7,9) (12, 7) (5, 12) (13, 5) (8, 13) (11, 8) (3, 11) (11, 7) (4, 11) (10, 3) (7, 10) (9, 4) (5, 9) (6, 5) (1, 6)
possible M+F: 11, 16, 19, 17, 18, 21, 19, 14
possible M-f: 7, 2, 5, 7, 8, 5, 3, 8, 4



fist we find minimum number 
for example 
min 2 = gen;pos max | 2; 3 | 3;5 | 4;7 | 5;9
min 3 = gen;pos max | 3; (4, 5) | 4;(7, 8) | 5;(10, 11) | 6;(13, 14)
min 4 = gen;pos max | 4; (5, 6, 7) | 5; (9, 10, 11) | 6; (13, 14, 15) | 7; (17, 18, 19)
min 5 = gen;pos max | 4; (7, 8) | 5; (6, 9, 12, 13)

(max / min) + min

f(min, max) = g, when (max / min) + min - 1

possible pair number 2^n
maximum bomb number (Fibonacci) 1, 2, 3, 5, 8, 13, 21
minimum bomb number always 1
why (4, 2) (4, 8) (3, 6) (2, 6) ans only pair with not devisable except pair with 1 

-- Python cases --
Input:
solution.solution('4', '7')
Output:
    4

Input:
solution.solution('2', '1')
Output:
    1

Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.