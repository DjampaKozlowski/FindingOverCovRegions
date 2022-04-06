import pandas as pd


def read_bedgraphlike_file(fpath):
    """
    Read a bedgraph-like file and return the content as pandas dataframe.
    
    Bedgraph-like file must be a 3 columns tab separated file with :
        - 1st col : the chromosome/contif/scaffold identifier
        - 2nd col : the position in the chromosome/contif/scaffold
        - 3rd col : the depth e.g. coverage at this position 
    
    Arguments:
    ----------
    fpath (str) -- the bedgraph-like file path
    
    Returns:
    --------
    (pandas DataFrame) -- a pandas dataframe with 3 columns named ['contig', 
                          'position', 'depth'] and the same number of lines
                          as the bedgraph-like input file.
    """
    return pd.read_csv(fpath,
                       sep='\t',
                       header=None,
                       names=['contig', 'position', 'depth'])
    

def write_results_as_bed6(fpath, df):
    """
    Save the overcovered regions as a bed6 file (one over-covered region per 
    line). The resulting file is composed of 3 columns :
        - 1 st : the chr/scaffold/contig id
        - 2 nd : the start position of the over-covered region
        - 3 rd : the end position of the over-covered region
    
    Arguments:
    ----------
    fpath (str) -- the file path. existing file will be replaced.
    df (pandas dataframe) -- a dataframe containing the over-covered regions
                             analysis
    """
    df[['contig', 'start', 'end']].to_csv(fpath,
                                          sep='\t',
                                          header=False,
                                          index=False)
    
def write_results_as_tsv(fpath, df):
    """
    Save the overcovered regions as a tsv file (one over-covered region per 
    line). The resulting file is composed of 3 columns :
        - 1 st : the chr/scaffold/contig id
        - 2 nd : the start position of the over-covered region
        - 3 rd : the end position of the over-covered region
    
    Arguments:
    ----------
    fpath (str) -- the file path. existing file will be replaced.
    df (pandas dataframe) -- a dataframe containing the over-covered regions
                             analysis
    """
    df.to_csv(fpath,
              sep='\t',
              index=False)
    
    