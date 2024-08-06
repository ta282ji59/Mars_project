#THEMIS,CRISM
#結果のみVer
import sys
import numpy as np
import bottleneck as bn
import matplotlib.pyplot as plt
import csv

#from csv file
#x軸y軸(array)を取得
def get_spectral(csvfile): 
    with open(csvfile, encoding='utf-8-sig') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)#文字列をfloat型に変換
        spectral_list = [row for row in reader]
        
    spectral_array = np.array(spectral_list)            #list型をNumPy配列に変換
    n = int(spectral_array.size/2)                      #要素数の半分を取得
    spectral_array_2 = spectral_array.reshape([n,2])    #n行2列配列に変換
    spectral_array_2_x = spectral_array_2[:, 0]         #1列目の全ての行を抽出
    spectral_array_2_y = spectral_array_2[:, 1]         #2列目の全ての行を抽出
    return (spectral_array_2_x, spectral_array_2_y)


#規格化
#x軸y軸(array)を取得
def normalization(csvfile_ref, csvfile_target):
    if type(csvfile_ref) is str:
        ref = get_spectral(csvfile_ref)
        target = get_spectral(csvfile_target)
    else:
        ref = csvfile_ref
        target = csvfile_target
    n1 = ref[0].size
    n2 = target[0].size
    
    if n1 != n2:
        if n1 > n2:
            nl = ref[0]
            arrl = ref[1]
            ns = target[0]
            arrs = target[1]
        else:
            nl = target[0]
            arrl = target[1]
            ns = ref[0]
            arrs = ref[1]
    
        lx = []
        ly = []
        c = []
        count = 0
        num = 0
        for x1 in nl:
            for x2 in ns:
                if x1 == x2:
                    num = 1
                    break
            if num == 0:
                c = np.append(c, count)
            else:
                num = 0
            count += 1
        c = c.astype(int)
        arrs = np.float_(arrs)
        for c in c:
            arrs = np.insert(arrs, c, np.nan)
            
        if arrl.all == ref[1].all:
            division = arrs / arrl
        else:
            division = arrl / arrs
    else:
        nl = ref[0]
        division = target[1]/ref[1]

    return (nl, division)


#移動平均
#x軸y軸(array,2つ)を取得
def moving_avg(csvfile, width):
    if type(csvfile) is str: 
        arr = get_spectral(csvfile)
    else:
        arr = csvfile
    mavg = bn.move_mean(arr[1], window=width)
    if width%2 == 0:
        w = int(width/2-1)
    else:
        w = int(width/2)
    mavg_r = np.roll(mavg, -w)
    return (arr[0], arr[1], arr[0], mavg_r)
    
    
#スタッキング
#x軸y軸(array)を取得
def stacking(*csv):
    count = 0
    for csv in csv:
        if type(csv) is str:
            arrcsv = get_spectral(csv)
        else:
            arrcsv = csv
        if count == 0:
            arrx = arrcsv[0]
            vs = arrcsv[1]
            count = 1
        else:
            vs = np.vstack([vs, arrcsv[1]])
    def mean_st(vs):
        arr_mean = np.mean(vs, axis=0)
        return (arr_mean)
    m = mean_st(vs)
    # print(m)
    # print(vs)
    return (arrx, m)



    
  