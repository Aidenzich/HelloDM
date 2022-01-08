###### tags: `Courses`
# DataMining Notes
## Keywords terminologies
### Maximal Pattern (Maximal Frequent Pattern)
If an itemset is frequent but ==none of its supersets is frequent==, then the itemset is called a maximal pattern. 
### Large Itemset (Freqent Itemset)
- An itemset whose support is greater than or equal to a minsupport threshold.
### Closed Itemset
- An itemset is closed if ==none of it's immediate supersets has the same support== as the itemset.
- supersets's support(e.g. {A,B,D}) > itemset's support(e.g. {A, C})
### Apriori Property
- All non-empty subsets of a frequent itemset must *also be frequent*.
### Information Gain
$$
    GAIN_{split} = Entropy(p) - \{\sum_{i=1}^k \frac{n_i}{n} {Entropy}(i) \}
$$
- Measures Reduction in Entropy achieved because of the split.
- Choose the split that achieves most reduction (maximizes Gain)
- [more](https://hackmd.io/1kWe7lAxTZCGickkXa31YQ####Entropy)
### Ensemble Method
- Construct a set of classifiers from the training data.
- Predict class label of previously unseen records by **aggregating predictions** made by **multiple classifiers**.
- [more](https://hackmd.io/1kWe7lAxTZCGickkXa31YQ#Ensemble-Learning)
### Sequential Pattern
-  A sequential pattern is a ==frequent subsequence== existing in a single sequence or a set of sequences.
### ROC Curve
![roc_curve](https://i.imgur.com/n2iDGUG.png)
- A ***R***eceiver ***O***perating ***C***haracteristic curve.
- It's a graphical plot that illustrates the diagnostic ability of a binary classifier system as its ==discrimination threshold is varied==.
## Criterions
### F1 Measure
$$
    2 \times \frac{precision \times recall}{precision + recall}
$$

- Dice(X, Y):
    - Prove that the F1 is equal to the Dice coefficient of the retrieved and relevant document sets.
    - Prove:
    $$
        \frac{2|X \cap Y|}{|X|+|Y|}
    $$

#### Recall(Sensitivity)
$$
    \frac{TP}{TP+NF}
$$
- ==The fraction of the relevant documents\(R\) which has been retrieved==.
- In all of the relevant documents, how many of them has been retrived.
#### Precision
- The fraction of the retrieved documents which is relevant.
- In all of the retrieved documents, how many of them is relevant.
#### at **break-even point** (R-Precision)
$$
    F1 = P = R
$$
### Confusion Matrix
![](https://i.imgur.com/jC4J8BM.png)
#### False Negative
- Predict the result is negative, but is positive in fact.
#### Precision at K (P@K)
- K is the total number of retrived documents.
- The precision value of the top-k results.
- Calculate for ==only K documents, documents ranked lower than K are ignored==.
- Frequently used in search engine evaluation.
### R-Precision
- R is the total number of relevant documents.
- R precision is the precision at the ***R***-th position in the ranking of results for a query that has R relevant documents.
- Also be called ==break even point==
### Normalize Discounted Cumulative Gain, NDCG
$$
    nDCG_p = \frac{DCG_p}{IDCG_p} 
$$
#### DCG
$$
    DCG_p = rel_1 + \sum_{i=2}^{p} \frac{rel_i}{log_2(i+1)}
$$
- Measures the usefulness or gain of a document based on its position in the result list.
- The gain is accumulated cumulatively.
#### IDCG
$$
    IDCG_p = \sum_{i=1}^{|REL_p|} \frac{rel_i}{log_2(i+1)}
$$
- ***i***deal DCG
- $REL_p$ represents the list of relevant documents (ordered by their relevence) in the corpus up to position p.
### Mean Reciprocal Rank,  MRR
$$
    MRR = \frac{1}{|Q|} \sum_{i=1}^{|Q|}\frac{1}{rank_i}
$$
- The ==multiplicative inverse== of the rank of the **first** correct answer.
- e.g.
    | Query | Results | Rank | MRR |
    |-|-|-|-|
    | 1 | X X O | 3 | 1/3 |
    | 2 | X O X | 3 | 1/2 |
    | 3 | O X X | 3 | 1 |
### Specificity
$$
    Specificity = \frac{TN}{TN+FP}
$$
- ==Negative== [Recall](####Recall)
- The proportion of negatives in a binary classification test which are correctly identified.
## Overfitting & Underfitting
- **bias**: an error from wrong assumptions in the model.
- **variance**: an error from sensitivity to small fluctuations in the training set.
### Overfitting
#### What?
- Low bias, High variance = overfitting
#### Why?
#### How to prevent?
##### Pruning
- [link](https://hackmd.io/1kWe7lAxTZCGickkXa31YQ####Generalization-and-Overfitting)
- Pre-Pruning (Early Stopping Rule)
    - Stop the algorithm before it becomes a fully-grown tree.
- Post-Pruning
    - Grow decision tree to its entirety, trim the nodes of the decision tree in a bottom-up fashion.
##### Dropout
- [link](https://hackmd.io/HVVBQRzHS_KKTLE22cP6Ew#dropout)
### Underfitting
#### What?
- High bias, Low variance = underfitting
#### How?
- Increase the number of datasets and epoch.

---
# Algorithm
## Apriori
### Apriori property
- All non-empty subsets of a frequent itemset must ==*also be frequent*==.

## *FP-growth
- **e.g.**
    | TID |  Items Bought |
    |-|-|
    | 100 | {a, c, d, f, g, i, m, p} |
    | 200 | {a, b, c, f, i, m, o} |
    | 300 | {b, f, h, j, o} |
    | 400 | {b, c, k, s, p} |
    | 500 | {a, c, e, f, l, m, n, p} |
- **Step1. Counter**
    | Item | a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | s|
    |-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
    | Num | 3 | 3 | 4 | 1 | 1 | 4 | 1 | 1 | 2 | 1 | 1 | 1 | 3 | 1 | 2 | 3 | 1 |
- **Step2. Sort with min support**
    - minsupport = 3
    - item count
        | Item | Num |
        |-|-|
        | c | 4 |
        | f | 4 |
        | a | 3 |
        | b | 3 |
        | m | 3 |
        | p | 3 |
    - new itemset
        | TID | Itemset |
        |-|-|
        | 100 | {c, f, a, m, p}|
        | 200 | {c, f, a, b, m}|
        | 300 | {f, b}|
        | 400 | {c, b, p }|
        | 500 | {c, f, a, b, m, p}|
- **Step3. Construct FP-Tree**
 ![FpTree](https://i.imgur.com/5rpNJjG.png)
    - p
     ![](https://i.imgur.com/N1LL0Fw.png)
    - m
      ![](https://i.imgur.com/0mEzoKG.png)
    - b
        ![](https://i.imgur.com/M5ogw92.png)
    - a
        ![](https://i.imgur.com/R8rdY2o.png)
    - f
        ![](https://i.imgur.com/D06JyVE.png)

- **Step4. Find Frequent Patterns**
    | item | Condition Base | Condition FP Tree |
    |-|-|-|
    | p | {c: 3} | p, cp|
    | m | {c, f, a: 3} | m, cm, cf, ca, cam, cfm, fam, cfam|
    | b | {} | b |
    | a | {c, f: 3}| a, ca, fa, cfa |
    | f | {c: 3}|f, cf|

# Clustering


BIRCH, CRUE skip
## K-means
![](https://i.imgur.com/cay2TWg.png)
- Partition objects into k nonempty subsets.
    - K, Number of clusters must be specified.
- Compute mean as ==the centroids of the clusters of the current partition==.
    - Initial centroids are often chosen randomly.
    - Compute ==mean as the centroids== of the clusters of the current partition.
- Relocate each object ==to the nearest cluster==
    - Each point is assigned to the cluster with the closest centroid
### Strength
- Effiecient
    - Complexity O(n\*K\*I\*d)
    - n: number of points
    - K: number of clusters
    - I: number of iterations
    - d: number of attributes
### Weakness
- Only applicable when mean can be defined.
- Need to specify the number of clusters K
- ==Unable to handle noisy data and outliers==.
## hierarchical clustering
- Prodcues a set of neseted clusters organized as as hierachical tree.
- Can be visualized as a dendrogram
- groups similar objects into groups called clusters.
- ==Once the classification has been made, it can not be undone.==
![](https://i.imgur.com/q9a9L0e.png)
### Two Type of hierarchical clustering
- Agglomerative (Buttom up)
    - Start with the indivaidual clusters.
    - Merge the closest pair util only one(k) cluster.
- Divisive(Top Down)
    - Start with one cluster with all-inclusive.
    - Split cluster util each cluster contains a point(or k clusters)
### Time & Space requirements
- $O(N^2)$ when use the proximity matrix.
- $O(N^3)$ in many case.
    - some approaches can reduce to $O(N^2log(N))$

## Naïve Bayes
- [link](https://hackmd.io/G18dRKjTQ9Kr1JbvwMZf5g?view#Bayes%E2%80%99-rule)

