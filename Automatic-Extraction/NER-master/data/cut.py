with open(r'source_BIO_2014_cropus.txt','r',encoding = 'utf-8') as r:
    with open(r'test_source.txt','w',encoding = 'utf-8') as w:
        for i in range(6000):
            w.write(r.readline().strip()+'\n')

with open(r'target_BIO_2014_cropus.txt','r',encoding = 'utf-8') as r:
    with open(r'test_target.txt','w',encoding = 'utf-8') as w:
        for i in range(6000):
            w.write(r.readline().strip()+'\n')                
