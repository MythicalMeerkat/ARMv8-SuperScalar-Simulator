import sys

# TODO: Look into the parameters of getIndexOfMemAddress()


class SetUp:

    def __init__(self):
        pass

    @classmethod
    def get_input_filename(cls):
        # Get the input file name via command line args and return the name
        for i in range(len(sys.argv)):
            if sys.argv[i] == '-i' and i < (len(sys.argv) - 1):
                inputFileName = sys.argv[i+1]

        return inputFileName

    @classmethod
    def get_output_filename(cls):
        # Get the output file name via command line and return the name
        for i in range(len(sys.argv)):
            if sys.argv[i] == '-o' and i < (len(sys.argv) - 1):
                outputFileName = sys.argv[i+1]

        return outputFileName

    @classmethod
    def import_data_file(cls):
        # get file name via command line and then download the input file
        for i in range(len(sys.argv)):
            if sys.argv[i] == '-i' and i < (len(sys.argv) - 1):
                inputFileName = sys.argv[i + 1]

        try:
            instructions = [line.rstrip() for line in open(inputFileName, 'r')]
        except IOError:
            print("Could not open input file, is path correct?")

        return instructions

    @classmethod
    def imm_bit_to_32_bit_converter(cls, num, bitsize):

        if bitsize == 12:
            negBitMask = 0x800
            extendMask = 0xFFFFF000
        elif bitsize == 9:
            negBitMask = 0x100
            extendMask = 0xFFFFFE00
        elif bitsize == 19:
            negBitMask = 0x40000
            extendMask = 0xFFFC0000
        elif bitsize == 16:
            negBitMask = 0x8000
            extendMask = 0xFFFF0000
        elif bitsize == 26:
            negBitMask = 0x2000000
            extendMask = 0xFD000000
        elif bitsize == 32:
            negBitMask = 0x80000000
            extendMask = 0x0
        elif bitsize == 6:
            negBitMask = 0x20
            extendMask = 0xFFFFFD0
        else:
            print("You ARE USING AN INVALID BIT LENGTH")

        if(negBitMask & num) > 0:  # Check if the num is negative
            num = num | extendMask
            num = num ^ 0xFFFFFFFF
            num = num + 1
            num = num * -1
            # num = SetUp.imm_32_bit_unsigned_to_32_bit_signed_converter(num)

        return num

    # Begin functions to format the output of the bit strings into the proper spacings
    @classmethod
    def bin2StringSpaced(cls, s):
            spacedStr = s[0:8] + " " + s[8:11] + " " + s[11:16] + " " + s[16:21] + " " + s[21:26] + " " + s[26:32]
            return spacedStr

    @classmethod
    def bin2StringSpacedD(cls, s):
        spacedStr = s[0:11] + " " + s[11:20] + " " + s[20:22] + " " + s[22:27] + " " + s[27:32]
        return spacedStr

    @classmethod
    def bin2StringSpacedIM(cls, s):
        spacedStr = s[0:9] + " " + s[9:11] + " " + s[11:27] + " " + s[27:32]
        return spacedStr

    @classmethod
    def bin2StringSpacedCB(cls, s):
        spacedStr = s[0:8] + " " + s[8:27] + " " + s[27:32]
        return spacedStr

    @classmethod
    def bin2StringSpacedI(cls, s):
        spacedStr = s[0:10] + " " + s[10:22] + " " + s[22:27] + " " + s[27:32]
        return spacedStr

    @classmethod
    def bin2StringSpacedR(cls, s):
        spacedStr = s[0:11] + " " + s[11:16] + " " + s[16:22] + " " + s[22:27] + " " + s[27:32]
        return spacedStr

    @classmethod
    def bin2StringSpacedB(cls, s):
        spacedStr = s[0:6] + " " + s[6:32]
        return spacedStr

    @classmethod
    def imm_32_bit_unsigned_to_32_bit_signed_converter(cls, num):
        bin_str = str(abs(num))  # Need to strip away the negative symbol to store as a string for processing with the bin function
        if num < 0 or num >= 2**31:  # is this number negative in decimal form or 2s Comp?
            num = int(bin_str, 2)
            num = num - (2 ** len(bin_str))  # Apply the negative with the MSB to num
        else:
            num = int(bin_str, 2)

        return num

    @classmethod
    def decimalToBinary(cls, num):
        if num > 1:
            cls.decimalToBinary(num // 2)
        print(num % 2, end=' ')

    @classmethod
    def binaryToDecimal(cls, binary):
        print("\n")
        print(int(binary, 2))

    @classmethod
    def getIndexOfMemAddress(cls, currAdr, isSW, dataval, address, numInstructions):

        tempIndex = 0
        try:

            if isSW:
                # Make sure that there is enough spaces in dataval
                # there has to be an even number of elements in dataval

                if len(address) > numInstructions:

                    lastInstructAddr = ((numInstructions - 1) * 4) + 96
                    lastMemAddr = lastInstructAddr + 4 * len(dataval)
                    if currAdr == lastMemAddr:
                        dataval.append(0)
                        dataval.append(0)
                        address.append(lastMemAddr + 4)
                        address.append(lastMemAddr + 8)

                    if currAdr > lastMemAddr:
                        addIndex = (currAdr - lastMemAddr) / 4
                        for i in range(int(addIndex)):
                            dataval.append(0)
                            address.append(lastMemAddr + (4 * (i + 1)))
                tempIndex = address.index(currAdr)
                tempIndex = tempIndex - numInstructions

            else:
                tempIndex = address.index(currAdr)

                if tempIndex >= numInstructions:
                    tempIndex = tempIndex - numInstructions

            return tempIndex
        except ValueError:
            print("ERROR -- did not find mem address currAddr " + str(currAdr))

    @classmethod
    # TODO: Finish out this function, or find the code. it might just see if the instruction needs to access memory directly or not
    # TODO: B,CBZ,CBNZ,LDUR,STUR ?
    def isMemOp(self, opcodeStr):
        if opcodeStr == "STUR" or opcodeStr == "LDUR":
            return True
        else:
            return False
