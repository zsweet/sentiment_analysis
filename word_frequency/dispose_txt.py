import os, codecs
import jieba
from collections import Counter


def get_words(txt):
    seg_list = jieba.cut(txt)
    print('cut is over >>>')
    c = Counter()
    tmpcount = 0
    for x in seg_list:
        if tmpcount%50000==0:
            print(tmpcount)
        if len(x)>1 and x != '\r\n':
            c[x] += 1
        tmpcount+=1
    print('常用词频度统计结果')
    for (k,v) in c.most_common(100):
        print('%s%s %d' % ('  '*(5-len(k)), k, v))

if __name__ == '__main__':
    with codecs.open('C:\\Users\\zsw\\Desktop\\网络排名项目\\舆情分析\\tmp\\content.txt', 'rb') as f:
        try:
            print('>>>>>')
            txt = f.read()
            get_words(txt)
        except Exception as e:
            print (e)
