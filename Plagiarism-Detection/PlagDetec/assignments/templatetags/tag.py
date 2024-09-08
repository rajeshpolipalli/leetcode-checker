from django import template
import jieba.analyse
import numpy as np
import math
from .simhash import Simhash
from .ac import aho_corasick
import re


register = template.Library()


@register.simple_tag
def get_hw_title(n, hws):
    return hws[n].hw_title


@register.assignment_tag
def get_seg_list(n, hws):
    return jieba.lcut(hws[n].hw_content)


@register.assignment_tag
def get_words(seg_list1, seg_list2):
    return list(set(seg_list1).union(seg_list2))


@register.assignment_tag
def get_zero_list(words):
    return [0] * len(words)


@register.assignment_tag
def get_tf_dict(words, zero_list):
    return dict(zip(words, zero_list))


@register.simple_tag
def tf_increment(tf_dict, word):
    tf_dict[word] += 1
    return None


@register.assignment_tag
def get_vec(tf_dict):
    return [tf_dict[f] for f in tf_dict]


@register.assignment_tag
def get_cos_sim(vec1, vec2):
    num = np.dot(vec1, vec2)
    denom = (np.linalg.norm(vec1)) * (np.linalg.norm(vec2))
    cos = 1 - (math.acos(num / denom) / math.pi * 180) / 90
    return cos


@register.assignment_tag
def get_eu_sim(vec1, vec2):
    vec_a = np.array(vec1)
    vec_b = np.array(vec2)
    eu = np.linalg.norm(vec_a - vec_b)
    return eu


@register.assignment_tag
def get_man_sim(vec1, vec2):
    vec_a = np.array(vec1)
    vec_b = np.array(vec2)
    man = np.sum(np.abs(vec_a - vec_b))
    return man


@register.assignment_tag
def get_jac_sim(vec1, vec2):
    union = len(vec1)
    intersection = len([i for i in range(len(vec1)) if vec1[i] == vec2[i]])
    jac = intersection / union
    return jac


@register.assignment_tag
def get_sd_sim(vec1, vec2):
    num = 2 * len([i for i in range(len(vec1)) if vec1[i] == vec2[i]])

    for i in range(vec1.count(0)):
        vec1.remove(0)
    for i in range(vec2.count(0)):
        vec2.remove(0)

    denom = len(vec1) + len(vec2)
    sd = num / denom
    return sd


@register.assignment_tag
def init_simhash(s):
    simhash_obj = Simhash(s)
    return simhash_obj


@register.assignment_tag
def get_hw_content(n, hws):
    return hws[n].hw_content


@register.filter
def get_sentencecount(content):
    return len(re.split(u'。|？|！', content)) - 1


@register.filter
def get_charcount(content):
    return len(content.encode("utf-8").decode("utf-8"))


@register.assignment_tag
def get_hamming_dis(simhash1, simhash2):
    return simhash1.distance(simhash2)


@register.assignment_tag
def get_hw_id(i, hws):
    return hws[i].id


@register.assignment_tag
def get_sentence_list(content):
    return re.split(u'。|？|！', content)


@register.assignment_tag
def get_stripped_sentence_list(sentence_list):
    return [s.strip() for s in sentence_list]


@register.simple_tag
def list_rem(l, *stop):
    for s in stop:
        while s in l:
            l.remove(s)
    return ''


@register.assignment_tag
def get_len(word_list):
    length = 0
    for word in word_list:
        length += len(word)
    return length


@register.assignment_tag
def get_clean_list(l, *stop):
    for s in stop:
        while s in l:
            l.remove(s)
    return l[:]


@register.assignment_tag
def get_keywords(sentence):
    return jieba.lcut(sentence, cut_all=False)


@register.assignment_tag
def get_matchwords(sentence, keywords):
    return aho_corasick(sentence, keywords)


@register.assignment_tag
def get_ratio(num, denom):
    return num / denom


@register.assignment_tag
def add_sim(sim1, sim2, sim3, sim4):
    s = sim1 + sim2 + sim3 + sim4
    return '{:.2%}'.format(s)


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def divide(value, arg):
    return value / arg


@register.filter
def percent2float(value):
    return float(value.replace('%', '')) / 100


@register.filter
def sim_format(value):
    return '%.2f' % value


















