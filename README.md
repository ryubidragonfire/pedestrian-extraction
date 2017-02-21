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

## Convert
- use [this<sup>1</sup>](https://github.com/hizhangp/caltech-pedestrian-converter/blob/master/converter.py) to convert Caltech dataset to individual images with annotations of bounding box.

[1] Written in python 2. Use `2to3` to convert from python 2 to python 3.
