#!/bin/python

import pandas
import copy
import itertools
from collections import defaultdict


class Item(object):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __eq__(self, other):
        assert isinstance(other, Item)
        return self.field == other.field

    def __lt__(self, other):
        assert isinstance(other, Item)
        if self.field == other.field:
            return self.value < other.value
        else:
            return self.field < other.field

    def __le__(self, other):
        assert isinstance(other, Item)
        if self.field == other.field:
            return self.value <= other.value
        else:
            return self.field <= other.field

    def __ne__(self, other):
        assert isinstance(other, Item)
        if self.field == other.field:
            return self.value != other.value
        else:
            return self.field != other.field

    def __gt__(self, other):
        assert isinstance(other, Item)
        if self.field == other.field:
            return self.value > other.value
        else:
            return self.field > other.field

    def __ge__(self, other):
        assert isinstance(other, Item)
        if self.field == other.field:
            return self.value >= other.value
        else:
            return self.field >= other.field
 
    def __hash__(self):
        return hash(self.field)

    def __str__(self):
        return '(%s, %s)' % (self.field, str(self.value))

    def __repr__(self):
        return '(%s, %s)' % (self.field, str(self.value))


class Itemset(object):
    def __init__(self, iterable):
        for t in itertools.combinations(iterable, 2):
            assert isinstance(t[0], Item)
            assert isinstance(t[1], Item)
            assert not t[0] == t[1], "Trying to merge %s and %s in same Itemset" % (t[0], t[1])
        self.items = frozenset([copy.deepcopy(i) for i in iterable])

    @property
    def fields(self):
        return [i.field for i in sorted(self.items)]

    @property
    def values(self):
        return tuple([i.value for i in sorted(self.items)]) if len(self) > 1 \
                else sorted(self.items)[0].value

    def __contains__(self, item):
        return item in self.items
   
    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return str(self.items)

    def __iter__(self):
        return self.items.__iter__()

    def __eq__(self, other):
        return self.items == other.items

    def __hash__(self):
        return sum([hash(i.field) + hash(i.value) for i in self.items])

       

class Apriori_Itemsets(object):
    """Implementation of apriori algorithm according to Han, Kamber, Pei
       (2006).  Data Mining: Concept and Techniques.  Morgan Kaufmann, p.253.
       
       Some modifications to the algorithm were necessary in order to deal
       with particular features of the data set at hand.  Mostly these are
       apparent in the Item and Itemset classes above.  A casual reading should
       look just like what is found in the text.
    """
    def __init__(self, datafile, fields, min_sup):
        self._data = pandas.read_csv(datafile, header=0, sep='<')
        self._fields = fields
        self._min_sup = min_sup
        self._L = defaultdict(list)

        #next 2 lines get frequent 1-itemsets
        L1 = get_1itemsets(self._data, self._fields)   # get 1-item sets
        self._L[1] = prune(L1, self._data, self._min_sup)
        k = 2
        while self._L[k-1]:
            # generate candidate k-itemsets
            Ck = apriori_gen(self._L[k-1])
            # prune step
            self._L[k] = prune(Ck, self._data, self._min_sup)
            k += 1

    @property
    def itemsets(self):
        return self._L



def support_count(itemset, data):
    dfview = data.groupby(itemset.fields)
    try:
        return dfview.size()[itemset.values]
    except KeyError:
        return 0

def get_1itemsets(data, fields):
    L = list()
    for field in fields:
        for value in data[field].unique():
            if pandas.isnull(value):
                continue
            item = Item(field, value)
            L.append(Itemset([item]))
    return L

def apriori_gen(L):
    C_k = set()
    for itemset1 in L:
        for itemset2 in L:
            c = joinable(itemset1, itemset2)
            if c and not has_infrequent_subset(c, L):
                C_k.add(c)
    return list(C_k)

def prune(L, data, min_sup):
    return [i for i in L if support_count(i, data) >= min_sup]

def joinable(itemset1, itemset2):
    assert len(itemset1) == len(itemset2)
    diff = itemset2.items - itemset1.items
    if len(diff) is not 1:
        return None
    return Itemset(list(itemset1) + list(diff))

def has_infrequent_subset(c, L):
    assert len(c) == len(L[0]) + 1, "%s not compatible with %s" % (str(c), str(L))
    kmin1 = len(c) - 1
    for ss in [Itemset(t) for t in itertools.combinations(c.items, kmin1)]:
        if ss not in L:
            return True
    return False


if __name__ == "__main__":
    import pickle
    """
    a = Apriori_Itemsets('../values.csv', ['instpartno', 'rmvdpartno', 'wccode', 'wuc', 'rmvdniin', 'sss'], 100000)
    with open('/home/bokinsky/822CSCE/Apriori/ms100000.pkl', 'w') as f:
        pickle.dump(a, f)
    
    a = Apriori_Itemsets('../values.csv', ['instpartno', 'rmvdpartno', 'wccode', 'wuc', 'rmvdniin', 'sss'], 10000)
    with open('/home/bokinsky/822CSCE/Apriori/ms10000.pkl', 'w') as f:
        pickle.dump(a, f)

    a = Apriori_Itemsets('../values.csv', ['instpartno', 'rmvdpartno', 'wccode', 'wuc', 'rmvdniin', 'sss'], 1000)
    with open('/home/bokinsky/822CSCE/Apriori/ms1000.pkl', 'w') as f:
        pickle.dump(a, f)
 
    a = Apriori_Itemsets('../values.csv', ['instpartno', 'rmvdpartno', 'wccode', 'wuc', 'rmvdniin', 'sss'], 100)
    with open('/home/bokinsky/822CSCE/Apriori/ms100.pkl', 'w') as f:
        pickle.dump(a, f)
    """
    pass
