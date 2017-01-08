;redcode
;name toast.red
;author John Metcalf
;assert 1

       ORG      START
       DAT.F  $    25, $    33
       DAT.F  $     9, $     1
       SPL.B  #    10, $   400
       MOV.I  @    -2, }    -3
       MOV.I  @    -3, }    -4
       DJN.F  $    -2, >    -3
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       SUB.F  $     1, $   -16
START  SNE.I  *   -17, @   -17
       DJN.F  $    -2, <  -169
       DJN.F  $   -17, $   -19
