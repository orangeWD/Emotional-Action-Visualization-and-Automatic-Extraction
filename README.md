# 情感行为可视化及自动抽取


<h1>语料处理</h1>

<b>例句：</b>他非常<keyword>生气</keyword>，Z打了野猪一顿X。

<b>输入：</b>"生气 他非常<keyword>生气</keyword>，打了野猪一顿。"    输出："打了野猪一顿"
（因为有的句子标了两个keyword，所以生气单独放在前面会比较好）

<b>处理输入输出：</b>
应该是以词向量（词向量好难搞哦，惹）的形式作为输入输出。分词-->编号表示-->用词向量表示

# 模型
大概是 输入-->Bi-LSTM(也许还需要attention来把注意力集中到情感词上)-->输出

# 评价模型
1.删除句子的准确度，评价模型能否准确地识别有情感行为存在的句子</br>
2.标注行为的准确度，评价模型能否准确地标注有情感行为的句子
