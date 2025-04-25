import os 
from PIL import Image 
from torch.utils.data import Dataset
from torchvision import transforms

class SketchToRealDataset (Dataset) : 
    def __init__ (self, sketch_dir, real_dir, transform=None) : 
        self.sketch_dir = sketch_dir
        self.real_dir = real_dir
        self.transform = transform
        self.filenames = sorted (os.listdir (sketch_dir))

    def __len__ (self) :
        return len (self.filenames)

    def __getitem__ (self, idx) : 
        sketch_path = os.path.join (self.sketch_dir, self.filenames[idx])
        real_path = os.path.join (self.real_dir, self.filenames[idx])
        sketch = Image.open (sketch_path).convert ('RGB')
        real = Image.open (real_path).convert ('RGB')
        if self.transform : 
            sketch = self.transform (sketch)
            real = self.transform (real)
        return sketch, real
