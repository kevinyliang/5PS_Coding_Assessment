

import unittest,os,sys
import numpy as np
from itertools import combinations
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import python_GWAS_helpers


class test_detect_palindrome(unittest.TestCase):
  def test_palindrome_unambig(self):
    """make sure palindrome outside of range is true
    for threshold of 0.1, the boundary is [0.4,0.6] inclusive
    """
    eaf_range = list(np.arange(0,0.4,0.01)) + list(np.arange(0.7,1,0.01)) 
    allele_pairs = [("A","T"),("T","A"),("C","G"),("G","C")]
    for i in eaf_range:
      for alleles in allele_pairs:
        self.assertTrue(
          python_GWAS_helpers.detect_palindrome(alleles[0],alleles[1],i,0.1)
        )
  def test_palindrome_ambig(self):
    """Palindromic variants within the specified boundary should not be kept
    """
    eaf_range = list(np.arange(0.4,0.5,0.01))
    allele_pairs = [("A","T"),("T","A"),("C","G"),("G","C")]
    for i in eaf_range:
      for alleles in allele_pairs:
        self.assertFalse(
          python_GWAS_helpers.detect_palindrome(alleles[0],alleles[1],i,0.1)
        )
  
  def test_indel_ok(self):
    """Indels are not filtered out
    """
    self.assertTrue(
      python_GWAS_helpers.detect_palindrome("ACTA","_",0.1,0.1)
    )
    self.assertTrue(
      python_GWAS_helpers.detect_palindrome("A","ATC",0.1,0.1)
    )

  def test_non_palindrome(self):
    """non palindromic regardless of allele frequency is true
    """
    allele_pairs = [
      ("A",x) for x in ["C","G"]
    ] + [
      ("T",x) for x in ["C","G"]
    ] + [
      ("C",x) for x in ["A","T"]
    ] + [
      ("G",x) for x in ["A","T"]
    ]
    for i in allele_pairs:
      self.assertTrue(
        python_GWAS_helpers.detect_palindrome(i[0],i[1],np.random.uniform(0,1),np.random.uniform(0,0.49))
      )
  def test_warnings(self):
    self.assertWarns(
      (UserWarning),python_GWAS_helpers.detect_palindrome,"A","T",1.2,0.1
    )
    self.assertWarns(
      (UserWarning),python_GWAS_helpers.detect_palindrome,"A","T",-0.1,0.1
    )
    return
    
if __name__ == "__main__":
  unittest.main()



