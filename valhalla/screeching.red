;redcode
;name screeching.red
;author G.Labarga
;assert 1

       ORG      START
       SUB.F  $     4, $     2
       MOV.I  $    10, @     1
START  SNE.I  }    50, *    37
       DJN.B  $    -3, <   -90
       SPL.B  #   -39, >   -39
       MOV.I  @     3, >    -3
       MOV.I  @     2, >    -4
       MOV.I  @     1, >    -5
       DJN.F  $    -3, {     2
       DAT.F  $   -20, $    14
       SPL.B  #  -100, $    14
       MOV.I  >    26, $     1
