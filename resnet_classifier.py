from torchvision import models, transforms
from PIL import Image
import torch

class ResnetClassifier:

    def __init__(self, path):
        self.path = path

    def classify(self):
        resnet = models.resnet18(pretrained=True)
        transform = transforms.Compose([
                      transforms.Resize(256),
                      transforms.CenterCrop(224),
                      transforms.ToTensor(),
                      transforms.Normalize(
                      mean=[0.485, 0.456, 0.406],
                      std=[0.229, 0.224, 0.225],
                      )])
        img = Image.open(self.path)
        img_t = transform(img)
        batch_t = torch.unsqueeze(img_t, 0)
        resnet.eval()
        out = resnet(batch_t)
        with open('imagenet_classes.txt') as f:
            classes = [line.strip() for line in f.readlines()]

        _, indices = torch.sort(out, descending=True)
        percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
        output = [(classes[idx], percentage[idx].item()) for idx in indices[0][:5]]
        return output
