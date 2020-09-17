import easyquotation
import json

if False:
    quotation = easyquotation.use('sina') # 新浪 ['sina'] 腾讯 ['tencent', 'qq'] 
    t = quotation.market_snapshot(prefix=True) # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀

if False:
    quotation = easyquotation.use("hkquote")
    data = quotation.real(['00001','00700','00522'])
    print(data)

quotation  = easyquotation.use("daykline")
for i in range(9999):
    try:
        print(i)
        data = quotation.real(['%.5d'%i])
        s = json.dumps(data)
        with open('%.5d.txt'%i, 'w') as f:
            f.write(s)
    except e:
        print(e)