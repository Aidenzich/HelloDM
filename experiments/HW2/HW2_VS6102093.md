# HW2 VS6102093 葉家任
- 主題：模擬基金交易，參數會來自於用戶與基金上，最終只會有兩種結果：
    - 買進基金
    - 不買進基金
- 分類基準，如果此分類器要有效我們需假設用戶購買基金的行為可以用函式來進行預測，此處我們假定該函式為經過以下計算得出一值
    ```python=
    ((df.local_total / df.value) + (df.local_demand_deposit ** 2) - (df.guaranteed ** 1.5 ** df.value_diff)) /df.foreign_total + random.random()
    ```
    - 如果此值介於0.097 與 1.2 之間，那麼該用戶就會購買該基金
    - 為模擬真實狀況的未知影響，加入random來決定該值
## 參數設置一欄

| 參數名 | 描述|
|---|---|
| local_total | 用戶本地存款 (介於之間) |
| foreign_total | 用戶外匯存款 (介於之間) |
| monthly_trade_vol | 用戶月交易額 (介於之間) |
| stock_inventory_val | 用戶股票存貨(介於之間) |
| invest_type | 投資風險類型 |
| age | 年紀 |
| KPI | 銀行kpi指數 |
| region | 基金發行地區 |
| fund_type | 基金風險類型 |
| AUM | 基金AUM類型 |
| local_or_foreign | 本地與外地存值 |
| guaranteed | 是否保證贖回 |
| realized_gain_loss | 已實現損益 |
| unrealized_gain_loss | 未實現損益 |
| local_demand_deposit | 本地活存 |
| local_fixed_deposit | 本地定存 |
| value | 基金價值 |
| value_diff | 基金變動值 |

## 使用 Decision Tree 與 Gradient Boosting 來進行分類
- 因為產生規則只是一個線性方程，因此預期模型可以達到不錯的分類成果
- 有趣的是，在此規則下，提高max_feature雖然能達成更好的準確率，但召回率反而下降了
    | max_features | accuracy_score | recall_score |
    |---|---|---|
    | 14 | 0.9912 | 0.997092281793603 |
    | 10 | 0.9883 | 0.9994898739988777 |
    | 5 | 0.9828 | 0.9981125337958475 |
- 因此我們可以得知，根據我們的評量方式的不同，調整參數的目標與結果都會有所不同，需要多多留意！
- e.g. 此為決策樹在各個不同參數的結果
    ```json=
    {
        'model_score': 0.9822375,
         'accuracy_score': 0.98285,
         'f1_score': 0.9913109563014566,
         'precision_score': 0.9846014492753623,
         'recall_score': 0.9981125337958475
     }
    ```
- 另外採用GradientBoosting的分類器，得出無論是在正確率還是召回率都更勝決策數分類器的結果
    ```json=
    {
        'model_score': 0.9919125,
         'accuracy_score': 0.9912,
         'f1_score': 0.9955179790159926,
         'precision_score': 0.9939486397152301,
         'recall_score': 0.997092281793603
    }
    ```