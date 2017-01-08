;redcode
;name bloodlust.red
;author John Metcalf
;assert 1

       ORG      START
       DAT.F  $    19, $     1
       SPL.B  #    21, $     0
       DAT.F  $     0, $     0
       ADD.F  $     5, $   -61
       MOV.I  $   -62, @   -62
       JMZ.F  $    -2, *   -63
       MOV.I  $   -64, *   -64
       JMZ.F  $    -4, $    65
       SPL.B  #   335, <  -335
       MOV.I  @    -8, }   -12
       MOV.I  @   -10, }   -13
       DJN.F  $    -2, }    -3
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       SPL.B  #     0, {     0
       JMP.B  >   400, >  -270
START  MOV.I  $    -2, $    56
       MOV.I  $    -3, $    56
       MOV.I  $    -3, $   -76
       DJN.F  $   -15, {    16
