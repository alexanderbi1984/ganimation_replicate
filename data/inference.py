from .base_dataset import BaseDataset
import os
import numpy as np


class InferenceDataset(BaseDataset):
    """Custom dataset for CelebA with fixed source and target sets."""

    def __init__(self, src_imgs, tar_imgs):
        """
        Initializes the dataset with fixed source and target image paths.

        Parameters:
            src_imgs (list): List of paths to source images.
            tar_imgs (list): List of paths to target images.
        """
        super(InferenceDataset, self).__init__()
        self.src_imgs = src_imgs  # Fixed source image paths
        self.tar_imgs = tar_imgs  # Fixed target image paths

    def initialize(self, opt):
        super(InferenceDataset, self).initialize(opt)
        # You can add any additional initialization here

    def get_aus_by_path(self, img_path):
        """Retrieve Action Units (AUs) for a given image path."""
        assert os.path.isfile(img_path), "Cannot find image file: %s" % img_path
        img_id = str(os.path.splitext(os.path.basename(img_path))[0])
        return self.aus_dict[img_id] / 5.0  # Normalize to [0, 1]

    def __getitem__(self, index):
        """Get the source and target image along with their attributes."""
        # Use the index to get source and target images
        src_img_path = self.src_imgs[index % len(self.src_imgs)]  # Wrap around if index exceeds src_imgs
        tar_img_path = self.tar_imgs[index % len(self.tar_imgs)]  # Wrap around if index exceeds tar_imgs

        # Load source image
        src_img = self.get_img_by_path(src_img_path)
        src_img_tensor = self.img2tensor(src_img)
        src_aus = self.get_aus_by_path(src_img_path)

        # Load target image
        tar_img = self.get_img_by_path(tar_img_path)
        tar_img_tensor = self.img2tensor(tar_img)
        tar_aus = self.get_aus_by_path(tar_img_path)

        # Optionally add noise to target AUs during training
        if self.is_train and not self.opt.no_aus_noise:
            tar_aus += np.random.uniform(-0.1, 0.1, tar_aus.shape)

        # Record paths for debug and test usage
        data_dict = {
            'src_img': src_img_tensor,
            'src_aus': src_aus,
            'tar_img': tar_img_tensor,
            'tar_aus': tar_aus,
            'src_path': src_img_path,
            'tar_path': tar_img_path
        }

        return data_dict

    def __len__(self):
        """Return the length of the dataset based on the fixed source images."""
        return max(len(self.src_imgs), len(self.tar_imgs))  # Return the maximum length for indexing
