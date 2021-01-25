from helpers import SetUp



#Cache Control Unit
#pre - nothing
#during  - will take an address and determine whether a hit, a miss, or a miss - miss
# if hit will return the WORD
# if miss will add to just missed list
# if miss - miss will check for full, execute mem write back if needed, update cache, clear just missed
#post - updated cache and updated memory if appropriate and a true or false hit value returned
class Cache:

    tagMask = 4294967264  # -> 11111111111111111111111111100000
    setMask = 24 # -> 0000000000000000000000000011000
    justMissedList = [] # as it implies address's that resulted from cache misses


    #one lru bit for sets
    lruBit = [0,0,0,0]

    # Architecture of Cache
    # valid, dirty, tag, data, data
    # 4 sets of two blocks with two words per block.  Each block has valid, dirty, tag
    cacheSets = [ [ [0,0,0,0,0], [0,0,0,0,0] ],     # SET 0
                  [ [0,0,0,0,0], [0,0,0,0,0] ],     # SET 1
                  [ [0,0,0,0,0], [0,0,0,0,0] ],     # SET 2
                  [ [0,0,0,0,0], [0,0,0,0,0] ] ]    # SET 3

    def __init__( self,numInstructions, instructions,dataval, address ):
        self.numInstructions = numInstructions
        self.instructions = instructions
        self.dataval = dataval
        self.address = address
        self.cacheSets = [[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]]

    #flushing cache checks all of the cache blocks for being valid and dirty.  Dirty means that the block has
    #changed but memory has not been updated.  Flush updates memory with the new value and
    #then resets the dirty bit to zero
    #pre - cache blocks in any state
    #inv - checks each block sequentially in the cache and writes to mem if valid and dirty bits set
    #post - all dirty bits at zero
    @classmethod
    def flush(self):
        # write all dirty entries into memory
        for i in range( 0, 4 ):
            for j in range( 0, 2 ):
                # the record is valid and dirty
                if self.cacheSets[i][j][0] == 1 and self.cacheSets[i][j][1] == 1:
                    # write to memory
                    wbAddr =  self.cacheSets[i][j][2] #tag
                    wbAddr = (wbAddr << 5) + (i << 3)
                    # we will only have dirty cache pages for data mem, not instructions
                    if( wbAddr >= ( self.numInstructions  *4) + 96 ):
                        self.dataval[SetUp.getIndexOfMemAddress(wbAddr, False, self.dataval, self.address, self.numInstructions)]= self.cacheSets[i][j][3]
                        #self.dataval[ self.getIndexOfMemAddress(wbAddr, False) ] = self.cacheSets[i][j][3]
                    if( wbAddr+4 >= (self.numInstructions *4) + 96 ):
                        self.dataval[SetUp.getIndexOfMemAddress(wbAddr+4, False, self.dataval, self.address, self.numInstructions)] = self.cacheSets[i][j][4]
                        #self.dataval[ self.getIndexOfMemAddress(wbAddr+4, False) ] = self.cacheSets[i][j][4]
                    # reset dirty bit
                    self.cacheSets[i][j][1] = 0


    def checkCache( self, dataIndex, instructionIndex, isWriteToMem, dataToWrite ):
        # isWritetoMem is aligned with isSW in the mem unit! data to write also comes from there
        # check the cache, if it is there, then we return true
        # otherwise, return a false and set up for next cycle

        # calculate the address from instruction index and base address
        #################### instruction or data??? ######################
        if( dataIndex == -1):
            #it is an instruction we are getting the address for
            addressLocal = 96 + ( 4 * instructionIndex ) # correct

            #if its a data location do this
        else:
            addressLocal = 96 + (4 *  (self.numInstructions) ) + (4 * dataIndex)

        # We are double word aligning so we need to make sure that the address of block 0 is always 96 or 96 + n8
        # 96, 104, 112 ......
        # this is critical since everything else assumes that block 0 is address1
        ################################## ALIGNMENT CHECK - generate addres for both words ##################################
        if addressLocal % 8 == 0:
            dataWord = 0 # block 0 was the address
            address1 = addressLocal
            address2 = addressLocal + 4

        #check for "alignment"
        # this picks the second word as address so we need to fix it
        # set address1 - block 1 address to address - 4
        if addressLocal % 8 != 0:
            dataWord = 1 # block 1 was the address
            address1 = addressLocal - 4
            address2 = addressLocal

        ############################ Deal with instruct/mem boundry ################################
        # if address1 is an instruction go to instruction list and get it
        if address1 < 96 + ( 4 * self.numInstructions ):   # cant use dataIndex because aligning might have bridged boundry!
            data1 = self.instructions[SetUp.getIndexOfMemAddress(address1, False, self.dataval, self.address, self.numInstructions)]
        #if data, go to the data memory and get the data
        else:
            data1 = self.dataval[SetUp.getIndexOfMemAddress(address1, False, self.dataval, self.address, self.numInstructions)]
        # same process for address 2
        if address2 < 96 + ( 4 *  self.numInstructions ):
            data2 = self.instructions[SetUp.getIndexOfMemAddress(address2, False, self.dataval, self.address, self.numInstructions)]
        else:
            if address2 <= (96 + ( 4 *  self.numInstructions ) + (4 * (len(self.dataval)-1))):
                data2 = self.dataval[SetUp.getIndexOfMemAddress(address2, False, self.dataval, self.address, self.numInstructions)]
            else:
                data2 = 0

        ###########################  WRITING TO MEMORY only one word! ##########################
        # if we are going to write to mem select which word it is. Don't write both
        # we will only be writing data to memory - not instructions
        # set the appropriate write element to the passed in data
        if isWriteToMem and dataWord == 0:
            data1 = dataToWrite
        elif isWriteToMem and dataWord == 1:
            data2 = dataToWrite


        # Architecture of Cache Sets [0,1,2,3,4]
        # [valid, dirty, tag, data, data]

        ##################  Check Cache #############################

        ##### DECODE THE CACHE ADDRESS FROM THE address for WORD0
        #####
        # get the tag and the set number based on the mem address
        #TODO make sure this binary op is working right !!!!!


        setNum = (address1 & self.setMask) >> 3
        tag = (address1 & self.tagMask) >> 5



        hit = False # initialize hit

        # look in the cache.
        #####################  check the valid bit  AND check the tag   #####################
        #figure out which block has the info or not.  It might not be there
        if( self.cacheSets[setNum][0][0] == 1 and self.cacheSets[setNum][0][2] == tag ):
            # we have a hit
            hit = True
            assocblock = 0   # block zero is the hit
        # look at the other associative block
        elif self.cacheSets[setNum][1][0] == 1 and self.cacheSets[setNum][1][2] == tag:
            # we have a hit
            hit = True
            assocblock = 1  # block 1 is the hit

        # if we have a hit, update the LRU and dirty bit if a data write
        # and return
        if( hit ):
            if hit and isWriteToMem:
                # update the dirty bit if we are going to be writing to cache - should only be to data not to instructs
                # TODO add check to make sure it is a data write and crash nice if some error occurs
                self.cacheSets[setNum][assocblock][1] = 1  # dirty bit

                # if the block hit in set was block zero, write the set LRU bit a 1, if block 1 write set lru bit to 0
                # default for lru bit is zero so same as block 1 hit
                self.lruBit[setNum] = (assocblock + 1) % 2 # lru bit -
                self.cacheSets[setNum][assocblock][dataWord+3] = dataToWrite  # +3 offsets to correct word element

            #if was an instruction hit or a non write to data mem
            elif hit:
                self.lruBit[setNum] = (assocblock + 1) % 2
            #returns a true we got a hit and the data or instruction in the specific dataword. Data word specifies
            #either the first or second word in a block based on what the instruction was.
            return [True, self.cacheSets[setNum][assocblock][dataWord+3] ] # the +3 is to point to either [4] or [5]



        # if we get here, we have a CACHE MISS

        # First check to see if we had a miss for this address in the previous cycle so we can update the cache with
        #the data in the requested mem address and allow the instruction to proceed
        # if we tried to get this address in the previous cycle
        # and had a cache miss, its address is in the JustMissedlist
        # therefore, we have waited one cycle, and now need to
        # perform the memory operation

        if address1 in self.justMissedList:
            # remove the address from the list - reset
            while(self.justMissedList.count( address1 ) > 0 ):
                self.justMissedList.remove( address1 )

            if isWriteToMem:
                if dataWord == 0:
                    data = data1
                else:
                    data = data2


                # Architecture of Cache
                # valid, dirty, tag, data, data
                # 4 sets of two blocks with two words per block.  Each block has valid, dirty, tag
                #cacheSets = [[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]]

            # now add to the the cache
            # check the set number, block number based on lru bit setting, and dirty bit for the block number: if dirty bit is 1 we got a data
            # if the block in the set in cache we want to write to is dirty we will write data words in that block to memory
            # if the lru bit for the set is zero, the set /  blocks could be empty. If so then blocks dirty bit will certainly be 0
            # if the dirty bit is 1 then fine, write back both words in block. But it is also possible that block 1 is dirty. SO write it back.   If the lru bit is 1, then certainly the set/block is not empty and it is
            # possible that block zero's dirty bit is 1. Then write back.
            #NOTE: we are getting the tag associated with the block that is being written back and set but we will write both blocks
            # back if both blocks are on the data side.  Takes care of the case where you are across the boundry.

            if self.cacheSets[setNum][ self.lruBit[setNum] ][1] == 1:
                # write back the memory address asociated with the block
                wbAddr =  self.cacheSets[setNum][ self.lruBit[setNum] ][2] #tag
                # modify tag to get back to the original address, remember all addresses are inherently word aligned
                # lower 2 bits are zero !!!!
                wbAddr = (wbAddr << 5) +( setNum << 3)

                # we will, we better,  only have dirty cache entries for data mem, not instructions
                # update data mem locations!
                # if the cache tag: set gives us a double word aligned value ie. 96,104,
                # Lets say that word 0 is the last instruction and word one is the first data element
                # we would only want to update the second word
                # But if lets say we have two data elemeents, then the cache would have two data element and we would write
                # back both even if one was dirty.  This takes care of the boundry condition.
                if( wbAddr >= (self.numInstructions  *4) + 96 ):
                    self.dataval[ SetUp.getIndexOfMemAddress(wbAddr,False, self.dataval, self.address, self.numInstructions) ] = \
                        self.cacheSets[setNum][ self.lruBit[setNum] ][3]

                if( wbAddr+4 >= (self.numInstructions  *4) + 96 ):
                    self.dataval[ SetUp.getIndexOfMemAddress(wbAddr+4,False, self.dataval, self.address, self.numInstructions) ] = \
                        self.cacheSets[setNum][ self.lruBit[setNum] ][4]

            # now update the cache flag bits
            self.cacheSets[setNum][ self.lruBit[setNum] ][0] = 1 #valid  we are writing a block
            self.cacheSets[setNum][ self.lruBit[setNum] ][1] = 0 #reset the dirty bit
            if( isWriteToMem ):
                self.cacheSets[setNum][ self.lruBit[setNum] ][1] = 1 #dirty if is data mem is dirty again, intruction mem never dirty
            # update both words in the actual cache block in set
            self.cacheSets[setNum][ self.lruBit[setNum] ][2] = tag #tag
            self.cacheSets[setNum][ self.lruBit[setNum] ][3] = data1 #data
            self.cacheSets[setNum][ self.lruBit[setNum] ][4] = data2 #nextData
            self.lruBit[setNum] = (self.lruBit[setNum] + 1) % 2 # set lru to show block is recently used


            #finally
            return [True, self.cacheSets[setNum][(self.lruBit[setNum] + 1) % 2][dataWord+3] ]   # dataword was the actual word thatgenerated the hit


        else:
            #VALID MISS on cycle
            # add the memory address to the just missed list if its not already there
            if( self.justMissedList.count( address1 ) == 0 ):
                self.justMissedList.append( address1 )
            return [False, 0]