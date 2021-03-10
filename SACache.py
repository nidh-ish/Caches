import random                                                                 #Import random

def hextobin(hexadecimal):                                                    #This function converts a hexadecimal number to a binary number

    hexvalue = hexadecimal[2:]                                                #This ignores the '0x' part of the hexadecimal number
    integer = int(hexvalue, 16)                                               #This converts the hexadecimal to its decimal equivalent
    binary = bin(integer)                                                     #The decimal number is then converted to its binary equivalent
    return binary[2:]                                                         #The binary equivalent contains '0b' in the beginning, that is why we use string slicing to return the remaining part(the binary part)

def bin32bits(binary):                                                        #The binary number we got might or might not be 32 bits in length 
                                                                              #So, this function appends 0's if it is less than 32 and returns the 32 bit binary number
    if(len(binary) < 32) :                                                    #If the length is less than 32 
        bin32bit = '0' * (32 - len(binary)) + binary                          #We append required number of 0's in the beginning of the binary number
        return bin32bit                                                       #and return the final number
    elif(len(binary) == 32) :                                                 #If it was 32 bits initially, then we return that 
        return binary

def bintonum(binary):                                                         #This function converts binary number to its decimal equivalent

    return int(binary, 2)

def gethitmissrate(filename):                                                 #This function takes filename as the parameter
                                                                              #We read input from this file
    print("\nHit/miss rate for the file", filename, "is : \n")

    getfile = open(filename, 'r')                                             #The file is open in reading mode
    lines = getfile.readlines()                                               #We read the data from the file line by line using readlines function

    total = 0                                                                 #This counts the total number of cache operations performed

    hit = 0                                                                   #This maintains a count of the number of cache hits

    miss = 0                                                                  #This maintains a count of the number of cache misses

    cache = {}

    for i in range(16384):
        cache[i] = ['0', '0', '0', '0']                                       #Cache is declared as a dictionary here. Initially, the valid bits are zero and tag bits are empty
                                                                              #Total cache memory is 256KB, and each block is 4B, and it is a 4-way set associative cache. so there are 16384 sets/lines in the cache 
    for line in lines:                                                        #We iterate line by line

        total = total + 1                                                     #Each time total is incresed by one

        line = line.rstrip('\n')                                              #Each line contains a newline character at the end, so we remove that using rstrip
        line = line.split(" ")                                                #Now, we split the line by spaces and now it is stored as a list
                                                                              #Example of the list - ["l", "0x1fffff90", "2"]
        address = line[1]                                                     #The only thing we need to worry about to calculate hit/miss is the address in the line which is stored in the second position in the list
        address_bits= hextobin(address)                                       #Now we convert the hexadecimal address to binary using the function we created above

        bin32bit = bin32bits(address_bits)                                    #Now using bin32bits function we make sure that the binary is 32 bits in length
                                                                              #Last 2 bits in the 32 bits is the byte-offset
        index_bits = bin32bit[16:30]                                          #Now since the number of sets in the cache is 16384 = 2^14, so the index bit becomes 14 bits wide

        tag_bits = bin32bit[:16]                                              #And the remaining bits, i.e., 16 bits becomes the tag bits

        index = bintonum(index_bits)                                          #Now, we convert the index bits to its decimal equivalent

#Now, since this is a 4-way set associative cache, at a particular index, a tag bits has four ways to be stored. So, multiple cases are formed accordingly.

        if(cache[index][0][0] == '0' and cache[index][1][0] == '0' and cache[index][2][0] == '0' and cache[index][3][0] == '0'):     #If all the blocks of the index are empty
                                                                                                                         #That is valid bit of every block is zero
            miss = miss + 1                                                                                              #This is counted as a miss
            x = random.choice([0, 1, 2, 3])                                                                              #The tag bit can now bre stored in any of the 4 blocks, we pick a random block using random
            cache[index][x] = "1" + tag_bits                                                                             #Make the tag bit as 1, and store the tag bit in that block of the index

