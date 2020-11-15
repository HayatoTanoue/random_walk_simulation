# random walk on networkx graph

研究でネットワーク上ランダムウォークのシミュレーションを行った際に作成.  
networkxで作成したグラフ上でのrandom walkシミュレーションを行うための関数.  

# DEMO

シミュレーションを可視化したgifを作成して掲載する(準備中)

# Features

シンプルランダムウォーク以外にも3つのランダムウォークを用意した.

* 次数比例ランダムウォーク  
遷移確率が対象ノードの次数比例して高くなる.  
次数の高いノードを優先的に選択するランダムウォーク

* 次数逆数比例ランダムウォーク  
遷移確率が対称ノードの次数と反比例して低くなる.  
次数の低いノードを優先的に選択するランダムウォーク

# Requirement

* networkx
* numpy

# Author

 作成者 : HayatoTanoue
 所属 : Kochi University of Technology
