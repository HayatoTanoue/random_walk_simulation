# coding: utf-8
import numpy as np
import networkx as nx

class Random_Walk:
    def __init__(self, G, kind):
        """
        Parameters
        ----------
        G : networkx graph

        walk_length : int
            length of random walk

        kind : str
            ex. 'simple', 'degree', 'reverse', 'weight'
        """
        self.G = G
        self.kind = kind

        self.prob_dict = self.make_prob_dict(self)

    def _make_prob_dict(self):
        """
        各ノード地点での各ノードへの遷移確率リストの作成
        
        Returns
        -------
        prob_dict : dict
            key : ノード, 
            value : 各接続ノードへの遷移確率
        """
        prob_dict = dict()
    
        if self.kind != 'weight':
            adj_list = nx.to_dict_of_lists(self.G)
            for k, v in adj_list.items():
                if self.kind == 'simple':
                    ratio = [1 for _ in v]
                elif self.kind == 'degree':
                    ratio = [self.G.degree(node) for node in v]
                elif self.kind == 'degree':
                    ratio = [1 / self.G.degree(node) for node in v]

                prob = np.array(ratio) / sum(ratio) #確率に変換
                prob_dict.setdefault(k, {'nodes': v, 'prob':list(prob)})

        else:
            for node in self.G.nodes():
                neighbor = [i[1] for i in self.G.edges(node,data=True)]
                prob = [i[2]['weight'] for i in self.G.edges(node,data=True)]
                prob = np.array(prob) / sum(prob)
                prob_dict.setdefault(node, {'nodes':neighbor, 'prob':list(prob)})

        self.prob_dict = prob_dict
        
        return prob_dict

    def random_walk_by_prob_dict(self, walk_length, start_position, start_count=False):
        """
        prob_dict(遷移確率)に従って重み付けされた抽選での
        ランダムウォークを行う
        
        Parameters
        ----------
        start_position : node number
            ランダムウォークを行う際のスタート位置
        
        start_count : bool
            スタート位置を訪問履歴に含めるかどうか
            (default = False)
        
        Returns
        -------
        walk : list
            ランダムウォークの訪問履歴
        """
        now = start_position
        length = 0
        
        #訪問ノードリスト
        walk = list()

        #start_count がTrue の場合にstart_positionを追加する
        if start_count:
            walk.append(start_position)

        while length < walk_length:
            #選択確率に従い,移動先のノードを抽選
            selected =  np.random.choice(self.prob_dict[now]['nodes'], 
                                     size=1, 
                                     p = self.prob_dict[now]['prob'])[0]
            
            walk.append(selected)
            now = selected
            length += 1

        return walk



