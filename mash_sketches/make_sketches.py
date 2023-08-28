import subprocess
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create mash sketches from a list of fna.gz files.")
    parser.add_argument('--genome_dir', '-g', type=str, help="Directory where the genomes are")
    args = parser.parse_args()
    genomes_directory = args.genome_dir

    file_list = os.listdir(genomes_directory)
    for filename in file_list:
        complete_file_path = os.path.join(genomes_directory, filename)
        mash_sketch_filename = filename+'.msh'
        mash_readable_sketch_filename = mash_sketch_filename+'.json'

        cmd = f'mash sketch -k 21 {complete_file_path} -o {mash_sketch_filename}'
        subprocess.call(cmd.split(' '))

        cmd = f'mash info {mash_sketch_filename} -d'
        f = open(mash_readable_sketch_filename, 'w')
        subprocess.call(cmd.split(' '), stdout=f)
        f.close()
