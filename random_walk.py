import numpy as np
import networkx as nx

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


def select_by_degree(G, now):
    """
    返り値: int
          選択されたノード番号
          
    Parameters
    ----------
    G : networkx graph
    
    now: int
        　現在位置(ノード番号)
    ----------
    各ノードの次数に応じた重み付き抽選
    重み = 対象ノードの次数 / 接続ノードの次数の和
    
    """
    #各接続ノードの次数リスト
    node_degrees = [G.degree(i) for i in list(G.neighbors(now))]
    
    total_degree = sum(node_degrees)
    #重み
    prob = [degree / total_degree for degree in node_degrees]
    
    selected =  np.random.choice(list(G.neighbors(now)), 
                                 size=1, 
                                 p=prob)
    return selected[0]

def select_by_reverse_degree(G, now):
    """
    返り値: int
          選択されたノード番号
          
    Parameters
    ----------
    G : networkx graph
    
    now: int
        　現在位置(ノード番号)
    ----------
    各ノードの次数に反比例した重み付き抽選
    重み = 対象ノードの次数の逆数 / 各接続ノードの次数の逆数和
    
    """
    #各接続ノードの次数リスト(逆数)
    node_degrees = [1 / G.degree(i) for i in list(G.neighbors(now))]
    
    total_degree = sum(node_degrees)
    
    #重み
    prob = [degree / total_degree for degree in node_degrees]
    
    selected =  np.random.choice(list(G.neighbors(now)), 
                                 size=1, 
                                 p=prob)
    return selected[0]