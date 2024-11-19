from torchvision import models, transforms
from torchvision.models import ResNet18_Weights
from PIL import Image
import torch
import io

class ResnetClassifier:

    def classify(self, img_bytes):
        resnet = models.resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
        img_t = self.__transform_image(img_bytes)
        batch_t = torch.unsqueeze(img_t, 0)
        resnet.eval()
        out = resnet(batch_t)
        with open('imagenet_classes.txt') as f:
            classes = [line.strip() for line in f.readlines()]

        _, indices = torch.sort(out, descending=True)
        percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
        output = [(classes[idx], percentage[idx].item()) for idx in indices[0][:5]]
        return output

    def __transform_image(self, img_bytes):
        transform = transforms.Compose([
                      transforms.Resize(256),
                      transforms.CenterCrop(224),
                      transforms.ToTensor(),
                      transforms.Normalize(
                      mean=[0.485, 0.456, 0.406],
                      std=[0.229, 0.224, 0.225],
                      )])
        img = Image.open(io.BytesIO(img_bytes))
        img_t = transform(img)
        return img_t