import sys
import pandas as pd
import numpy as np
import os

from module.utils.preprocessor import get_sentences
from module.utils.crowler_collection import get_en_docs, get_ko_docs
from module.dic_converter import convert2xml


ids = [
    "2017021201", 
    "2018121029",
    "2012312312",
    "2018171392"
]

name2path = {
    "ko": "./data/ko-sens",
    "en": "./data/en-sens"
}
name2type = {
    "ko": "keyboard",
    "en": "keyboard"
}
name2size = {
    "ko": 100,
    "en": 100
}


def get_experiments(id_, name):
        
    type_ = name2type[name]
    path = name2path[name]
    size = name2size[name]
    
    datas = np.random.choice(pd.read_pickle(path), size)
    
    challenges = [{"challenge type='"+type_+"'": data} for data in datas]
    experiments = [{"experiment name='"+name+"-"+id_+"'": challenges}]
    
    return experiments

def set_test(ids, names, sample_n):

    experiments = sum([get_experiments(id_, name)
                    for id_ in ids
                    for name in name2path],
                    [])
    
    arrdic = [{"configure": experiments}]
    bs = convert2xml(arrdic)
    
    with open("./data/config.xml", "w") as f:
        f.write(str(bs))


if __name__ == "__main__":


# http://novel.naver.com/webnovel/list.nhn?novelId=126772
# 구르미 그린 달빛 - 윤이수
# http://novel.naver.com/webnovel/list.nhn?novelId=126772
# 광해의 여인 - 유오디아
# http://novel.naver.com/webnovel/list.nhn?novelId=398090
# 해시의 신루 - 윤이수
# http://novel.naver.com/webnovel/list.nhn?novelId=374465
# 원하는 건 너 하나 - 달콤j
# http://novel.naver.com/webnovel/list.nhn?novelId=153308
# 프렌시아의 꽃 - 김레인 
# http://novel.naver.com/webnovel/list.nhn?novelId=2
# 고양이가 있는 서점 - 
    novel_ids = [126772, 4, 398090, 374465, 153308, 2]
    args = [
        {"novel_id": id_, "volume_no": no+1}
        for no in range(7)
        for id_ in novel_ids
    ]


    i = 0
    total_ko_sens = []
    np.random.seed(1050554145)

    while not os.path.isfile("./data/ko-sens"):

        try:
            docs = get_ko_docs(**args[i])
            i += 1
        except:
            continue
        
        sens = sum([get_sentences(doc, "ko", [160, 180]) for doc in docs], [])
        total_ko_sens += sens

        total_len = len(set(total_ko_sens))
        sys.stdout.write("\r% 4d | % 4d" % (i, total_len))
        
        if total_len >= 2000:
            idxs = np.random.choice(total_len, 2000, replace=False)
            total_ko_sens = list(set(total_ko_sens))
            total_ko_sens = np.array(total_ko_sens)[idxs]
            total_ko_sens = total_ko_sens.tolist()
            pd.to_pickle(total_ko_sens, "./data/ko-sens")

        if i == len(args):
            total_ko_sens = list(set(total_ko_sens))
            pd.to_pickle(total_ko_sens, "./data/ko-sens")
            break


    # i = 0
    # total_en_sens = []

    # while not os.path.isfile("./data/en-sens"):

    #     try:
    #         docs = get_en_docs()
    #         i += 1
    #     except:
    #         continue
        
    #     sens = sum([get_sentences(doc, "en", [160, 180]) for doc in docs], [])
    #     total_en_sens += sens

    #     total_len = len(set(total_en_sens))
    #     sys.stdout.write("\r% 4d | % 4d" % (i, total_len))
        
    #     if total_len >= 1000:
    #         total_en_sens = list(set(total_en_sens))
    #         pd.to_pickle(total_en_sens, "./data/en-sens")


    # np.random.seed(1050554145)
    # set_test(ids, ["ko", "en"], 100)