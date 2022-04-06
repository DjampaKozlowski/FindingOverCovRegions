# FindOverCovRegions.py

## General description
FindOverCovRegions.py search for genomic regions with abnormal read coverage (e.g. depth).

To do so, this program requieres begraph-like file (e.g. bedtools genomecov per-base reports) where for each position of the genome, the coverage depth is reported (even 0 values).

This type of file can be obtained using bedtools genomecov (https://bedtools.readthedocs.io/en/latest/content/tools/genomecov.html) on a bam file using the -d or -d split options. /!\ The BAM file must be sorted by position. Using samtools sort aln.bam aln.sorted will suffice.

## Brief explanation of the algorithm
Each position of the genome is scanned using a sliding window. For each position, the mean depth is computed over the sliding window. If this value is superior to the threshold value, an interval is created. The interval is closed when the mean depth value over the sliding window become inferior to the threshold value and so on. 

## Installation
FindOverCovRegions.py was developed using python=3.9.9. It requieres the following packages :
- MENDATORY : pandas (dev with version 1.4.2) 
- OPTIONAL : jupyter notebook (dev with version)

To install FindOverCovRegions, it is advised to create a dedicated virtual environment (here named focr_env) where to install the program. 

For conda users :
```
conda create -n focr_env python=3.9.9
```
### automatic
When using a dedicated environment, first activate it
```
conda activate focr_env
```
Then using pip and the requirement file install the following dependencies (and their respective dependencies):
```
pip install -r requirements.txt
```
Finally, install the package 
```
pip install -e .
```

### manual
When using a dedicated environment, first activate it
```
conda activate focr_env
```
Then using pip install the following dependencies (and their respective dependencies):
```
pip install pandas==1.4.2
pip install notebook==6.4.10
```
Finally, install the package 
```
pip install -e .
```
NB : the installation of jupyter notebook is optional but mendatory if you want to play with the notebook ('/notebooks/OvercoveredRegions.ipynb')


## Usage
general usage :

If you chosed to install the program using conda, first activate the environment:
```
conda activate focr_env
```
Then, either you use the jupyter notebook
```
jupyter notebook notebooks/OvercoveredRegions.ipynb
```
or use the command line
```
python FindOverCovRegions.py [-h] -i < INPUTFILEPATH > -o < OUTPUTDIR > -p < PREFIX > -d < DEPTH > -m < MINOVERCOVREGIONSIZE > -s < SLIDINGWINSIZE >
```
where :
- < INPUTFILEPATH > : the path to a begraph-like file (bedtools genomecov per-base reports)
- < OUTPUTDIR > : the ouput directory path where the results files will saved. NB : files with the same name as the output files will be replaced.
- < PREFIX > : (str) a prefix that will be added to each output file name
- < DEPTH > : (float) the threshold depth value to consider a region as over-covered
- < MINOVERCOVREGIONSIZE > : (int) minimal size for an overcovered region to be retained. 
- < SLIDINGWINSIZE > : (int) sliding window size. For each position, the mean depth will be computed and compared to < DEPTH > to initialize/fill/close an over-covered region.

example on a toy dataset (test/begraph-like_sample.txt):
``` 
python FindOverCovRegions.py -i test/begraph-like_sample.txt -o test/ -p 'example_overcovregions' -d 11 -m 4 -s 3
```

## Futur improvments

- parallelise the contigs analysis.




