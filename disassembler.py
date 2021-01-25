from helpers import SetUp
import os
import masking_constants as masks
import sys


class Disassembler:

    def __init__(self):
        # We could turn masking_constants into a self reference here
        pass

    opcodeStr = []
    instrSpaced = []
    arg1 = []
    arg2 = []
    arg3 = []
    arg1Str = []
    arg2Str = []
    arg3Str = []
    dataval = []
    rawdata = []
    address = []
    numInstructs = 0

    # Simulator Lists
    destReg = []
    src1Reg = []
    src2Reg = []

    def run(self):

        instructions = []
        instructions = SetUp.import_data_file()

        outputFileName = SetUp.get_output_filename()

        print("raw output filename is ", outputFileName)

        # Create an address list with appropriate length
        for i in range(len(instructions)):
            self.address.append(96 + (i * 4))

        opcode = []

        # Create an opcode list by selecting the left 11 bits
        for z in instructions:
            opcode.append(int(z, base=2) >> 21)

        # Now the fun begins! Decode and dissect!
        for i in range(len(opcode)):
            self.numInstructs = self.numInstructs + 1
            if opcode[i] == 1112:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("ADD")
                self.arg1.append((int(instructions[i], base=2) & masks.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & masks.rmMask) >> 16)
                self.arg3.append((int(instructions[i], base=2) & masks.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))
                # Simulator List Operations
                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(self.arg2[i])
            elif opcode[i] == 1624:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("SUB")
                self.arg1.append((int(instructions[i], base=2) & masks.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & masks.rmMask) >> 16)
                self.arg3.append((int(instructions[i], base=2) & masks.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))
                # Simulator List Operations
                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(self.arg2[i])
            elif opcode[i] == 1160 or opcode[i] == 1161:
                self.instrSpaced.append(SetUp.bin2StringSpacedI(instructions[i]))
                self.opcodeStr.append("ADDI")
                self.arg1.append((int(instructions[i], base=2) & masks.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & masks.rdMask) >> 0)
                self.arg3.append((int(instructions[i], base=2) & masks.imMask) >> 10)
                self.arg1Str.append("\tR" + str(self.arg2[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg3[i]))
                # Simulator List Operations
                self.destReg.append(self.arg2[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(self.arg3[i])
            elif opcode[i] == 1360:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("ORR")
                self.arg1.append((int(instructions[i], base=2) & masks.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & masks.rmMask) >> 16)
                self.arg3.append((int(instructions[i], base=2) & masks.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))
                # Simulator List Operations
                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(self.arg2[i])
            elif opcode[i] == 1104:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("AND")
                self.arg1.append((int(instructions[i], base=2) & masks.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & masks.rmMask) >> 16)
                self.arg3.append((int(instructions[i], base=2) & masks.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))
                # Simulator List Operations
                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(self.arg2[i])
            elif 1440 <= opcode[i] <= 1447:
                self.instrSpaced.append(SetUp.bin2StringSpacedCB(instructions[i]))
                self.opcodeStr.append("CBZ")
                self.arg1.append(SetUp.imm_bit_to_32_bit_converter(((int(instructions[i], base=2) & masks.addr2Mask) >> 5), 19))
                self.arg2.append((int(instructions[i], base=2) & masks.rdMask))
                self.arg3.append(0)
                self.arg1Str.append("\tR" + str(self.arg2[i]))
                self.arg2Str.append(", #" + str(self.arg1[i]))
                self.arg3Str.append("")
                # Simulator List Operations
                self.destReg.append(self.arg2[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(-16)
            elif 1448 <= opcode[i] <= 1455:
                self.instrSpaced.append(SetUp.bin2StringSpacedCB(instructions[i]))
                self.opcodeStr.append("CBNZ")
                self.arg1.append(SetUp.imm_bit_to_32_bit_converter(((int(instructions[i], base=2) & masks.addr2Mask) >> 5), 19))
                self.arg2.append((int(instructions[i], base=2) & masks.rdMask) >> 0)  # We Need to treat the conditional as rd for mask
                self.arg3.append(0)
                self.arg1Str.append("\tR" + str(self.arg2[i]))
                self.arg2Str.append(", #" + str(self.arg1[i]))
                self.arg3Str.append("")
                # Simulator List Operations
                self.destReg.append(self.arg2[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(-16)
            elif 1672 <= opcode[i] <= 1673:
                self.instrSpaced.append(SetUp.bin2StringSpacedI(instructions[i]))
                self.opcodeStr.append("SUBI")
                self.arg1.append((int(instructions[i], base=2) & masks.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & masks.rdMask) >> 0)
                self.arg3.append((int(instructions[i], base=2) & masks.imMask) >> 10)
                self.arg1Str.append("\tR" + str(self.arg2[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg3[i]))
                self.destReg.append(self.arg2[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(self.arg3[i])
            elif 1684 <= opcode[i] <= 1687:
                self.instrSpaced.append(SetUp.bin2StringSpacedIM(instructions[i]))
                self.opcodeStr.append("MOVZ")
                self.arg1.append((int(instructions[i], base=2) & masks.rdMask) >> 0)
                self.arg2.append((int(instructions[i], base=2) & masks.imdataMask) >> 5)
                self.arg3.append(((int(instructions[i], base=2) & masks.imsftMask) >> 21) * 16)
                self.arg1Str.append("\tR" + str(self.arg1[i]))
                self.arg2Str.append(", " + str(self.arg2[i]))
                self.arg3Str.append(", LSL " + str(self.arg3[i]))
                # Simulator List Operations
                self.destReg.append(self.arg1[i])
                self.src1Reg.append(self.arg2[i])
                self.src2Reg.append(self.arg3[i])
            elif 1940 <= opcode[i] <= 1943:
                self.instrSpaced.append(SetUp.bin2StringSpacedIM(instructions[i]))
                self.opcodeStr.append("MOVK")
                self.arg1.append((int(instructions[i], base=2) & masks.rdMask) >> 0)
                self.arg2.append((int(instructions[i], base=2) & masks.imdataMask) >> 5)
                self.arg3.append(((int(instructions[i], base=2) & masks.imsftMask) >> 21) * 16)
                self.arg1Str.append("\tR" + str(self.arg1[i]))
                self.arg2Str.append(", " + str(self.arg2[i]))
                self.arg3Str.append(", LSL " + str(self.arg3[i]))
                # Simulator List Operations
                self.destReg.append(self.arg1[i])
                self.src1Reg.append(self.arg2[i])
                self.src2Reg.append(self.arg3[i])
            elif opcode[i] == 1690:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("LSR")
                self.arg1.append((int(instructions[i], base=2) & masks.rnMask) >> 5)
                self.arg2.append(SetUp.imm_bit_to_32_bit_converter(((int(instructions[i], base=2) & masks.shmtMask) >> 10), 6))
                self.arg3.append((int(instructions[i], base=2) & masks.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg2[i]))
                # Simulator List Operations
                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(self.arg2[i])
            elif opcode[i] == 1691:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("LSL")
                self.arg1.append((int(instructions[i], base=2) & masks.rnMask) >> 5)
                self.arg2.append(SetUp.imm_bit_to_32_bit_converter(((int(instructions[i], base=2) & masks.shmtMask) >> 10), 6))
                self.arg3.append((int(instructions[i], base=2) & masks.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg2[i]))
                # Simulator List Operations
                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(self.arg2[i])
            elif opcode[i] == 1984:
                self.instrSpaced.append(SetUp.bin2StringSpacedD(instructions[i]))
                self.opcodeStr.append("STUR")
                self.arg1.append((int(instructions[i], base=2) & masks.rdMask) >> 0)
                self.arg2.append((int(instructions[i], base=2) & masks.rnMask) >> 5)
                self.arg3.append(SetUp.imm_bit_to_32_bit_converter(((int(instructions[i], base=2) & masks.addrMask) >> 12), 9))
                self.arg1Str.append("\tR" + str(self.arg1[i]))
                self.arg2Str.append(", [R" + str(self.arg2[i]))
                self.arg3Str.append(", #" + str(self.arg3[i]) + "]")
                # Simulator List Operations
                self.destReg.append(self.arg1[i])
                self.src1Reg.append(self.arg2[i])
                self.src2Reg.append(self.arg3[i])
            elif opcode[i] == 1986:
                self.instrSpaced.append(SetUp.bin2StringSpacedD(instructions[i]))
                self.opcodeStr.append("LDUR")
                self.arg1.append((int(instructions[i], base=2) & masks.rdMask) >> 0)
                self.arg2.append((int(instructions[i], base=2) & masks.rnMask) >> 5)
                self.arg3.append(SetUp.imm_bit_to_32_bit_converter(((int(instructions[i], base=2) & masks.addrMask) >> 12), 9))
                self.arg1Str.append("\tR" + str(self.arg1[i]))
                self.arg2Str.append(", [R" + str(self.arg2[i]))
                self.arg3Str.append(", #" + str(self.arg3[i]) + "]")
                # Simulator List Operations
                self.destReg.append(self.arg1[i])
                self.src1Reg.append(self.arg2[i])
                self.src2Reg.append(self.arg3[i])
            elif opcode[i] == 1692:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("ASR")
                self.arg1.append((int(instructions[i], base=2) & masks.rnMask) >> 5)
                self.arg2.append(SetUp.imm_bit_to_32_bit_converter(((int(instructions[i], base=2) & masks.shmtMask) >> 10), 6))
                self.arg3.append((int(instructions[i], base=2) & masks.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg2[i]))
                # Simulator List Operations
                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(self.arg2[i])
            elif opcode[i] == 1872:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("EOR")
                self.arg1.append((int(instructions[i], base=2) & masks.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & masks.rmMask) >> 16)
                self.arg3.append((int(instructions[i], base=2) & masks.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))
                # Simulator List Operations
                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(self.arg2[i])
            elif opcode[i] == 1360:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("ORR")
                self.arg1.append((int(instructions[i], base=2) & masks.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & masks.rmMask) >> 16)
                self.arg3.append((int(instructions[i], base=2) & masks.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))
                # Simulator List Operations
                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(self.arg2[i])
            elif 160 <= opcode[i] <= 191:
                self.instrSpaced.append(SetUp.bin2StringSpacedB(instructions[i]))
                self.opcodeStr.append("B")
                self.arg1.append(SetUp.imm_bit_to_32_bit_converter((int(instructions[i], base=2) & masks.bMask) >> 0, 26))
                self.arg2.append(0)
                self.arg3.append(0)
                self.arg1Str.append("\t#" + str(self.arg1[i]))
                self.arg2Str.append("")
                self.arg3Str.append("")
                # Simulator List Operations
                self.destReg.append(-18)
                self.src1Reg.append(-17)
                self.src2Reg.append(-16)
            elif opcode[i] == 2038 and (int(instructions[i], base=2) & masks.specialMask) == 2031591:
                self.instrSpaced.append(SetUp.bin2StringSpaced(instructions[i]))
                self.opcodeStr.append("BREAK")
                self.arg1.append(0)
                self.arg2.append(0)
                self.arg3.append(0)
                self.arg1Str.append("")
                self.arg2Str.append("")
                self.arg3Str.append("")
                print("breaking")
                break
            elif opcode[i] == 0:
                self.instrSpaced.append(SetUp.bin2StringSpaced(instructions[i]))
                self.opcodeStr.append("NOP")
                self.arg1.append(0)
                self.arg2.append(0)
                self.arg3.append(0)
                self.arg1Str.append("")
                self.arg2Str.append("")
                self.arg3Str.append("")
                # Simulator List Operations
                self.destReg.append(-18)
                self.src1Reg.append(-17)
                self.src2Reg.append(-16)
            else:
                self.opcodeStr.append("unknown")
                self.arg1.append(0)
                self.arg2.append(0)
                self.arg3.append(0)
                self.arg1Str.append("")
                self.arg2Str.append("")
                self.arg3Str.append("")
                # Simulator List Operations
                self.destReg.append(-18)
                self.src1Reg.append(-17)
                self.src2Reg.append(-16)
                print("i=: " + str(opcode[i]))
                sys.exit("You have found an unknown instruction, investigate NOW")

        # I created parser here because I needed to preserve/reference numInstructs as the beginning of the rawData at a later time
        # Read in the 32 bit strings raw into this vector, will be used for printing and handing data to the converter
        parser = self.numInstructs
        while parser < len(opcode):
            self.rawdata.append(str(instructions[parser]))
            parser = parser + 1

        # Convert the signed 32 bit strings into a signed int and store them in the dataval vector for printing later
        for i in range(len(self.rawdata)):
            self.dataval.append(SetUp.imm_32_bit_unsigned_to_32_bit_signed_converter(int(self.rawdata[i])))

        return {
            "opcodes": opcode,
            "opcodeStr": self.opcodeStr,
            "arg1": self.arg1,
            "arg1Str": self.arg1Str,
            "arg2": self.arg2,
            "arg2Str": self.arg2Str,
            "arg3": self.arg3,
            "arg3Str": self.arg3Str,
            "dataval": self.dataval,
            "address": self.address,
            "numInstrs": self.numInstructs,
            "destReg": self.destReg,
            "src1Reg": self.src1Reg,
            "src2Reg": self.src2Reg,
            "instructions": instructions}

    def print(self):
        outFile = open(SetUp.get_output_filename() + "_dis.txt", 'w')  # Open the file for writing

        for i in range(self.numInstructs):
            outFile.write(str(self.instrSpaced[i]) + '\t' + str(self.address[i]) + '\t' + str(self.opcodeStr[i]) + "\t"
                          + str(self.arg1Str[i]) + str(self.arg2Str[i]) + str(self.arg3Str[i]) + '\n')

        for i in range(len(self.dataval)):
            outFile.write(str(self.rawdata[i]) + '\t' + str(self.address[self.numInstructs + i]) + '\t'
                          + str(self.dataval[i]) + '\n')

        outFile.close()




