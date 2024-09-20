version 1.0

workflow hello_word_q1{
  call hello_world
}

task hello_world {
  command <<<
  echo "hello world"
  >>>
  output {
    String res = read_string(stdout())
  }
}