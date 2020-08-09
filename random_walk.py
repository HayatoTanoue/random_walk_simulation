import networkx as nx
import pandas as pd
import numpy as np
import random
%matplotlib inline
import matplotlib.pyplot as plt

G = nx.barabasi_albert_graph(10,2)

nx.draw_networkx(G)
plt.axis("off")


#シンプルランダムウォーク
def simple_random_walk(G, walk_length, start_position):
    """
    返り値: list
          ランダムウォークの訪問ノードリスト
          
    Parameters
    ----------
    G : networkx graph
        networkxで作成したgraph, このグラフ上をランダムウォークする。
    
    walk_length : int
                  ランダムウォークのステップ数(歩数)
    
    start_position : int
                     ランダムウォークを開始する位置のノード番号
    ----------
    
    各ノードへの遷移確率が等しい場合のランダムウォーク
    
    """
    
    now = start_position
    length = 0
    
    #訪問ノードリスト
    walk = list()
    
    while length < walk_length:
        
        #接続ノードリストからランダムで一つ選択(等確率)
        selected = np.random.choice(list(G.neighbors(now)))
        
        walk.append(selected)
        
        now = selected
        length += 1
    
    return walk

#選択確率