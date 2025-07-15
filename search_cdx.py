from io import TextIOWrapper
import os
from cdx_reader import CDXReader


def getStartAndEndCursors(f:CDXReader,surt:str,mode='domain'):
    # Returns the lines from the CDX file that match the search

    linear_size = 100000 
    # Each line has ~100-5000 chars, we switch to linear search when our size goes below this threshold.
    # It makes the search much simpler, and the performance is fast enough for this size.

    f_EOF = f.getFileSize()

    # Find the first line that matches the surt:
    l = 0
    r = f_EOF

    # Binary search: 
    while r-l > linear_size: 
        f.seek((l+r)//2)
        guess = f.getNextStartOfLineCursor()

        read_line = f.readLine()
        read_surt = read_line.split(' ')[0]

        if compareSURT(read_surt,surt,mode) >= 0:
            r = guess
        else:
            l = guess 
    
    # Linear search:
    start = l
    f.seek(start)
    read_line = f.readLine()
    read_surt = read_line.split(' ')[0]
    while start < r and compareSURT(read_surt,surt,mode) != 0:
        start = f.tell()
        read_line = f.readLine()
        read_surt = read_line.split(' ')[0]

    if start >= r: #failed to find any match
        return 0,0
    

    # Find the first line that no longer matches the surt:
    l = start 
    r = f_EOF

    # Binary search
    while r-l > linear_size: 
        f.seek((l+r)//2)
        guess = f.getNextStartOfLineCursor()

        read_line = f.readLine()
        read_surt = read_line.split(' ')[0]

        if compareSURT(read_surt,surt,mode) > 0:
            r = guess
        else:
            l = guess
    
    # Linear search:
    end = l
    f.seek(end)
    read_line = f.readLine()
    read_surt = read_line.split(' ')[0]
    while end < r and compareSURT(read_surt,surt,mode) <= 0:
        end = f.tell()
        read_line = f.readLine()
        read_surt = read_line.split(' ')[0]

    return start,end




# def getPrevStartOfLineCursor(f:TextIOWrapper):
#     char = f.read(1)
#     cursor = f.tell()

#     while (char != "\n") and (cursor > 1):
#         cursor -= 1
#         f.seek(cursor-1)
#         char = f.read(1)
#     return cursor

def compareSURT(s1:str,s2:str,mode:str):
        if(mode == 'domain'):
            s1 = s1.split(')',1)[0] + ","
            s2 = s2.split(')',1)[0] + ","

        l1 = len(s1)
        l2 = len(s2)

        l = l1
        if(l2 < l1):
            l = l2
        for i in range(l):
            if(s1[i] < s2[i]):
                return -1
            elif(s1[i] > s2[i]):
                return 1
        if(l1 < l2) :
            return -1
        if(mode == 'exact'):
            if(l1 > l2):
                return 1
        return 0 