bMask = 0x3FFFFFF
jAddrMask = 0xFC000000
specialMask = 0x1FFFFF
rnMask = 0x3E0  # 1st Argument ARM Rn
rmMask = 0x1F0000  # 2nd Argument ARM Rm
rdMask = 0x1F  # Destination ARM Rd
imMask = 0x3FFC00  # ARM I Format Immediate
shmtMask = 0xFC00  # ARM ShAMT
addrMask = 0x1FF000  # ARM address for ld (load) and st (store)
addr2Mask = 0xFFFFE0  # addr for CB format
imsftMask = 0x600000  # shift for IM format
imdataMask = 0x1FFFE0  # data for IM type

