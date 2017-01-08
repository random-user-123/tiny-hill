;redcode
;name Creeping_Horror.red
;author John Metcalf
;assert 1

       ORG      START
       SPL.B  #  -195, <   195
       MOV.I  >  -390, $   391
       ADD.F  $    -2, $    -1
       DJN.F  $    -2, {  -399
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $   400, $    -9
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
START  SPL.B  $   -12, {  -250
       MOV.I  $     6, $  -205
       SPL.B  $     1, {  -204
       SPL.B  $     1, {    61
       SPL.B  $     2, {   326
       DJN.A  >     0, #  -209
       DJN.F  @     0, #    57
       MOV.I  #   -10, $   267
