import pandas as pd
import numpy as np
from util import transaction_to_df


def generate_new_combinations(o_combs):
    # 轉乘一維陣列
    items_types_in_previous_step = np.unique(o_combs.flatten())
    for o_comb in o_combs:
        max_combination = o_comb[-1]
        mask = items_types_in_previous_step > max_combination
        valid_items = items_types_in_previous_step[mask]
        old_tuple = tuple(o_comb)
        for item in valid_items:
            yield from old_tuple
            yield item



def apriori(df, min_support=0.5, use_colnames=False, max_len=None):
    def _support(_x, _n_rows):
        out = (np.sum(_x, axis=0) / _n_rows)
        return np.array(out).reshape(-1)
    
    if min_support <= 0.:
        raise ValueError('min_support is not positive ')

    X = df.values
    support = _support(X, X.shape[0])
    ary_col_idx = np.arange(X.shape[1])
    support_dict = {1: support[support >= min_support]}
    itemset_dict = {1: ary_col_idx[support >= min_support].reshape(-1, 1)}
    max_itemset = 1
    rows_count = float(X.shape[0])

    while max_itemset and max_itemset < (max_len or float('inf')):
        next_max_itemset = max_itemset + 1

        combin = generate_new_combinations(itemset_dict[max_itemset])
        combin = np.fromiter(combin, dtype=int)
        combin = combin.reshape(-1, next_max_itemset)

        if combin.size == 0:
            break

        _bools = np.all(X[:, combin], axis=2)

        support = _support(np.array(_bools), rows_count)
        _mask = (support >= min_support).reshape(-1)
        if any(_mask):
            itemset_dict[next_max_itemset] = np.array(combin[_mask])
            support_dict[next_max_itemset] = np.array(support[_mask])
            max_itemset = next_max_itemset
        else:
            break

    all_res = []
    for k in sorted(itemset_dict):
        support = pd.Series(support_dict[k])
        itemsets = pd.Series([frozenset(i) for i in itemset_dict[k]], dtype='object')
        res = pd.concat((support, itemsets), axis=1)
        all_res.append(res)

    res_df = pd.concat(all_res)
    res_df.columns = ['support', 'itemsets']
    if use_colnames:
        mapping = {idx: item for idx, item in enumerate(df.columns)}
        res_df['itemsets'] = res_df['itemsets'].apply(lambda x: frozenset([
                                                      mapping[i] for i in x]))
    res_df = res_df.reset_index(drop=True)


    return res_df