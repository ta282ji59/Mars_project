from tqdm import tqdm 
from tqdm.notebook import trange 
import csv
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import find_peaks, peak_prominences
from scipy.interpolate import interp1d


class SpectraInterpolation:
    def __init__(self, spectrumA_2d_arr, spectrumB_2d_arr):
        """NaNであるインデックスを取得。重複を削除し、ユニークなインデックスを取得。NaNを取り除く。共通の波長範囲を計算。波長ステップを計算し、共通の波長を生成。

        Args:
            spectrumA_2d_arr (_type_): １列目波長、２列目反射率。
            spectrumB_2d_arr (_type_): １列目波長、２列目反射率。
        """
        nan_indicesA = np.where(np.isnan(spectrumA_2d_arr[:, 1]))[0].tolist()
        nan_indicesB = np.where(np.isnan(spectrumB_2d_arr[:, 1]))[0].tolist()
        unique_indicesA = list(set(nan_indicesA))
        unique_indicesB = list(set(nan_indicesB))
        self.spectrumA_2d_arr = np.delete(spectrumA_2d_arr, unique_indicesA, axis=0)
        self.spectrumB_2d_arr = np.delete(spectrumB_2d_arr, unique_indicesB, axis=0)
        self.min_wavelength = max(spectrumA_2d_arr[0, 0], spectrumB_2d_arr[0, 0])
        self.max_wavelength = min(spectrumA_2d_arr[-1, 0], spectrumB_2d_arr[-1, 0])
        wavelength_step = min(np.diff(spectrumA_2d_arr[:, 0]).min(), np.diff(spectrumB_2d_arr[:, 0]).min())
        self.common_wavelength = np.arange(self.min_wavelength, self.max_wavelength, wavelength_step)
    
    def get_min_max_wav(self):
        return self.min_wavelength,  self.max_wavelength

    def liner(self):
        interpolated_refA = np.interp(self.common_wavelength, self.spectrumA_2d_arr[:, 0], self.spectrumA_2d_arr[:, 1])
        interpolated_refB = np.interp(self.common_wavelength, self.spectrumB_2d_arr[:, 0], self.spectrumB_2d_arr[:, 1])
        return [self.common_wavelength, interpolated_refA, interpolated_refB]

    def spline(self, kind):
        spA = interp1d(self.spectrumA_2d_arr[:, 0], self.spectrumA_2d_arr[:, 1], kind=kind, fill_value='extrapolate')
        spB = interp1d(self.spectrumB_2d_arr[:, 0], self.spectrumB_2d_arr[:, 1], kind=kind, fill_value='extrapolate')
        interpolated_refA = spA(self.common_wavelength)
        interpolated_refB = spB(self.common_wavelength)
        return [self.common_wavelength, interpolated_refA, interpolated_refB]
    
    def quadratic_spline(self):
        return self.spline('quadratic')

    def cubic_spline(self):
        return self.spline('cubic')


class SpectrumScaling:
    def normalization(self, ref_1d_arr, exception=True):
        if ref_1d_arr.size == 0 or ref_1d_arr.size == 1:
            if exception:
                print('Not enough elements.')
            return np.nan
        denom = (np.nanmax(ref_1d_arr) - np.nanmin(ref_1d_arr))
        if denom == 0:
            if exception:
                print('ZeroDivisionError.')
            return np.nan
        return (ref_1d_arr - np.nanmin(ref_1d_arr)) / (np.nanmax(ref_1d_arr) - np.nanmin(ref_1d_arr))

    def standardization(self, ref_1d_arr, exception=True):# nanが入っていても大丈夫？
        if ref_1d_arr.size == 0 or ref_1d_arr.size == 1:
            if exception:
                print('Not enough elements.')
            return np.nan
        sd = np.nanstd(ref_1d_arr)
        if sd == 0:
            if exception:
                print('ZeroDivisionError.')
            return np.nan
        return (ref_1d_arr - np.nanmean(ref_1d_arr)) / sd

    def relative_ref(self, target_ref_1d_arr, base_ref_1d_arr, exception=True):
        if target_ref_1d_arr.size == 0 or base_ref_1d_arr.size == 0:
            if exception:
                print('Not enough elements.')
            return np.nan
        if base_ref_1d_arr == 0:
            if exception:
                print('ZeroDivisionError.')
            return np.nan
        return target_ref_1d_arr / base_ref_1d_arr


