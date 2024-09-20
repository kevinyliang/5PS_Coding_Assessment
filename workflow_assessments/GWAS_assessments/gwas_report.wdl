
version 1.0

workflow make_gwas_report {
  input {
    String cleaned_sumstat_file
    String rsid
    String ld_ref_file
    String report_quarto
    String output_dir
  }

  call run_quarto{
    input:
      cleaned_sumstat_file = cleaned_sumstat_file,
      rsid = rsid,
      ld_ref_file = ld_ref_file,
      report_quarto = report_quarto,
      output_dir = output_dir
  }
}


task run_quarto{
  input{
    String cleaned_sumstat_file
    String rsid
    String ld_ref_file
    String report_quarto
    String output_dir
  }
  
  command<<<
  quarto render ~{report_quarto} -P sumstat_file:~{cleaned_sumstat_file} -P ld_file:~{ld_ref_file} -P lead_snp:~{rsid} --output-dir ~{output_dir}
  >>>

}