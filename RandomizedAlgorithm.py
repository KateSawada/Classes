#!usr/bin/env python3
"""
数理情報学序論2 7/3課題3
k番目の要素を求める乱択アルゴリズムを実装し,
実験により平均の比較回数を求めよ.
>使用するプログラミング言語は問わない
>多くの回数(少なくとも1000回くらい)実行して平均をとれ
"""
import time
import random
import numpy as np
from matplotlib import pyplot as plt

class RandomizedAlgorithm():
    """
    乱択アルゴリズムを実行する関数
    Parameters
    ----------
    n: int
        探索対象のコインの枚数
    iter: int
        何度繰り返すか

    Patameters
    ----------
    trial: int
        比較回数
    avg:  float
        比較回数の平均
    """
    def __init__(self, n, iter=10000):
        #比較回数を0で初期化
        self.trial = 0
        #コインn枚でiterの分繰り返し試行する
        for _ in range(iter):
            #要素数nの数列を生成(0.0以上1.0未満)
            all_coins = [random.random() for i in range(n)]
            #何番目の要素を探索するか決定
            k = random.randint(1, n)
            #探索
            self.findK(k, all_coins)
        #比較回数の平均値
        self.avg = self.trial / iter

    def findK(self, k, coins):
        """
        探索の本体
        Parameters
        ----------
        k: int
            何番目の要素を探索するか
        coins: list of int
            探索対象の配列
        Returns
        ----------
        None
        """
        #coinsの中から無作為にコインを1枚選び，これを基準に他の要素と比較する
        pivot_val = coins.pop(coins.index(random.choice(coins)))
        #基準より軽いコイン，重いコインの集合
        S = []
        L = []
        #pivot_valと他のコインを比較
        for coin in coins:
            #比較するためカウントアップ
            self.trial += 1
            if coin > pivot_val:
                #基準より重いコインはLに追加
                L.append(coin)
            else:
                #基準より軽いコインはSに追加
                S.append(coin)
        #Sの要素数に応じて処理を分ける
        #k番目のコインが見つかったら探索終了
        if len(S) == k - 1:
            return
        #Sの中でk番目の重さのコインを探索するよう再帰呼び出し
        elif len(S) > k - 1:
            self.findK(k, S)
        #Lの中でk - (|S| + 1)番目の重さのコインを探索するよう再帰呼び出し
        elif len(S) < k - 1:
            self.findK((k - len(S) - 1), L)

if __name__ == "__main__":
    #処理の開始時刻
    start = time.time()

    #n = 10, 20, 30, ... , 10000で各10000回ずつ試行し，比較回数の平均値の配列を生成する．
    results = [RandomizedAlgorithm((i + 1) * 10).avg for i in range(1000)]
    
    #グラフのx軸のデータを生成
    x = np.arange(10, 10001, 10)
    #グラフの作成
    fig = plt.figure()
    plt.title("Randomized Algorithm")
    plt.xlabel("n")
    plt.ylabel("comparison")
    plt.plot(x, np.poly1d(np.polyfit(x, results, 1))(x),
            label="y = {:.4f}n + {:.4f}".format(np.polyfit(x, results, 1)[0], np.polyfit(x, results, 1)[1]),
            color="red")
    plt.plot(x, results, label="results", color="blue")
    plt.legend()
    #グラフを表示する場合は次の行のコメントアウトを解除
    #plt.show()
    #グラフの画像の保存
    fig.savefig("RandomizedAlgorithm.png")

    #処理の終了時刻
    end = time.time()
    print("processing time: ", end - start)