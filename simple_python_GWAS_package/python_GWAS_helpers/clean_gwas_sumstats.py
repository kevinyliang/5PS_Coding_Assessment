import re,csv,shutil,sys,gzip,warnings
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

def detect_palindrome(a1,a2,af,threshold):
  """Determines if 2 variants are palindromic and determine whether keep or remove based on minor allele frequency threhsold.

  keep:
    non palindromic (SNPs or Indels)
    palindromic but allele frequency is not within 0.5 +- threshold
  remove:
    palindromic and within the boundary


  Args:
      a1 (str): first allele
      a2 (str): second allele
      af (float): allele frequency of the SNP (minor or major is fine)
      threshold (float): the region around 0.5 for determining keep or drop. (i.e., 0.5 +- threshold is the boundary)
  """

  # standardize the notations
  ## cast to the right type. Error if not possible
  a1 = str(a1)
  a2 = str(a2)
  af = float(af)
  threshold = float(threshold)
  a1 = a1.upper()
  a2 = a2.upper()

  # input checks
  assert(len(a1) > 0 and len(a2) > 0),f"invalid inputs: {a1} {a2}"
  assert(threshold < 0.5),f"Cannot specify a threshold of 0.5 or more (0.5 +- threshold will be 0 or less)"
  if af < 0 or af > 1:
    warnings.warn(f"{af} af not bounded between 0 and 1, kept, but probably should check..")
    return True


  # determines if a1 and a2 are palindromic or not
  is_palindrom = None
  if len(a1) > 1 or len(a2) > 1:
    is_palindrom = False
  elif a1 == "A" and a2 == "T":
    is_palindrom = True
  elif a1 == "T" and a2 == "A":
    is_palindrom = True
  elif a1 == "C" and a2 == "G":
    is_palindrom = True
  elif a1 == "G" and a2 == "C":
    is_palindrom = True
  else:
    is_palindrom = False
  
  assert(is_palindrom != None)
  # determines boundary
  af_lower_bound = 0.5 - threshold
  af_upper_bound = 0.5 + threshold
  # default is keep. Only change if palindromic and ambiguous frequency
  keep = True
  if is_palindrom:
    if af >= af_lower_bound and af <= af_upper_bound:
      keep = False
    else:
      keep = True

  return keep



if __name__ == "__main__":
  print("this module contains function for basic GWAS sumstats processing")
  print("This contains function definitions only")
  print("This is not meant to be ran separately")