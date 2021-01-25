# TODO: Finish implementing this

from helpers import SetUp


class Issue:

    def __init__(self, instructions, opcodeStr, dataval, address, arg1, arg2, arg3, numInstructions, destReg,
                 src1Reg, src2Reg, R, preIssueBuff, preMemBuff, postMemBuff, preALUBuff,
                 postALUBuff):
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

    def run(self):
        print("Issuing")

        numIssued = 0
        numInPreIssueBuff = 0
        issueMe = True

        if self.preIssueBuff[0] != -1:
            numInIssueAtClockCycleBegin = self.preIssueBuff[0]
            curr = 0

        for element in self.preIssueBuff:
            if element != -1:
                numInPreIssueBuff += 1

        while numIssued < 2 and numInPreIssueBuff > 0 and curr < 4:
            index = self.preIssueBuff[curr]
            if SetUp.isMemOp(self.opcodeStr[index]) and not -1 in self.preMemBuff:
                if curr > 0:
                    for i in range(0, curr):
                        if self.src1Reg[index] == self.destReg[self.preIssueBuff[i]] or self.src2Reg[index] == self.destReg[self.preIssueBuff[i]]:
                            # found RAW in pre issue buff
                            issueMe = False
                            break
                # See if there is a RAW in the pre mem buff
                for i in range(0, len(self.preMemBuff)):
                    if self.preMemBuff[i] != -1:
                        if self.src1Reg[index] == self.destReg[self.preMemBuff[i]] or self.src2Reg[index] == self.destReg[self.preMemBuff[i]]:
                            # Found Raw in pre issue buff
                            issueMe = False
                            break
                # See if there is a RAW in the pre ALU buff
                for i in range(0, len(self.preALUBuff)):
                    if self.preALUBuff[i] != -1:
                        if self.src1Reg[index] == self.destReg[self.preALUBuff[i]] or self.src2Reg[index] == self.destReg[self.preALUBuff[i]]:
                            # Found Raw in pre ALU buff
                            issueMe = False
                            break

                # see if there is a RAW in the post buffs too
                if self.postALUBuff[1] != -1:
                    if self.src1Reg[index] == self.destReg[self.postALUBuff[1]] or self.src2Reg[index] == self.destReg[self.postALUBuff[1]]:
                        # Found raw in post ALU buff
                        issueMe = False
                if self.postMemBuff[1] != -1:
                    if self.src1Reg[index] == self.destReg[self.postMemBuff[1]] or self.src2Reg[index] == self.destReg[self.postMemBuff[1]]:
                        # Found raw in post ALU buff
                        issueMe = False

                # TODO: Enforce ordering of LDUR and STUR

            # Issue:
            if issueMe:
                numIssued += 1
                # Copy the instruction into the appropriate buffer
                if SetUp.isMemOp(self.opcodeStr[index]):
                    self.preMemBuff[self.preMemBuff.index(-1)] = index
                else:
                    self.preALUBuff[self.preALUBuff.index(-1)] = index

                # Move the instrs in the preissue buff down one level
                self.preIssueBuff[0:curr] = self.preIssueBuff[0:curr]
                self.preIssueBuff[curr:3] = self.preIssueBuff[curr + 1:]
                self.preIssueBuff[3] = -1
                numInPreIssueBuff -= 1
            else:
                curr += 1





