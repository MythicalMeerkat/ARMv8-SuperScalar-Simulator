import disassembler
import sim

mydis = disassembler.Disassembler()
output = {}
output = mydis.run()
mydis.print()

mysim = sim.simClass(**output)
mysim.run()
