ROOT_DIR = 'D:/文档/Projects/标注规则/NER-MASTER/'
TRAIN_FILE = 'output/intermediate/train.json'
VALID_FILE = 'output/intermediate/valid.json'
RAW_SOURCE_DATA = 'data/test_source.txt'
RAW_TARGET_DATA = 'data/test_target.txt'

WORD2ID_FILE = 'output/intermediate/word2id.pkl'
EMBEDDING_FILE = 'embedding/zh.vec'#peopel_paper_min_count_1_window_5_300d.word2vec'
LOG_PATH = 'output/logs'

checkpoint_dir = 'output/checkpoints/bilstm_ner.ckpt'
plot_path = 'output/images/img'


# -----------PARAMETERS----------------
tag_to_ix = {
    "B_PER": 0,   # 人名
    "I_PER": 1,
    "B_LOC": 2,   # 地点
    "I_LOC": 3,
    "B_ORG": 4,   # 机构
    "I_ORG": 5,
    "B_T": 6,     # 时间
    "I_T": 7,
    "O": 8,       # 其他
    "SOS": 9,     # 起始符
    "EOS":10      # 结束符
    
    # "B_HAP": 0,   # 开心
    # "I_HAP": 1,
    # "B_SAD": 2,   # 难过
    # "I_SAD": 3,
    # "B_ANG": 4,   # 生气
    # "I_ANG": 5,
    # "B_FEA": 6,     # 害怕
    # "I_FEA": 7,
    # "B_DIS": 8,     # 讨厌
    # "I_DIS": 9,
    # "B_SUR": 10,     # 惊讶
    # "I_SUR": 11,
    # "O": 12,       # 其他
    # "SOS": 13,     # 起始符
    # "EOS":14      # 结束符
}

labels = [i for i in range(0, 9)]

flag_words = ['<pad>', '<unk>']
max_len = 100
vocab_size = 10000
is_debug = False

# ------------NET　PARAMS----------------
use_mem_track = False
device = 0
use_cuda = True
word_embedding_dim = 300
batch_size = 128
cell_type ='GRU'
dropout = 0.5
num_epoch = 4
lr_decay_mode = 'custom_decay'
initial_lr = 0.001