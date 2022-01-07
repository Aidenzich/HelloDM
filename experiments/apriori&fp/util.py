import numpy as np
import pandas as pd
import time
from itertools import combinations
from itertools import chain, combinations
from tqdm import tqdm

def association_rules(df, min_support=0.1, min_conf = 0.0):
    metric_dict = {
        "from_support": lambda _, sA, __: sA,
        "to_support": lambda _, __, sC: sC,
        "support": lambda sAC, _, __: sAC,
        "confidence": lambda sAC, sA, _: sAC/sA,
    }

    columns_ordered = ["from_support", "to_support",
                       "support",
                       "confidence"
                       ]

    # get dict of {frequent itemset} -> support
    keys = df['itemsets'].values
    values = df['support'].values
    frozenset_vect = np.vectorize(lambda x: frozenset(x))
    frequent_items_dict = dict(zip(frozenset_vect(keys), values))

    # prepare buckets to collect frequent rules
    rule_from = []
    rule_to = []
    rule_supports = []

    # iterate over all frequent itemsets
    for k in frequent_items_dict.keys():
        sAC = frequent_items_dict[k]
        # to find all possible combinations
        for idx in range(len(k)-1, 0, -1):
            # of antecedent and consequent
            for c in combinations(k, r=idx):
                antecedent = frozenset(c)
                consequent = k.difference(antecedent)                
                sA = frequent_items_dict[antecedent]
                sC = frequent_items_dict[consequent]

                if (metric_dict["support"](sAC, sA, sC) >= min_support) and  (
                    metric_dict["confidence"](sAC, sA, sC) >= min_conf):
                    rule_from.append(antecedent)
                    rule_to.append(consequent)
                    rule_supports.append([sAC, sA, sC])



    # check if frequent rule was generated
    if not rule_supports:
        return pd.DataFrame(
            columns=["from", "to"] + columns_ordered)

    else:
        # generate metrics
        rule_supports = np.array(rule_supports).T.astype(float)
        df_res = pd.DataFrame(
            data=list(zip(rule_from, rule_to)),
            columns=["from", "to"])
        
        sAC = rule_supports[0]
        sA = rule_supports[1]
        sC = rule_supports[2]
        for m in columns_ordered:
            df_res[m] = metric_dict[m](sAC, sA, sC)
        return df_res
    

def subsets_by_len(dataframe: pd.DataFrame):            
    all_subset_lists = dataframe.item.apply(lambda x: tuple(powerset(x))).unique()
    all_subsets = []
    len_subsets = {}
    for subsets in all_subset_lists:    
        all_subsets = all_subsets + list((set(subsets) - set(all_subsets)))
    # Group subsets by length
    for subsets in all_subsets:
        try:
            len_subsets[len(subsets)].append(subsets)
        except:
            len_subsets[len(subsets)] = [subsets]
    return len_subsets

def list_contains(BigList, SmallList):   
    # return true if Smallset is in Bigset
    Bigset = set(BigList)
    Smallset = set(SmallList)     
    return all(item in Bigset for item in Smallset)

def count_item(origin_value_counts, c_item_set, init=False):
    # count the appearance of itemset
    total = origin_value_counts.sum()
    itemset_count = []
    for c in c_item_set:
        if (init):
            c = tuple([c])
        count = 0
        for items in origin_value_counts.index.tolist():        
            items = tuple(sorted(items))                        
            if list_contains(items, c):                 
                count += origin_value_counts[items]                
        itemset_count.append(count/total)
    return itemset_count


def check_all_subset_inside(df_item_set_list, itemset_list, length):
    c_item_set = []
    for sets in tqdm(itemset_list):
        sets = tuple(sorted(sets))
        if (length - 2) > 0:
            subsets = list(combinations(sets, length - 1))
        else:
            subsets = list(sets)        
        if list_contains(df_item_set_list, subsets):
            c_item_set.append(sets)
    return c_item_set

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1) if r != 0)
    
def init_min_sup(data, min_support:float):
    c_item_set = []
    origin_itemset_valcount = data.item.value_counts()
    for i in data.item:
        new_elems = list(i)
        c_item_set = c_item_set + list((set(new_elems) - set(c_item_set)))
    
    df = pd.DataFrame({
        "item": c_item_set,
        "support": count_item(origin_itemset_valcount, c_item_set, init=True)
    })
    
    df.drop(df[df.support < min_support].index, inplace=True) # prune
    return df

def transaction_to_df(transaction_df):
    # transform transaction_df to onehot-like form
    X = transaction_df.item.tolist()
    unique_items = set()
    for transaction in X:
        for item in transaction:
            unique_items.add(item)
    columns_ = sorted(unique_items)
    columns_mapping = {}
    for col_idx, item in enumerate(columns_):
        columns_mapping[item] = col_idx
    columns_mapping_ = columns_mapping
    array = np.zeros((len(X), len(columns_)), dtype=bool)
    for row_idx, transaction in enumerate(X):
        for item in transaction:
            col_idx = columns_mapping_[item]
            array[row_idx, col_idx] = True
    df = pd.DataFrame(array)
    df.columns = columns_
    return df

def timer(func):
    def wrapper( *args , **kwargs ):
        s = time.perf_counter()
        v = func( *args , **kwargs )
        e = time.perf_counter()
        print(f"{func.__name__} takes {round((e-s)*1000)} ms.")
        return v
    return wrapper