<?php

//Random php code
session_start();
echo 'Hello world';

// CVE
$FILE = "test/";
$path = "/home/aman/".$FILE."poc.xml";
echo simplexml_load_file($path);


//Random PHP code
session_destroy();
echo "Bye";
