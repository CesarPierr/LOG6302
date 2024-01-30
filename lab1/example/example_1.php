<?php

function f2() {
    
    $a = '123';

    $i = 3;


    if (($i == 2) or ($i ==3)) {

        if ($i == 2) {
            $a = '456';
        } else {
            $a = '789';
        }
    }

    $df_y = $a;

    return;
}

f2();
