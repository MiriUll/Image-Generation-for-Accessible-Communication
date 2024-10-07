# Image generation for accessible communication

This repository contains the code and the data for the paper "Images Speak Volumes: User-Centric Assessment of Image Generation for
Accessible Communication".
<object data="https://github.com/MiriUll/Image-Generation-for-Accessible-Communication/blob/main/eig_vis_abs.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="https://github.com/MiriUll/Image-Generation-for-Accessible-Communication/blob/main/eig_vis_abs.pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="https://github.com/MiriUll/Image-Generation-for-Accessible-Communication/blob/main/eig_vis_abs.pdf">Download PDF</a>.</p>
    </embed>
</object>

## Dataset
The original data is taken from the [LEICHTE SPRACHE - Bildergalerie](https://www.lag-sb-rlp.de/projekte/bildergalerie-leichte-sprache) of the LAG Selbsthilfe von Menschen mit Behinderungen und chronischen Erkrankungen Rheinland-Pfalz e.V.
Their image gallery provides images that can be used in Easy-2-Read texts and is categorized into 16 categories.
We samples five images from each of the categories, resulting in 80 reference images.

The dataset can be found in [sampled_data_fixed.csv](https://github.com/MiriUll/Image-Generation-for-Accessible-Communication/blob/main/sampled_data_fixed.csv).
The generated images are in the ```images``` folder, sorted by the text-to-image model that created them. The reference images are not contained in this repository and must be downloaded for which the image URLs are provided.

## Evaluation
The paper provides a detailed evaluation of the generated images. All evaluation material is provided in the ```evaluation``` folder.

### Automated evalation
We evaluated the images with [FID](https://lightning.ai/docs/torchmetrics/stable/image/frechet_inception_distance.html), [CLIP](https://github.com/openai/CLIP.git) and [TIFA](https://github.com/Yushi-Hu/tifa) scores. The FID scores can be found in the respective (evaluate_FID_scores.ipynb)[] notebook. The TIFA and CLIP scores can be found in their respective ```*.csv``` files. All code and material to recreate the scores is provided in the evaluation folder.

### Human evaluation: Easy-to-read expert
An E2R expert manually reviewed 560 of the generated images on four scales: coherence with the prompt, content correctned, bias toward people with disabilities, and suitability for the target group.  
The annotations can be found in [evaluation/human_eval.csv](https://github.com/MiriUll/Image-Generation-for-Accessible-Communication/blob/main/evaluation/human_eval.csv).

### Human evaluation: Target group
In addition, we asked the target group of E2R texts about their opinions of the images. Details can be found in our paper, but we added the tested images and the [target group votings](https://github.com/MiriUll/Image-Generation-for-Accessible-Communication/blob/main/evaluation/target_group_votings.xlsx) in this repository.

## Citation
If you use any material in this repository, please cite our paper as:
```
@misc{anschütz2024imagesspeakvolumesusercentric,
      title={Images Speak Volumes: User-Centric Assessment of Image Generation for Accessible Communication}, 
      author={Miriam Anschütz and Tringa Sylaj and Georg Groh},
      year={2024},
      eprint={2410.03430},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2410.03430}, 
}
```
