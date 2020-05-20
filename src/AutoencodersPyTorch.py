import torch
import torchvision
from torch import nn
from torch import optim
import torch.nn.functional as F
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import transforms
import os

class CESVarAutoencoder(nn.Module):
    def __init__(self):
        super(CESVarAutoencoder, self).__init__()

        self.fc1 = nn.Linear(784, 400)
        self.fc21 = nn.Linear(400, 20)
        self.fc22 = nn.Linear(400, 20)
        self.fc3 = nn.Linear(20, 400)
        self.fc4 = nn.Linear(400, 784)

    def encode(self, x):
        h1 = F.relu(self.fc1(x))
        return self.fc21(h1), self.fc22(h1)

    def reparametrize(self, mu, logvar):
        std = logvar.mul(0.5).exp_()
        if torch.cuda.is_available():
            eps = torch.cuda.FloatTensor(std.size()).normal_()
        else:
            eps = torch.FloatTensor(std.size()).normal_()
        eps = Variable(eps)
        return eps.mul(std).add_(mu)

    def decode(self, z):
        h3 = F.relu(self.fc3(z))
        return F.sigmoid(self.fc4(h3))

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparametrize(mu, logvar)
        return self.decode(z), mu, logvar

def fonction_loss(recon_x, x, mu, logvar):
    """
    recon_x: generating images
    x: origin images
    mu: latent mean
    logvar: latent log variance
    """
    reconstruction_function = nn.MSELoss(size_average=False)
    BCE = reconstruction_function(recon_x, x)  # mse loss
    # loss = 0.5 * sum(1 + log(sigma^2) - mu^2 - sigma^2)
    KLD_element = mu.pow(2).add_(logvar.exp()).mul_(-1).add_(1).add_(logvar)
    KLD = torch.sum(KLD_element).mul_(-0.5)
    # KL divergence
    return BCE + KLD



if __name__ == '__main__':
    nb_epochs = 100
    taille_batch = 128
    learning_rate = 1e-3

    img_transform = transforms.Compose([
        transforms.ToTensor()
        # transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    dataset = None  # réfléchir à cela
    dataloader = DataLoader(dataset, batch_size=taille_batch, shuffle=True)

    VAEmodele = CESVarAutoencoder()
    if torch.cuda.is_available():
        VAEmodele.cuda()

    optimizer = optim.Adam(VAEmodele.parameters(), lr=1e-3)


    # === entrainement ===
    for epoch in range(nb_epochs):
        # epochs
        VAEmodele.train()
        loss_entrainement = 0
        for batch_idx, data in enumerate(dataloader):
            # batch
            img, _ = data
            img = img.view(img.size(0), -1)
            img = Variable(img)
            if torch.cuda.is_available():
                img = img.cuda()
            optimizer.zero_grad()
            recon_batch, mu, logvar = VAEmodele(img)
            loss = fonction_loss(recon_batch, img, mu, logvar)
            loss.backward()
            loss_entrainement += loss.data[0]
            optimizer.step()

            # affichage tous les 1OO batchs
            if batch_idx % 100 == 0:
                img_nb = batch_idx * len(img)
                print(f'Entraînement epoch {epoch} [{img_nb}/{len(dataloader.dataset)} ({100. * batch_idx / len(dataloader):.0f}%)]\tLoss: {loss.data[0] / len(img):.6f}')

        # affichage toutes les epochs
        print(f'====> Epoch: {epoch} Loss moyenne : {loss_entrainement / len(dataloader.dataset):.4f}')

    torch.save(VAEmodele.state_dict(), './cesvae.pth')
