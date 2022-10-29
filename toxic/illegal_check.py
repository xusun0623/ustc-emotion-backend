from .config import SystemConfig, FastTextConfig
from .preprocess import TradToSimple, word_segment
from .ac import AhocorasickNer
from .models.fasttext_model import FastText
from .api import toxic_type

config = SystemConfig()
f2s = TradToSimple(config.trad2simple_file)
illegal_match = AhocorasickNer()
illegal_match.add_keywords(config.illegal_dicts_file)
suspected_illegal_match = AhocorasickNer()
suspected_illegal_match.add_keywords_by_file(config.suspected_illegal_dicts_file)

ft_config = FastTextConfig()
fasttext_model = FastText(ft_config, train=False)


def check(text):
    """
    检测文本中是否有违规内容
    :param text: str
    :return:bool, True: 存在违规内容，False:不存在违规内容
    """
    # 繁简转换
    text = f2s.transform_sentence(text)

    # 违规关键词匹配
    if illegal_match.match_results(text):
        return toxic_type(text)

    # 疑似违规关键词匹配
    suspect_illegal = False
    if suspected_illegal_match.match_results(text):
        suspect_illegal = True
    # fasttext 分类
    fasttext_check = False
    words = word_segment(text)
    pred = fasttext_model.predict(' '.join(words))
    if pred == '__label__1':
        fasttext_check = True
    # print(suspect_illegal)
    # print(fasttext_check)
    if suspect_illegal or fasttext_check:
        return toxic_type(text)
    else:
        return -1


if __name__ == '__main__':
    print(check("那个男的是真tm前凸后翘"))


