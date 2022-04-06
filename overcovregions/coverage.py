import numpy as np
import pandas as pd
from collections import deque



def find_overcov_regions(df_contig, sliding_win_len, depth_thresh):
    """
    Find overcovered regions in a list of coverage and return the start and end
    positions of the overcovered regions
    
    Parameters:
    -----------
    df_contig (pandas dataframe) -- a bedgraph like dataframe (columns : 
                                    'contig', 'position', 'depth'). Must 
                                    contain data for only one contig.
    sliding_win_len (int) -- the length of the sliding window. The average depth
                             will be computed on this window.
    depth_thresh (float) -- the depth threshold value to consider a region as
                            overcovered
    
    Returns:
    --------
    (pandas dataframe) -- a pandas dataframe containing all the over-covered 
                          regions (no minimal size) for the analysed contig. 
                          The dataframe is composed of 7 columns:
                            - 'contig' : the contig id
                            - 'start'  : the start position of the over-covered
                            region.
                            - 'end'    : end position of the over-covered region
                            - length   : the length of the over-covered region (
                            including the last position)
                            - median_depth : median depth value in the 
                            over-covered region
                            - mean_depth : mean depth value in the 
                            over-covered region
                            - mean_depth : standard deviation of depth value in 
                            the over-covered region.
                           If no overcovered region was found, return an empty 
                           dataframe.
    
    """
    
    ## Create a deque (double ended queue) i.e list like ojectect containing a
    #  definined number of elements. Here used as a FIFO (first in first out). 
    sl_win = deque([], int(sliding_win_len))
    
    ## Init an empty list which will contain the first over-covered region
    overcov_region=[]

    ## Create the ouput list that will contain all the over-covered regions
    #  information
    lst_overcov_regions = []    
    
    ## Iterate through df_contig
    for idx, row in df_contig.iterrows():
        ## Create two variables : position and depth
        position, depth = row['position'], row['depth']
        ## Fill the sliding window
        sl_win.append(depth)

        ## When the sliding window is full 
        if len(sl_win)>=(sliding_win_len):
            ## Once filled, 
            #       If the mean depth value in the sliding window is above 
            #       the threshold value and the overcov-region is empty e.g.
            #       begining of an overcov region :
            #           i)  the content of the sliding window is copied into the
            #               the overcov_region list
            #           ii) the start position is set
            if (np.mean(sl_win) >= depth_thresh) and (len(overcov_region)==0):
                overcov_region = list(sl_win)
                start_position = position +1 - sliding_win_len

            #       If the mean depth value in the sliding window is above 
            #       the threshold value and an over-covered region already 
            #       exists:
            #           i)  fill the overcov-region   
            elif (np.mean(sl_win) >= depth_thresh) and (len(overcov_region)>0):
                overcov_region.append(depth)

            #       If the mean depth value in the sliding window pass below 
            #       the threshold value and an over-covered region already 
            #       exists (case of an over-covered region ending):
            #           i)  set the end position
            #           ii) store the over-covered region infos into 
            #               lst_overcov_regions
            #           iii)empty the overcov_region
            elif (np.mean(sl_win) < depth_thresh) and (len(overcov_region)>0):
                end_position = position -1 
                lst_overcov_regions.append({
                    'contig':row['contig'],
                    'start':start_position,
                    'end':end_position,
                    'length':len(overcov_region),
                    'median_depth':np.median(overcov_region),
                    'mean_depth':np.mean(overcov_region),
                    'std_depth':np.std(overcov_region)
                    })
                overcov_region = []
    
    ## In case an overcovered region was open when reaching the end of the 
    #  contig, store the region in lst_overcov_regions
    if len(overcov_region)>0:
        lst_overcov_regions.append({
            'contig':row['contig'],
            'start':start_position,
            'end':position,
            'length':len(overcov_region),
            'median_depth':np.median(overcov_region),
            'mean_depth':np.mean(overcov_region),
            'std_depth':np.std(overcov_region)
            })
    return pd.DataFrame(lst_overcov_regions) 
               
             

