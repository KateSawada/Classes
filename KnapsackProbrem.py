#!usr/bin/env python3
"""
数理情報学序論2 7/10課題問6
ナップサック問題に対する以下の問題例に対して，
できるだけ総満足度の高い商品の組み合わせを求めよ．
(注．満足度合計だけでなく商品の組み合わせも回答すること)
最適解でなくてもよい．総満足度が大きい回ほど高い得点を与える．
ただし，値段の合計が予算上限を超える組み合わせには得点を与えない．
また，解を求めた方法についても説明せよ．

(a)
商品数n = 6，予算上限b = 16
商品番号 1,  2,  3,  4,  5,  6
値段     4,  4,  3,  5,  3,  5
満足度   40, 41, 30, 52, 28, 54

(b)
商品数n = 8, 予算上限b = 184
商品番号 1,  2,  3,  4,  5,  6,  7,  8
値段     70, 41, 40, 50, 60, 71, 51, 61
満足度   66, 41, 40, 52, 61, 67, 54, 65
"""
import time
def Knapsack(ary, cost_sup):
    """
    ナップサック問題の最適解を見つける関数
    
    Parameters
    ------------
    ary: dict(key: int, value: [int, int])
        キーに商品番号，値に値段と満足度のリストを持つ
    cost_sup: int
        予算の上限
    
    Returns
    ------------
    list of int
        解となる商品番号
    int
        満足度
    int
        合計の費用
    """
    #処理の開始時刻
    start = time.time()
    
    #商品数を取得
    n = len(ary)
    #最適解，その時の満足度と商品の選び方を初期化
    ans_cost = 0
    ans_satisfaction = 0
    ans_combination = ""
    #全組み合わせを検討
    for i in range(2**n):
        cost = 0
        satisfaction = 0
        #商品の選び方の組み合わせをn桁の2進数で表現．各桁が商品番号に対応
        #0=>買わない, 1=>買う
        combination = bin(i)[2:].zfill(n)
        #生成した組み合わせで購入した時の費用と満足度を計算
        for j in range(len(combination)):
            if combination[j] == "1":
                cost += ary[int(j + 1)][0]
                satisfaction += ary[int(j + 1)][1]
        #満足度を更新できる，かつ，費用が上限以下であれば解を更新
        if ans_satisfaction < satisfaction and cost <= cost_sup:
            ans_satisfaction = satisfaction
            ans_cost = cost
            ans_combination = combination
    #最適解の商品の組み合わせを2進数での表記から商品番号のリストに変換
    ans_list = [int(i + 1) for i in range(n) if ans_combination[i] == "1"]

    #処理の終了時刻
    end = time.time()
    #処理に要した時間の出力
    print("processing time: ", end - start)
    return ans_list, ans_satisfaction, ans_cost


if __name__ == "__main__":
    #問題例の設定
    arya = {
        1: [4, 40],
        2: [4, 41],
        3: [3, 30],
        4: [5, 52],
        5: [3, 28],
        6: [5, 54]
    }
    aryb = {
        1: [70, 66],
        2: [41, 41],
        3: [40, 40],
        4: [50, 52],
        5: [60, 61],
        6: [71, 67],
        7: [51, 54],
        8: [61, 65]
    }

    #最適解の計算と出力
    print(Knapsack(arya, 16))
    print()
    print(Knapsack(aryb, 184))

