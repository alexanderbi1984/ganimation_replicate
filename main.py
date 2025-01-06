"""
Created on Dec 13, 2018
@author: Yuedong Chen
"""

from options import Options
from solvers import create_solver
from video_generator import VideoGenerator




if __name__ == '__main__':
    opt = Options().parse()
    if opt.mode == 'generate':
        instance = VideoGenerator(opt)
        instance.generate_images(opt.src_img_path, opt.tar_aus)
    else:
        solver = create_solver(opt)
        solver.run_solver()

    print('[THE END]')