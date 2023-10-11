# -*- coding: utf-8 -*-
import csv
import matplotlib.pyplot as plt
from matplotlib import patches
import tkinter.filedialog
import os
import pathlib

filetypes = [("CSV (コンマ区切り)", "*.csv")]
data_pass = tkinter.filedialog.askopenfilename(filetypes=filetypes, title="ファイルをひらく")
filename = data_pass.split("/")[-1].split(".csv")[0].split("_")


with open(data_pass, "r", encoding="utf-8") as csvfile:
    f = csv.DictReader(csvfile, delimiter=",", doublequote=True, lineterminator="\r\n", 
                   quotechar='"', skipinitialspace=True)

    pen_num = 0 # ペンの使用回数
    eraser_num = 0 # 消しゴムの使用回数⇒俗に言う使用回数　ただし全消去も含む
    allclear_num = 0 # 全消去の使用回数

    active_num = 0
    active_num2 = 0

    mode = 0 # 全消去:0, ペン:1, 消しゴム:2
    all_num = 0

    for row in f:
        all_num += 1
        if row["Action"] == "start-drawing" and mode != 1:
            mode = 1
            pen_num += 1
        elif row["Action"] == "start-erasing" and mode != 2:
            mode = 2
            eraser_num += 1

            active_num2 += 1
        elif row["Action"] == "savenote":
            break
        elif row["Action"] == "allclear":
            mode = 0
            allclear_num += 1
            eraser_num += 1
        elif row["Action"] == "move-drawing":
            active_num += 1
            active_num2 += 1
        else:
            continue

    all_num -= 1 # savenote を除外

    print("アクティブ度:" + str(active_num)) # move-drawing の数
    print("アクティブ度 2:" + str(active_num2/all_num)) # start-drawingとmove-drawing の全体に占める割合
    print("消しゴム使用回数:" + str(eraser_num))
    print("全消去回数:" + str(allclear_num))

pen_box = [[] for i in range(pen_num)]
eraser_box = [[] for i in range(eraser_num)]

