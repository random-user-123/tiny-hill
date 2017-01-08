;redcode
;name sprinklespike.red
;author Roy van Rijn
;assert 1

       ORG      START
       ADD.F  $     4, @     6
START  MOV.I  #  -379, {     1
       SNE.I  *  -348, }    57
       DJN.F  $    -3, <    -1
       SPL.B  #    31, {    31
       MOV.I  @     2, >    -3
       MOV.I  @     1, >    -4
       DJN.F  $    -2, {     2
       DAT.F  }  -123, }     9
       SPL.B  #  -123, }     9
