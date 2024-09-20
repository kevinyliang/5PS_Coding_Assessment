version 1.0


workflow hello_w_input_q2 {
  input {
    String user_string
  }
  call hello_with_inputs_q2{
    input:
      usr_input = user_string
  }
}

task hello_with_inputs_q2 {
  input {
    String usr_input
  }
  command <<<
  echo "~{usr_input}"
  >>>
  output {
    String res = read_string(stdout())
  }
}