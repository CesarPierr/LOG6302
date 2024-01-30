<?php
function f2($v1, $v2, $v3, $v4, $v5, $v6, $v7, $v8, $v9) {

    $i = 3;

    $a = $v1 . $v2 . $v3;

    if (($i == 2) or ($i == 3)) {

        if ($i == 2) {
            $a = $v4 . $v5 . $v6;
        } else {
            $a = $v7 . $v8 . $v9;
        }
    }

    return $a;
}

function f1() {
    
    $w1 = '1';
    $w2 = '2';
    $w3 = '3';
    $w4 = '4';
    $w5 = '5';
    $w6 = '6';
    $w7 = '7';
    $w8 = '8';
    $w9 = '9';

    $b = f2($w1, $w2, $w3, $w4, $w5, $w6, $w7, $w8, $w9);

    $df_y = $b;

    return;
}

f1();
    
