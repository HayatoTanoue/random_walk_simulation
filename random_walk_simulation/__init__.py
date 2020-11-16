# coding: utf-8
'''
    random_walk_simulation
    =====
    networkxのgraph上のランダムウォークを行う

    simple :　シンプル ランダムウォーク
    		　各ノードの遷移確率が等しい		

    degree : 次数比例 ランダムウォーク
    		　各ノードへの遷移確率が次数に比例した値となる
    		 (次数が高いノードが選択されやすい)

    reverse : 次数の逆数比例 ランダムウォーク
    		  各ノードへの遷移確率が次数に反比例した値となる
    		  (次数が低いノード選択されやすい)

    weight : エッジの重み比例 ランダムウォーク
    		 各ノードへの遷移確率がエッジの重みに比例した値となる
    		 (エッジの重みが高いほど選択されやすい)

    Repository: https://github.com/HayatoTanoue/random_walk_simulation
    License: MIT
'''

__author__ = 'Hayato Tanoue'
__version__ = '0.3'
__license__ = 'MIT'

from .random_walk import Random_Walk