from overcovregions.read_and_write import read_bedgraphlike_file,\
    write_results_as_bed6, write_results_as_tsv
from overcovregions.coverage import find_overcov_regions
from overcovregions.interface import arguments_parser

import pandas as pd
import sys
import os


########### MAIN
######

### Get the script arguments' values
#
args = arguments_parser()
sliding_win_len = int(args.slidingwinsize)
depth_thresh = float(args.depth)
region_min_len = int(args.minovercovregionsize)
input_fpath = os.path.abspath(args.inputfilepath)
output_dpath = os.path.abspath(args.outputdir)
file_prefix = args.prefix


if sliding_win_len > region_min_len:
    print(f"ERROR : sliding window (size : {sliding_win_len}) must be smaler \
          than the minimum over covered region size (size : {region_min_len})")
    sys.exit()
else:
    ### Open the bedgraph like file
    #
    df_data = read_bedgraphlike_file(input_fpath)

    ### Sort the dataframe by 'contig' and 'position'
    #
    df_data = df_data.sort_values(by=['contig', 'position'])

    ### iterate through 'contigs' and look for over-covered regions
    #
    lst_df_overcov = []
    for contig in df_data.contig.unique():
        df_contig = df_data[df_data.contig==contig]
        lst_df_overcov.append(
            find_overcov_regions(df_data[df_data.contig==contig],
                                sliding_win_len=sliding_win_len,
                                depth_thresh=depth_thresh,
                                )
        )
        
    ### create a pd.DataFrame containing the results for every contig
    #
    df_overcov_regions = pd.concat(lst_df_overcov)
    
    ### Remove regions that are too short
    #
    df_overcov_regions = df_overcov_regions[
        df_overcov_regions.length >= region_min_len
        ]
    
    ### Prepare output files basename
    #
    out_fbasename = '_'.join([file_prefix,
                              'sliWinLen'+str(sliding_win_len),
                              'depthThresh'+str(depth_thresh),
                              'minWinSize'+str(region_min_len)])
    
    ### Save results as bed file (only 'contig', 'start', 'end' columns)
    #
    write_results_as_bed6(
        fpath=os.path.join(output_dpath, out_fbasename+'.bed'),
        df=df_overcov_regions
    )

    ### Save results as tsv file (all the columns)
    #
    write_results_as_tsv(
        fpath=os.path.join(output_dpath, out_fbasename+'.tsv'),
        df=df_overcov_regions
    )
    
