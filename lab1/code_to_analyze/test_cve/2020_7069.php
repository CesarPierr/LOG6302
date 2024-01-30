<?php

//Random php code
session_start();
echo 'Hello world';

// CVE
$plaintext = "message to be encrypted";
$ivlen = openssl_cipher_iv_length("aes-128-gcm");
$iv = openssl_random_pseudo_bytes($ivlen);
$ciphertext = openssl_encrypt($plaintext, "aes-128-gcm", $key, $options=0, $iv, $tag);
echo $ciphertext;

//Random PHP code
session_destroy();
echo "Bye";
