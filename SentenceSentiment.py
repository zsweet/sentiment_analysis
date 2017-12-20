# coding=utf-8

from WordSentiment import *
import pynlpir
import time

class SentenceSentiment(object):
	def __init__(self):
		self.WINDOW = 2
		self.wordSentiment = WordSentiment()

	def segment(self, sentence):    #分词
		pynlpir.open(license_code=")VhTW_9s02tDm")
		list = pynlpir.segment(sentence)
		wordList = []
		for res in list:
			wordList.append(res[0])
		return wordList

	def predictSentence(self, sentence):    #返回句子的情感值
		wordList = self.segment(sentence) #使用nlpir进行分词
		print('分词结果：',wordList)
		scoreDict = self.searchSentimentWordAndScore(wordList)
		return self.determinePolarity(scoreDict)

	def determinePolarity(self, scoreDict):
		posMax = -1 #最大的正向分值
		posInstances = 0 #正向词语个数
		posTotal = 0 #正向分值和

		negMax = 1 #最小的负面分值
		negInstances = 0 #负向词语个数
		negTotal = 0 #负向分值和
		for (word, score) in scoreDict.items():
			if (score > 0):
				posInstances += 1
				posTotal += score
				if (score > posMax): posMax = score
			if (score < 0):
				negInstances += 1
				negTotal += -score
				if (score < negMax): negMax = score
		# 计算情感值
		print('最大正向分值：',posMax,'正向词语个数：',posInstances,'正向分值和',posTotal)
		print('最大负向分值：', negMax, '负向词语个数：', negInstances, '负向分值和', negTotal)
		if (posMax > -negMax):  #该句的情感是积极的，情感值是正数
			return int(float(posTotal)/(posTotal+negTotal)*10)
		if (posMax < -negMax):  #该句的情感是消极的，情感值是负数
			return -int(float(negTotal)/(posTotal+negTotal)*10)
		if (posInstances > negInstances):   #该句的情感是积极的，情感值是正数
			return int(float(posTotal)/(posTotal+negTotal)*10)
		if (posInstances < negInstances):   #该句的情感是消极的，情感值是负数
			return -int(float(negTotal)/(posTotal+negTotal)*10)
		return 0

	def searchSentimentWordAndScore(self, wordList):#计算句子中每个词的情感值
		scoreDict = {}
		for i in range(len(wordList)):
			word = wordList[i]
			score = self.wordSentiment.isWord(word)
			if (score != 0):#对于正向和负向的词语
				#以word为中心，WINDOW为半径的范围内，通过除word以外的其他词，对score进行修正
				score = self.searchWordWindow(wordList, i, score)
				#检查以WINDOW为半径的范围内是否有反语，并对score进行修正
				score = self.ironySearch(wordList, i, score)
				#防止句子中出现同一个词时，dict被覆盖。
				#对同样的word，词尾加上一个时间戳，以此区别。
				if word in scoreDict:
					scoreDict[word+str(time.time())] = score
				else:
					scoreDict[word] = score
			i += 1
		print(scoreDict)
		return scoreDict

	def ironySearch(self, wordList, index, score):
		for i in range(self.WINDOW):
			left = index - (i+1)
			if (left >= 0):
				word = wordList[left]
				score = self.modifyScoreForIrony(word, score)
			right = index + (i+1)
			if (right < len(wordList)):
				word = wordList[right]
				score = self.modifyScoreForIrony(word, score)
		return score

	def modifyScoreForIrony(self, word, score):
		if (self.wordSentiment.isIrony(word)):
			if (score > 0):
				score = -(score + 1)
			else:
				score = score - 1
		return score

	def searchWordWindow(self, wordList, index, score):
		for i in range(self.WINDOW):
			left = index - (i+1)
			if (left >= 0):
				word = wordList[left]
				score = self.modifyWordScore(word, score)
			right = index + (i+1)
			if (right < len(wordList)):
				word = wordList[right]
				score = self.modifyWordScore(word, score)
		return score

	def modifyWordScore(self, word, score):
		#如果word是表示减弱的程度副词，则减小情感值的绝对值
		if (self.wordSentiment.isDiminisher(word)):
			if (score > 0):
				score -= 1
			else:
				score += 1
		#如果word是表示增强的程度副词，则加大情感值的绝对值
		if (self.wordSentiment.isIntensifier(word)):
			if (score > 0):
				score += 1
			else:
				score -= 1
		#如果word是反语，则score取反
		if (self.wordSentiment.isNegation(word)):
			score = -score
		#如果word是感叹号，则加大score的绝对值
		if self.isExclamation(word):
			if (score > 0):
				score += 1
			else:
				score -= 1

		return score

	def isExclamation(self, word):
		if (word == u"!" or word == u"！"):
			return True
		return False
def demo():
	content = u'''据新华社北京9月8日电（记者孙辰茜潘洁）对于俄罗斯总统普京近日有关菲律宾南海仲裁案的表态，
    外交部发言人华春莹8日表示，这体现了俄罗斯在有关问题上客观公正的立场，代表国际社会主持正义的声音，代表国际社会主持正义的声音。
    '''
	# content = '特别不好'
	score = 0.0
	count = 0
	while content != '':  # 分句
		index = []
		index.append(content.find(u'。')) if content.find(u'。') >= 0 else None
		index.append(content.find(u'！')) if content.find(u'！') >= 0 else None
		index.append(content.find(u'？')) if content.find(u'？') >= 0 else None
		cut_index = min(index) + 1 if len(index) > 0 else len(content)  # 没有结束符号就获取剩下的全部内容
		sentence = content[:cut_index].strip()
		content = content[cut_index:]
		if len(sentence) == 0:
			continue
		# SnowNLP情感分析 BEGIN
		# s_score = SnowNLP(sentence).sentiments
		# s_score = self.__f_score(s_score)
		# score += round(s_score, 2)
		# SnowNLP情感分析 END

		# BUAA情感分析 BEGIN
		ss = SentenceSentiment()
		s_score = ss.predictSentence(sentence)
		score += s_score
		# BUAA情感分析 END

		count += 1
	result = 0;

	print(score, count)
	if count != 0:
		result = int(round(score / count))

	print(result)

def tmp():
	from snownlp import SnowNLP

	s = SnowNLP(u'''据新华社北京9月8日电（记者孙辰茜潘洁）对于俄罗斯总统普京近日有关菲律宾南海仲裁案的表态，
    外交部发言人华春莹8日表示，这体现了俄罗斯在有关问题上客观公正的立场，代表国际社会主持正义的声音，代表国际社会主持正义的声音。''')

	s.words  # [u'这个', u'东西', u'真心',
	# u'很', u'赞']

	s.tags  # [(u'这个', u'r'), (u'东西', u'n'),
	# (u'真心', u'd'), (u'很', u'd'),
	# (u'赞', u'Vg')]

	print(s.sentiments)  # 0.9769663402895832 positive的概率

if __name__ == "__main__":
	#demo()
	tmp()
