
version 1.0

workflow make_regional_plot {
  input {
    File cleaned_sumstat_file
    String rsid
    File ld_ref_file
    File report_quarto
    File output_dir
  }

  call make_gwas_report{
    input:
      cleaned_sumstat_file = cleaned_sumstat_file,
      rsid = rsid,
      ld_ref_file = ld_ref_file,
      report_quarto = report_quarto,
      output_dir = output_dir
  }
}


task make_gwas_report{
  input{
    File cleaned_sumstat_file
    String rsid
    File ld_ref_file
    File report_quarto
    File output_dir
  }
  command<<<
  echo quarto render ~{report_quarto} -P sumstat_file:~{cleaned_sumstat_file} -P ld_file:~{ld_ref_file} -P lead_snp:~{rsid} --output-dir ~{output_dir}
  >>>
  output {
    File res = 'GWAS_report.html'
  }
}