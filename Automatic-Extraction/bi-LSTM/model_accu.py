import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os
import jieba

#随机数固定，老哥稳！
torch.manual_seed(1)


class LSTMTagger(nn.Module):

    def __init__(self, embedding_dim, hidden_dim, vocab_size, tagset_size):
        super(LSTMTagger, self).__init__()
        self.hidden_dim = hidden_dim

        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)

        # LSTM以word_embeddings作为输入, 输出维度为 hidden_dim 的隐藏状态值
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, bidirectional=True)

        # 线性层将隐藏状态空间映射到标注空间
        self.hidden2tag = nn.Linear(hidden_dim * 2, tagset_size)
        self.hidden = self.init_hidden()

    def init_hidden(self):
        # 一开始并没有隐藏状态所以我们要先初始化一个
        # 关于维度为什么这么设计请参考Pytoch相关文档
        # 各个维度的含义是 (num_layers, minibatch_size, hidden_dim)
        return (torch.zeros(1 * 2, 1, self.hidden_dim),
                torch.zeros(1 * 2, 1, self.hidden_dim))

    def forward(self, sentence):
        embeds = self.word_embeddings(sentence)
        lstm_out, self.hidden = self.lstm(
            embeds.view(len(sentence), 1, -1), self.hidden)
        tag_space = self.hidden2tag(lstm_out.view(len(sentence), -1))
        tag_scores = F.log_softmax(tag_space, dim=1)
        return tag_scores

model = torch.load('bilstm_realDataXie.pkl')

#输入[1,2,3,...],输出预测的[0,0,1,...]
def train_data(input):
    with torch.no_grad():
        inputs = torch.tensor(input)#training_data[0][0])
        tag_scores = model(inputs)
        output = []
        for two_value in tag_scores:
            if two_value[0].item() > two_value[1].item():
                output.append(0)
            else:
                output.append(1)
    return output

#'''
input_file = r'xie_data\\xie_x.txt'
output_file = r'xie_data\\xie_y.txt'
with open(input_file, 'r', encoding='utf-8') as fh:
    input_all = eval(fh.read())
with open(output_file, 'r', encoding='utf-8') as fh:
    output_all = eval(fh.read())

print(len(input_all), len(output_all))
y_hat = []
count = 0
#遍历测试集，应该改成矩阵形式才行，但我懒得弄惹，下次吧
for input1 in input_all:
    count += 1
    if count % 20 == 0:
        print(count, '/', len(input_all))
    output = train_data(input1)
    y_hat.append(output)
#'''


with open(
        r"E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\\xie0-4_19-23\\all_sentences\idx2word.txt",
        "r", encoding="utf-8") as fh:
    idx2word = eval(fh.read())
#参数是预测的y_hat，以及对应的y存的地址
def cal_accu(input_all, y_hat,y):

    sum = len(y_hat)
    count = 0
    for i in range(sum):
        if y[i] == y_hat[i]:
            count += 1
    accu_rate = float(count/sum*100)
    return accu_rate

#'''
accu_rate = cal_accu(input_all, y_hat, output_all)
print("测试集句数：", sum, "\n准确率：", accu_rate)
#'''

#瞎掰一句话测试
'''
line = "小S看到林俊杰兴致一来突然跳到他身上，而他也很有默契地接住，让小S<keyword>开心</keyword>地Z说，“没想到我们这麽有默契，他下盘好有力X"
line = line.replace('<keyword>', '')
line = line.replace('</keyword>', '')
line = line.replace('Z', '')
line = line.replace('X', '')
line = list(jieba.cut(line))
print(line)
with open(
        r"E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\\xie0-4_19-23\\all_sentences\word2idx.txt",
        "r", encoding="utf-8") as fh:
    word2idx = eval(fh.read())
line_idx = []
for i in line:
    print(line.index(i), i)
    line_idx.append(word2idx[i])
y_hat = train_data(line_idx)
print(y_hat)
'''
