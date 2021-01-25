# TODO: Check if this works correctly, after implementing the other units


class WriteBack:

    def __init__(self, R, postMemBuff, postALUBuff, destReg):
        self.R = R
        self.postMemBuff = postMemBuff
        self.postALUBuff = postALUBuff
        self.destReg = destReg

    def run(self):
        print("Writing Back")
        if self.postMemBuff[1] != -1:
            self.R[self.destReg[self.postMemBuff[1]]] = self.postMemBuff[0]
            self.postMemBuff = [-1, -1]

        if self.postALUBuff[1] != -1:
            self.R[self.destReg[self.postALUBuff[1]]] = self.postALUBuff[0]
            self.postALUBuff = [-1, -1]
