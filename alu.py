# TODO: Finish implementing the rest of the Instructions
# TODO: Test for LSL and LSR
# TODO: Review that the ALU only fetches one instruction from the PreALUBuff per clock cycle


class ALU:

    def __init__(self, R, postALUBuff, preALUBuff, opcodeStr, arg1, arg2, arg3):
        self.R = R
        self.postALUBuff = postALUBuff
        self.preALUBuff = preALUBuff
        self.opcodeStr = opcodeStr
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

    def run(self):
        print("Running ALU")
        i = self.preALUBuff[0]
        if i != -1:
            if self.opcodeStr[i] == "ADD":
                self.postALUBuff[0] = self.R[self.arg1[i]] + self.R[self.arg2[i]]
                self.postALUBuff[1] = i
            elif self.opcodeStr[i] == "SUB":
                self.postALUBuff[0] = self.R[self.arg1[i]] - self.R[self.arg2[i]]
                self.postALUBuff[1] = i
            elif self.opcodeStr[i] == "AND":
                self.postALUBuff[0] = self.R[self.arg1[i]] & self.R[self.arg2[i]]
                self.postALUBuff[1] = i
            elif self.opcodeStr[i] == "ORR":
                self.postALUBuff[0] = self.R[self.arg1[i]] | self.R[self.arg2[i]]
                self.postALUBuff[1] = i
            elif self.opcodeStr[i] == "ADDI":
                self.postALUBuff[0] = self.R[self.arg1[i]] + self.arg3[i]
                self.postALUBuff[1] = i
            elif self.opcodeStr[i] == "SUBI":
                self.postALUBuff[0] = self.R[self.arg1[i]] - self.arg3[i]
                self.postALUBuff[1] = i
            elif self.opcodeStr[i] == "MOVZ":
                self.R[self.arg2[i]] = 0
                self.postALUBuff[0] = self.R[self.arg3[i]] * self.arg1[i]
                self.postALUBuff[1] = i
            elif self.opcodeStr[i] == "MOVK":
                self.postALUBuff[0] = self.R[self.arg2[i]] + (self.R[self.arg3[i]] * self.arg1[i])
                self.postALUBuff[1] = i
            elif self.opcodeStr[i] == "LSR":
                self.postALUBuff[0] = (self.R[self.arg2[i]] % (1 << 32) >> self.arg1[i])
                self.postALUBuff[1] = i
            elif self.opcodeStr[i] == "LSL":
                self.postALUBuff[0] = self.R[self.arg1[i]] << self.arg2[i]
                self.postALUBuff[1] = i
            elif self.opcodeStr[i] == "EOR":
                self.postALUBuff[0] = self.R[self.arg1[i]] ^ self.R[self.arg2[i]]
                self.postALUBuff[1] = i
            elif self.opcodeStr[i] == "ASR":
                self.postALUBuff[0] = self.R[self.arg1[i]] >> self.arg2[i]
                self.postALUBuff[1] = i

            self.preALUBuff[0] = self.preALUBuff[1]
            self.preALUBuff[1] = -1



