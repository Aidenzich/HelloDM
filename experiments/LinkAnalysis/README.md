# Data Mining HomeWork 3
Name: VS6102093 葉家任

## Implementation detail
The Directory Structure is shown as follows.
```
./
├── datasets/
│   ├── graph_1.txt    
│   ├── graph_2.txt
│   ├── graph_3.txt
│   ├── graph_4.txt
│   ├── graph_5.txt
│   ├── graph_6.txt
│   └── ibm.txt
├── src/
│   ├── graph.py
│   ├── HITS.py
│   ├── PageRank.py
│   ├── path.py
│   ├── SimRank.py
│   └── temp...
└── README.md
```
### Environment
`python 3.8`, `numpy`
### Run Implementation code
#### HITS
- Bash Script
    ```sh=
    $ python src/HITS.py
    $ python src/HITS.py --dataset 1
    $ python src/HITS.py --itr 50
    ```
    - `--dataset` Use to point at specific dataset
    - `--itr` Set number of iterations
- Standard output
    ![stdout_HITS](./img/stdout_HITS.png)
#### PageRank
- Bash Script
    ```sh=
    $ python src/PageRank.py
    ```
- Standard output
    ![stdout_PageRank](./img/stdout_PageRank.png)
#### SimRank
- Bash Script
    ```sh=
    $ python src/SimRank.py
    ```
- Standard output
    ![stdout_SimRank](./img/stdout_SimRank.png)
## Result analysis and discussion
## Computation performance analysis
## Discussion (what you learned from this project and your comments about this project



