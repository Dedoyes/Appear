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

def main () :
    genePictureNum = 0
    transform = transforms.Compose ([
        transforms.Resize ((512, 512)),
        transforms.ToTensor (),
        transforms.Normalize ((0.5,), (0.5,))
    ])
    device = torch.device ("cuda" if torch.cuda.is_available () else "cpu")
    lr = 2e-4
    epochs = 20
    lambda_l1 = 100 

    if not os.path.exists ("./dcgan_params") : 
        os.mkdir ("./dcgan_params")
    print (device)
    netD = discriminator.Discriminator (in_channels=6).to (device)
    netG = generator.Generator (in_channels=4, out_channels=3).to (device)
    d_weight_file = r"./dcgan_params/d_net.pth" 
    g_weight_file = r"./dcgan_params/g_net.pth"
    if os.path.exists (d_weight_file) and os.path.getsize (d_weight_file) != 0 : 
        netD.load_state_dict (torch.load (d_weight_file))
        print ("Discriminator load success.")
    else : 
        netD.apply (generator.weight_init_normal)
        print ("Discriminator random parameters generate success.")
    if os.path.exists (g_weight_file) and os.path.getsize (g_weight_file) != 0 : 
        netG.load_state_dict (torch.load (g_weight_file))
        print ("Generator load success.")
    else : 
        netG.apply (generator.weight_init_normal)
        print ("Generator random parameters generate success.")
    opt_G = torch.optim.Adam (netG.parameters (), lr=lr, betas=(0.5, 0.999))
    opt_D = torch.optim.Adam (netD.parameters (), lr=lr, betas=(0.5, 0.999))
    L1 = torch.nn.L1Loss ()
    BCE = torch.nn.BCEWithLogitsLoss ()
    dataset = PairedDataset ("./sketch", "./reals_regu/", transforms=transform)
    loader = DataLoader (dataset, batch_size=1, shuffle=True)
   
    print ("start training.")
    for epoch in range (epochs) :
        print ("--------epoch", epoch)
        for idx, (sketch, real) in enumerate (loader) :
            #print ("        idx = ", idx)
            sketch, real = sketch.to (device), real.to (device)
            z = torch.randn (1, 1, 512, 512).to (device)
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
            if epoch == 19:
                outPath = "./gene_picture/" + str(genePictureNum) + ".jpg"
                save_image (fake, outPath)
                print ("G_loss = ", loss_G)
                print ("D_loss = ", loss_D)  
                genePictureNum = genePictureNum + 1
    torch.save (netG.state_dict (), "./dcgan_params/g_net.pth")
    torch.save (netD.state_dict (), "./dcgan_params/d_net.pth")

if __name__ == '__main__' : 
    main ()

