def getText(filepath):    # 传入待读取文件的文件名
    f = open(filepath, "r",encoding='utf-8')
    text = f.read()
    f.close()
    return text            # 返回读出的文本数据
import jieba
def stopwordslist(filepath):  
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]  
    return stopwords
def wordFreq(filepath,text,topn):
    words  = jieba.lcut(text.strip())
    counts = {}
    stopwords = stopwordslist('stop_words.txt')
    for word in words:
        if len(word) == 1:
            continue
        elif word not in stopwords:  
            if word == "凤姐儿" :
                word="凤姐"
            elif word=="林黛玉" or word=="林妹妹" or word=="黛玉笑":
                word="黛玉"
            elif word == "宝二爷":
                word="宝玉"
            elif word == "袭人道":
                word="袭人"
            counts[word] = counts.get(word,0) + 1        
    items = list(counts.items())
    items.sort(key = lambda x:x[1], reverse = True)
    f = open(filepath[:-4]+'_词频.txt', "w")
    for i in range(topn):
        word, count = items[i]
        f.writelines("{}\t{}\n".format(word, count))
    f.close()
text=getText('红楼梦.txt')
wordFreq('红楼梦.txt',text,300)
print('统计结束')
