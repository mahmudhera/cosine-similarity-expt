import os
from scipy.stats.stats import pearsonr
import numpy as np
from matplotlib import pyplot as plt

ksizes = [11, 21, 31]
seed_list = range(20)
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
    minhash_avg_pearson_coefficients = []
    fmh_avg_pearson_coefficients = []
    minhash_errors = []
    fmh_errors = []

    chosen_ground_truth_cosines = None
    chosen_mash_cosines = None
    chosen_fmh_cosines = None

    for k in ksizes:
        ground_truth_mat_filename = f'fmh_signatures_and_matrices/sourmash_cos_sim_mat_k_{k}_scaled_1.csv'
        f = open(ground_truth_mat_filename, 'r')
        order = f.readlines()[0].strip()
        order = order.replace('../ecoli_genomes/', '')
        order_ground_truth = order.replace('.gz', '')
        f.close()

        for seed in seed_list:
            fmh_cos_sim_mat_filename = f'fmh_signatures_and_matrices/sourmash_cos_sim_mat_k_{k}_scaled_1000_seed_{seed}.csv'
            f = open(fmh_cos_sim_mat_filename, 'r')
            order = f.readlines()[0].strip()
            order = order.replace('../ecoli_genomes/', '')
            order_this_file = order.replace('.gz', '')
            f.close()

            if order_this_file != order_ground_truth:
                print('NOOO')

        for seed in seed_list:
            mash_cos_sim_mat_filename = f'mash_sketches/mash_cos_sim_mat_k_{k}_seed_{seed}'
            f = open(mash_cos_sim_mat_filename, 'r')
            order_this_file = f.readlines()[0].strip()
            f.close()

            if order_this_file != order_ground_truth:
                print('NOOO')

        # so, we know that the order in all files are the same
        # therefore, can now just concat all rows one after another
        ground_truth_mat_filename = f'fmh_signatures_and_matrices/sourmash_cos_sim_mat_k_{k}_scaled_1.csv'
        f = open(ground_truth_mat_filename, 'r')
        all_lines = f.readlines()
        ground_truth_vector = []
        for line in all_lines[1:]:
            line = line.strip()
            ground_truth_vector = ground_truth_vector + [float(x) for x in line.split(',')]
        f.close()

        if k == selected_k:
            chosen_ground_truth_cosines = ground_truth_vector

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

            if k == selected_k and seed == 0:
                chosen_fmh_cosines = vector_this_file

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

            if k == selected_k and seed == 0:
                chosen_mash_cosines = vector_this_file

        print(f'ksize = {k}')
        print(f'FMH pearson coefficient avg: {np.mean(fmh_pearson_coefficients)}, stddev: {np.var(fmh_pearson_coefficients)}')
        print(f'MinHash pearson coefficient avg: {np.mean(mash_person_coefficients)}, stddev: {np.var(mash_person_coefficients)}')
        minhash_avg_pearson_coefficients.append(np.mean(mash_person_coefficients))
        fmh_avg_pearson_coefficients.append(np.mean(fmh_pearson_coefficients))
        minhash_errors.append(np.var(mash_person_coefficients)**0.5)
        fmh_errors.append(np.var(fmh_pearson_coefficients)**0.5)

    print(ksizes)
    print(minhash_avg_pearson_coefficients)
    print(fmh_avg_pearson_coefficients)

    labels = [ f'$k$ = {k}' for k in ksizes ]
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, minhash_avg_pearson_coefficients, width, label='MinHash (sketch size = 1000)', yerr=minhash_errors, ecolor='black', capsize=5)
    rects2 = ax.bar(x + width/2, fmh_avg_pearson_coefficients, width, label='FracMinHash (scale factor = 0.001)', yerr=fmh_errors, ecolor='black', capsize=5)

    autolabel(rects1)
    autolabel(rects2)

    ax.set_ylim(0.0, 1.3)

    ax.set_ylabel('Average Pearson correlarion coefficient')
    ax.set_xlabel('$k$-mer size')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_yticklabels(['0.0', '0.2', '0.4', '0.6', '0.8', '1.0', ''])
    ax.legend()

    fig.tight_layout()
    plt.savefig('avg_corr_coeff.pdf')


    plt.clf()
    plt.scatter(chosen_ground_truth_cosines, chosen_mash_cosines, label='MinHash (sketch size = 1000)', alpha=0.4)
    plt.scatter(chosen_ground_truth_cosines, chosen_fmh_cosines, label='FMH (scale factor = 0.001)', alpha=0.4)
    plt.plot([0,1], [0,1], linestyle='--', color='grey', alpha=0.7)
    plt.legend()
    plt.xlabel(f'Pairwise cosine using all {selected_k}-mers')
    plt.ylabel('Pairwise cosine using sketches')
    plt.savefig(f'true_vs_est_for_{selected_k}_mers.pdf')
