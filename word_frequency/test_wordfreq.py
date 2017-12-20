#coding:utf-8
__author__ = 'G930'

import pynlpir
import jieba
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')




class StatWordFreq():
    # 获取停用词
    def get_stopWord(self):
        #file = open("F:/svn/opinion_new/news/txt", "r")
        file = open("C:\\Users\\G930\\Desktop\\stat\\stopWords.txt", 'r')
        stopWords = file.read()
        file.close()
        print('stopwords')
        return stopWords

    #结巴分词，得到原始分词结果
    def get_split(self):
        default_mode = jieba.cut(report)
        res = "/".join(default_mode).split('/')
        return res

    def get_unigram(self,res,stopWords):
        uni_dict = {}
        for res_unigram in res:
            if len(res_unigram) >= 1 and res_unigram not in stopWords:
                # print res_unigram
                # 生成词语信息字典
                if res_unigram in uni_dict:
                    uni_dict[res_unigram] += 1
                else:
                    uni_dict[res_unigram] = 1
        print(len(uni_dict))
        return uni_dict

    def get_bigram(self,res,uni_dict,stopWords):
        bi_dict = {}

        res_bigram_detail_dict = {}
        res_bigram = []
        for i in range(len(res)-1):
            if res[i].strip() in stopWords or res[i+1].strip() in stopWords:
                continue

            res_bigram_detail_dict[res[i] + res[i+1]] = [res[i],res[i+1]]
            res_bigram.append(res[i] + res[i+1])

        # for result in res:
        for result in res_bigram:
            # print result
            word_res = result.replace('\n', '')

            # 过滤词语(词性过滤， 词语长度过滤， 停用词过滤)
            if len(word_res) == 1 or word_res in stopWords:
                continue

            # 生成词语信息字典
            if word_res in bi_dict:
                bi_dict[word_res] += 1
            else:
                bi_dict[word_res] = 1



        #删除unigram字典中的部分内容
        del_list = set()
        for bi_words in bi_dict:
            cnt_biWords = bi_dict[bi_words]
            # if cnt_biWords < 10:
            #
            #     continue
            words_list = res_bigram_detail_dict[bi_words]

            cnt_triWords=cnt_biWords
            bi_word1 = words_list[0]
            bi_word2 = words_list[1]
            if bi_words == "人民军队":
                print(1)
            if bi_word1 in uni_dict.keys() and bi_word2 in uni_dict.keys():
                cnt_biWord1 = uni_dict[bi_word1]
                cnt_biWord2 = uni_dict[bi_word2]
                per1 = 1.0 * cnt_triWords / cnt_biWord1
                per2 = 1.0 * cnt_triWords / cnt_biWord2
                if ((per1 > 0.1) or (per2 >0.1)) and cnt_triWords>3:
                    del_list.add(bi_word1)
                    del_list.add(bi_word2)
            # for uni_word in words_list:
            #     #判断一元词组是否存在于一元词组字典列表中，存在的话比较二者数量
            #     if uni_word in uni_dict.keys():
            #         cnt_uniWord = uni_dict[uni_word]
            #         if 1.0 * cnt_biWords / cnt_uniWord > 0.2:
            #             uni_dict.pop(uni_word)

        # print words_dict

        for item in del_list:
            # print(item)
            uni_dict.pop(item)

        for item in uni_dict.keys():
            if len(item)<4:
                uni_dict.pop(item)

        return bi_dict, uni_dict

    def get_trigram(self,res,bi_dict,stopWords):
        tri_dict = {}

        res_trigram_detail_dict = {}
        res_trigram = []
        for i in range(len(res)-2):
            if res[i].strip() in stopWords or res[i+1].strip() in stopWords or res[i+2].strip() in stopWords:
                continue
            word_res = (res[i] + res[i+1] + res[i+2]).replace('\n', '')
            res_trigram_detail_dict[word_res] = [res[i] + res[i+1] ,res[i+1] + res[i+2]]
            res_trigram.append(word_res)

        # for result in res:
        for word_res in res_trigram:
            # print word_res

            # 生成词语信息字典
            if word_res in tri_dict:
                tri_dict[word_res] += 1
            else:
                tri_dict[word_res] = 1

        #删除bigram字典中的部分内容

        del_list = set()
        for tri_words in tri_dict:

            cnt_triWords = tri_dict[tri_words]
            # if cnt_triWords < 4:
            #     continue

            words_list = res_trigram_detail_dict[tri_words]

            bi_word1 = words_list[0]
            bi_word2 = words_list[1]
            if bi_word1 in bi_dict.keys() and bi_word2 in bi_dict.keys():
                cnt_biWord1 = bi_dict[bi_word1]
                cnt_biWord2 = bi_dict[bi_word2]
                per1 = 1.0 * cnt_triWords / cnt_biWord1
                per2 = 1.0 * cnt_triWords / cnt_biWord2
                if tri_words == "中国特色社会主义":
                    print(1)
                if ((per1 > 0.2) or (per2 >0.2)) and cnt_triWords>3:
                    del_list.add(bi_word1)
                    del_list.add(bi_word2)
            # for bi_words in words_list:
            #     #判断二元词组是否存在于二元词组字典列表中，存在的话比较二者数量
            #     if bi_words in bi_dict.keys():
            #         cnt_biWords = bi_dict[bi_words]
            #         if 1.0 * cnt_triWords / cnt_biWords > 0.05:
            #             bi_dict.pop(bi_words)

        # print words_dict
        for item in del_list:
            bi_dict.pop(item)
        return bi_dict, tri_dict

    def sortedWords(self,bi_dict, uni_dict,tri_dict):
        words_dict = dict(bi_dict.items() + uni_dict.items() + tri_dict.items())
        words_list = sorted(words_dict.iteritems(), key=lambda d: d[1],reverse = True)  # words = [(word, [frequence, source])]
        # for i in range(100):
            # print words_list[i]

        # with open("C:\\Users\\G930\\Desktop\\stat\\stat1.txt","w") as f:
        #     for words in words_list:
        #         f.write(words[0] + '\t' + str(words[1]) + '\n')
        #     print("加载入文件完成...")
        return words_list

    def step(self):
        stopWords = self.get_stopWord()
        res = self.get_split()
        uni_dict =self.get_unigram(res,stopWords)
        bi_dict, uni_dict = self.get_bigram(res,uni_dict,stopWords)
        bi_dict, tri_dict = self.get_trigram(res,bi_dict,stopWords)
        words_list = self.sortedWords(bi_dict, uni_dict,tri_dict)
        return words_list



if __name__ == "__main__":
    f = open("C:\\Users\\G930\\Desktop\\stat\\15.txt")
    report = f.read()
    f.close()
    wordFreq1 = StatWordFreq()
    words_list1 = wordFreq1.step()
    print(len(words_list1))
    print('77777777777777777777777777777777777777777777')


    f = open("C:\\Users\\G930\\Desktop\\stat\\14.txt")
    report = f.read()
    f.close()
    wordFreq2 = StatWordFreq()
    words_list2 = wordFreq2.step()
    print(len(words_list2))
    print('888888888888888888888888888888888888888888888')


    words_before = []
    words_new = []
    for words in words_list2:
        words_before.append(words[0])

    for words in words_list1:
        if words[0] not in words_before:
            words_new.append(words)

    with open("C:\\Users\\G930\\Desktop\\stat\\stat1.txt","w") as f:
        for words in words_new:
            f.write(words[0] + '\t' + str(words[1]) + '\n')
        print("加载入文件完成...")



