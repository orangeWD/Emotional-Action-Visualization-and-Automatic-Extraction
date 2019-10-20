'''
#生成x
word2idx_path = r'E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\all_sentences\word2idx.txt'
input_file_path = r'E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\all_sentences\128lines_jieba'
output_x_path = r'E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\all_sentences\x'
inputPath_list = os.listdir(input_file_path) #列出文件夹下所有的目录与文件
for inputPath in inputPath_list:
        print(inputPath)
        input_path = input_file_path + '\\' + inputPath
        output_path = output_x_path + '\\' + inputPath
        save_x(word2idx_path, input_path, output_path)

#生成word2idx, idx2word
input_file_path = r'E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\all_sentences\128lines_jieba'
output_w2i_path = r'E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\all_sentences\word2idx.txt'
output_i2w_path = r'E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\all_sentences\idx2word.txt'
inputPath_list = os.listdir(input_file_path) #列出文件夹下所有的目录与文件
lines = []
for inputPath in inputPath_list:
        with open(input_file_path + '\\' + inputPath, 'r' ,encoding="utf-8") as fh:
            lines += eval(fh.read())
word_and_idx(lines, output_w2i_path, output_i2w_path)

#生成y_hat
input_file_path = r'E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\all_sentences\128lines_jieba'
output_yHat_path = r'E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\all_sentences\y_hat'
inputPath_list = os.listdir(input_file_path) #列出文件夹下所有的目录与文件
for inputPath in inputPath_list:
        print(inputPath)
        input_path = input_file_path + '\\' + inputPath
        output_path = output_yHat_path + '\\' + inputPath
        save_y(input_path, output_path)

#分词
input_file_path = r'E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\all_sentences\128lines'
jieba_output = r'E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\all_sentences\128lines_jieba'
inputPath_list = os.listdir(input_file_path) #列出文件夹下所有的目录与文件

for inputPath in inputPath_list:
    print(inputPath)
    input_path = input_file_path + '\\' + inputPath
    output_path = jieba_output + '\\' + inputPath
    save_wordcut(input_path, output_path)

#简单处理了一下num_emotion的文件，当时是脑袋进了多少水才会存成那么麻烦的文件啊

#把标了和删了的句子合一块儿，完事了 文件是
oriInput_path = r"E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\all_sentences\ori_input.txt"
inputFile_path = r"E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\mark_results"
outputFile_path = r"E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\all_sentences"
list_inPath = os.listdir(inputFile_path) #列出文件夹下所有的目录与文件

with open(r"E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\num_emotion.txt", 'r', encoding='utf-8') as fh:
    emotionList = (fh.read()).split('\n')
emotionDict = {}
for item in emotionList:
    if len(item) < 1:
        continue
    temp = item.split('   ')
    emotionDict[temp[0]] = temp[1]
print(emotionDict)
with open(r"E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\num_emotion.txt", 'w', encoding='utf-8') as fh:
    fh.write(str(emotionDict))
# 要考虑到一个句子里有多个情感关键词的情况
# 设置一下自己放有标好的文件和ori文件的文件夹，再设置输出文件夹就行啦
with open(r"E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\num_emotion.txt",
          'r', encoding='utf-8') as fh:
    emotionDict = eval(fh.read())
output_line = []
for i in range(int(len(list_inPath)/2)):
    print(i)
    try:
        with open(inputFile_path+'\\'+list_inPath[i], 'r', encoding='utf-8') as fh:
            exa_lines = (fh.read()).split('\n')
    except Exception as e:
        with open(inputFile_path+'\\'+list_inPath[i], 'r', encoding='gbk') as fh:
            exa_lines = (fh.read()).split('\n')
    try:
        with open(inputFile_path+'\\'+list_inPath[i+int(len(list_inPath)/2)], 'r', encoding='utf-8') as fh:
            lines = (fh.read()).split('\n')
    except Exception as e:
        with open(inputFile_path+'\\'+list_inPath[i+int(len(list_inPath)/2)], 'r', encoding='gbk') as fh:
            lines = (fh.read()).split('\n')
    for num_line in range(100):
        emotion_num = (re.findall(r"emotion-(.+?) ", list_inPath[i]))[0]
        emotion = '<keyword>' + emotionDict[emotion_num] + '</keyword>'
        emotions = re.findall(r"(<keyword>.+?</keyword>)", lines[num_line])
        emotions.remove(emotion)
        for emotion1 in emotions:
            temp_emotion = (re.findall(r"<keyword>(.+?)</keyword>", emotion1))[0]
            print("其他情感词：", temp_emotion, "目标情感词：", emotion)
            lines[num_line] = lines[num_line].replace(emotion1, temp_emotion)
            exa_lines[num_line] = exa_lines[num_line].replace(emotion1, temp_emotion)
        if exa_lines[num_line] != '':
            output_line.append(exa_lines[num_line])
            print(exa_lines[num_line][:5], lines[num_line][:5])
        else:
            output_line.append(lines[num_line])
with open(outputFile_path + r'\ori_input.txt', 'w', encoding='utf-8') as fh:
    for i in range(len(output_line)):
        fh.write(output_line[i])
        if i == len(output_line)-1:
            continue
        fh.write('\n')


#把所有句子打乱顺序，按128个一组，存成单独的文本文件



raw_input = outputFile_path + r'\ori_input.txt'
output_path = r'E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\all_sentences\128lines'
with open(raw_input, "r", encoding="utf-8") as fh:
    all_lines = (fh.read()).split('\n')
random.shuffle(all_lines)
for i in range(int(len(all_lines)/128)):
    print(i)
    with open(output_path + '\\' + str(i) + r'.txt', "w", encoding="utf-8") as fh:
        for j in range(128):
            fh.write(all_lines[i*128+j])
            if j ==127:
                continue
            fh.write('\n')
if len(all_lines) % 128 != 0:
    print('left sentences', len(all_lines) % 128)
    with open(output_path + '\\' + str(i+1) + r'.txt', "w", encoding="utf-8") as fh:
        for j in range(len(all_lines) % 128):
            fh.write(all_lines[i * 128 + j])
            if j == (len(all_lines) % 128 - 1):
                continue
            fh.write('\n')
'''
