'''
    处理1. 例句：听到他爸爸又出去打麻将赌钱了，他<keyword>生气</keyword>得就Z往外面跑X；
        ----把所有语料文件处理成“生气 往外面跑 听到他爸爸又出去打麻将赌钱了，他生气得就往外面跑；”的格式，没有情感行为的句子删掉,标注时做的标记也删掉
            line.split()[0]='情感' ，line.split()[1]='行为' ，line.split()[2]='原句'
            分离情感词时记得和文件名对照否则容易出问题                               --保存
    处理2. 例句：听到他爸爸又出去打麻将赌钱了，他<keyword>生气</keyword>得就Z往外面跑X；
        1.分词    听到,他爸爸,又,出去,打麻将,赌钱,了,，他,<keyword>,生气,</keyword>,得,就,Z,往,外面,跑,X,；
                                                                              --保存
        2.遍历所有句子生成单词词典    {"听到":0,"他爸爸":1,....}              --保存
        3.遍历所有句子生成序号词典    {0:"听到",...}                         --保存
        4.把所有处理好的文件用序号表示：
            生气 往外面跑 听到他爸爸又出去打麻将赌钱了，他生气得就往外面跑；
            比如->[1] [15,2] [0,1,2,3,4......]                           --保存
'''
import jieba
import re
#处理1
def process1():
    with open(r"data\fakeData.txt", "r", encoding="utf-8") as fh:
        fd = fh.readlines()
    with open(r"data\ori_fakeData.txt", "r", encoding="utf-8") as fh:
        ori_fd = fh.readlines()
    output=""
    for i in range(len(fd)):
        pattern = re.compile(r'<keyword>(.*?)</keyword>')
        emotion = (pattern.findall(fd[i]))[0]
        #真正使用时需加入判断是否目标情感词的代码（与文件名对比）
        pattern2 = re.compile(r'Z(.*?)X')
        action = (pattern2.findall(fd[i]))[0]
        output += emotion + 'xxxx' + action + 'xxxx' + ((ori_fd[i]).replace('<keyword>', '')).replace('</keyword>', '')
    with open(r"data\result_fakeData.txt", "w", encoding="utf-8") as fh:
        fh.write(output)

#处理2
def save_wordcut():
    with open(r"data\result_fakeData.txt", "r", encoding="utf-8") as fh:
        e_a_lines = (fh.read()).split('\n')
    lines = []
    for e_a_line in e_a_lines:
        lines.append(e_a_line.split('xxxx')[2])
    jieba_words = ''
    for i in range(len(lines)):
        if i % 5 == 0:
            print(i)
        seg_list = jieba.cut(lines[i], cut_all=False)
        jieba_words += ' '.join(seg_list) + '\n'
    jieba_lines = jieba_words.split('\n')[:-1]
    jieba_words = []
    for jieba_line in jieba_lines:
        jieba_words.append(jieba_line.split(' '))
    print(jieba_words)
    with open(r"data\fakeData_jieba.txt", "w", encoding="utf-8") as fh:
        fh.write(str(jieba_words))
    jieba_word = [x for words in jieba_words for x in words]
    word2idx={}
    for word in jieba_word:
        i = len(word2idx)+1
        if word in word2idx.keys():
            pass
        else:
            word2idx[word] = i

    print(word2idx)
    idx2word = {idx: word for word, idx in word2idx.items()}
    print(idx2word)

    with open(r"data\fakeData_word2idx.txt", "w", encoding="utf-8") as fh:
        fh.write(str(word2idx))
    with open(r"data\fakeData_idx2word.txt", "w", encoding="utf-8") as fh:
        fh.write(str(idx2word))

def word2idx():
    with open(r"data\fakeData_word2idx.txt", "r", encoding="utf-8") as fh:
        word2idx = eval(fh.read())
    with open(r"data\fakeData_jieba.txt", "r", encoding="utf-8") as fh:
        words = eval(fh.read())
    idxs = []
    for line_words in words:
        idx = []
        for word in line_words:
            idx.append(word2idx[word])
        idxs.append(idx)
    with open(r"data\fakeData_idx.txt", "w", encoding="utf-8") as fh:
        fh.write(str(idxs))

word2idx()