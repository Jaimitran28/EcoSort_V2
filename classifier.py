# classifier.py
import io
from PIL import Image
import torch
from torchvision import models, transforms
from torchvision.models import MobileNet_V2_Weights, ResNet18_Weights
import requests
from rules import keyword_map
from ai import PREDEFINED_TIPS, generate_disposal_tips

# --- Load Models ---
mobilenet = models.mobilenet_v2(weights=MobileNet_V2_Weights.DEFAULT)
mobilenet.eval()

resnet = models.resnet18(weights=ResNet18_Weights.DEFAULT)
resnet.eval()

# --- Image Preprocessing ---
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# --- Load ImageNet Labels ---
LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
imagenet_labels = requests.get(LABELS_URL).text.splitlines()


# --- Utility Functions ---
def map_to_category(text: str):
    text = text.lower()
    for keyword, category in keyword_map.items():
        if keyword in text:
            return category
    return "unknown"

#--- Main Classification Function ---
async def classify_image(file):
    try:
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        
        # Test-time augmentation: original + horizontal flip
        images = [preprocess(img)]
        images.append(preprocess(img.transpose(Image.FLIP_LEFT_RIGHT)))

        input_tensor = torch.stack(images)  # batch of images

        with torch.no_grad():
            m_outputs = mobilenet(input_tensor)
            r_outputs = resnet(input_tensor)
            
            m_probs = torch.nn.functional.softmax(m_outputs, dim=1).mean(dim=0)
            r_probs = torch.nn.functional.softmax(r_outputs, dim=1).mean(dim=0)

        # Weighted ensemble
        combined_probs = 0.6 * m_probs + 0.4 * r_probs
        conf, idx = torch.max(combined_probs, 0)
        top5_idx = torch.topk(combined_probs, 5).indices.tolist()
        top5_labels = [imagenet_labels[i].lower() for i in top5_idx]

        # Top-K voting for category
        category_votes = {}
        for i, lbl in zip(top5_idx, top5_labels):
            cat = map_to_category(lbl)
            if cat != "unknown":
                category_votes[cat] = category_votes.get(cat, 0) + float(combined_probs[i])

        if category_votes:
            category = max(category_votes, key=category_votes.get)
            chosen_label = next(lbl for lbl in top5_labels if map_to_category(lbl) == category)
            best_conf = category_votes[category]
            
            # Get tips from Gemini API dynamically
            try:
                best_tips = await generate_disposal_tips(chosen_label, category)  # or gt(category) if your function expects the category
                if not isinstance(best_tips, list):
                    best_tips = [str(best_tips)]  # ensure it's a list
            except Exception as e:
                best_tips = ["No tips available."]

        else:
            # fallback
            chosen_label = top5_labels[0]
            best_conf = float(conf)
            if any(x in chosen_label for x in ["bottle", "can", "jar", "metal", "plastic", "glass", "paper"]):
                category = "recyclable"
                best_tips = PREDEFINED_TIPS.get("recyclable")
            elif any(x in chosen_label for x in ["food", "banana", "apple", "leaf", "plant"]):
                category = "compostable"
                best_tips = PREDEFINED_TIPS.get("compostable")
            elif any(x in chosen_label for x in ["battery", "chemical", "paint", "oil"]):
                category = "hazardous"
                best_tips = PREDEFINED_TIPS.get("hazardous")
            else:
                category = "trash"
                best_tips = PREDEFINED_TIPS.get("trash")

        return {
            "category": category,
            "label": chosen_label,
            "confidence": best_conf,
            "tips": best_tips,
            "top_labels": top5_labels
        }

    except Exception as e:
        return {
            "category": "unknown",
            "label": "error",
            "confidence": 0.0,
            "tips": [f"Failed to process image: {str(e)}"],
            "top_labels": []
        }
