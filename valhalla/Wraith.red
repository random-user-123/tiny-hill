;redcode
;name Wraith.red
;author John Metcalf
;assert 1

       ORG      START
       MOV.I  $   195, $     1
       MOV.I  $    -1, @     1
       MOV.I  $    -2, {   223
       ADD.AB #  -389, $    -1
       DJN.B  $    -3, #    89
       DIV.BA #     9, #     1
       SPL.B  #     8, $    30
       MOV.I  @    -2, }    -4
       DJN.F  $    -1, >    -2
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
       DAT.F  $     0, $     0
START  MOV.I  >   205, {   226
       MOV.I  <   226, {   246
       MOV.I  <   246, {   266
       MOV.I  <   266, {   286
       MOV.I  <   286, {   307
       MOV.I  <   307, {   327
       MOV.I  <   327, {   347
       DJN.F  $   -18, <   367
