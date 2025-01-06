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
        instance.generate_video(opt.src_img_path, opt.tar_aus_path,opt.out_img_path)
        # # Read the CSV file into a DataFrame
        # data = pd.read_csv(opt.tar_aus_path)
        # # Select the columns from index 2 (3rd column) to index 18 (19th column)
        # aus = data.iloc[:, 2:19].values  # This selects all rows and columns 2 to 18
        # print(aus.shape)
        # instance.generate_images(opt.src_img_path, aus)
    else:
        solver = create_solver(opt)
        solver.run_solver()

    print('[THE END]')

#how to use the generate image function
# python main.py --mode generate --src_img_path "W:\Nan\ganimation_replicate\datasets\biovid\imgs\071911_w_24-PA3-009_frame_det_00_000002.bmp" --tar_aus_path "W:\Nan\OpenFace_2.2.0_win_x64\OpenFace_2.2.0_win_x64\processed\frame_det_00_000002.csv" --ckpt_dir ckpts/emotionNet/ganimation/190327_160828 --load_epoch 30 --data_root dataset/biovid --batch_size 1