#If, one of the block is filled(valid bit is 1)
#Now, here we get four different cases, if the first block is filled, if the second block is filled, if the third block is filled, or if the fourth block is filled

        elif(cache[index][0][0] == '1' and cache[index][1][0] == '0' and cache[index][2][0] == '0' and cache[index][3][0] == '0'):   #This cases checks if the valid bit of first block is 1 and that of the rest of the blocks is 0
 
            if(cache[index][0][1:] == tag_bits):                                                                         #Here if the first block contains the tag bit, then it is a hit

                hit = hit + 1

            else:                                                                                                        #Else, out of the remaining three blocks, we chose a random block and place the tag bit there

                x = random.choice([1, 2, 3])                                                                             #And make the valid bit 1, and count it as a miss
                cache[index][x] = "1" + tag_bits
                miss = miss + 1

        elif(cache[index][0][0] == '0' and cache[index][1][0] == '1' and cache[index][2][0] == '0' and cache[index][3][0] == '0'):   #This cases checks if the second block is filled and rest are empty

            if(cache[index][1][1:] == tag_bits):                                                                                     #We follow similar steps as above

                hit = hit + 1

            else:

                x = random.choice([0, 2, 3])
                cache[index][x] = "1" + tag_bits
                miss = miss + 1

        elif(cache[index][0][0] == '0' and cache[index][1][0] == '0' and cache[index][2][0] == '1' and cache[index][3][0] == '0'):   #This cases checks if the third block is filled and rest are empty

            if(cache[index][2][1:] == tag_bits):                                                                                     #We follow similar steps as above

                hit = hit + 1

            else:

                x = random.choice([0, 1, 3])
                cache[index][x] = "1" + tag_bits
                miss = miss + 1

        elif(cache[index][0][0] == '0' and cache[index][1][0] == '0' and cache[index][2][0] == '0' and cache[index][3][0] == '1'):   #This cases checks if the third block is filled and rest are empty

            if(cache[index][3][1:] == tag_bits):                                                                                     #We follow similar steps as above

                hit = hit + 1

            else:

                x = random.choice([0, 1, 2])
                cache[index][x] = "1" + tag_bits
                miss = miss + 1

#If two blocks are filled(valid bit of two blocks is 1)
#Now, here we get six different cases as mentioned below

        elif(cache[index][0][0] == '1' and cache[index][1][0] == '1' and cache[index][2][0] == '0' and cache[index][3][0] == '0'):  #This case checks if the first and second blocks are filled
                                                                                                                                    #That is, their valid bit is 1
            if(cache[index][0][1:] == tag_bits or cache[index][1][1:] == tag_bits):                                                 #We check if the content of any of the filled block is equal to the tag bit

                hit = hit + 1                                                                                                       #If it is, then it is a hit

            else:                                                                                                                   #Else, it is a miss

                x = random.choice([2, 3])                                                                                           #And out of the remaining two unfilled blocks, we chose one using random
                cache[index][x] = "1" + tag_bits                                                                                          #And store the tag bit there, and make the tag bit 1
                miss = miss + 1

        elif(cache[index][0][0] == '1' and cache[index][1][0] == '0' and cache[index][2][0] == '1' and cache[index][3][0] == '0'):  #This case checks if the first and third blocks are filled

            if(cache[index][0][1:] == tag_bits or cache[index][2][1:] == tag_bits):                                                #We follow similar steps as above

                hit = hit + 1

            else:

                x = random.choice([1, 3])
                cache[index][x] = "1" + tag_bits
                miss = miss + 1

        elif(cache[index][0][0] == '1' and cache[index][1][0] == '0' and cache[index][2][0] == '0' and cache[index][3][0] == '1'):  #This case checks if the first and fourth blocks are filled 

            if(cache[index][0][1:] == tag_bits or cache[index][3][1:] == tag_bits):                                                 #We follow similar steps as above 

                hit = hit + 1

            else:

                x = random.choice([1, 2])
                cache[index][x] = "1" + tag_bits
                miss = miss + 1

        elif(cache[index][0][0] == '0' and cache[index][1][0] == '1' and cache[index][2][0] == '1' and cache[index][3][0] == '0'):  #This case checks if the second and third blocks are filled
                                                                                        
            if(cache[index][1][1:] == tag_bits or cache[index][2][1:] == tag_bits):                                                 #We follow similar steps as above            

                hit = hit + 1

            else:

                x = random.choice([0, 3])
                cache[index][x] = "1" + tag_bits
                miss = miss + 1

        elif(cache[index][0][0] == '0' and cache[index][1][0] == '1' and cache[index][2][0] == '0' and cache[index][3][0] == '1'):  #This case checks if the second and fourth blocks are filled

            if(cache[index][1][1:] == tag_bits or cache[index][3][1:] == tag_bits):                                                 #We follow similar steps as above

                hit = hit + 1

            else:

                x = random.choice([0, 2])
                cache[index][x] = "1" + tag_bits
                miss = miss + 1

        elif(cache[index][0][0] == '0' and cache[index][1][0] == '0' and cache[index][2][0] == '1' and cache[index][3][0] == '1'):  #This case checks if the third and fourth blocks are filled

            if(cache[index][2][1:] == tag_bits or cache[index][3][1:] == tag_bits):                                         #We follow similar steps as above                

                hit = hit + 1

            else:

                x = random.choice([0, 1])
                cache[index][x] = "1" + tag_bits
                miss = miss + 1

