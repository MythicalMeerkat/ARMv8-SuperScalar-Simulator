import cache
import alu
import writeBack
import issue
import memory
import fetch
from helpers import SetUp

global_cycle = 0


class simClass:

    def __init__(self, instructions, opcodes, opcodeStr, dataval, address, arg1,
                 arg2, arg3, arg1Str, arg2Str, arg3Str, numInstrs, destReg,
                 src1Reg, src2Reg):
        self.instruction = instructions
        self.opcode = opcodes
        self.dataval = dataval
        self.address = address
        self.numInstructions = numInstrs
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.arg1Str = arg1Str
        self.arg2Str = arg2Str
        self.arg3Str = arg3Str
        self.destReg = destReg
        self.src1Reg = src1Reg
        self.src2Reg = src2Reg
        self.opcodeStr = opcodeStr
        self.PC = 96
        self.cycle = 1
        self.R = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.postMemBuff = [-1, -1]
        self.postALUBuff = [-1, -1]
        self.preMemBuff = [-1, -1]
        self.preALUBuff = [-1, -1]
        self.preIssueBuff = [-1, -1, -1, -1]
        self.cycleList = [0]

        # Functional Units
        self.WB = writeBack.WriteBack(self.R, self.postMemBuff, self.postALUBuff, destReg)
        self.cache = cache.Cache(numInstrs, instructions, dataval, address)
        self.ALU = alu.ALU(self.R, self.postALUBuff, self.preALUBuff, opcodeStr, arg1, arg2, arg3)
        self.MEM = memory.Memory(self.R, self.postMemBuff, self.preMemBuff, opcodeStr, arg1, arg2, arg3, dataval, address,
                                 self.numInstructions, self.cache, self.cycleList)
        self.issue = issue.Issue(instructions, opcodeStr, dataval, address, arg1, arg2, arg3, self.numInstructions, destReg,
                                 src1Reg, src2Reg, self.R, self.preIssueBuff, self.preMemBuff, self.postMemBuff, self.preALUBuff,
                                 self.postALUBuff)
        self.fetch = fetch.Fetch(instructions, opcodeStr, dataval, address, arg1, arg2, arg3, self.numInstructions, destReg,
                                 src1Reg, src2Reg, self.R, self.preIssueBuff, self.preMemBuff, self.postMemBuff, self.preALUBuff,
                                 self.postALUBuff, self.PC, self.cache)

        self.outputFileName = SetUp.get_output_filename()

    def printState(self):

        with open(self.outputFileName + "_pipeline.txt", 'a') as outFile:

            outFile.write("--------------------\n")
            outFile.write("cycle:" + str(self.cycle) + "\n")
            outFile.write("\n")

            # Buffers
            outFile.write("Pre-Issue Buffer: \n")
            for x in range(len(self.preIssueBuff)):
                outFile.write("\t Entry " + str(x) + ": ")
                if self.preIssueBuff[x] != -1:
                    outFile.write("[" + str(self.opcodeStr[self.preIssueBuff[x]])
                                  + str(self.arg1Str[self.preIssueBuff[x]]) + str(self.arg2Str[self.preIssueBuff[x]])
                                  + str(self.arg3Str[self.preIssueBuff[x]]) + "] \n")
                else:
                    outFile.write("\n")
            outFile.write("Pre_ALU Queue: \n")
            for x in range(len(self.preALUBuff)):
                outFile.write("\t Entry " + str(x) + ": ")
                if self.preALUBuff[x] != -1:
                    outFile.write("[" + str(self.opcodeStr[self.preALUBuff[x]])
                                  + str(self.arg1Str[self.preALUBuff[x]]) + str(self.arg2Str[self.preALUBuff[x]])
                                  + str(self.arg3Str[self.preALUBuff[x]]) + "] \n")
                else:
                    outFile.write("\n")
            outFile.write("Post_ALU Queue: \n")
            for x in range(1):
                outFile.write("\t Entry " + str(x) + ": ")
                if self.postALUBuff[x] != -1:
                    outFile.write("[" + str(self.opcodeStr[self.postALUBuff[x]])
                                  + str(self.arg1Str[self.postALUBuff[x]]) + str(self.arg2Str[self.postALUBuff[x]])
                                  + str(self.arg3Str[self.postALUBuff[x]]) + "] \n")
                else:
                    outFile.write("\n")
            outFile.write("Pre_MEM Queue: \n")
            for x in range(len(self.preMemBuff)):
                outFile.write("\t Entry " + str(x) + ": ")
                if self.preMemBuff[x] != -1:
                    outFile.write("[" + str(self.opcodeStr[self.preMemBuff[x]])
                                  + str(self.arg1Str[self.preMemBuff[x]]) + str(self.arg2Str[self.preMemBuff[x]])
                                  + str(self.arg3Str[self.preMemBuff[x]]) + "] \n")
                else:
                    outFile.write("\n")
            outFile.write("Post_MEM Queue: \n")
            for x in range(1):
                outFile.write("\t Entry " + str(x) + ": ")
                if self.postMemBuff[x] != -1:
                    outFile.write("[" + str(self.opcodeStr[self.postMemBuff[x]])
                                  + str(self.arg1Str[self.postMemBuff[x]]) + str(self.arg2Str[self.postMemBuff[x]])
                                  + str(self.arg3Str[self.postMemBuff[x]]) + "] \n")
                else:
                    outFile.write("\n")
            outFile.write("\n")

            # Registers
            outFile.write("Registers:\n")
            outStr = "r00:"
            for i in range(0, 8):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outStr = "r08:"
            for i in range(8, 16):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outStr = "r16:"
            for i in range(16, 24):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outStr = "r24:"
            for i in range(24, 32):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outFile.write("\n")

            # Cache
            outFile.write("Cache \n")
            for i in range(4):
                outFile.write("Set " + str(i) + ": LRU=" + str(self.cache.lruBit[i]) + "\n")
                for j in range (2):
                    outFile.write("\t Entry " + str(j) + ": [(" + str(self.cache.cacheSets[i][j][0]) + ", " + str(self.cache.cacheSets[i][j][1]) + ", "
                                  + str(self.cache.cacheSets[i][j][2]) + ")<" + str(self.cache.cacheSets[i][j][3]) + ", "
                                  + str(self.cache.cacheSets[i][j][4]) + ">]" + "\n")
            outFile.write("\n")

            # Data
            outFile.write("Data:\n")
            outStr = "\n"
            for i in range(len(self.dataval)):

                if i % 8 == 0 and i != 0 or i == len(self.dataval):
                    outFile.write(outStr + "\n")

                if i % 8 == 0:
                    outStr = str(self.address[i + self.numInstructions]) + ":" + str(self.dataval[i])

                if i % 8 != 0:
                    outStr = outStr + "\t" + str(self.dataval[i])

            outFile.write(outStr + "\n")
            outFile.close()

    def run(self):
        go = True
        while go:
            self.WB.run()
            self.ALU.run()
            self.MEM.run()
            self.issue.run()
            go = self.fetch.run()
            self.printState()
            self.cycle += 1
