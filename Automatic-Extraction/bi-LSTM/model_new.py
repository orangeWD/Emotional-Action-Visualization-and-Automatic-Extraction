#bi-LSTM
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

#随机数固定，老哥稳！
torch.manual_seed(1)

#读入training_data    格式 [(input, output)]
with open(r"data\fakeData_input.txt", "r", encoding="utf-8") as fh:
    inputs = eval(fh.read())
with open(r"data\fakeData_output.txt", "r", encoding="utf-8") as fh:
    outputs = eval(fh.read())
training_data = []
for inp, outp in zip(inputs, outputs):
    training_data.append((inp, outp))
'''
training_data格式    [(input, output)]
training_data = [
    ([1, 2, 3, 4, 5], [0, 1, 0, 0, 1]),
    ([1, 4, 6, 7], [1, 0, 0, 1])
]
'''


def train_model(training_data):
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
    EMBEDDING_DIM = 120     #模型生成的词向量的维度
    HIDDEN_DIM = 120        #隐藏神经元个数？

    with open(r"data\fakeData_word2idx.txt", "r", encoding="utf-8") as fh:
        word2idx = eval(fh.read())

    model = LSTMTagger(EMBEDDING_DIM, HIDDEN_DIM, len(word2idx)+1, 2)#后两个参数是不同的词语个数(?怎么说啊)，输出的维度(这里只有0 1，所以是2)
    loss_function = nn.NLLLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    # 查看训练前的分数
    # 注意: 输出的 i,j 元素的值表示单词 i 的 j 标签的得分
    # 这里我们不需要训练不需要求导，所以使用torch.no_grad()
    with torch.no_grad():
        inputs = torch.tensor(training_data[0][0])
        print(inputs)
        tag_scores = model(inputs)
        print(tag_scores)

    for epoch in range(300):  # 实际情况下你不会训练300个周期, 此例中我们只是随便设了一个值
        if epoch%5 == 0:      #输出进度
            print(epoch/5, '/', 300/5)
        for sentence, tags in training_data:
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
    print(sentence_in, targets)

    torch.save(model, 'lstm_fakedata.pkl')

#load已经训练好的模型
model = torch.load('lstm_fakedata.pkl')
# 查看训练后的得分
y_hat = []

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

#遍历测试集，应该改成矩阵形式才行，但我懒得弄惹，下次吧
for input, _ in training_data:
    output = train_data(input)
    # 句子是 "the dog ate the apple", i,j 表示对于单词 i, 标签 j 的得分.
    # 我们采用得分最高的标签作为预测的标签. 从下面的输出我们可以看到, 预测得
    # 到的结果是0 1 2 0 1. 因为 索引是从0开始的, 因此第一个值0表示第一行的
    # 最大值, 第二个值1表示第二行的最大值, 以此类推. 所以最后的结果是 DET
    # NOUN VERB DET NOUN, 整个序列都是正确的!

    y_hat.append(output)

#参数是预测的y_hat，以及对应的y存的地址
def cal_accu(y_hat,output_file_path):
    with open(output_file_path, "r", encoding="utf-8") as fh:
        y = eval(fh.read())
    sum = len(y_hat)
    count = 0
    for i in range(sum):
        if y[i] == y_hat[i]:
            count += 1
    accu_rate = count/sum*100
    return accu_rate


accu_rate = cal_accu(y_hat, r"data\fakeData_output.txt")
print("测试集句数：", sum, "\n准确率：", accu_rate)
#自己瞎掰了一句话，看看标的怎么样
print("小女孩 生气 得 把 手机 扔 了", "57,10,23,42,27,8", "0,0,0,1,1,1,1")
input = [57, 10, 23, 42, 27, 8]
print(train_data(input))