<?php

//Random php code
session_start();
echo 'Hello world';

// CVE
$url = "https://polymtl.ca/";
filter_var($url, FILTER_VALIDATE_URL);


//Random PHP code
session_destroy();
echo "Bye";
