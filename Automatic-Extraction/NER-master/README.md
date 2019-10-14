# NER
## DATA
- 2014 people daily newspaper tagged dataset
- For convience, the preprocessed data is free to download at https://pan.baidu.com/s/17sa7a-u-cDXjbW4Rok2Ntg
## pycrf
- A implement of crf by feature template with pysuite
## 运行步骤

- 将下载语料（上面的链接），解压后放在data里（或者直接用data里的小语料）
- 下载[词向量](https://github.com/Gromy1211/Bilibili-Web-Crawler/blob/master/data/zh.vec)(125MB) 放在embedding里
- 把output/checkpoints/bilstm_ner.ckpt output/img.png output/intermediate/目录下的三个文件删除
- 修改BILSTM+CRF/config/config.py里的文件目录（注意对应）（目前用的6000句的小数据）
- 在NER-master下运行 python .\BILSTM+CRF\test.py 和 python .\BILSTM+CRF\run_bilstm_crf.py

## bilstm_crf

- pytorch 0.4.0
- bilstm + crf

Thanks to the blog of createMoMo for enlightening the implements of crf.

https://createmomo.github.io/2017/09/12/CRF_Layer_on_the_Top_of_BiLSTM_1/

The chinese version of this blog is also available in https://state-of-art.top

If you have any question, please feel free to contact me at circlepi@gmail.com.