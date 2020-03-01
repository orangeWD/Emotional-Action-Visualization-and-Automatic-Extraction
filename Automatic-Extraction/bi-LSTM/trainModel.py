#bi-LSTM
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import pickle
import os

#随机数固定，老哥稳！
torch.manual_seed(1)



with open(
        r"E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\all_sentences\word2idx.txt",
        "r", encoding="utf-8") as fh:
    word2idx = eval(fh.read())

input_file = r'xie_data\xie_x.txt'
output_file = r'xie_data\xie_y.txt'
print(input_file)
#读入training_data    格式 [(input, output)]
with open(input_file, "r", encoding="utf-8") as fh:
    inputs = eval(fh.read())
with open(output_file, "r", encoding="utf-8") as fh:
    outputs = eval(fh.read())
training_data = []
for inp, outp in zip(inputs, outputs):
    training_data.append((inp, outp))
print(len(training_data))
'''
training_data格式    [(input, output)]
training_data = [
    ([1, 2, 3, 4, 5], [0, 1, 0, 0, 1]),
    ([1, 4, 6, 7], [1, 0, 0, 1])
]
'''
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



# 实际中通常使用更大的维度如32维, 64维.
# 这里我们使用小的维度, 为了方便查看训练过程中权重的变化.
EMBEDDING_DIM = 200     #模型生成的词向量的维度
HIDDEN_DIM = 256        #隐藏神经元个数？


#model = LSTMTagger(EMBEDDING_DIM, HIDDEN_DIM, len(word2idx)+1, 2)#后两个参数是不同的词语个数(?怎么说啊)，输出的维度(这里只有0 1，所以是2)
model = torch.load('bilstm_realDataXie.pkl')#载入已有模型
loss_function = nn.NLLLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

'''不看了
# 查看训练前的分数
# 注意: 输出的 i,j 元素的值表示单词 i 的 j 标签的得分
# 这里我们不需要训练不需要求导，所以使用torch.no_grad()
with torch.no_grad():
    inputs = torch.tensor(training_data[0][0])
    print(inputs)
    tag_scores = model(inputs)'''

for epoch in range(30):  # 梯度下降循环次数
    #输出进度
    print(epoch, '/', 30)
    count = 0
    for sentence, tags in training_data:
        count += 1
        if count % 20 == 0:
            print(count/20, len(training_data)/20, epoch/5)
        # 第一步: 请记住Pytorch会累加梯度.
        # 我们需要在训练每个实例前清空梯度
        model.zero_grad()

        # 此外还需要清空 LSTM 的隐状态,
        # 将其从上个实例的历史中分离出来.
        model.hidden = model.init_hidden()

        # 准备网络输入, 将其变为词索引的 Tensor 类型数据
        sentence_in = torch.tensor(sentence)
        targets = torch.tensor(tags)

        # 第三步: 前向传播.
        tag_scores = model(sentence_in)

        # 第四步: 计算损失和梯度值, 通过调用 optimizer.step() 来更新梯度
        loss = loss_function(tag_scores, targets)
        loss.backward()
        optimizer.step()
    torch.save(model, 'bilstm_realDataXie.pkl')



