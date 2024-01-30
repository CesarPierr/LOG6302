<?php

//Random php code
session_start();
echo 'Hello world';

// CVE
var_dump(mb_split("\w","\xfc"));

//Random PHP code
session_destroy();
echo "Bye";
