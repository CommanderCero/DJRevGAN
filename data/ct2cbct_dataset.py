import os.path
from data.base_dataset import BaseDataset, get_transform
from data.image_folder import make_dataset
from PIL import Image
import random
import torch
import numpy as np


class ct2cbctDataset(BaseDataset):
    @staticmethod
    def modify_commandline_options(parser, is_train):
        return parser

    def initialize(self, opt):
        self.opt = opt
        self.root = opt.dataroot
        self.cbct_dir = os.path.join(opt.dataroot, opt.phase + 'CBCT')
        self.ct_dir = os.path.join(opt.dataroot, opt.phase + 'CT')

        self.cbct_paths = make_dataset(self.cbct_dir)
        self.ct_paths = make_dataset(self.ct_dir)

        # Do we really need to sort the paths?
        #self.cbct_paths = sorted(self.cbct_paths)
        #self.ct_paths = sorted(self.ct_paths)
        
        self.cbct_size = len(self.cbct_paths)
        self.ct_size = len(self.ct_paths)
        
        print('len(CBCT),len(CT)=', self.cbct_size, self.ct_size)
        #self.transform = get_transform(opt)

    def __getitem__(self, index):
        
        # Calculate indices
        index_cbct = index % self.cbct_size
        cbct_path = self.cbct_paths[index_cbct]
        if self.opt.serial_batches:
            index_ct = index % self.ct_size
        else:
            index_ct = random.randint(0, self.ct_size - 1)
        ct_path = self.ct_paths[index_ct]

        # Load data
        cbct_img = np.load(cbct_path)
        ct_img = np.load(ct_path)
        
        # Normalize data
        # Do this here to prevent storing the values as floats, taking up much more memory
        cbct = torch.from_numpy(cbct_img).unsqueeze(0).float() / 1000.0 # <-- CT normalization hack HU/1000
        ct = torch.from_numpy(ct_img).unsqueeze(0).float() / 1000.0


        return {'A': cbct, 'B': ct,
                'A_paths': cbct_path, 'ct_paths': ct_path}

    def __len__(self):
        return max(self.cbct_size, self.B_size)

    def name(self):
        return 'UnalignedDataset'
