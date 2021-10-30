import numpy as np
import pandas as pd
from itertools import combinations
from itertools import chain, combinations
from tqdm import tqdm
def association_rules(df, metric="confidence", min_threshold=0.8):    
    """
    A lighter version of mlxtend/association_rules  
    """
    metric_dict = {
        "antecedent support": lambda _, sA, __: sA,
        "consequent support": lambda _, __, sC: sC,
        "support": lambda sAC, _, __: sAC,
        "confidence": lambda sAC, sA, _: sAC/sA,
        "lift": lambda sAC, sA, sC: metric_dict["confidence"](sAC, sA, sC)/sC,
        }

    columns_ordered = ["antecedent support", "consequent support",
                       "support",
                       "confidence", "lift",
                       ]

    # get dict of {frequent itemset} -> support
    keys = df['itemsets'].values
    values = df['support'].values
    frozenset_vect = np.vectorize(lambda x: frozenset(x))
    frequent_items_dict = dict(zip(frozenset_vect(keys), values))

    # prepare buckets to collect frequent rules
    rule_antecedents = []
    rule_consequents = []
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

                score = metric_dict[metric](sAC, sA, sC)
                if score >= min_threshold:
                    rule_antecedents.append(antecedent)
                    rule_consequents.append(consequent)
                    rule_supports.append([sAC, sA, sC])

    # check if frequent rule was generated
    if not rule_supports:
        return pd.DataFrame(
            columns=["antecedents", "consequents"] + columns_ordered)

    else:
        # generate metrics
        rule_supports = np.array(rule_supports).T.astype(float)
        df_res = pd.DataFrame(
            data=list(zip(rule_antecedents, rule_consequents)),
            columns=["antecedents", "consequents"])
        
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
        "itemsets": c_item_set,
        "support": count_item(origin_itemset_valcount, c_item_set, init=True)
    })
    
    df.drop(df[df.support < min_support].index, inplace=True) # prune
    return df