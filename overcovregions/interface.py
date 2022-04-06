import argparse


def arguments_parser():
    """
    Description :
    -------------
    Parse script arguments to get the following information:
            - input file path
            - output directory
            - depth threshold value
            - minimum size of an over covered region
            - size of sliding window (must be smaller than the window above)


    Returns :
    ---------
     *  -- object, parser object
    """
    parser = argparse.ArgumentParser(description="find overcovered regions with a sliding window system")

    requiredargs = parser.add_argument_group('required arguments')
    requiredargs.add_argument("-i", "--inputfilepath", help="path of perbase bedgraph-like file [mendatory]", required=True)
    requiredargs.add_argument("-o", "--outputdir", help="output directory  [mendatory]", required=True)
    requiredargs.add_argument("-p", "--prefix", help="prefix of the ouput files [mendatory]", required=True)
    requiredargs.add_argument("-d", "--depth", help="depth threshold  [mendatory]", required=True)
    requiredargs.add_argument("-m", "--minovercovregionsize", help="minimum size for an over covered region  [mendatory]", required=True)
    requiredargs.add_argument("-s", "--slidingwinsize", help="size of the sliding window (must be smaller than the minimum size for an over covered region)  [mendatory]", required=True)
    return parser.parse_args()