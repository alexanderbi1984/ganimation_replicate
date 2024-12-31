from .base_dataset import BaseDataset
import os
import random
import numpy as np


class CelebADataset(BaseDataset):
    """docstring for CelebADataset"""
    def __init__(self):
        super(CelebADataset, self).__init__()
        
    def initialize(self, opt):
        super(CelebADataset, self).initialize(opt)

    def get_aus_by_path(self, img_path):
        assert os.path.isfile(img_path), "Cannot find image file: %s" % img_path
        img_id = str(os.path.splitext(os.path.basename(img_path))[0])
        return self.aus_dict[img_id] / 5.0   # norm to [0, 1]
    def get_src_aus_by_path(self, img_path):
        assert os.path.isfile(img_path), "Cannot find image file: %s" % img_path
        img_id = str(os.path.splitext(os.path.basename(img_path))[0])
        return self.src_aus_dict[img_id] / 5.0
    def get_tar_aus_by_path(self, img_path):

        assert os.path.isfile(img_path), "Cannot find image file: %s" % img_path
        img_id = str(os.path.splitext(os.path.basename(img_path))[0])
        return self.tar_aus_dict[img_id] / 5.0

    def make_dataset(self,imgs_name_file=None):
        # return all image full path in a list
        imgs_path = []
        if self.opt.mode != 'inference':
            imgs_name_file = self.imgs_name_file
        assert os.path.isfile(imgs_name_file), "%s does not exist." % self.imgs_name_file
        with open(imgs_name_file, 'r') as f:
            lines = f.readlines()
            imgs_path = [os.path.join(self.imgs_dir, line.strip()) for line in lines]
            imgs_path = sorted(imgs_path)
        return imgs_path

    def __getitem__(self, index):
        if self.opt.mode == 'train' or self.opt.mode == 'test':
            img_path = self.imgs_path[index]

            # load source image
            src_img = self.get_img_by_path(img_path)
            src_img_tensor = self.img2tensor(src_img)
            src_aus = self.get_aus_by_path(img_path)
            src_img_path = img_path

            # load target image
            tar_img_path = random.choice(self.imgs_path)
            tar_img = self.get_img_by_path(tar_img_path)
            tar_img_tensor = self.img2tensor(tar_img)
            tar_aus = self.get_aus_by_path(tar_img_path)

        else:
            src_img_path = self.src_imgs_path[index]
            src_img = self.get_img_by_path(src_img_path)
            src_img_tensor = self.img2tensor(src_img)
            src_aus = self.get_src_aus_by_path(src_img_path)
            tar_img_path = self.tar_imgs_path[index]
            tar_img = self.get_img_by_path(tar_img_path)
            tar_img_tensor = self.img2tensor(tar_img)
            tar_aus = self.get_tar_aus_by_path(tar_img_path)

        if self.is_train and not self.opt.no_aus_noise:
            tar_aus = tar_aus + np.random.uniform(-0.1, 0.1, tar_aus.shape)
        # record paths for debug and test usage
        data_dict = {'src_img':src_img_tensor, 'src_aus':src_aus, 'tar_img':tar_img_tensor, 'tar_aus':tar_aus, \
                        'src_path':src_img_path, 'tar_path':tar_img_path}

        return data_dict