#If three blocks are filled(valid bit of three blocks is 1)
#Now, here we get 4 different cases as mentioned below

        elif(cache[index][0][0] == '1' and cache[index][1][0] == '1' and cache[index][2][0] == '1' and cache[index][3][0] == '0'):  #This case checks if the first, second and third blocks are filled
                                                                                                                                    #That is their valid bit is 1
            if(cache[index][0][1:] == tag_bits or cache[index][1][1:] == tag_bits or cache[index][2][1:] == tag_bits):              #We check if the content of any of the filled block is equal to the tag bit

                hit = hit + 1                                                                                                       #If it is, then it is a hit

            else:                                                                                                                   #Else, it is a miss

                cache[index][3] = "1" + tag_bits                                                                                    #And we store the tag bit in the only unfilled block, and make the valid bit 1
                miss = miss + 1

        elif(cache[index][0][0] == '1' and cache[index][1][0] == '1' and cache[index][2][0] == '0' and cache[index][3][0] == '1'):  #This case checks if the first, second and fourth blocks are filled

            if(cache[index][0][1:] == tag_bits or cache[index][1][1:] == tag_bits or cache[index][3][1:] == tag_bits):          #We follow similar steps as above

                hit = hit + 1

            else:

                cache[index][2] = "1" + tag_bits
                miss = miss + 1

        elif(cache[index][0][0] == '1' and cache[index][1][0] == '0' and cache[index][2][0] == '1' and cache[index][3][0] == '1'):  #This case checks if the first, third and fourth blocks are filled

            if(cache[index][0][1:] == tag_bits or cache[index][2][1:] == tag_bits or cache[index][3][1:] == tag_bits):              #We follow similar steps as above

                hit = hit + 1

            else:

                cache[index][1] = "1" + tag_bits
                miss = miss + 1

        elif(cache[index][0][0] == '0' and cache[index][1][0] == '1' and cache[index][2][0] == '1' and cache[index][3][0] == '1'):  #This case checks if the second, third and fourth blocks are filled 

            if(cache[index][1][1:] == tag_bits or cache[index][2][1:] == tag_bits or cache[index][3][1:] == tag_bits):              #We follow similar steps as above

                hit = hit + 1

            else:

                cache[index][0] = "1" + tag_bits
                miss = miss + 1

#If all 4 blocks are filled(valid bit of every block is 1)

        elif(cache[index][0][0] == '1' and cache[index][1][0] == '1' and cache[index][2][0] == '1' and cache[index][3][0] == '1'):

            if(cache[index][0][1:] == tag_bits or cache[index][1][1:] == tag_bits or cache[index][2][1:] == tag_bits or cache[index][3][1:] == tag_bits):  #We check if any of the filled blocks is equal to the tag bit

                hit = hit + 1                                                                                                                              #If it is, then we increase the hit rate

            else:

                x = random.choice([0, 1, 2, 3])                                                                                                            #We pick one random block and replace its content with the tag bit
                cache[index][x] = "1" + tag_bits                                                                                                           #Valid bit is made 1 
                miss = miss + 1                                                                                                                            #And it is counted as a miss 

    getfile.close()                                                                                                                        #After going through the complete file, we close the file 
       
    for i in range(16384):                                                                                                                 #Emptying the cache contents 
        cache[i] = ['0', '0', '0', '0'] 

    print("Hits      : ", hit)                                                                                                             #We print the number of cache hits
    print("Misses    : ", miss)                                                                                                            #We print the number of cache misses
    print("Hit rate  : ", hit/total)                                                                                                       #We print the hit rate of the cache
    print("Miss rate : ", miss/total)                                                                                                      #We print the miss rate of the cache


gethitmissrate('gcc.trace')                                                                                                                #Now we call the above function for all the given 5 input files one by one
gethitmissrate('gzip.trace')
gethitmissrate('mcf.trace')
gethitmissrate('swim.trace')
gethitmissrate('twolf.trace')
print()                                                                                                                                    #print a newline at the end
