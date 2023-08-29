import os
from scipy.stats import pearsonr
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

ksizes = [11, 21, 31]
seed_list = range(100)
selected_k = 11

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{:.3f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

if __name__ == '__main__':

    data_boxplot = {}
    data_boxplot['Pearson correlation coefficient'] = []
    data_boxplot['$k$-mer size'] = []
    data_boxplot['Sketch technique'] = []

    for k in ksizes:
        ground_truth_mat_filename = f'fmh_signatures_and_matrices/sourmash_cos_sim_mat_k_{k}_scaled_1.csv'
        f = open(ground_truth_mat_filename, 'r')
        all_lines = f.readlines()
        ground_truth_vector = []
        for line in all_lines[1:]:
            line = line.strip()
            ground_truth_vector = ground_truth_vector + [float(x) for x in line.split(',')]
        f.close()

        fmh_pearson_coefficients = []
        for seed in seed_list:
            fmh_cos_sim_mat_filename = f'fmh_signatures_and_matrices/sourmash_cos_sim_mat_k_{k}_scaled_1000_seed_{seed}.csv'
            f = open(fmh_cos_sim_mat_filename, 'r')
            all_lines = f.readlines()
            vector_this_file = []
            for line in all_lines[1:]:
                line = line.strip()
                vector_this_file = vector_this_file + [float(x) for x in line.split(',')]
            f.close()
            fmh_pearson_coefficients.append( pearsonr(ground_truth_vector, vector_this_file)[0] )

        mash_person_coefficients = []
        for seed in seed_list:
            mash_cos_sim_mat_filename = f'mash_sketches/mash_cos_sim_mat_k_{k}_seed_{seed}'
            f = open(mash_cos_sim_mat_filename, 'r')
            all_lines = f.readlines()
            vector_this_file = []
            for line in all_lines[1:]:
                line = line.strip()
                vector_this_file = vector_this_file + [float(x) for x in line.split(',')]
            f.close()
            mash_person_coefficients.append( pearsonr(ground_truth_vector, vector_this_file)[0] )

        data_boxplot['Pearson correlation coefficient'] = data_boxplot['Pearson correlation coefficient'] + mash_person_coefficients
        data_boxplot['$k$-mer size'] = data_boxplot['$k$-mer size'] + [f'$k$={k}' for _ in seed_list]
        data_boxplot['Sketch technique'] = data_boxplot['Sketch technique'] + ['MinHash (sketch size = 1000)' for _ in seed_list]

        data_boxplot['Pearson correlation coefficient'] = data_boxplot['Pearson correlation coefficient'] + fmh_pearson_coefficients
        data_boxplot['$k$-mer size'] = data_boxplot['$k$-mer size'] + [f'$k$={k}' for _ in seed_list]
        data_boxplot['Sketch technique'] = data_boxplot['Sketch technique'] + ['FracMinHash (scale factor = 0.001)' for _ in seed_list]

    df = pd.DataFrame(data_boxplot)
    plt.ylim(0.89, 1.0)
    sns.boxplot(y='Pearson correlation coefficient', x='$k$-mer size', data=df, hue='Sketch technique', saturation=1, linewidth=0.6, fliersize=3)
    plt.savefig('boxplot_of_pearson_coefficients.pdf')
