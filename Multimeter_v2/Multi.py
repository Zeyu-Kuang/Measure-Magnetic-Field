import visa

def init_multi(sample_delay, sample_counts):
    '''
    Use to initialize the multimeter
    :param sample_delay: delay between each sampling
    :param sample_counts: sampling number
    :return:
    '''
    # searching for devices
    print('Searching for devices ...')
    rm = visa.ResourceManager()
    print('Avaliable devices: ' + str(rm.list_resources()))  # print avaliable devices
    inst = rm.open_resource('GPIB0::22::INSTR')  # selecting Multimeter
    print('Selecting devices: ' + str(inst.query("*IDN?")))  # print Multimeter

    # set parameters
    #sample_delay = 0.0001  #  set the sample delay (seconds)
    #sample_counts = 1  # set the sample counts (maxium 512)
    del inst.timeout  # set infinite timeout

    # intialization
    inst.write("CONF:VOLT:DC 10, 0.3")  # Configure the initial state: DC voltage with certain range and resolution
    inst.write("TRIGger:DElay " + str(sample_delay))  # set the triggering delay
    inst.write("SAMPle:COUNt " + str(sample_counts))  # set the sampling numbers in one trigger
    inst.write("TRIG:SOUR IMM")  # chose a trigger source (immediate internal trigger)

    # reporting settings
    print('Triggering delay (seconds) set to: ' + inst.query("TRIGger:DELay?"))
    print('Sample Counts set to ' + inst.query("SAMPle:COUNt?"))
    print('Timeout: infinite')


    return inst