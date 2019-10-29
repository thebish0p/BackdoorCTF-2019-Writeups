def revmine(block):
    bl = block
    i = 0
    while True:
        i+=1
        sid = hexhash(long_to_bytes(block['nonce'])+long_to_bytes(i)+block['prev'].encode('utf-8'))
        if sid[:3] == '000':
            bl['data'] = i
            bl['self'] = sid
            bl['nonce'] = (s1*i+s2)%s3
            return bl