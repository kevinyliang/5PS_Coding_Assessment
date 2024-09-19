import re,csv,shutil,sys,gzip
import pandas as pd
import numpy as np

def clean_sumstats(gwas_file,rsid_col,output_file):
  """Performs basic cleaning for summary statistics. Specifically it
 will
  1. remove rows without valid rsid numbers (matching to "^rs")
  2. will print out basic counts

  Requirements:
    - the gwas file must be in gzipped format

  Args:
      gwas_file (str): the absolute path to the summary statistic file in gzipped format
      rsid_col (int): 0-based indexing of the column for rsid
      output_file (str): absolute path to where cleaned summary statistics are stored
  """

  sumstats = pd.read_csv(
    gwas_file,quoting=csv.QUOTE_NONE,sep="\t"
  )
  valid_rows = sumstats.iloc[:,rsid_col].apply(lambda val: bool(re.match("^rs",val)))
  valid_sumstats = sumstats[valid_rows]
  valid_sumstats.to_csv(
    output_file,
    sep="\t",quoting=csv.QUOTE_NONE,compression="gzip",index=False
  )

  n_invalid_rsids = np.sum([not x for x in valid_rows])
  valid_rows = np.sum(valid_rows)
  assert(valid_rows == valid_sumstats.shape[0])

  print(f"# SNPs with invalid RS ids: {n_invalid_rsids}")
  print(f"# remaining rows: {valid_sumstats.shape[0]}")

  return

if __name__ == "__main__":
  print("this module contains function for basic GWAS sumstats processing")
  print("This contains function definitions only")
  print("This is not meant to be ran separately")