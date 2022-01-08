# How to preprocess datas with Pandas
## Example Data Structure
```
data
├── crm.csv
├── fund_info.py
├── trans_stock.py
└── trans_buy.py
```

## 技巧
1. 針對各個檔案先做資料清洗後再做合併運用
2. 每個動作都要導出做儲存，方便下次使用
3. 針對過大的資料集，採用批次處理
   1. 同時注意記憶體上限，`merge`方式會佔用大量記憶體，可能會被系統環境killed掉
4. 在Python中，盡可能使用Pandas 或 Numpy 來執行迴圈