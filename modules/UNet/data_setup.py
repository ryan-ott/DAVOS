import torch
from torchvision import transforms
import torchvision.transforms.functional as TF
from torch.utils.data import Dataset, DataLoader
import os

class SegmentationDataset(Dataset):
    def __init__(self, image_dir, mask_dir, true_mask_dir, transform=None):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.true_mask_dir = true_mask_dir
        self.filenames = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
        self.transform = transform
        
    def load_image(self, idx: int):
        image_path = os.path.join(self.image_dir, self.filenames[idx])
        mask_path = os.path.join(self.mask_dir, self.filenames[idx])
        true_mask_path = os.path.join(self.true_mask_dir, self.filenames[idx])
        return torch.load(image_path), torch.load(mask_path), torch.load(true_mask_path)
    
    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        # image_path = os.path.join(self.image_dir, self.filenames[idx])
        # mask_path = os.path.join(self.mask_dir, self.filenames[idx])

        # image = torch.load(image_path)  # Load the image tensor
        # mask = torch.load(mask_path)    # Load the mask tensor
        image, mask, true_mask = self.load_image(idx)
        input_tensor = torch.cat([image, mask], dim=0)  # Concatenating image and mask

        if self.transform:
            input_tensor = self.transform(input_tensor)
            true_mask = self.transform(true_mask)

        return input_tensor, true_mask