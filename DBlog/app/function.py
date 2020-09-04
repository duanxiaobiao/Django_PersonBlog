

import hashlib
def my_md5(s,salt=''):      #加盐，盐的默认值是空
    s=s+salt
    news=str(s).encode()    #先变成bytes类型才能加密
    m=hashlib.md5(news)     #创建md5对象
    return m.hexdigest()    #获取加密后的字符串