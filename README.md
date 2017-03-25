# pedestrian-extraction

## Data Source
https://www.vision.caltech.edu/Image_Datasets/CaltechPedestrians/

## Python Utility 
  - https://github.com/mitmul/caltech-pedestrian-dataset-converter
  - https://github.com/hizhangp/caltech-pedestrian-converter
  - www.kanadas.com/program-e/2015/06/converting_caltech_pedestrian.html
  - https://gist.github.com/psycharo/7e6422a491d93e1e3219/
    - Convert Caltech Pedestrains Dataset into list of images.

## Download data
- use [this](https://github.com/jainanshul/caltech-pedestrian-dataset-extractor/blob/master/download.sh) to download to `./data`, and extract.

- for convenience, it is included here as `download-untar.sh`

## Convert
- use [this<sup>1</sup>](https://github.com/hizhangp/caltech-pedestrian-converter/blob/master/converter.py) to convert Caltech dataset to individual images with annotations of bounding box. 
  - <sup>1</sup> is written in python 2. Use `2to3` to convert from python 2 to python 3.
  - in a python console, 
  ```python
      2to3 filename.py -w # -w is to write
  ```
- for convenience, it is included here as `converter.py`

## Extract necessary data required for Fast-R-CNN
- use `extract-unique-labels-used.py` to extract unique labels used to label the Caltech images.
  - it output a `set` of labels on the stdout.
  - use only `person` and `people` in `extract-labelled-data-for-cntk-fast-r-cnn.py` (I believe those two labels mean that there is a person in the image. Please let me know if you think otherwise.)
- use `extract-labelled-data-for-cntk-fast-r-cnn.py` to:
  - extract only images that contains one or more people, where the size of bounding box [w,h] >= [40, 70], since not all the images contain a person, then:
    1. extract position of bounding box of a person, then write to a file `imagename.bboxes.tsv`
    2. write label `person` to a file `imagename.bboxes.labels.tsv`
    3. copy corresponding image files to `./output_for_cntk/`
    
It gives:
  - Training images: 13,414
  - Test images: 1,940
  - Validation images: 3,847
  
See `anno-06.txt` to get an idea of the data sturcture

## Filter Negative Samples from database
- use `extract-negative-samples.py`
- will copy images contain no people into a `negatives` folder

It gives:
  - Training images: 61,336
  - Test images: 19,828
  - Validation images: 36,638

## Create Small Dataset
- use `extract-labelled-data-for-cntk-fast-r-cnn-small.py` and `extract-negative-samples-small.py` to create dataset of size of your choice. 
- In `extract-labelled-data-for-cntk-fast-r-cnn-small.py`, size is described by *fraction of the whole dataset*
- In `extract-negative-samples-small.py`, size is described by *number of samples*

## Example on CNTK Fast-R-CNN
- Done with small set of training data.

## TODO:
- re-train with large dataset
- deploy as an [Azure webapp](https://github.com/ilkarman/Blog/blob/master/rndm/AzureWebApp.md)
- deploy via [node.js](https://github.com/nadavbar/node-cntk-fastrcnn)
- deploy as [web service](https://blogs.technet.microsoft.com/machinelearning/2015/08/21/build-and-deploy-a-predictive-web-app-using-python-and-azure-ml/)
- deploy as [web service](https://gallery.cortanaintelligence.com/Notebook/Deployment-of-AzureML-Web-Services-from-Python-Notebooks-4)
- [Flask](https://medium.com/@amirziai/a-flask-api-for-serving-scikit-learn-models-c8bcdaa41daa#.cs5694sq3)
  - [code](https://github.com/amirziai/sklearnflask/blob/master/main.py)
- [linux](https://loads.pickle.me.uk/2016/04/04/deploying-a-scikit-learn-classifier-to-production/)

## Notes:
- see my notes on [cntk-fast-r-cnn](https://github.com/ryubidragonfire/cntk-and-fast-r-cnn)

## Known Bugs:

