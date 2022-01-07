# def apriori(data, min_support:float, max_length):
#     data = transaction_to_df(data)
#     subsets_len_dict = subsets_by_len(data)
#     origin_itemset_valcount = data.item.value_counts()    
    
#     apriori_dict = {}
#     if len(apriori_dict) == 0:
#         apriori_dict[1] = init_min_sup(data, min_support)
    
#     for i in range(max_length + 1):        
#         if i <= 1: continue
#         c_item_set = check_all_subset_inside(apriori_dict[i-1].itemsets, subsets_len_dict[i], i)

#         c = pd.DataFrame({
#             "itemsets": c_item_set,
#             "support": count_item(origin_itemset_valcount, c_item_set)
#         })

#         c.drop(c[c.support < min_support].index, inplace=True)        
#         apriori_dict[i] = c
#     result_df = pd.DataFrame({"itemsets":[], "support":[]})
    
#     for i in apriori_dict:        
#         result_df = result_df.append(apriori_dict[i])

#     result_df.itemsets = result_df.itemsets.apply(lambda x: x if type(x) == tuple else (int(x), ))
    
#     return result_df