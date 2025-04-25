import torch
import torch.nn as nn 
import generator

class CNNBLock (nn.Module) : 
    def __init__ (self, in_channels, out_channels, stride) : 
        super ().__init__ ()
        self.conv = nn.Sequential (
            nn.Conv2d (in_channels, out_channels, 4, stride, 1, bias=False, padding_mode="reflect"),
            nn.BatchNorm2d (out_channels),
            nn.LeakyReLU (0.2),
        )

    def forward (self, x) : 
        return self.conv (x)

class Discriminator (nn.Module) : 
    def __init__ (self, in_channels=6) :
        super ().__init__ ()
        self.model = nn.Sequential (
            nn.Conv2d (in_channels, 64, 4, 2, 1, padding_mode="reflect"),
            nn.LeakyReLU (0.2),
            CNNBLock (64, 128, 2),
            CNNBLock (128, 256, 2),
            CNNBLock (256, 512, 1),
            CNNBLock (512, 256, 2),
            CNNBLock (256, 128, 2),
            CNNBLock (128, 64, 2),
            CNNBLock (64, 32, 2),
            nn.Conv2d (32, 1, 4, 2, 1, padding_mode="reflect")
        )

    def forward (self, x) :
        x = self.model (x)
        return x

