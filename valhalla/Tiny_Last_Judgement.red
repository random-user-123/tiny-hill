;redcode
;name Tiny_Last_Judgement.red
;author Christian Schmidt
;assert 1

       ORG      START
START  MOV.I  <     7, {     7
       MOV.I  $    13, $  -203
       MOV.I  $    11, $  -135
       SPL.B  $     1, <   -75
       SPL.B  $     1, <   158
       MOV.I  <     2, {     2
       MOV.I  <     2, {     2
       SPL.B  $  -214, $    13
       JMP.B  $   235, $     5
       SPL.B  #   267, <  -295
       ADD.F  $    -1, $     1
       SPL.B  $   158, <    82
       DJN.F  $   346, <   281
       MOV.I  #   267, *     0
       DAT.F  <  -196, >     1
       SPL.B  #     0, <  -195
       MOV.I  $     9, {  -335
       MOV.I  $     8, @    -1
       SUB.AB #    12, $    -2
       DJN.F  $    -3, <  -199
