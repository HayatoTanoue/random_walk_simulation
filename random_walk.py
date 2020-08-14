import numpy as np
import networkx as nx

def select_by_degree(G, now):
    """
    返り値: int
          選択されたノード番号
          
    Parameters
    ----------
    G : networkx graph
    
    now : int
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
    返り値 : int
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

def select_add_wight(G, now, weight_list, add_weight):
    """
    返り値 : int 選択されたノード番号
            list 重みを更新した weight_list
          
    Parameters
    ----------
    G : networkx graph
    
    now : int
        　現在位置(ノード番号)
         
    weight_list : list
                  edgeの重みリスト
    
    add_weight : float
                　random walker 通過時のエッジ強化量
    ----------
    
    エッジの重みに応じた選択確率でノードを選択する
    
    通過したエッジにadd_wieight分エッジの重みを追加する
    """
    
    #重み
    prob = [weight / sum(weight_list) for weight in weight_list]
    
    selected = np.random.choice(list( np.arange(nx.number_of_nodes(G) ) ),
                                size=1,
                                p=prob)
    
    weight_list[ selected[0] ] += add_weight
    
    return selected[0],  weight_list


def select_add_degree(G, now, weight_list):
    """
    返り値 : int 選択されたノード番号
            list 重みを更新した weight_list
          
    Parameters
    ----------
    G : networkx graph
    
    now : int
        　現在位置(ノード番号)
         
    weight_list : list
                  edgeの重みリスト
    ----------
    
    エッジの重みに応じた選択確率でノードを選択する
    
    通過したエッジに次数分エッジの重みを追加する
    """
    
    #重み
    prob = [weight / sum(weight_list) for weight in weight_list]
    
    selected = np.random.choice(list( np.arange(nx.number_of_nodes(G) ) ),
                                size=1,
                                p=prob)
    
    weight_list[ selected[0] ] += G.degree( now )
    
    return selected[0],  weight_list


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

def degree_random_walk(G, walk_length, start_position):
    """
    

    Parameters
    ----------
    G : TYPE
        DESCRIPTION.
    walk_length : TYPE
        DESCRIPTION.
    start_position : TYPE
        DESCRIPTION.

    Returns
    -------
    walk : TYPE
        DESCRIPTION.

    """
    now = start_position
    length = 0
    
    #訪問ノードリスト
    walk = list()
    
    while length < walk_length:
        
        #接続ノードリストからランダムで一つ選択(等確率)
        selected = select_by_degree(G, now)
        walk.append(selected)
        
        now = selected
        length += 1
    return walk

def reverse_degree_random_walk(G, walk_length, start_position):
    """
    

    Parameters
    ----------
    G : TYPE
        DESCRIPTION.
    walk_length : TYPE
        DESCRIPTION.
    start_position : TYPE
        DESCRIPTION.

    Returns
    -------
    walk : TYPE
        DESCRIPTION.

    """
    now = start_position
    length = 0
    
    #訪問ノードリスト
    walk = list()
    
    while length < walk_length:
        
        #接続ノードリストからランダムで一つ選択(等確率)
        selected = select_by_reverse_degree(G, now)
        walk.append(selected)
        
        now = selected
        length += 1
    return walk

def fixed_rainforce_random_walk(G, walk_length, start_position, add_weight):
    """
    Parameters
    ----------
    G : TYPE
        DESCRIPTION.
    walk_length : TYPE
        DESCRIPTION.
    start_position : TYPE
        DESCRIPTION.
    add_weight : TYPE
        DESCRIPTION.

    Returns
    -------
    walk : TYPE
        DESCRIPTION.

    """
    
    now = start_position
    length = 0
    
    #networkの遷移行列の作成
    matrix = nx.to_numpy_matrix(G)
    
    #訪問ノードリスト
    walk = list()
    
    while length < walk_length:
        
        #エッジの重みに応じて選択確率は変化, 選択されたエッジを固定分強化
        selected, matrix[now] = select_add_wight(G, now, matrix[now].tolist()[0], add_weight)
        walk.append(selected)
        
        now = selected
        length += 1
    
    return walk

def reinforce_random_walk(G, walk_length, start_position):
    """
    Parameters
    ----------
    G : TYPE
        DESCRIPTION.
    walk_length : TYPE
        DESCRIPTION.
    start_position : TYPE
        DESCRIPTION.

    Returns
    -------
    walk : TYPE
        DESCRIPTION.

    """
    now = start_position
    length = 0
    
    #networkの遷移行列の作成
    matrix = nx.to_numpy_matrix(G)
    
    #訪問ノードリスト
    walk = list()
    
    while length < walk_length:
        
        #エッジの重みに応じて選択確率は変化, 選択されたエッジを次数分強化
        selected, matrix[now] = select_add_degree(G, now, matrix[now].tolist()[0])
        walk.append(selected)
        
        now = selected
        length += 1
    return walk

