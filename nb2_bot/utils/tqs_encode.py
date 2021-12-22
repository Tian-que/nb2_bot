# coding=utf-8
Luen = '阿贼呢'
Luen = [i for i in Luen]
BlockSize = 128
endcode = '哦'

encodeLen = len(Luen)
def luen_encode(strc):
    # 进行utf-8编码，转化后为typts字节
    utf = strc.encode('utf-8')
    circ = lambda a:'0'*(8-len(str(bin(a))[2:])) + str(bin(a))[2:]
    de = ''
    # 将所有编码转换为二进制字符串
    for i in utf:
        de = circ(i) + de
    # 以128为一组进行编码，不断对 encodeLen 除余，余数查表转码
    ret = ''
    while len(de) != 0:
        # 将128位二进制数字转化为十进制
        b = int(de[-BlockSize:],2)
        # test = b
        while b != 0:
            ret += Luen[b%encodeLen]
            b = b//encodeLen
        ret += endcode
        de = de[:-BlockSize]
    return ret

def luen_decode(strr):
    ret = b''
    # 对分割的组进行重组
    for str in strr.split(endcode)[:-1]:
        new = 0
        # 查表将卢恩符文恢复为十进制数字
        while str != '':
            new =  new * encodeLen + Luen.index(str[-1])
            str = str[:-1]
        # 十进制转二进制字符串
        if len(bin(new)[2:])% 8!= 0:
            new = '0'*(8-len(bin(new)[2:])%8) + bin(new)[2:]
        else:
            new = bin(new)[2:]
        # 将二进制字符串还原为typts格式串
        while new != '':
            ret += int(new[-8:],2).to_bytes(length=1, byteorder='big')
            new = new [:-8]
        # 返回utf-8解码信息
    return ret.decode('utf-8')

dd = luen_encode("你是猪")
luen_decode(dd)