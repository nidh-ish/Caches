# Caches

About :

A direct mapped cache of size 256kilobytes. Block size: 4 bytes. 32 bit address.
A 4-way Set associative cache of the same size (256kB).

To report the hit/miss rates of the two caches for the input memory trace files (5 traces) provided.

To run the code :

  1. Make sure you are in the directory where all the five trace files are present along with the files DMCache.py and SACache.py.
  2. Now execute the following commands for Direct mapped cache, 
              
              python3 DMCache.py in the terminal.
 
  3. Now execute the following commands for 4-Way Set Associative cache, 
        
              python3 SACache.py in the terminal.
 

Replacement policy used:

Randomized replacement policy has been used in this code. The hit/miss rates for 4-way Set Associative Cache has been generated using random function. So, we may not get the same number of hits/miss, next time the program is run.


Observation:

1. gcc.trace

Clearly, we can see that the hit rate for set associatve cache is more than that of direct mapped cache.

2. gzip.trace

Clearly, we can see that the hit rate for set associatve cache is equal to that of direct mapped cache.

3. mcf.trace

Clearly, we can see that the hit rate for set associatve cache is more than that of direct mapped cache.

4. swim.trace

Clearly, we can see that the hit rate for set associatve cache is more than that of direct mapped cache.

5. twolf.trace

Clearly, we can see that the hit rate for set associatve cache is more than that of direct mapped cache.


Remarks: 

From the above data, we see that, in most of the cases, the hit rate has increased in the 4-Way Set Associative Cache as compared to the Direct Mapped Cache. Well, this is obvious, as in Direct Mapped Cache, at a particular index we can store only one word, whereas in the 4-Way Set Associative Cache, at a particular index we can store 4 different words at the same time. This increases the odds of getting hits in case of 4-Way Set Associative Cache
