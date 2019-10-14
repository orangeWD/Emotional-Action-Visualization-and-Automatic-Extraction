'''
    处理1. 例句：听到他爸爸又出去打麻将赌钱了，他<keyword>生气</keyword>得就Z往外面跑X；
        ----把所有语料文件处理成“生气 往外面跑 听到他爸爸又出去打麻将赌钱了，他生气得就往外面跑；”的格式，没有情感行为的句子删掉,标注时做的标记也删掉
            line.split()[0]='情感' ，line.split()[1]='行为' ，line.split()[2]='原句'
            分离情感词时记得和文件名对照否则容易出问题                               --保存
    input[1,2,3,4,5,...]   output[0,0,0,1,1,...]
'''
import jieba
import re
#处理2
def save_wordcut():
    with open(r"data\fakeData.txt", "r", encoding="utf-8") as fh:
        text = fh.read()
        text = text.replace('</keyword>', 'eokeyword')
        text = text.replace('<keyword>', 'keyword')
        e_a_lines = (text).split('\n')
    jieba_words = []

    for i in range(len(e_a_lines)):
        if i % 5 == 0:
                print(i)
        seg_list = jieba.cut(e_a_lines[i])
        jieba_words.append(list(seg_list))
    print(jieba_words)
    with open(r"data\fakeData_jieba.txt", "w", encoding="utf-8") as fh:
        fh.write(str(jieba_words))

def save_y():
    with open(r"data\fakeData_jieba.txt", "r", encoding="utf-8") as fh:
        lines = eval(fh.read())
    y_s = []
    for line in lines:
        y = []
        flag = 0
        for word in line:
            if word == 'eokeyword' or word == 'keyword':
                continue
            if word == 'Z':
                flag = 1
                continue
            if word == 'X':
                flag = 0
                continue
            if flag == 1:
                y.append(1)
            else:
                y.append(0)
        y_s.append(y)
    with open(r"data\fakeData_output.txt", "w", encoding="utf-8") as fh:
        fh.write(str(y_s))

def word_and_idx():
    with open(r"data\fakeData_jieba.txt", "r", encoding="utf-8") as fh:
        lines = eval(fh.read())
    word2idx = {}
    count = 0
    for line in lines:
        for word in line:
            if word == 'eokeyword' or word == 'keyword' or word == 'Z' or word == 'X':
                continue
            if word in word2idx.keys():
                continue
            count += 1
            word2idx[word] = count
    idx2word = {idx:word for word,idx in word2idx.items()}
    with open(r"data\fakeData_word2idx.txt", "w", encoding="utf-8") as fh:
        fh.write(str(word2idx))
    with open(r"data\fakeData_idx2word.txt", "w", encoding="utf-8") as fh:
        fh.write(str(idx2word))



def save_x():
    with open(r"data\fakeData_word2idx.txt", "r", encoding="utf-8") as fh:
        word2idx = eval(fh.read())
    with open(r"data\fakeData_jieba.txt", "r", encoding="utf-8") as fh:
        words = eval(fh.read())
    idxs = []
    for line_words in words:
        idx = []
        for word in line_words:
            if word == 'eokeyword' or word == 'keyword' or word == 'Z' or word == 'X':
                continue
            idx.append(word2idx[word])
        idxs.append(idx)
    with open(r"data\fakeData_input.txt", "w", encoding="utf-8") as fh:
        fh.write(str(idxs))

save_x()