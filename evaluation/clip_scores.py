import torch
import clip
from PIL import Image
import pandas as pd
from tqdm import tqdm
import glob

# Load the pre-trained CLIP model and the image
clip_model, preprocess = clip.load('ViT-L/14@336px')
#clip_model, preprocess = clip.load('ViT-L/14')
#clip_model, preprocess = clip.load('RN50x64')
# Move the inputs to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model = clip_model.to(device)

def get_clip_score(image, text):
    # Preprocess the image and tokenize the text
    image_input = preprocess(image).unsqueeze(0)
    text_input = clip.tokenize([text])

    image_input = image_input.to(device)
    text_input = text_input.to(device)

    # Generate embeddings for the image and text
    with torch.no_grad():
        image_features = clip_model.encode_image(image_input)
        text_features = clip_model.encode_text(text_input)

    # Normalize the features
    image_features = image_features / image_features.norm(dim=-1, keepdim=True)
    text_features = text_features / text_features.norm(dim=-1, keepdim=True)

    # Calculate the cosine similarity to get the CLIP score
    clip_score = torch.matmul(image_features, text_features.T).item()

    return clip_score


ls_bilder = pd.read_csv("../sampled_data_fixed.csv")

base_path = "../images/"
models = {
    "DALLE-3": ".jpg",
    "Midjourney": ".png",
    "artbreeder": ".jfif",
    "SD1_4": ".png",
    "SD2_1_base": ".png",
    "Wuerstchen": ".png",
    "references": ".jpg",
    "SD_3": ".png"
}

#clip_scores = pd.DataFrame(columns=["name", "model", "id", "description", "clip_score"])
clip_scores = pd.read_csv("clip_scores_ViT-L.csv")

for model, file_ending in models.items():
    print("**", model)
    for i, row in tqdm(ls_bilder.iterrows(), total=len(ls_bilder)):
        image_name = row["english_name"].replace(' ', '_')
        image_list = glob.glob(f"{base_path}{model}/{image_name}_?{file_ending}") if model != "references" \
            else glob.glob(f"{base_path}{model}/{image_name}{file_ending}")
        for image in image_list:
            pil_img = Image.open(image)
            img_clrs = pil_img.getcolors(pil_img.size[0] * pil_img.size[1])
            if len(img_clrs) == 1 and img_clrs[0][1] == (0, 0, 0):
                clip_score = 0.0
            else:
                try:
                    clip_score = get_clip_score(pil_img, row["english_description"])
                except RuntimeError:
                    print(f"\t Description too long ({row['english_name']})")
                    clip_score = -1
            entry = pd.DataFrame({
                "name": row["english_name"],
                "model": model,
                "id": image.split('_')[-1].replace(file_ending, ''),
                "description": row["english_description"],
                "clip_score": clip_score
            }, index=[0])
            clip_scores = pd.concat([clip_scores, entry], ignore_index=True)
        clip_scores.to_csv("clip_scores_ViT-L.csv", index=False)