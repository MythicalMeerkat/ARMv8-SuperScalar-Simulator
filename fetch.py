# TODO: Finish implementing this

from helpers import SetUp


class Fetch:

    def __init__(self, instructions, opcodeStr, dataval, address, arg1, arg2, arg3, numInstructions, destReg,
                 src1Reg, src2Reg, R, preIssueBuff, preMemBuff, postMemBuff, preALUBuff,
                 postALUBuff, PC, cache):
        self.instructions = instructions
        self.opcodeStr = opcodeStr
        self.dataval = dataval
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.numInstructions = numInstructions
        self.destReg = destReg
        self.src1Reg = src1Reg
        self.src2Reg = src2Reg
        self.R = R
        self.preIssueBuff = preIssueBuff
        self.preMemBuff = preMemBuff
        self.postMemBuff = postMemBuff
        self.preALUBuff = preALUBuff
        self.postALUBuff = postALUBuff
        self.cache = cache
        self.PC = PC

    def incrementPC(self):
        self.PC = self.PC + 4

    def run(self):
        print("Fetching")
        #  Find and Fetch two empty slots in the pre issue buffer. We will send instructions to these slots
        slot1 = -2
        slot2 = -2
        slot1Filled = False
        slot2Filled = False

        for x in range(2):
            for i in range(len(self.preIssueBuff)):
                if self.preIssueBuff[i] == -1:
                    if slot1 == -2 and not slot1Filled:
                        slot1 = i
                        slot1Filled = True
                    elif slot2 == -2 and not slot2Filled:
                        slot2 = i
                        slot2Filled = True
            #  We were able to find a slot to send info too
            if slot1Filled:
                # Get an instruction and check if it is in the cache
                # index = SetUp.getIndexOfMemAddress(self.PC, True, self.dataval, self.address, self.numInstructions)
                index = int((self.PC - 96) / 4)
                Hit = self.cache.checkCache(-1, index, False, 0) # THIS ISN'T WORKING. WHY?
                if Hit[0]:
                    if self.opcodeStr[index] == "CBZ" or self.opcodeStr[index] == "CBNZ":
                        # TODO: Somehow check if there as a Hazard
                        hazard = False
                        if hazard:
                            pass
                        else:
                            self.preIssueBuff[slot1] = index
                    elif self.opcodeStr[index] == "B":
                        self.preIssueBuff[slot1] = index
                    elif self.opcodeStr[index] == "BREAK":
                        # TODO: Perform clean up and make sure the rest of the instructions are handled
                        return False
                    else:
                        self.preIssueBuff[slot1] = index
                else:
                    return True
            """"
            if slot2Filled:
                # Get an instruction and check if it is in the cache
                # index = SetUp.getIndexOfMemAddress(self.PC, True, self.dataval, self.address, self.numInstructions)
                index = int((self.PC + 4 - 96) / 4)
                Hit = self.cache.checkCache(-1, index, False, 0)  # THIS ISN'T WORKING. WHY?
                if Hit[0]:
                    if self.opcodeStr[index] == "CBZ" or self.opcodeStr[index] == "CBNZ":
                        # TODO: Somehow check if there as a Hazard
                        hazard = False
                        if hazard:
                            pass
                        else:
                            self.preIssueBuff[slot2] = index
                    elif self.opcodeStr[index] == "B":
                        self.preIssueBuff[slot2] = index
                    elif self.opcodeStr[index] == "BREAK":
                        # TODO: Perform clean up and make sure the rest of the instructions are handled
                        return False
                    else:
                        self.preIssueBuff[slot2] = index
            """
        self.PC += 4
        return True

