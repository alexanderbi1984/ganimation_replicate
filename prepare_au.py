import numpy as np
import os
from tqdm import tqdm
import argparse
import glob
import re
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('-ia', '--input_aus_filesdir', type=str, help='Dir with imgs aus files')
parser.add_argument('-op', '--output_path', type=str, help='Output path')
args = parser.parse_args()

def get_data(filepaths):
    data = dict()
    for filepath in tqdm(filepaths):
        content = np.loadtxt(filepath, delimiter=',', skiprows=1)
        data[os.path.basename(filepath[:-4])] = content[2:19]

    return data

def save_dict(data, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def main():
    input_aus_filesdir = r"W:\Nan\OpenFace_2.2.0_win_x64\OpenFace_2.2.0_win_x64\processed"
    output_path = r'datasets/biovid'
    filepaths = glob.glob(os.path.join(input_aus_filesdir, '*.csv'))
    filepaths.sort()

    # create aus file
    data = get_data(filepaths)

    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    save_dict(data, os.path.join(output_path, "aus_openface"))


if __name__ == '__main__':
    main()