;redcode
;name flux.red
;author John Metcalf
;assert 1

       ORG      START
       ADD.BA #   195, #    12
       JMZ.F  $    -1, *    -1
       DIV.BA #     9, #     1
       SPL.B  #     8, $    30
       MOV.I  @    -2, }    -4
       DJN.F  $    -1, >    -2
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
START  MOV.I  <   190, {   177
       MOV.I  <   177, {   164
       MOV.I  <   164, {   151
       MOV.I  <   151, {   138
       MOV.I  <   138, {   125
       MOV.I  <   125, {   112
       DJN.F  $   -17, <   100
