"""
Created on Dec 13, 2018
@author: Yuedong Chen
"""

from options import Options
from solvers import create_solver
from video_generator import VideoGenerator
import pandas as pd




if __name__ == '__main__':
    opt = Options().parse()
    if opt.mode == 'generate':
        instance = VideoGenerator(opt)
        # Read the CSV file into a DataFrame
        data = pd.read_csv(opt.tar_aus_path)
        # Select the columns from index 2 (3rd column) to index 18 (19th column)
        aus = data.iloc[:, 2:19].values  # This selects all rows and columns 2 to 18
        instance.generate_images(opt.src_img_path, aus)
    else:
        solver = create_solver(opt)
        solver.run_solver()

    print('[THE END]')