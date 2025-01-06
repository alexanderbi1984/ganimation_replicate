from model import create_model
import torch
import os
from PIL import Image
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt


class VideoGenerator:
    def __init__(self,opt):
        super(VideoGenerator, self).__init__()
        self.name = "VideoGenerator"
        self.model = create_model(opt)
        self.opt = opt
        
    def get_img_by_path(self, img_path):
        assert os.path.isfile(img_path), "Cannot find image file: %s" % img_path
        img_type = 'L' if self.opt.img_nc == 1 else 'RGB'
        return Image.open(img_path).convert(img_type)
    
    def identity_transform(self, image):
        return image  # Identity transformation

    def numpy2im(self, image_numpy, imtype=np.uint8):
        if image_numpy.shape[0] == 1:
            image_numpy = np.tile(image_numpy, (3, 1, 1))
        # input should be [0, 1]
        #image_numpy = np.transpose(image_numpy, (1, 2, 0)) * 255.0
        image_numpy = (np.transpose(image_numpy, (1, 2, 0)) / 2. + 0.5) * 255.0
        # print(image_numpy.shape)
        image_numpy = image_numpy.astype(imtype)
        im = Image.fromarray(image_numpy)
        return im   # np.array(im)
    
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

        transform_list.append(transforms.ToTensor())
        transform_list.append(transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)))

        img2tensor = transforms.Compose(transform_list)

        return img2tensor
    
    def generate_images(self, src_img_path, tar_aus):
        with (torch.no_grad()):
            src_img_raw = self.get_img_by_path(src_img_path)
            img2tensor = self.img_transformer()
            src_img_tensor = img2tensor(src_img_raw)
            src_img= src_img_tensor.to(self.opt.device)
            tar_aus = tar_aus / 5.0
            color_mask, aus_mask, embed = self.model.net_gen(src_img, tar_aus)
            fake_img = aus_mask * src_img + (1 - aus_mask) * color_mask
            fake_img = fake_img.cpu().float().numpy()
            fake_img = self.numpy2im(fake_img)
            # Display the fake_img using matplotlib
            plt.imshow(fake_img)
            plt.axis('off')  # Turn off axis for better visualization
            plt.show()