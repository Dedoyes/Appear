import discriminator
import generator
from torchvision.utils import save_image
import os
from PIL import Image
import torch
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as transforms

class PairedDataset (Dataset) : 
    def __init__ (self, sketch_dir, reals_dir, transforms=None) : 
        self.sketch_dir = sketch_dir
        self.reals_dir = reals_dir
        self.transforms = transforms
        self.image_names = sorted (os.listdir (sketch_dir))
    
    def __len__ (self) : 
        return len (self.image_names)

    def __getitem__ (self, idx) : 
        sketch_path = os.path.join (self.sketch_dir, self.image_names[idx])
        reals_path = os.path.join (self.reals_dir, self.image_names[idx])
        sketch = Image.open (sketch_path).convert ("RGB")
        reals = Image.open (reals_path).convert ("RGB")
        if self.transforms : 
            sketch = self.transforms (sketch)
            reals = self.transforms (reals)
        return sketch, reals

def draw () :
    objectiveWidth = 1024
    objectiveHeight = 1024    
    transform = transforms.Compose ([
        transforms.Resize ((objectiveWidth, objectiveHeight)),
        transforms.ToTensor (),
        transforms.Normalize ((0.5,), (0.5,))
    ])
    device = torch.device ("cuda" if torch.cuda.is_available () else "cpu")
    filePath = os.path.abspath (__file__)
    dirPath = os.path.dirname (filePath)
    paramsPath = os.path.join (dirPath, "dcgan_params")
    netGPath = os.path.join (paramsPath, "g_net.pth")
    basePath = os.path.dirname (dirPath)
    savesPath = os.path.join (basePath, "saves")
    sketchPath = os.path.join (savesPath, "save.jpg")
    sketchImage = Image.open (sketchPath).convert ("RGB")
    sketch = transform (sketchImage)
    sketch = sketch.unsqueeze (0).to (device)
    genePath = os.path.join (savesPath, "gene.jpg")

    if not os.path.exists (netGPath) : 
        print ("Error : no generator!")
        return 
    else : 
        netG = generator.Generator (in_channels=4, out_channels=3).to (device)
        if (os.path.getsize (netGPath) == 0) : 
            print ("Error : the file is empty!")
            return
        netG.load_state_dict (torch.load (netGPath))
        print ("generator load success.")
        z = torch.rand (1, 1, objectiveWidth, objectiveHeight).to (device)
        print ("sketch : ", sketch.size ())
        print ("z : ", z.size ())
        genePicture = netG (torch.cat ([sketch, z], dim=1))
        save_image (genePicture, genePath)

def train () :
    objectiveWidth = 1024 
    objectiveHeight = 1024
    genePictureNum = 0
    transform = transforms.Compose ([
        transforms.Resize ((objectiveWidth, objectiveHeight)),
        transforms.ToTensor (),
        transforms.Normalize ((0.5,), (0.5,))
    ])
    device = torch.device ("cuda" if torch.cuda.is_available () else "cpu")
    lrG = 2e-4
    lrD = 2e-4
    epochs = 10
    lambda_l1 = 100 
    
    filePath = os.path.abspath (__file__)
    dirPath = os.path.dirname (filePath)
    paramsPath = os.path.join (dirPath, "dcgan_params")
    netGPath = os.path.join (paramsPath, "g_net.pth")
    netDPath = os.path.join (paramsPath, "d_net.pth")
    realsReguPath = os.path.join (dirPath, "reals_regu")
    sketchPath = os.path.join (dirPath, "sketch")
    genePicturePath = os.path.join (dirPath, "gene_picture")

    if not os.path.exists (paramsPath) : 
        os.mkdir (paramsPath)
    print (device)
    netD = discriminator.Discriminator (in_channels=6).to (device)
    netG = generator.Generator (in_channels=4, out_channels=3).to (device)
    if os.path.exists (netDPath) and os.path.getsize (netDPath) != 0 : 
        netD.load_state_dict (torch.load (netDPath))
        print ("Discriminator load success.")
    else : 
        netD.apply (generator.weight_init_normal)
        print ("Discriminator random parameters generate success.")
    if os.path.exists (netGPath) and os.path.getsize (netGPath) != 0 : 
        netG.load_state_dict (torch.load (netGPath))
        print ("Generator load success.")
    else : 
        netG.apply (generator.weight_init_normal)
        print ("Generator random parameters generate success.")
    opt_G = torch.optim.Adam (netG.parameters (), lr=lrG, betas=(0.5, 0.999))
    opt_D = torch.optim.Adam (netD.parameters (), lr=lrD, betas=(0.5, 0.999))
    L1 = torch.nn.L1Loss ()
    BCE = torch.nn.BCEWithLogitsLoss ()
    dataset = PairedDataset (sketchPath, realsReguPath, transforms=transform)
    loader = DataLoader (dataset, batch_size=1, shuffle=True)
   
    print ("start training.")
    for epoch in range (epochs) :
        print ("--------epoch", epoch)
        for idx, (sketch, real) in enumerate (loader) :
            #print ("        idx = ", idx)
            sketch, real = sketch.to (device), real.to (device)
            z = torch.randn (1, 1, objectiveWidth, objectiveHeight).to (device)
            g_input = torch.cat ([sketch, z], dim=1)
            fake = netG (g_input).detach ()
            #print ("sketch size : ", sketch.shape)
            #print ("fake size : ", fake.shape)
            #print ("real size : ", real.shape)
            D_fake = netD (torch.cat ([sketch, fake], dim=1))
            D_real = netD (torch.cat ([sketch, real], dim=1))
            real_labels = torch.ones_like (D_real).to (device)
            fake_labels = torch.zeros_like (D_fake).to (device)
            loss_D_real = BCE (D_real, real_labels)
            loss_D_fake = BCE (D_fake, fake_labels)
            loss_D = (loss_D_real + loss_D_fake) * 0.5 
            opt_D.zero_grad ()
            loss_D.backward ()
            opt_D.step ()

            fake = netG (torch.cat ([sketch, z], dim=1))
            D_fake = netD (torch.cat ([sketch, fake], dim=1))
            loss_G_adv = BCE (D_fake, real_labels)
            loss_G_l1 = L1 (fake, real) * lambda_l1
            loss_G = loss_G_adv + loss_G_l1
            opt_G.zero_grad ()
            loss_G.backward ()
            opt_G.step ()
            if idx % 10 == 0 : 
                print ("idx = ", idx)
            if epoch == epochs - 1 and idx % 5 == 0:
                outPath = os.path.join (genePicturePath, str(genePictureNum) + ".jpg")
                save_image (fake, outPath)
                print ("G_loss = ", loss_G)
                print ("D_loss = ", loss_D)
                print ("L1_loss = ", loss_G_l1)
                genePictureNum = genePictureNum + 1
    torch.save (netG.state_dict (), netGPath)
    torch.save (netD.state_dict (), netDPath)

if __name__ == '__main__' : 
    opt = int (input ("please input the opt, 1 for train, other for draw : "))
    if opt == 1 : 
        train () 
    else : 
        draw ()

