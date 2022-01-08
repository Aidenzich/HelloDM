## Scaling Dataframe's memory
- Step1. Common ways to quick understand your data.
  - `df.memory_usage(deep=True)`
  - `df_csv.info(memory_usage='deep')`
- Step2. Convert duplicate column data (e.g. email, id...) to index.
  - Use util method `get_cat2id` and `id2cat` like this showcase:
    ```python
      ap2idx, ap_cat = get_cat2id(df.authorPersonId)  # return dict and converted series data
      df.authorPersonId = ap_cat

      del ap_cat                  # delete unnecessary variables

      ap2idx[4340306774493623681] # return 195
      id2cat(ap2idx, 195)         # return 4340306774493623681  
    ```
  - Remember to save dictionary into json file for future works.
    ```python
    dict = {'a':[1,2,3,4]}
    with open('data.json', 'w') as fp:
      json.dump(dict, fp)
    ```
- Step3. 
  - float64 -> float32