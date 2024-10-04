from tifascore import filter_question_and_answers, UnifiedQAModel, tifa_score_single, VQAModel
import openai
import pandas as pd
import glob
from tqdm import tqdm
import ast
from PIL import Image


vqa_model = VQAModel("mplug-large")
#vqa_model = VQAModel("git-large")
#vqa_model = VQAModel("blip-base")

ls_bilder = pd.read_csv("../sampled_data_fixed.csv")
tifa_meta = pd.read_csv("tifa_metadata.csv")
tifa_meta["filtered_questions"] = tifa_meta["filtered_questions"].apply(lambda x: ast.literal_eval(x))

base_path = "../images/"
models = {
    "DALLE-3/": ".jpg",
    "Midjourney/": ".png",
    "artbreeder/": ".jfif",
    "SD1_4/": ".png",
    "SD2_1_base/": ".png",
    "Wuerstchen/": ".png",
    "references/": ".jpg",
    "SD_3/": ".png"
}

#tifa_scores = pd.DataFrame(columns=["name", "model", "id", "description", "tifa_score", "question_details"])
tifa_scores = pd.read_csv("tifa_scores_mplug.csv")

for model, file_ending in models.items():
    print("**", model)
    for i, tifa_row in tqdm(tifa_meta.iterrows(), total=len(tifa_meta)):
        image_name = tifa_row["name"].replace(' ', '_')
        image_list = glob.glob(f"{base_path}{model}/{image_name}_?{file_ending}") if model != "references/" \
            else glob.glob(f"{base_path}{model}/{image_name}{file_ending}")
        for image in image_list:
            pil_img = Image.open(image)
            img_clrs = pil_img.getcolors(pil_img.size[0]*pil_img.size[1])
            if len(img_clrs) == 1 and img_clrs[0][1] == (0,0,0):
                tifa_result = {"tifa_score": 0.0, "question_details": {"all_black": True}}
            else:
                tifa_result = tifa_score_single(vqa_model, tifa_row["filtered_questions"], image)
            #print(tifa_result["tifa_score"], [tr["scores"] for _, tr in tifa_result["question_details"].items()])
            entry = pd.DataFrame.from_records([{
                "name": tifa_row["name"],
                "model": model.replace('/', ''),
                "id": image.split('_')[-1].replace(file_ending, ''),
                "description": tifa_row["description"],
                "tifa_score": tifa_result["tifa_score"],
                "question_details": str(tifa_result["question_details"])
            }])
            tifa_scores = pd.concat([tifa_scores, entry], ignore_index=True)
        tifa_scores.to_csv("tifa_scores_mplug.csv", index=False)
