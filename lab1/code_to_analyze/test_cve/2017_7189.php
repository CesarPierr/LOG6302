<?php

//Random php code
session_start();
echo 'Hello world';

// CVE

$fp = fsockopen("udp://127.0.0.1:8080", 13, $errno, $errstr);
if (!$fp) {
  echo "ERREUR : $errno - $errstr<br />\n";
} else {
  fwrite($fp, "\n");
  echo fread($fp, 26);
  fclose($fp);
}


//Random PHP code
session_destroy();
echo "Bye";
