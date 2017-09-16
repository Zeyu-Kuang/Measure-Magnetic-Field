__author__ = 'Franics'

import visa

rm = visa.ResourceManager()
print(rm.list_resources())

inst = rm.get_instrument("GPIB0::19::INSTR")

print(inst.query("*IDN?"))

for i in range(10000):
    print(inst.query("CALC:DATA?"))
    print(i)