class SpectraSimilarity:
    def pcc(self, refA_1d_arr, refB_1d_arr, exception=True):
        if refA_1d_arr.size == 0 or refA_1d_arr.size == 1 or refB_1d_arr.size == 0 or refB_1d_arr.size == 1:
            if exception:
                print('Not enough elements.')
            return np.nan
        # 計算結果が行列形式のため、０行１列目を取得。
        return np.corrcoef(refA_1d_arr, refB_1d_arr)[0, 1]

    def cos(self, refA_1d_arr, refB_1d_arr, exception=True):
        if refA_1d_arr.size == 0 or refA_1d_arr.size == 1 or refB_1d_arr.size == 0 or refB_1d_arr.size == 1:
            if exception:
                print('Not enough elements.')
            return np.nan
        v1_norm = np.linalg.norm(refA_1d_arr)
        v2_norm = np.linalg.norm(refB_1d_arr)
        if v1_norm == 0 or v2_norm == 0:
            if exception:
                print('ZeroDivisionError.')
            return np.nan
        return np.dot(refA_1d_arr, refB_1d_arr) / (v1_norm * v2_norm)

    def euclid_dis(self, refA_1d_arr, refB_1d_arr, exception=True):
        if refA_1d_arr.size == 0 or refB_1d_arr.size == 0:
            if exception:
                print('Not enough elements.')
            return np.nan
        return np.linalg.norm(refA_1d_arr - refB_1d_arr)


class SpectrumSmoothing:
    def moving_avg(self, ref, window_size):
        b = np.ones(window_size) / window_size
        ref_mean = np.convolve(ref, b, mode="same")
        n_conv = window_size // 2

        # 補正部分、始めと終わり部分をwindow_sizeの半分で移動平均を取る
        ref_mean[0] *= window_size / n_conv
        for i in range(1, n_conv):
            ref_mean[i] *= window_size / (i + n_conv)
            ref_mean[-i] *= window_size / (i + n_conv - (window_size % 2)) # size % 2は奇数偶数での違いに対応するため
        return ref_mean


