#THEMIS
import sys
import numpy as np
import pandas as pd
import bottleneck as bn
import matplotlib.pyplot as plt
import csv


#spectralのx軸y軸を取得
def get_spectral(csvfile): 
    print("Function: Spectral Plot\n")
    print("File name\n"+csvfile+"\n")
    
    with open(csvfile, encoding='utf-8-sig') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)#文字列をfloat型に変換
        spectral_list = [row for row in reader]
    print(spectral_list)
    print("\n")
        
    spectral_array = np.array(spectral_list)            #list型をNumPy配列に変換
    
    print(spectral_array.size)
    print("\n")
    
    n = int(spectral_array.size/2)                      #要素数の半分を取得
    spectral_array_2 = spectral_array.reshape([n,2])    #1行20列配列を10行2列配列に変換
    spectral_array_2_x = spectral_array_2[:, 0]         #1列目の全ての行を抽出
    spectral_array_2_y = spectral_array_2[:, 1]         #2列目の全ての行を抽出
    
    print("x: wavelength")
    print(spectral_array_2_x)
    print("\ny: reflectance")
    print(spectral_array_2_y)

    plt.plot(spectral_array_2_x, spectral_array_2_y)#, marker=".")
    plt.xlabel('Wavelength [µm]', fontsize=15)
    plt.ylabel('Radiance', fontsize=15)
    # plt.ylabel('Reflentance')
    # plt.title('THEMIS', fontsize=15)
    # plt.title('Spectral')
    plt.grid()
    # plt.savefig("MasterThesis/I52359002SNU_E_-73.31904_N_30.72080.pdf", bbox_inches="tight", pad_inches=0.2)
    return (spectral_array_2_x, spectral_array_2_y)



#spectralのx軸y軸を取得
def standardization(csvfile_base, csvfile_2nd):
    print("Function: Spectral Standardization\n")
    print("File name\n"+csvfile_base+" -Base-\n"+csvfile_2nd+" -2nd-\n")
    
    with open(csvfile_base, encoding='utf-8-sig') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)#文字列をfloat型に変換
        spectral_list1 = [row for row in reader]
    with open(csvfile_2nd, encoding='utf-8-sig') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)#文字列をfloat型に変換
        spectral_list2 = [row for row in reader]

    spectral_array1 = np.array(spectral_list1)            #list型をNumPy配列に変換
    spectral_array2 = np.array(spectral_list2)
    
    print(spectral_array1.size)
    print(spectral_array2.size)
    print("\n")
    
    
    n1 = int(spectral_array1.size/2)                       #要素数の半分を取得
    n2 = int(spectral_array2.size/2)                       #要素数の半分を取得

    spectral_array1_2 = spectral_array1.reshape([n1,2])    #1行20列配列を10行2列配列に変換
    spectral_array2_2 = spectral_array2.reshape([n2,2]) 
    
    spectral_array1_2_x = spectral_array1_2[:, 0]         #1列目の全ての行を抽出
    spectral_array2_2_x = spectral_array2_2[:, 0]
    
    spectral_array1_2_y = spectral_array1_2[:, 1]         #2列目の全ての行を抽出
    spectral_array2_2_y = spectral_array2_2[:, 1]
    
    
    if n1 != n2:
        if n1 > n2:
            nl = spectral_array1_2_x
            arrl = spectral_array1_2_y
            ns = spectral_array2_2_x
            arrs = spectral_array2_2_y
        else:
            nl = spectral_array2_2_x
            arrl = spectral_array2_2_y
            ns = spectral_array1_2_x
            arrs = spectral_array1_2_y
    
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
        print(c)
        print(type(c))
        print(arrs)
        print(type(arrs))
        arrs = np.float_(arrs)
        for c in c:
            arrs = np.insert(arrs, c, np.nan)
            
        if arrl.all == spectral_array1_2_y.all:
            division = arrs / arrl
        else:
            division = arrl / arrs
    
    else:
        nl = spectral_array1_2_x
        division = spectral_array2_2_y / spectral_array1_2_y

    print("y: reflectance -base-")
    print(spectral_array1_2_y)
    print("y: reflectance -2nd-")
    print(spectral_array2_2_y)

    print("\nx: wavelength")
    print(nl)#spectral_array1_2_x)
    print("\ny: reflectance -standardization_2nd/base-")
    print(division)
    print("\n")

    plt.plot(nl, division)#spectral_array1_2_x, division)#, marker=".")
    plt.xlabel('Wavelength [µm]')
    plt.ylabel('Reflentance')
    plt.title('Spectral Standardization')
    
    return (nl, division)#spectral_array1_2_x, division)



#spectralのx軸y軸(2つ)を取得
def moving_avg(csvfile, width):
    print("Function: Spectral Moving Average\n")
    print("File name\n"+csvfile+"\n")

    with open(csvfile, encoding='utf-8-sig') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)#文字列をfloat型に変換
        spectral_list = [row for row in reader]

    spectral_array = np.array(spectral_list)            #list型をNumPy配列に変換
    n = int(spectral_array.size/2)                      #要素数の半分を取得
    spectral_array_2 = spectral_array.reshape([n,2])    #1行20列配列を10行2列配列に変換
    spectral_array_2_x = spectral_array_2[:, 0]         #1列目の全ての行を抽出
    spectral_array_2_y = spectral_array_2[:, 1]         #2列目の全ての行を抽出

    print("x: wavelength")
    print(spectral_array_2_x)
    print("\ny: reflectance")
    print(spectral_array_2_y)

    def rollavg_bottlneck(a,n):
        return bn.move_mean(a, window=n, min_count = None)

    mv_data = rollavg_bottlneck(spectral_array_2_y, width)#入力させる
    
    if width%2 == 0:
        w = int(width/2-1)
    else:
        w = int(width/2)
    mv_data_roll = np.roll(mv_data, -w)
    
    print("\ny: reflectance  -Moving Average-")
    print(mv_data_roll)
    print("\n")

    plt.plot(spectral_array_2_x, spectral_array_2_y, color="#1f77b4")
    plt.plot(spectral_array_2_x, mv_data_roll, color="#ff7f0e")
    plt.xlabel('Wavelength [µm]')
    plt.ylabel('Reflentance')
    plt.title('Spectral Moving Average')
    
    return (spectral_array_2_x, spectral_array_2_y, spectral_array_2_x, mv_data_roll)



#配列からグラフ作成
def spectralplot(array):
    array = iter(array)
    count = 1
    for x, y in zip(array, array):
        num = str(count)
        lbl = "No."+num
        plt.plot(x, y, label=lbl)
        print(lbl)
        print(x)
        print(y)
        count += 1
    plt.legend()
    plt.xlabel('Wavelength [µm]')
    plt.ylabel('Reflentance')
    plt.title('Spectral')