import pandas as pd
import time
import json
import matplotlib.pyplot as plt
import seaborn as sns

def dtype_memory_usage(dataframe, dtype_list=['float','int','object']):
    for dtype in dtype_list:
        selected_dtype = dataframe.select_dtypes(include=[dtype])
        mean_usage_b = selected_dtype.memory_usage(deep=True).mean()
        mean_usage_mb = mean_usage_b / 1024 ** 2
        print(f'Average memory usage for {dtype} columns: {mean_usage_mb:03.2f} MB')

def memory_usage(pandas_obj):
    r"""A Quick method to read pandas_obj used memory.
    """
    if isinstance(pandas_obj, pd.DataFrame):
        usage_byte = pandas_obj.memory_usage(deep=True).sum()
    else: 
        usage_byte = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_byte / 1024 ** 2
    return "{:03.2f} MB".format(usage_mb)

def get_cat2id(pandas_series):
    r"""Convert `pandas_series` to a catgories base id dictionary.

    Usually used with below method id2cat.

    Returns
    ========
    dict
        cat2idx dictionary
    list
        catsid list
    """
    cats = pandas_series.astype('category').cat.codes
    cat_dict = dict(zip(pandas_series, cats))
    return cat_dict, cats

def id2cat(cat_dict, idx):
    return list(cat_dict.keys())[list(cat_dict.values()).index(idx)]

def timer(func):
    def wrapper( *args , **kwargs ):
        s = time.perf_counter()
        v = func( *args , **kwargs )
        e = time.perf_counter()
        print(f"{func.__name__} takes {e-s} s.")
        return v
    return wrapper

def readjson2dict(filename):
    filename = filename + ".json"
    with open(filename) as jf:
        json_dict = json.load(jf)
    return json_dict

def heatmap(dataframe):
    """
    This is an Axes-level function and will draw the heatmap into the currently-active Axes if none 
    is provided to the ax argument. Part of this Axes space will be taken and used to plot a colormap,
    unless cbar is False or a separate Axes is provided to cbar_ax.
    """
    corr = dataframe.corr()
    sns.set(rc={'figure.figsize':{11.87, 11.27}})
    sns.heatmap(data=corr, annot=True)

