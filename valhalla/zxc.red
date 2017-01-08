;redcode
;name zxc.red
;author G.Labarga
;assert 1

       ORG      START
       MOV.I  $   -95, $     1
       MOV.I  $    -1, @     2
       MOV.I  $    -2, *     1
       MOV.I  $   -93, *  -188
       SUB.F  $     2, $    -1
       DJN.B  $    -4, #    53
       SPL.B  #   285, <   285
       MOV.I  $     2, }    -9
       DJN.F  $    -1, }   -10
       DAT.F  $    12, {   267
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
START  DJN.F  $     1, <  -324
       MOV.I  {  -324, <  -328
       MOV.I  {  -324, <  -331
       DJN.A  $   -18, <  -334
