import torch
import os
from PIL import Image
import random
import numpy as np
import pickle
import torchvision.transforms as transforms



class BaseDataset(torch.utils.data.Dataset):
    """docstring for BaseDataset"""
    def __init__(self):
        super(BaseDataset, self).__init__()

    def name(self):
        return os.path.basename(self.opt.data_root.strip('/'))

    def initialize(self, opt):
        self.opt = opt
        self.imgs_dir = os.path.join(self.opt.data_root, self.opt.imgs_dir)
        self.is_train = self.opt.mode == "train"

        # load images path 
        filename = self.opt.train_csv if self.is_train else self.opt.test_csv
        self.imgs_name_file = os.path.join(self.opt.data_root, filename)
        self.imgs_path = self.make_dataset()


        # load AUs dicitionary 
        aus_pkl = os.path.join(self.opt.data_root, self.opt.aus_pkl)
        self.aus_dict = self.load_dict(aus_pkl)
        if self.opt.mode == 'inference':
            aus_pkl_src = os.path.join(self.opt.data_root, self.opt.aus_pkl_src)
            self.aus_dict_src = self.load_dict(aus_pkl_src)
            aus_pkl_tar = os.path.join(self.opt.data_root, self.opt.aus_pkl_tar)
            self.aus_dict_tar = self.load_dict(aus_pkl_tar)


        # load image to tensor transformer
        self.img2tensor = self.img_transformer()

        # if the mode is inference, then set src_img and tar_img
        if self.opt.mode == 'inference':
            src_filename = self.opt.src_csv  # Fixed source image paths
            tar_filename = self.opt.tar_csv  # Fixed target image paths
            self.src_imgs_name_file = os.path.join(self.opt.data_root, src_filename)
            self.src_imgs_path = self.make_dataset()
            self.tar_imgs_name_file = os.path.join(self.opt.data_root, tar_filename)
            self.tar_imgs_path = self.make_dataset()



    def make_dataset(self):
        return None

    def load_dict(self, pkl_path):
        saved_dict = {}
        with open(pkl_path, 'rb') as f:
            saved_dict = pickle.load(f, encoding='latin1')
        return saved_dict

    def get_img_by_path(self, img_path):
        assert os.path.isfile(img_path), "Cannot find image file: %s" % img_path
        img_type = 'L' if self.opt.img_nc == 1 else 'RGB'
        return Image.open(img_path).convert(img_type)

    def get_aus_by_path(self, img_path):
        return None

    def img_transformer(self):
        transform_list = []
        if self.opt.resize_or_crop == 'resize_and_crop':
            transform_list.append(transforms.Resize([self.opt.load_size, self.opt.load_size], Image.BICUBIC))
            transform_list.append(transforms.RandomCrop(self.opt.final_size))
        elif self.opt.resize_or_crop == 'crop':
            transform_list.append(transforms.RandomCrop(self.opt.final_size))
        elif self.opt.resize_or_crop == 'none':
            # Replace lambda with a separate method call
            transform_list.append(transforms.Lambda(self.identity_transform))
            # transform_list.append(transforms.Lambda(lambda image: image))
        else:
            raise ValueError("--resize_or_crop %s is not a valid option." % self.opt.resize_or_crop)

        if self.is_train and not self.opt.no_flip:
            transform_list.append(transforms.RandomHorizontalFlip())

        transform_list.append(transforms.ToTensor())
        transform_list.append(transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)))

        img2tensor = transforms.Compose(transform_list)

        return img2tensor

    # def __len__(self):
    #     return len(self.imgs_path)
    def identity_transform(self, image):
        return image  # Identity transformation

    def __len__(self):
        return len(self.imgs_path)

    def __getitem__(self, idx):
        img_path = self.imgs_path[idx]
        image = self.get_img_by_path(img_path)
        return self.img2tensor(image)  # Apply the transformation




    







