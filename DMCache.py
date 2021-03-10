def hextobin(hexadecimal):                                           #This function converts a hexadecimal number to a binary number

    hexvalue = hexadecimal[2:]                                       #This ignores the '0x' part of the hexadecimal number
    integer = int(hexvalue, 16)                                      #This converts the hexadecimal to its decimal equivalent
    binary = bin(integer)                                            #The decimal number is then converted to its binary equivalent
    return binary[2:]                                                #The binary equivalent contains '0b' in the beginning, that is why we use string slicing to return the remaining part(the binary part)   

def bin32bits(binary):                                               #The binary number we got might or might not be 32 bits in length
                                                                     #So, this function appends 0's if it is less than 32 and returns the 32 bit binary number
    if(len(binary) < 32) :                                           #If the length is less than 32  
        bin32bit = '0' * (32 - len(binary)) + binary                 #We append required number of 0's in the beginning of the binary number
        return bin32bit                                              #and return the final number
    elif(len(binary) == 32) :                                        #If it was 32 bits initially, then we return that
        return binary

def bintonum(binary):                                                #This function converts binary number to its decimal equivalent

    return int(binary, 2)

def gethitmissrate(filename):                                        #This function takes filename as the parameter
                                                                     #We read input from this file 
    print("\nHit/miss rate for the file", filename, "is : \n")       

    getfile = open(filename, 'r')                                    #The file is open in reading mode 
    lines = getfile.readlines()                                      #We read the data from the file line by line using readlines function

    total = 0                                                        #This counts the total number of cache operations performed

    hit = 0                                                          #This maintains a count of the number of cache hits

    miss = 0                                                         #This maintains a count of the number of cache misses

    cache = ['0'] * 65536                                            #Cache is implemented as a list here, initially, the list contains 0 as the valid bit, and there is nothing stored in tag bits 
                                                                     #Total cache memory is 256KB, and each block is 4B, so there are 65536 sets/lines in the cache 
    for line in lines:                                               #We iterate line by line

        total = total + 1;                                           #Each time total is incresed by one

        line = line.rstrip('\n')                                     #Each line contains a newline character at the end, so we remove that using rstrip
        line = line.split(" ")                                       #Now, we split the line by spaces and now it is stored as a list
                                                                     #Example of the list - ["l", "0x1fffff90", "2"]
        address = line[1]                                            #The only thing we need to worry about to calculate hit/miss is the address in the line which is stored in the second position in the list
        address_bits = hextobin(address)                             #Now we convert the hexadecimal address to binary using the function we created above

        bin32bit = bin32bits(address_bits)                           #Now using bin32bits function we make sure that the binary is 32 bits in length
                                                                     #Last two bits in the 32 bits is the byte-offset 
        index_bits = bin32bit[14:30]                                 #Now since the number of sets in the cache is 65536 = 2^16, so the index bit becomes 16 bits wide

        tag_bits = bin32bit[:14]                                     #And the remaining bits, i.e., 14 bits becomes the tag bits

        index = bintonum(index_bits)                                 #Now, we convert the index bits to its decimal equivalent

        if(0 <= index < 65536):                                      #We make sure that the index bit lies in the range [0, 65536)

            if(cache[index][0] == '0'):                              #We check if the valid bit is equal to 0

                cache[index] = "1" + tag_bits                        #We store tag bit in that position, make the valid bit 1, and increase the miss rate of the cache by one
                miss = miss + 1

            elif(cache[index][0] == '1'):                            #If the valid bit is equal to 1 

                if(cache[index][1:] == tag_bits):                    #We go to that particular index in the cache memory(here a list) and check if the value stored over there is equal to tag bits or not

                    hit = hit + 1                                    #If it is, then we increase the hit rate of the cache by one 

                else:
            
                    cache[index] = "1" + tag_bits                    #Else, we store tag bit in that position and increase the miss rate of the cache by one
                    miss = miss + 1

    getfile.close()                                                  #After going through the complete file, we close the file 

    for i in range(65536):                                           #Emptying the cache contents   
        cache[i] = '0'

    print("Hits      : ", hit)                                       #We print the number of cache hits
    print("Misses    : ", miss)                                      #We print the number of cache misses
    print("Hit rate  : ", hit/total)                                 #We print the hit rate of the cache
    print("Miss rate : ", miss/total)                                #We print the miss rate of the cache

gethitmissrate('gcc.trace')                                          #Now we call the above function for all the given 5 input files one by one
gethitmissrate('gzip.trace')
gethitmissrate('mcf.trace')
gethitmissrate('swim.trace')
gethitmissrate('twolf.trace')
print()                                                              #print a newline at the end
