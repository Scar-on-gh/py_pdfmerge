#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
"""
----------------------------------------------------
Title:      pdfmerge.py
License:    agpl-3.0
Author:     Samuel Carlson
Created on: 2022-12-17
----------------------------------------------------

Description: Input filenames to merge.

----------------------------------------------------

Arguments: 
-i (--input_dir)      - Provide custom input dir containing pdfs to merge.
-o (--output_dir)     - Provide custom output dir to place merged pdfs.
-f (--output_file)    - Provide custom output filename to place merged pdfs.

----------------------------------------------------

Notes:
How the VENV was made:
virtualenv -p python3.11 venv/py3.11

How to run this script:
cd /mnt/f/Documents/Personal/Scripts/
source /mnt/f/Documents/Personal/Scripts/python_pdf_mergetool/activate
python pdfmerge.py
----------------------------------------------------
"""

from typing import Union # Globally required, used for function type hints.
from pathlib import Path # Globally required, used for type hints
import logging # For logging of debug, info, warning, errors
import sys # Needed for logging
log_fh = logging.FileHandler(filename="pdfmerge.log")
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [log_fh, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG,
    # format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    format='[%(asctime)s] %(levelname)s: %(message)s', 
    #datefmt='%d-%b-%y %H:%M:%S', 
    handlers=handlers
)

def pdf_merge(pdf_input_dir : Union[Path, str], pdf_output_dir : Union[Path, str], pdf_output_fn : str):
    """ 
    Merges all the pdf files in current directory
    """
    # Imports
    from PyPDF2 import PdfMerger
    from glob import glob
    
    logging.info(f"Merging PDFs in directory: {pdf_input_dir}.")
    # Convert output filename to Path so we can use some of Path's nice functions (stem, suffix)
    pdf_output_fn = Path(pdf_output_fn)
    output_fullpath = Path(pdf_output_dir, pdf_output_fn)
    #logging.debug(f"output_fullpath = {output_fullpath}")
    # Create unique file each time, do not overwrite existing (don't be destructive if we can help it!)
    while Path.exists(output_fullpath):
        logging.debug(f"output_fullpath at point 2 = {output_fullpath}")
        # stem = return just the filename and no extension, then split from right on "_" 
        # If the file has already been indexed, then the first element returned is our index.
        # Cannot use pdf_output_fn here unless it is updated below. Otherwise infinite loop (same value tested)
        file_index_i = output_fullpath.stem.rsplit("_",1)[1]
        logging.debug(f"file_index_i = {file_index_i}")
        try:
            file_index_i = int(file_index_i)
            file_index_i = f"_{file_index_i + 1}"
        # Then the filename contains "_" but is not incremented already.
        except ValueError:
            logging.info(f"File has not been incremented but contains '_' character")
            file_index_i = f"_0"
        output_fullpath = Path(pdf_output_dir, f"{pdf_output_fn.stem}{file_index_i}{pdf_output_fn.suffix}")
        logging.debug(f"output_fullpath at point 3 = {output_fullpath}")
        #import time
        #time.sleep(5)
    # Perform the merge function - https://pypdf2.readthedocs.io/en/latest/modules/PdfMerger.html
    merger = PdfMerger()
    allpdfs = [file for file in glob("*.pdf", root_dir=pdf_input_dir)]
    logging.debug(f"allpdfs = {allpdfs}")
    # Glob returns just file names, so we have to remake into abs. path for PdfFileMerger
    [merger.append(Path(pdf_input_dir,pdf)) for pdf in allpdfs]
    with open(output_fullpath, "wb") as out_file:
        merger.write(out_file)
    
    logging.info(f"Merged PDF written to: {output_fullpath}.")

def main():
    """
    Main to setup args and call pdf_merge function
    """
    # Imports
    import argparse
    
    # __file__ doesn't exist if this script is called from interactive session. Work around that with except clause.
    try:
        filepath = Path(__file__).resolve()
        basepath = filepath.parent
    except NameError:
        basepath = Path.cwd()
        filepath = Path(basepath, "pdfmerge.py")

    # Declare a default merge path. I'd like to make pdf_input_dir an arg.
    pdf_input_dir   = Path(basepath, "files_to_merge")
    pdf_output_dir  = Path(basepath, "merged_files")
    pdf_output_fn   = "merged_pdfs.pdf"
    
    parser = argparse.ArgumentParser(description="Used to pass in custom args to pdfmerge script.")
    parser.add_argument("-i", "--input_dir", help="Provide custom input dir containing pdfs to merge", 
        required=False, default=pdf_input_dir) 
    parser.add_argument("-o", "--output_dir", help="Provide custom output dir to place merged pdfs", 
        required=False, default=pdf_output_dir)
    parser.add_argument("-f", "--output_file", help="Provide custom output filename to place merged pdfs", 
        required=False, default=pdf_output_fn) 
    args = parser.parse_args()

    # Assign possible arg appropriately, uses default if arg not used.
    pdf_input_dir   = args.input_dir
    pdf_output_dir  = args.output_dir
    pdf_output_fn  = args.output_file
    
    pdf_merge(pdf_input_dir, pdf_output_dir, pdf_output_fn)

if __name__ == "__main__":
    main()