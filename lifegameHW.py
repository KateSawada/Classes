#!/usr/bin/env python3
import numpy as np
import sys
from time import time
import datetime

def simulate(size, start_size, end_size, start_time):
    """
    関数本体 盤面を生成し、check関数を呼び出す
    Parameters:
    ----------
    size : int
        現在計算している盤面一辺の長さ
    start_size : int
        計算したい盤面の一辺の最小値(ファイル出力用)
    end_size : int
        計算したい盤面の一辺の最大値(ファイル出力用)
    start_time : float
        プログラムの実行を開始したUNIX時間(ファイル出力用)
    """
    print("Now Checking : "+str(size)+"x"+str(size))
    #size*sizeの盤面での全探索
    for cel_num in range(2**(size**2)):
        #2進数で0と1の盤面を生成
        field_str = format(cel_num,'b').zfill(size**2)
        field = np.zeros((size, size))
        #strからndarrayに変換
        for i in range(size**2):
            if field_str[-(i+1)] == '1':
                field[i//size, i%size] = 1

        #条件に合致しているか調べる関数を呼び出し・答えが見つかったら途中でプログラムを終了
        check(field, size, start_time, start_size, end_size)
    print("Answer Not Found : "+str(size)+"x"+str(size))


def check(field, size, start_time, start_size, end_size):
    """
    与えられた盤面が条件を満たすか判定 答えが見つかればファイルに出力して終了
    98行目 sys.ext()を削除すれば、終了せず次の答えを探し続ける
    Parameters:
    ----------
    field : ndarray
        課題の条件を満たしているか判定したい盤面(0,1で表現)
    size : int
        現在計算している盤面一辺の長さ
    start_time : float
        プログラムの実行を開始したUNIX時間(ファイル出力用)
    start_size : int
        計算したい盤面の一辺の最小値(ファイル出力用)
    end_size : int
        計算したい盤面の一辺の最大値(ファイル出力用)
    """
    #過密で死ぬセルがあったか(周囲に4つ以上1がある1があったか)
    #生き残るセルがあるか(すべての1の周りの1が2or3個ではなかったか)
    #誕生するセルがあるか(すべての0の周りの1が3個ではなかったか)
    isCrowd = False
    isNotVanish = True
    isBirth = True
    #「端は使ってはいけない」という条件のため、周囲に0を追加
    field = np.append(np.zeros((size, 1)), field, 1)
    field = np.append(field, np.zeros((size, 1)), 1)
    field = np.append(np.zeros((1, size+2)), field, 0)
    field = np.append(field, np.zeros((1, size+2)), 0)
    #fieldで渡された盤面と、その外周のすべてのマスの周囲の状況を調べる
    for row in range(size+2):
        for col in range(size+2):
            surrounding = 0
            #周囲8マスのセルの合計を示す
            surrounding += (checksurrounding(field, row - 1, col - 1) +
                            checksurrounding(field, row - 1, col    ) +
                            checksurrounding(field, row - 1, col + 1) +
                            checksurrounding(field, row    , col - 1) +
                            checksurrounding(field, row    , col + 1) +
                            checksurrounding(field, row + 1, col - 1) +
                            checksurrounding(field, row + 1, col    ) +
                            checksurrounding(field, row + 1, col + 1))
            #生成されたfieldの中について
            if row > 0 and row < size + 1 and col > 0 and col < size + 1:
                if surrounding >= 4 and field[row, col] == 1:
                    isCrowd = True
                if (surrounding == 2 or surrounding == 3) and field[row, col] == 1:
                    isNotVanish = False
                if surrounding == 3 and field[row, col] == 0:
                    isBirth = False
                else:
                    pass
            #周囲に追加した部分について、誕生しないか確認
            else:
                if surrounding == 3:
                    isBirth = False

    #もし条件をすべて満たしているなら、結果をテキストファイルに出力する関数を呼び出して終了
    if (isCrowd and isNotVanish and isBirth):
        write_log(field, True, start_time, size, start_size, end_size)
        print("Answer Found")
        #↓sys.exit()を消すと、答えが見つかっても次の答えを探し続ける
        sys.exit()

def checksurrounding(field, row, col):
    """
    fieldの指定座標にセルがあるかを返す ただし、盤面外の参照にも対応している
    Parameters:
    ----------
    field : ndarray
        盤面
    row : int
        セルの有無を確認したいマスの行
    col : int
        セルの有無を確認したいマスの列
    Returns:
    ----------
    int
        field[row, col]が1なら1を、
                         0もしくは盤面の外ならば0を返す
    """
    try:
        if field[row, col] == 1:
            return 1
        else:
            return 0
    except IndexError:
        return 0

#結果をテキストファイルに出力する関数
def write_log(field, isFound, start_time, size, start_size, end_size):
    """
    答えが見つかった場合、見つからなかった場合の情報をlifegame_log.txt に出力する
    すでに lifegame_log.txt が存在する場合は追記する
    Parameters:
    ----------
    field : ndarray
        出力したい盤面(0,1で表現)
    isFound : bool
        答えが見つかった場合はTrue, 見つからなかった場合はFalse
    start_time : float
        プログラムの実行を開始したUNIX時間(ファイル出力用)
    size : int
        答えが見つかった盤面の一辺の長さ
    start_size : int
        計算したい盤面の一辺の最小値)
    end_size : int
        計算したい盤面の一辺の最大値
    """
    filename = "lifegame_log.txt"
    end_time = datetime.datetime.now()
    process_time = end_time - start_time
    if isFound:
        with open(filename, mode='a') as f:
            f.write("Found Answer")
            f.write("\n")
            f.write(str(field))
            f.write("\n")
            f.write("time : "+str(process_time))
            f.write("\n")
            f.write("end : "+str(end_time))
            f.write("\n")
            f.write("size : "+str(size))
            f.write("\n\n")
    else:
        with open(filename, mode='a') as f:
            f.write("Not Found Ans")
            f.write("\n")
            f.write("time : "+str(process_time))
            f.write("\n")
            f.write("end : "+str(end_time))
            f.write("\n")
            f.write("size : from "+str(start_size)+" to "+str(end_size-1))
            f.write("\n\n")

#コマンドライン引数で計算する盤面のサイズの範囲を指定(最小でも3x3)
args = sys.argv
#引数が正しいか確認
if len(args) != 3:
    print("Invalid Arguments\nusage : $ ./HWlifegame.py start_size(int) end_size(int)")
    exit()
#サイズ指定の引数をint型に変換 型が違う場合はここで終了
try:
    start_size = int(args[1])
    end_size = int(args[2]) + 1
except:
    print("Invalid Arguments Type\nusage : $ ./HWlifegame.py start_size(int) end_size(int)")
    exit()
#引数が正しいか確認
if start_size < 3:
    print("Invalid Arguments Value\nusage : $ ./HWlifegame.py start_size(int) end_size(int)\nNOTE : start_size must be larger than 2")
    exit()
if start_size > end_size:
    print("Invalid Arguments Value\nusage : $ ./HWlifegame.py start_size(int) end_size(int)\nNOTE : start_size mustn't be laeger than end_size")
    exit()

#処理時間の計測
start_time = datetime.datetime.now()
print("Program Start...")
#指定サイズの計算 答えが見つかったらその場でファイルを出力して終了
for size in range(start_size, end_size):
    simulate(size, start_size, end_size, start_time)
#答えが見つからなかったら結果を出力
write_log(np.zeros(1), False, start_time, 0, start_size, end_size)
print("Answer Not Found in "+str(start_size)+" to "+str(end_size-1))