class LibraryComparison:
    def __init__(self, library_file, sample_catalogue_file, target_spectrum_file):
        self.load_library(library_file)
        self.load_catalogue(sample_catalogue_file)
        self.load_target(target_spectrum_file)

    def load_library(self, library_file):
        """_summary_

        Args:
            library_file (_type_): _description_
        """
        csv_file = open(library_file, 'r')
        csv_data = list(csv.reader(csv_file))
        csv_file.close()
        self.library_len = len(csv_data)
        # progress_tqdm = tqdm(total=self.library_len, unit=' count')
        self.spectrumID_list = np.empty(self.library_len, dtype=object)
        self.sampleID_list = np.empty(self.library_len, dtype=object)
        self.library_spectra = [None] * self.library_len # 要素数が不均等のためlist
        
        for (i, row), _ in zip(enumerate(csv_data), trange(self.library_len, unit=' count')):
            self.sampleID_list[i] = row[0].upper()
            self.spectrumID_list[i] = row[1]
            band = int(float(row[2]))
            self.library_spectra[i] = np.column_stack((np.array(row[3:band+3], dtype=float), np.array(row[band+3:band*2+3], dtype=float)))
            # progress_tqdm.update(1)
            
        print('>>> Library loading completed.\n')

    def load_catalogue(self, sample_catalogue_file):
        sample_catalogue_df = pd.read_excel(sample_catalogue_file)
        extracted_df = sample_catalogue_df[sample_catalogue_df['SampleID'].isin(self.sampleID_list)]
        self.subtype_df = extracted_df[["SampleID", "SubType"]]

    def load_target(self, target_spectrum_file):
        """対象スペクトルのCSVファイルを読み込み、データフレーム化する。numpy配列を取得。ライブラリのnumpy配列と合体。

        Args:
            target_spectrum_file (str): _description_
        """
        self.raw_target = pd.read_csv(target_spectrum_file).values
        self.target_spectrum = self.raw_target.copy()
        self.raw_spectra = self.library_spectra.copy()
        self.raw_spectra.insert(0, self.target_spectrum)

    def slice_wav(self, min_index=0, max_index=99999):
        """指定の波長範囲にスライス（numpy配列）。必ず線形補間の前に実行しなければならない。

        Args:
            min_index (int, optional): _description_. Defaults to 0.
            max_index (_type_, optional): _description_. Defaults to 99999.
            sliced_target (_type_): スライス済ターゲットスペクトル（numpy配列）。
            target_spectrum (_type_): この先使用するターゲットスペクトル（numpy配列）。
        """
        self.sliced_target = self.target_spectrum[min_index:max_index, :]
        self.target_spectrum = self.sliced_target

    def interpolate(self, interp_type='liner'):
        """補間。

        Args:
            interp_type (str, optional): _description_. Defaults to 'liner'.
            interpolation (): インスタンス。
            interpolated_arr (): 対象スペクトルとの共通波長、補間後の対象スペクトル、補間後のライブラリスペクトル。
            spectra_set (): 対象スペクトルとの共通波長、補間後の対象スペクトル、補間後のライブラリスペクトル。
            min_wav_list (): 比較後の波長最小値。
            max_wav_list (): 比較後の波長最大値。
        """
        target_spectrum = self.target_spectrum
        library_spectra = self.library_spectra
        interpolated_arr = np.empty(self.library_len).tolist()
        min_wav_list = np.empty(self.library_len).tolist()
        max_wav_list = np.empty(self.library_len).tolist()

        if interp_type == 'liner':
            for i in trange(self.library_len, unit=' count'):
                interpolation = SpectraInterpolation(target_spectrum, library_spectra[i])
                interpolated_arr[i] = interpolation.liner()
                min_wav_list[i], max_wav_list[i] = interpolation.get_min_max_wav()
        elif interp_type == 'sp':
            for i in trange(self.library_len, unit=' count'):
                interpolation = SpectraInterpolation(target_spectrum, library_spectra[i])
                interpolated_arr[i] = interpolation.spline()
                min_wav_list[i], max_wav_list[i] = interpolation.get_min_max_wav()
        # elif interp_type == 'quadsp':
        #     for i in tqdm(range(self.library_len), unit=' count'):
        #         interpolation = SpectraInterpolation(target_spectrum, library_spectra[i])
        #         interpolated_arr[i] = interpolation.quadratic_spline()
        #         min_wav_list[i], max_wav_list[i] = interpolation.get_min_max_wav()
        # elif interp_type == 'cubicsp':
        #     for i in tqdm(range(self.library_len), unit=' count'):
        #         interpolation = SpectraInterpolation(target_spectrum, library_spectra[i])
        #         interpolated_arr[i] = interpolation.cubic_spline()
        #         min_wav_list[i], max_wav_list[i] = interpolation.get_min_max_wav()

        self.interpolated_arr = interpolated_arr
        self.spectra_set = interpolated_arr
        self.min_wav_list = min_wav_list
        self.max_wav_list = max_wav_list
        print('>>> Interpolation completed.\n')

    def scaling(self, method, base_ref=None):
        # note scikit-learnで良くない？
        """_summary_

        Args:
            method (_type_): _description_
            base_ref (_type_, optional): _description_. Defaults to None.
        """
        interpolated_arr = self.spectra_set
        scaled_arr = np.empty(self.library_len).tolist()
        band_list = np.empty(self.library_len).tolist()
        ss = SpectrumScaling()

        if method == 'norm':
            for i in trange(self.library_len, unit=' count'):
                scaled_target = ss.normalization(interpolated_arr[i][1], False)
                scaled_library = ss.normalization(interpolated_arr[i][2], False)

                if type(scaled_target).__module__ != np.__name__:
                    interp_wav, scaled_target, scaled_library = np.empty(0), np.empty(0), np.empty(0) 
                else:
                    interp_wav = interpolated_arr[i][0]

                scaled_arr[i] = np.vstack((interp_wav, scaled_target, scaled_library))
                band_list[i] = len(interp_wav)
        elif method == 'st':
            for i in trange(self.library_len, unit=' count'):
                scaled_target = ss.standardization(interpolated_arr[i][1], False)
                scaled_library = ss.standardization(interpolated_arr[i][2], False)

                if type(scaled_target).__module__ != np.__name__:
                    interp_wav, scaled_target, scaled_library = np.empty(0), np.empty(0), np.empty(0) 
                else:
                    interp_wav = interpolated_arr[i][0]

                scaled_arr[i] = np.vstack((interp_wav, scaled_target, scaled_library))
                band_list[i] = len(interp_wav)
        elif method == 'if': 
            # check
            for i in trange(self.library_len, unit=' count'):
                scaled_target = ss.relative_ref(interpolated_arr[i][1], False)
                scaled_library = ss.relative_ref(interpolated_arr[i][2], False)
                interp_wav = interpolated_arr[i][0] if scaled_target != np.nan else np.empty(0)
                scaled_arr[i] = np.vstack((interp_wav, scaled_target, scaled_library))
                band_list[i] = len(interp_wav)

        self.scaled_arr = scaled_arr
        self.spectra_set = scaled_arr
        self.band_list = band_list
        print('>>> Scaling completed.\n')

    def get_scaled_arr(self):
        return self.scaled_arr

    def find_common_valley_indices(self, prominence=0.1):
        """共通の谷点（インデックス）を取得する。
        """
        common_valleys = np.empty(self.library_len).tolist()
        spectra_set = self.spectra_set

        for i in trange(self.library_len, unit=' count'):
            if spectra_set[i][1].size != 0:
                valleys_indexA, _ = find_peaks(-spectra_set[i][1], prominence=prominence)
                valleys_indexB, _ = find_peaks(-spectra_set[i][2], prominence=prominence)
                common_valleys[i] = np.intersect1d(valleys_indexA, valleys_indexB)
                if common_valleys[i].size == 0:
                    spectra_set[i] = np.vstack((np.empty(0), np.empty(0), np.empty(0)))
            else:
                common_valleys[i] = np.empty(0)

        self.common_valleys = common_valleys
        print('>>> Find common valleys completed.\n')

    def measure_similarity(self, similarity_type='pcc'):
        """類似度比較には、同じ要素数であること、
        補間が必要。

        Args:
            similarity_type (str, optional): _description_. Defaults to 'pcc'.

        Returns:
            _type_: _description_
        """
        sim_results = np.empty(self.library_len).tolist()
        spectra_set = self.spectra_set
        sim = SpectraSimilarity()

        if similarity_type == 'pcc':
            for i in trange(self.library_len, unit=' count'):
                sim_results[i] = sim.pcc(spectra_set[i][1], spectra_set[i][2], False)
        elif similarity_type == 'cos':
            for i in trange(self.library_len, unit=' count'):
                sim_results[i] = sim.cos(spectra_set[i][1], spectra_set[i][2], False)
        elif similarity_type == 'edis':
            for i in trange(self.library_len, unit=' count'):
                sim_results[i] = sim.euclid_dis(spectra_set[i][1], spectra_set[i][2], False)
        print('>>> Similarity measurement completed.\n')

        result_df = pd.DataFrame(
            data={
                'SpectrumID': self.spectrumID_list, 
                'SampleID': self.sampleID_list,
                similarity_type: sim_results, 
                'Band': self.band_list, 
                'Min Wavelength': self.min_wav_list, 
                'Max Wavelength': self.max_wav_list,
                }
        )
        result_df = pd.merge(result_df, self.subtype_df, on='SampleID', how='outer')
        data = [['target', 'target', 1, len(self.target_spectrum), self.target_spectrum[0][0], self.target_spectrum[-1][0], 'target']]
        target_row = pd.DataFrame(data=data, columns=result_df.columns)
        result_df = pd.concat([target_row, result_df]).reset_index(drop=True)
        # result_df = pd.concat([target_row, result_df])#.reset_index(drop=True)
        # result_df.set_index("SpectrumID", inplace=True)
        self.result_df = result_df
        # print(result_df)
        # return result_df

    def result(self):
        return self.result_df
    
    def plot(self, df, index_list, sp_type, avg_size=None, find=None, prominence=0.1):

        def find_valleys(wav, ref):
            valleys, _ = find_peaks(-ref, prominence=prominence)
            valleys_wav = wav[valleys]
            valleys_ref = ref[valleys]
            plt.plot(valleys_wav, valleys_ref, 'bx')#, label=f'valley (index), prominence {prominence}')

            for i, label in enumerate([n for n in valleys]):
                # plt.text(valleys_wav[i], valleys_ref[i], label)
                pass


        colors = ['red', 'blue', 'green', 'orange', 'pink']
        plt.figure(figsize=(8, 6))

        if sp_type == 'raw':
            plt.title('Raw Spectra Data')
            for i, index in enumerate(index_list):
                x = [row[0] for row in self.raw_spectra[index]]
                y = [row[1] for row in self.raw_spectra[index]]
                # x = [row[0] for row in df[index]]
                # y = [row[1] for row in df[index]]

                if avg_size != None:
                    y = SpectrumSmoothing().moving_avg(y, avg_size)
                    plt.plot(x, y, color=colors[i % 5], label=f'Ind {index}, {self.result_df.iloc[index,6]}, moving size {avg_size}')
                else:
                    plt.plot(x, y, color=colors[i % 5], label=f'Ind {index}, {self.result_df.iloc[index,6]}')

                if find == 'valley':
                    find_valleys(np.array(x), np.array(y))

        elif sp_type == 'scaled':
            if len(index_list) == 0:
                return print('Please specify a index other than 0.')
            # print(len(index))
            # if len(index) > 1:
            #     return print('Please specify one index.')

            x1 = self.scaled_arr[index - 1][0]
            y1 = self.scaled_arr[index - 1][1]
            y2 = self.scaled_arr[index - 1][2]
            # y_d = signal.detrend(self.scaled_arr[index-1][1])

            valleys1, _ = find_peaks(-y1, prominence=0.1)
            valleys2, _ = find_peaks(-y2, prominence=0.1)
            valleys_wav1 = x1[valleys1]
            valleys_wav2 = x1[valleys2]
            valleys_ref1 = y1[valleys1]
            valleys_ref2 = y2[valleys2]


            plt.plot(x1, y1, color=colors[0], label=f'Index {0}')
            # plt.plot(x1, y_d, color=colors[1], label=f'Index {0} Detrend')
            plt.plot(x1, y2, color=colors[2], label=f'Ind {index}, {self.result_df.iloc[index,6]}')
            # plt.plot(x1, y-y_d, color=colors[3],label="Trend")

            plt.plot(valleys_wav1, valleys_ref1, 'bx', label='peak point')
            labels = ['idx.'+str(num) for num in valleys1]
            for i, label in enumerate(labels):
                # plt.text(valleys_wav1[i], valleys_ref1[i], label)
                pass

            plt.plot(valleys_wav2, valleys_ref2, 'bx', label='peak point')
            labels = ['idx.'+str(num) for num in valleys2]
            for i, label in enumerate(labels):
                # plt.text(valleys_wav2[i], valleys_ref2[i], label)
                pass

            plt.title('Scaled Spectra Data')

        plt.xlabel('Wavelength')
        plt.ylabel('Reflectance')
        plt.rcParams["font.size"] = 18
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0) 
        plt.grid(True)
        plt.show()

    