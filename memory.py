# TODO: Finish implementing this


class Memory:

    def __init__(self, R, postMemBuff, preMemBuff, opcodeStr, arg1, arg2, arg3, dataval, address, numInstructions, cache, cycleList):
        self.R = R
        self.preMemBuff = preMemBuff
        self.postMemBuff = postMemBuff
        self.opcodeStr = opcodeStr
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.dataval = dataval
        self.address = address
        self.numInstructions = numInstructions
        self.cache = cache
        self.cycleList = cycleList

    '''
    Doohwan, for both of our sakes here is the info provided by Mr. Lakomski regarding the usage of LDUR and STUR:
    
    LDUR: 
    
    For LDUR, it takes one cycle to finish if it hits in the cache.  
    If it misses in the cache, then the operation cannot be performed and must be retried in the next cycle.  
    In this case, the operation remains in the pre-mem buffer while the needed element in memory gets moved to cache. 
    When a cache hit occurs, the operation finishes and the instruction and data will be written to the post-MEM buffer.
    
    STUR: A STUR takes one cycle to finish if there is room in the cache set. 
    If it cannot write in the cache set, then the operation cannot be performed and must be retried in the next cycle.  
    In this case, the operation remains in the pre-mem buffer.  When a cache write occurs, the STUR instruction  just finshes.  
    The STUR instruction never goes into the post-MEM buffer. It just disappears.  
    Everything gets updated in the same cycle that the write happens. 
    If the required set is full then you must figure out what to kick out on that cycle and write the cache the next cycle. 
    This may cause a stall since you are checking to see that all instructions in flight that might access the memory location have to wait.  
    A RAW hazard.
 

    As you can see I have blueprinted out the idea of the mem unit.
    

    '''

    def run(self):
        print("Digging in Memory Unit")
        isST = False
        isLD = False
        i = self.preMemBuff[0]
        if i != -1:
            if self.opcodeStr[i] == "LDUR":
                # TODO: Review slides and code the functionality for LDUR (Above)
                isLD = True
            elif self.opcodeStr[i] == "STUR":
                # TODO: Review slides and code the functionality for STUR (Above)
                isST = True
                pass
            cacheCheck = self.cache.checkCache(self.preMemBuff[0], self.preMemBuff[0], isST, self.R[self.preMemBuff[0]])
            Hit = cacheCheck[0]
            Data = cacheCheck[1]
            # Shift down the buffer and set the last slot to be empty
            if Hit:
                if isLD:
                    self.postMemBuff = [Data, i]
                    self.preMemBuff[0] = self.preMemBuff[1]
                    self.preMemBuff[1] = -1
                if isST:
                    datavalEntry = ((self.R[self.arg2[i]] + (self.arg3[i] * 4)) - (96 + (self.numInstructions * 4)))
                    self.dataval[int(datavalEntry / 4)] = self.R[self.arg1[i]]
                    self.preMemBuff[0] = self.preMemBuff[1]
                    self.preMemBuff[1] = -1


