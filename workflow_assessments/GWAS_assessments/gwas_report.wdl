
version 1.0

workflow make_regional_plot {
  input {
    File cleaned_sumstat_file
    String rsid
    File ld_ref_file
    File report_quarto
  }

  call make_gwas_report{
    input:
      cleaned_sumstat_file = cleaned_sumstat_file,
      rsid = rsid,
      ld_ref_file = ld_ref_file,
      report_quarto = report_quarto
  }
}


task make_gwas_report{
  input{
    File cleaned_sumstat_file
    String rsid
    File ld_ref_file
    File report_quarto
  }
  command<<<
  quarto render ~{report_quarto} -P sumstat_file:~{cleaned_sumstat_file} -P ld_file:~{ld_ref_file} -P lead_snp:~{rsid}
  >>>
}