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
        aus = pd.read_csv(opt.tar_aus_path)[2:19].values
        instance.generate_images(opt.src_img_path, aus)
    else:
        solver = create_solver(opt)
        solver.run_solver()

    print('[THE END]')