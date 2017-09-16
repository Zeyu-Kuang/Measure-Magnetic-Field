from Multi import init_multi

inst = init_multi(0, 500)

inst.write("ZERO:AUTO OFF")

N = 5000
for i in range(N):
    #print('INIT stuck ...')
    #inst.write("INIT")
    #print('FETC stuck ...')
    #inst.write("FETC?")
    print('READ stuck ...')
    inst.write("READ?")
    print('reading stuck ...')
    print(inst.read())
    print(i)