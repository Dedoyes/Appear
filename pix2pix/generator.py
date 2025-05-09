import torch 
import torch.nn as nn 
from torch.nn.modules.batchnorm import BatchNorm2d 
from torch.nn.modules.conv import ConvTranspose2d
from torchvision.utils import save_image

def weight_init_normal (m) : 
    classname = m.__class__.__name__
    if classname.find ('Conv') != -1 : 
        nn.init.normal_ (m.weight.data, 0.0, 0.02)
        if m.bias is not None : 
            nn.init.constant_ (m.bias.data, 0.0)
    elif classname.find ('BatchNorm2d') != -1 : 
        nn.init.normal_ (m.weight.data, 1.0, 0.02)
        nn.init.constant_ (m.bias.data, 0.0)

class Block (nn.Module) : 
    def __init__ (self, in_channels, out_channels, down=True, act="relu", use_dropout=False) : 
        super ().__init__ ()
        self.conv = nn.Sequential (
            nn.Conv2d (in_channels, out_channels, 4, 2, 1, bias=False, padding_mode="reflect")
            if down 
            else nn.ConvTranspose2d (in_channels, out_channels, 4, 2, 1, bias=False),
            nn.BatchNorm2d (out_channels),
            nn.ReLU () if act == "relu" else nn.LeakyReLU (0.2)
        )
        self.use_dropout = use_dropout
        self.dropput = nn.Dropout (0.5)

    def forward (self, x) : 
        x = self.conv (x)
        return self.dropput (x) if self.use_dropout else x 

class Generator (nn.Module) : 
    def __init__ (self, in_channels=4, out_channels=3, features=64) : 
        super ().__init__ ()
        self.initial_down = nn.Sequential (
            nn.Conv2d (in_channels, features, 4, 2, 1, padding_mode="reflect"),
            nn.LeakyReLU (0.2),
        )
        self.down1 = Block (features, features * 2, down=True, act="leaky", use_dropout=False)
        self.down2 = Block (features * 2, features * 4, down=True, act="leaky", use_dropout=False)
        self.down3 = Block (features * 4, features * 8, down=True, act="leaky", use_dropout=False)
        self.down4 = Block (features * 8, features * 8, down=True, act="leaky", use_dropout=False) 
        self.down5 = Block (features * 8, features * 8, down=True, act="leaky", use_dropout=False)
        self.down6 = Block (features * 8, features * 8, down=True, act="leaky", use_dropout=False)
        self.bottleneck = nn.Sequential (
            nn.Conv2d (features * 8, features * 8, 4, 2, 1),
            nn.ReLU (),
        )
        self.up1 = Block (features * 8, features * 8, down=False, act="relu", use_dropout=True)
        self.up2 = Block (features * 16, features * 8, down=False, act="relu", use_dropout=True)
        self.up3 = Block (features * 16, features * 8, down=False, act="relu", use_dropout=True)
        self.up4 = Block (features * 16, features * 8, down=False, act="relu", use_dropout=True)
        self.up5 = Block (features * 16, features * 4, down=False, act="relu", use_dropout=True)
        self.up6 = Block (features * 8, features * 2, down=False, act="relu", use_dropout=True)
        self.up7 = Block (features * 4, features, down=False, act="relu", use_dropout=True)
        self.final_up = nn.Sequential (
            ConvTranspose2d (features * 2, out_channels, 4, 2, 1),
            nn.Tanh ()
        )

    def forward (self, x) : 
        d1 = self.initial_down (x)
        d2 = self.down1 (d1)
        d3 = self.down2 (d2)
        d4 = self.down3 (d3)
        d5 = self.down4 (d4)
        d6 = self.down5 (d5)
        d7 = self.down6 (d6)
        bottleneck = self.bottleneck (d7)
        u1 = self.up1 (bottleneck)
        u2 = self.up2 (torch.cat ([u1, d7], dim=1))
        u3 = self.up3 (torch.cat ([u2, d6], dim=1))
        u4 = self.up4 (torch.cat ([u3, d5], dim=1))
        u5 = self.up5 (torch.cat ([u4, d4], dim=1))
        u6 = self.up6 (torch.cat ([u5, d3], dim=1))
        u7 = self.up7 (torch.cat ([u6, d2], dim=1))
        final = self.final_up (torch.cat ([u7, d1], dim=1))
        return final

if __name__ == '__main__' : 
    netG = Generator(in_channels=4, features=64)
    netG.apply (weight_init_normal)
    rgb_0_1 = torch.rand (1, 3, 512, 512)
    rgb_m1_1 = rgb_0_1 * 2.0 - 1.0 
    z_dim = 1
    noise = torch.randn (1, z_dim, 512, 512)
    in_tensor = torch.cat ([rgb_m1_1, noise], dim=1)
    fake = netG.forward (in_tensor)
    print (fake.shape)
    save_image (fake, "./gene_picture/1.jpg")
