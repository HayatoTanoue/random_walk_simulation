import random
import numpy as np
import networkx as nx

def select_by_degree(G, now):
    """
    各ノードの次数に応じた重み付き抽選
    重み = 対象ノードの次数 / 接続ノードの次数の和

    Parameters
    ----------
    G : networkx graph
        
    now : int
        walkerの現状の位置(ノード番号)

    Returns
    -------
    selected : int
        選択されたノード番号

    """
    
    #各接続ノードの次数リスト
    node_degrees = [G.degree(i) for i in list(G.neighbors(now))]
    
    total_degree = sum(node_degrees)
    #重み
    prob = [degree / total_degree for degree in node_degrees]
    
    selected =  np.random.choice(list(G.neighbors(now)), 
                                 size=1, 
                                 p=prob)
    selected = selected[0]
    
    return selected

def select_by_reverse_degree(G, now):
    """
    各ノードの次数に反比例した重み付き抽選
    重み = 対象ノードの次数の逆数 / 各接続ノードの次数の逆数和

    Parameters
    ----------
    G : networkx graph
        
    now : int
        walkerの現状の位置(ノード番号)

    Returns
    -------
    selected : int
        選択されたノード番号

    """
    
    #各接続ノードの次数リスト(逆数)
    node_degrees = [1 / G.degree(i) for i in list(G.neighbors(now))]
    
    total_degree = sum(node_degrees)
    
    #重み
    prob = [degree / total_degree for degree in node_degrees]
    
    selected =  np.random.choice(list(G.neighbors(now)), 
                                 size=1, 
                                 p=prob)
    selected = selected[0]
    
    return selected

def simple_random_walk(G, walk_length, start_position):
    """
    シンプルランダムウォーク : 各ノードへの遷移確率が等しい random walk
    
    Parameters
    ----------
    G : networkx graph
        random walk を行うネットワーク
    walk_length : int
        random walk のステップ数(歩数)
    start_position : int
        random walk を行う際のスタート位置(ノード番号)

    Returns
    -------
    walk : list
        random walk の訪問ノードリスト

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
    次数比例ランダムウォーク : 遷移確率が次数に比例する random walk
    
    Parameters
    ----------
    G : networkx graph
        random walk を行うネットワーク
    walk_length : int
        random walk のステップ数(歩数)
    start_position : int
        random walk を行う際のスタート位置(ノード番号)

    Returns
    -------
    walk : list
        random walk の訪問ノードリスト

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
    次数逆数比例ランダムウォーク : 遷移確率が次数に反比例する random walk
    
    Parameters
    ----------
    G : networkx graph
        random walk を行うネットワーク
    walk_length : int
        random walk のステップ数(歩数)
    start_position : int
        random walk を行う際のスタート位置(ノード番号)

    Returns
    -------
    walk : list
        random walk の訪問ノードリスト
        
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
    強化量固定エッジ強化ランダムウォーク : 強化量固定のエッジ強化ランダムウォーク
    
    エッジ強化ランダムウォーク : walkerがエッジを通過するたびのエッジの重みを追加する

    Parameters
    ----------
    G : networkx graph
        random walk を行うネットワーク
    walk_length : int
        random walk のステップ数(歩数)
    start_position : int
        random walk を行う際のスタート位置(ノード番号)
    add_weight : float
        エッジを通過した際に追加する重み

    Returns
    -------
    walk : list
        random walk の訪問ノードリスト

    """
    now = start_position
    length = 0
    
    now = start_position
    length = 0

    #訪問ノードリスト
    walk = list()

    #隣接リストの作成
    adj_list = nx.to_dict_of_lists(G)
    #重みリストの作成
    weight_list = {}
    for l in range(nx.number_of_nodes(G)):
        weight_list.setdefault(l, [1 for i in adj_list[l]])
    
    while length < walk_length:
        
        #エッジの重みに応じて選択確率は変化, 選択されたエッジを次数分強化
        selected = random.choices(adj_list[now], k=1, weights=weight_list[now])[0]
        
        #選択された(通過した)エッジに重みを追加する(強化量固定)
        weight_list[ now ][ adj_list[now].index(selected) ] += add_weight
        weight_list[ selected ][ adj_list[selected].index(now) ] += add_weight
        
        walk.append(selected)
        
        now = selected
        length += 1
    return walk

def degree_reinforce_random_walk(G, walk_length, start_position):
    """
    次数分強化ランダムウォーク : 次数分エッジを強化するエッジ強化ランダムウォーク
    
    Parameters
    ----------
    G : networkx graph
        random walk を行うネットワーク
    walk_length : int
        random walk のステップ数(歩数)
    start_position : int
        random walk を行う際のスタート位置(ノード番号)

    Returns
    -------
    walk : list
        random walk の訪問ノードリスト

    """
    now = start_position
    length = 0

    #訪問ノードリスト
    walk = list()

    #隣接リストの作成
    adj_list = nx.to_dict_of_lists(G)
    #重みリストの作成
    weight_list = {}
    for l in range(nx.number_of_nodes(G)):
        weight_list.setdefault(l, [1 for i in adj_list[l]])
    
    while length < walk_length:
        
        #エッジの重みに応じて選択確率は変化, 選択されたエッジを次数分強化
        selected = random.choices(adj_list[now], k=1, weights=weight_list[now])[0]
        
        #選択された(通過した)エッジに重みを追加する(移動前にいたノードの次数分)
        weight_list[ now ][ adj_list[now].index(selected) ] += G.degree(now)
        weight_list[ selected ][ adj_list[selected].index(now) ] += G.degree(now)
        
        walk.append(selected)
        
        now = selected
        length += 1
    return walk

def make_adj_list(G):
    """
    各ノードの接続ノードとエッジのweightに比例した遷移確率のセットのリストを作成
    {node_num : 
        { nodes : [接続ノードリスト], prob : [遷移確率リスト] }
    }

    """
    adj_list = {}

    for node in G.nodes():
        neighbor = [i[1] for i in G.edges(node,data=True)]
        p = [i[2]['weight'] for i in G.edges(node,data=True)]
        p = np.array(p) / sum(p)
        adj_list.setdefault(node, {'nodes':neighbor, 'prob':list(p)})

    return adj_list

def random_walk_by_edge_weight(G, walk_length, start_position, adj_list):
    now = start_position
    length = 0
    
    #訪問ノードリスト
    walk = list()
    while length < walk_length:
        #エッジの重みに応じて選択確率は変化, 選択されたエッジを次数分強化
        selected =  np.random.choice(adj_list[now]['nodes'], 
                                 size=1, 
                                 p=adj_list[now]['prob'])[0]
        
        walk.append(selected)
        now = selected
        length += 1
    return walk