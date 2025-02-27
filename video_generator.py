from model import create_model
import torch
import os
from PIL import Image
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from assemble_video_from_frames import assemble_videos_from_frames



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
        image_numpy = image_numpy[0]
        # print(f"the shape of image_numpy is {image_numpy.shape}")

        # if image_numpy.shape[0] == 1:
        #     image_numpy = np.tile(image_numpy, (3, 1, 1))
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
            gpu_ids = self.opt.gpu_ids
            device = torch.device('cuda:%d' % gpu_ids[0] if gpu_ids else 'cpu')
            src_img= src_img_tensor.unsqueeze(0).to(device)
            tar_aus = tar_aus / 5.0
            if isinstance(tar_aus, np.ndarray):
                tar_aus = torch.from_numpy(tar_aus)  # Convert NumPy array to PyTorch tensor

            tar_aus = tar_aus.type(torch.FloatTensor).to(device)
            # print(f"the shape of source image is {src_img.shape}")
            # print(f"the shape of target image is {tar_aus.shape}")
            color_mask, aus_mask, embed = self.model.net_gen(src_img, tar_aus)
            fake_img = aus_mask * src_img + (1 - aus_mask) * color_mask
            fake_img = fake_img.cpu().float().numpy()
            fake_img = self.numpy2im(fake_img)
            # Display the fake_img using matplotlib
            # plt.imshow(fake_img)
            # plt.axis('off')  # Turn off axis for better visualization
            # plt.show()
            return fake_img
        
        
    def generate_video(self, src_img_path, tar_aus_path, output_path):
        assert os.path.isdir(src_img_path), "src_img_path should be a folder"
        os.makedirs(output_path, exist_ok=True)
        
        for i, file_name in enumerate(sorted(os.listdir(src_img_path))):
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                img_path = os.path.join(src_img_path, file_name)
                aus_data = pd.read_csv(tar_aus_path)
                base_name_src = os.path.splitext(os.path.basename(file_name))[0]
                base_name_tar = os.path.splitext(os.path.basename(tar_aus_path))[0]
                for i in range(aus_data.shape[0]):
                    # tar_aus = aus_data.iloc[i].values[5:22]
                    tar_aus = aus_data.iloc[i, 5:22].values.reshape(1,17)
                    # print(f"the target aus is like {tar_aus}")
                    # print(f"the shape of aus is {tar_aus.shape}")
                    fake_img = self.generate_images(img_path, tar_aus)
                    # Create unique filename using the specified convention
                    fake_img_name = f'{base_name_tar}-{base_name_src}_{i}.bmp'
                    fake_video_name = f'{base_name_src}-{base_name_tar}'
                    fake_video_path = os.path.join(output_path, fake_video_name)
                    os.makedirs(fake_video_path, exist_ok=True)
                    fake_img_path = os.path.join(fake_video_path, fake_img_name)
                    fake_img.save(fake_img_path)
                fake_video_path = os.path.abspath(fake_video_path)
                output_path = os.path.abspath(output_path)
                # print(fake_video_path)
                # print(output_path)
                assemble_videos_from_frames(fake_video_path,output_path)