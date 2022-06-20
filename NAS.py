def convert_msg(msg):
    for n in range(len(msg)):
        msg[n] = msg[n].replace('  ', '\t')
    return msg
