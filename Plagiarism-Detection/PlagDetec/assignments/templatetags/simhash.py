import sys
import re
import hashlib
import logging
import collections
from itertools import groupby

if sys.version_info[0] >= 3:
    basestring = str
    unicode = str
    long = int


def _hashfunc(x):
    return int(hashlib.md5(x).hexdigest(), 16)


class Simhash(object):

    def __init__(
        self, value, f=64, reg=r'[\w\u4e00-\u9fcc]+', hashfunc=None, log=None
    ):

        self.f = f
        self.reg = reg
        self.value = None

        if hashfunc is None:
            self.hashfunc = _hashfunc
        else:
            self.hashfunc = hashfunc

        if log is None:
            self.log = logging.getLogger("simhash")
        else:
            self.log = log

        if isinstance(value, Simhash):
            self.value = value.value
        elif isinstance(value, basestring):
            self.build_by_text(unicode(value))
        elif isinstance(value, collections.Iterable):
            self.build_by_features(value)
        elif isinstance(value, long):
            self.value = value
        else:
            raise Exception('Bad parameter with type {}'.format(type(value)))

    def _slide(self, content, width=4):
        return [content[i:i + width] for i in range(max(len(content) - width + 1, 1))]

    def _tokenize(self, content):
        content = content.lower()
        content = ''.join(re.findall(self.reg, content))
        ans = self._slide(content)
        return ans
        # segl = jieba.lcut(content)
        # jieba.analyse.set_stop_words('stopword.txt')
        # keywords = jieba.analyse.extract_tags('|'.join(segl), withWeight=True)
        # return keywords

    def build_by_text(self, content):
        features = self._tokenize(content)
        features = {k:sum(1 for _ in g) for k, g in groupby(sorted(features))}
        return self.build_by_features(features)

    def build_by_features(self, features):
        v = [0] * self.f
        masks = [1 << i for i in range(self.f)]
        if isinstance(features, dict):
            features = features.items()
        for f in features:
            if isinstance(f, basestring):
                h = self.hashfunc(f.encode('utf-8'))
                w = 1
            else:
                assert isinstance(f, collections.Iterable)
                h = self.hashfunc(f[0].encode('utf-8'))
                w = f[1]
            for i in range(self.f):
                v[i] += w if h & masks[i] else -w
        ans = 0
        for i in range(self.f):
            if v[i] > 0:
                ans |= masks[i]
        self.value = ans

    def distance(self, another):
        assert self.f == another.f
        x = (self.value ^ another.value) & ((1 << self.f) - 1)
        ans = 0
        while x:
            ans += 1
            x &= x - 1
        return ans


class SimhashIndex(object):

    def __init__(self, objs, f=64, k=2, log=None):
        self.k = k
        self.f = f
        count = len(objs)

        if log is None:
            self.log = logging.getLogger("simhash")
        else:
            self.log = log

        self.log.info('Initializing %s data.', count)

        self.bucket = collections.defaultdict(set)

        for i, q in enumerate(objs):
            if i % 10000 == 0 or i == count - 1:
                self.log.info('%s/%s', i + 1, count)

            self.add(*q)

    def get_near_dups(self, simhash):
        assert simhash.f == self.f

        ans = set()

        for key in self.get_keys(simhash):
            dups = self.bucket[key]
            self.log.debug('key:%s', key)
            if len(dups) > 200:
                self.log.warning('Big bucket found. key:%s, len:%s', key, len(dups))

            for dup in dups:
                sim2, obj_id = dup.split(',', 1)
                sim2 = Simhash(long(sim2, 16), self.f)

                d = simhash.distance(sim2)
                if d <= self.k:
                    ans.add(obj_id)
        return list(ans)

    def add(self, obj_id, simhash):
        assert simhash.f == self.f

        for key in self.get_keys(simhash):
            v = '%x,%s' % (simhash.value, obj_id)
            self.bucket[key].add(v)

    def delete(self, obj_id, simhash):
        assert simhash.f == self.f

        for key in self.get_keys(simhash):
            v = '%x,%s' % (simhash.value, obj_id)
            if v in self.bucket[key]:
                self.bucket[key].remove(v)

    @property
    def offsets(self):
        return [self.f // (self.k + 1) * i for i in range(self.k + 1)]

    def get_keys(self, simhash):
        for i, offset in enumerate(self.offsets):
            if i == (len(self.offsets) - 1):
                m = 2 ** (self.f - offset) - 1
            else:
                m = 2 ** (self.offsets[i + 1] - offset) - 1
            c = simhash.value >> offset & m
            yield '%x:%x' % (c, i)

    def bucket_size(self):
        return len(self.bucket)