with open(data_pass, "r", encoding="utf-8") as csvfile:
    f = csv.DictReader(csvfile, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

    mode = 1 # 全消去:0, ペン:1, 消しゴム:2
    mode_time = 0

    pen_address = 0
    eraser_address = -1

    for row in f:
        if row["Action"] == "start-drawing":
            if mode == 1:
                pen_box[pen_address].append(row)
            elif mode != 1:
                mode = 1
                pen_address += 1
                pen_box[pen_address].append(row)

            if mode_time == 0: # 最初の行の時間のみ取得
                mode_time = 1
                start_time = int(row["Time"])
            elif mode_time == 1:
                continue
        elif row["Action"] == "move-drawing":
            pen_box[pen_address].append(row)
        elif row["Action"] == "start-erasing":
            if mode == 2:
                eraser_box[eraser_address].append(row)
            elif mode != 2:
                mode = 2
                eraser_address += 1
                eraser_box[eraser_address].append(row)
        elif row["Action"] == "move-erasing":
            eraser_box[eraser_address].append(row)
        elif row["Action"] == "allclear":
            mode = 0
            eraser_address += 1
            eraser_box[eraser_address].append(row)
        elif row["Action"] == "savenote": # 終了時の時間を取得
            finish_time = int(row["Time"])
            break
        else:
            continue

    m_sec = finish_time - start_time
    sec = m_sec // 1000
    d = sec // (3600 * 24)
    h = (sec % (3600 * 24)) // 3600
    m = (sec % 3600 ) // 60
    s = sec % 60
    print("所要時間:{0}日{1}時間{2}分{3}秒".format(d, h, m, s))
    print("画像の保存先は作成済みですか？: Y/n")
    new = input()
    path = 0
    path_dir = ""
        
    while path == 0:
        if (new == "y") or (new == "Y"):
            path_dir = pathlib.Path(r"C:\Users\user\OneDrive\デスクトップ\research\result\Q{}\q{}\S{}".format(filename[0], filename[1], filename[2]))
            path = 1
        elif (new == "n") or (new == "N"):
            print("保存先を以下のように指定して下さい。ただし、数値のみを入力して下さい。")
            print("(課題番号).(問番号).(解答者番号)")
            id = input()
            Q = "Q" + id.split(".")[0]
            q = "q" + id.split(".")[1]
            S = "S" + id.split(".")[2]
            new_dir_path = './result/{}/{}/{}'.format(Q, q, S)
            try:
                os.makedirs(new_dir_path)
            except FileExistsError:
                print("保存先が作成済みです")
            path_dir = pathlib.Path(r"C:\Users\user\OneDrive\デスクトップ\research\result\{}\{}\{}".format(Q, q, S))
            path = 1
        else:
            print("解答形式が正しくありません。打ち直して下さい。")
            new = input()

def before():
    target = 0
    while target < len(pen_box):
        fig, ax = plt.subplots()
        plt.rcParams["figure.figsize"] = [6.0,7.0] # グラフのサイズ調整

        ax.set_xlim(0, 750)
        ax.set_ylim(0, 1000)

        order = 1

        i = 0

        while i <= target:
            if i != 0:
                se_count = 0
                for j in eraser_box[i - 1]:
                    if j["Action"] == "move-erasing":
                        continue
                    else:
                        se_count += 1

                eraser_x = [[] for j in range(se_count)]
                eraser_y = [[] for j in range(se_count)]

                num = -1
                for j in eraser_box[i - 1]:
                    if j["Action"] == "move-erasing":
                        eraser_x[num].append(int(j["X"]))
                        eraser_y[num].append(int(j["Y"]))
                    else:
                        num += 1
                        eraser_x[num].append(int(j["X"]))
                        eraser_y[num].append(int(j["Y"]))

                for j in range(len(eraser_x)):
                    x_min = 5000
                    x_Max = 0
                    y_min = 5000
                    y_Max = 0
                    if len(eraser_x) == 1 and len(eraser_x[0]) == 1:
                        x_min = 10
                        x_Max = 750
                        y_min = 10
                        y_Max = 1000
                        r = patches.Rectangle( (x_min, y_min) , x_Max - x_min, 
                                              y_Max - y_min, zorder=order, facecolor="white", 
                                              alpha=1, fill=True) # 四角形のオブジェクト

                        ax.add_patch(r)
                    elif len(eraser_x[j]) == 1:
                        ax.plot(eraser_x[j], eraser_y[j], zorder=order, linewidth=5, color = "white")
                    else:
                        l = 0
                        while l <= num:
                            ax.plot(eraser_x[l], eraser_y[l], zorder=order, linewidth=5, color = "white")
                            l += 1
                order += 1

            sd_count = 0

            for j in pen_box[i]:
                if j["Action"] == "start-drawing":
                    sd_count += 1

            pen_x = [[] for j in range(sd_count)] # 通し番号ごとのペンストロークデータの x 座標を保管した空の 2 次元配列
            pen_y = [[] for j in range(sd_count)] # 通し番号ごとのペンストロークデータの y 座標を保管した空の 2 次元配列

            num = -1

            for j in pen_box[i]:
                if j["Action"] == "start-drawing":
                    num += 1
                    pen_x[num].append(int(j["X"]))
                    pen_y[num].append(int(j["Y"]))
                else:
                    pen_x[num].append(int(j["X"]))
                    pen_y[num].append(int(j["Y"]))

            k = 0
            while k <= num:
                ax.plot(pen_x[k], pen_y[k], zorder=order, color = "black")
                k += 1
            order += 1

            i += 1

        save_num = 2 * target + 1

        ax.invert_yaxis() # y 軸反転
        # plt.show() # 画像を一枚ずつ表示
        path_img = path_dir.joinpath(str(save_num) + ".png")

        fig.savefig(path_img)
        plt.close()
        target += 1

def after():
    target = 0
    while target < len(eraser_box):
        fig, ax = plt.subplots()
        plt.rcParams["figure.figsize"] = [6.0,7.0] # グラフのサイズ調整
    
        ax.set_xlim(0, 750)
        ax.set_ylim(0, 1000)
        
        order = 1
        i = 0
    
        while i <= target:
            sd_count = 0
        
            for j in pen_box[i]:
                if j["Action"] == "start-drawing":
                    sd_count += 1
    
            pen_x = [[] for j in range(sd_count)] # 通し番号ごとのペンストロークデータのx座標を保管した空の2次元配列
            pen_y = [[] for j in range(sd_count)] # 通し番号ごとのペンストロークデータのy座標を保管した空の2次元配列
    
            num = -1
        
            for j in pen_box[i]:
                if j["Action"] == "start-drawing":
                    num += 1
                    pen_x[num].append(int(j["X"]))
                    pen_y[num].append(int(j["Y"]))
                else:
                    pen_x[num].append(int(j["X"]))
                    pen_y[num].append(int(j["Y"]))
        
            k = 0
            while k <= num:
                ax.plot(pen_x[k], pen_y[k], zorder=order, color = "black")
                k += 1
            order += 1
        
            se_count = 0
            for j in eraser_box[i]:
                if j["Action"] == "move-erasing":
                    continue
                else:
                    se_count += 1
            
            eraser_x = [[] for j in range(se_count)]
            eraser_y = [[] for j in range(se_count)]
            
            num = -1
        
            for j in eraser_box[i]:
                if j["Action"] == "move-erasing":
                    eraser_x[num].append(int(j["X"]))
                    eraser_y[num].append(int(j["Y"]))
                else:
                    num += 1
                    eraser_x[num].append(int(j["X"]))
                    eraser_y[num].append(int(j["Y"]))
            
            for j in range(len(eraser_x)):
                x_min = 5000
                x_Max = 0
                y_min = 5000
                y_Max = 0
                if len(eraser_x) == 1 and len(eraser_x[0]) == 1:
                    x_min = 10
                    x_Max = 750
                    y_min = 10
                    y_Max = 1000
                    r = patches.Rectangle( (x_min, y_min) , x_Max - x_min, y_Max - y_min, zorder=order, facecolor="white", alpha=1, fill=True) # 四角形のオブジェクト
                    ax.add_patch(r)
                elif len(eraser_x[j]) == 1:
                    ax.plot(eraser_x[j], eraser_y[j], zorder=order, linewidth=5, color = "white")
                else:
                    l = 0
                    while l <= num:
                        ax.plot(eraser_x[l], eraser_y[l], zorder=order, linewidth=5, color = "white")
                        l += 1
            order += 1  
            
            i += 1
        
        save_num = 2 * (target + 1)
            
        ax.invert_yaxis() # y軸反転
        # plt.show() # 画像を一枚ずつ表示
        path_img = path_dir.joinpath(str(save_num) + ".png")
        
        fig.savefig(path_img)
        plt.close()
        
        target += 1


before()
after()