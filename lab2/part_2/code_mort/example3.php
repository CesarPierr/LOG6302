<?php

function hello_world() {
  echo "Hello World !";
  return;
  echo "Dead code";
}


function stop() {
  echo "End Programme";
  if(true)
    return 0;
  else
    exit(0);
  echo "Dead code";
}

hello_world();
