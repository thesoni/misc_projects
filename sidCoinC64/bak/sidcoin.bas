
10 v = 53248
11 l = 5                                :rem lives
12 s = 0                                :rem score
13 m1 = 10                              :rem m1 is player move amt
14 m2 = 2                               :rem m2 is bomb move amt
15 x1 = 24                              :rem init locations
16 y1 = 100
18 x2 = 150
19 y2 = 150
20 x3 = 200
21 y3 = 200

30 rem set screen colors (border and background)
31 poke 53280,0
32 poke 53281, peek(53280)
33 for x = 54272 to 54296:poke x,0:next 
34 poke 54296,15                        :rem init SID chip

35 print chr$(147)
36 print "use w/a/s/d to move your guy"
37 for x = 1 to 100: POKE54296,0:POKE54296,15:next x

39 gosub 900                            :rem refresh screen labels

40 poke v+21, 7                         :rem Turn on first 3 sprites (255 = all 8)

41 :rem 2040 is the pointer for sprite 0
42 :rem the ratio between the sprite memory location and the value 64.
43 :rem eg: 12288 / 64 = 192

51 poke 2040, 192                       :rem Set sprite 0's mem address
52 for t = 12288 to 12288+63            :rem loop for S0's 'pixels  (24x21)
53 read y
54 poke t , y
55 next t
56 poke v+39,14                          :rem set color register for sprite 0

61 poke 2041, 193                       :rem Set sprite 1's mem address
62 for t = 12352 to 12352+63            :rem loop to set pixels
63 read y
64 poke t , y
65 next t
66 poke v+40,2                          :rem set color register for sprite 2

71 poke 2042, 194                       :rem Set sprite 2's mem address
72 for t = 12416 to 12416+63            :rem loop to set pixels
73 read y: 
74 poke t , y
75 next t
76 poke v+41,5                          :rem set color register for sprite 3

81 poke 2043, 195                       :rem Set sprite 3's mem address
82 for t = 12480 to 12480+63            :rem loop to set pixels
83 read y: 
84 poke t , y
85 next t
86 poke v+42,14                          :rem set color register for sprite 3


100 poke v,x1                           :rem X location S0
101 poke v+1,y1                         :rem Y location S0
102 poke v+2,x2                         :rem X location  S1
103 poke v+3,y2                         :rem Y location S1
104 poke v+4,x3                         :rem X location  S2
105 poke v+5,y3                         :rem Y location S2

150 poke v+30,0                          :rem clear collision register

200 a = peek(56321)                     :rem joystick register
205 a = peek(197)                        :rem keyboard input register
210 if a = 9 then y1 = y1 - m1          :rem UP
215 if a = 13 then y1 = y1 + m1         :rem DOWN
218 if a = 10 then x1 = x1 - m1         :rem LEFT
219 if a = 18 then x1 = x1 + m1         :rem RIGHT

223 rem screen borders 
224 if x1 > 250 then x1 = 250                       
226 if x1 < 24 then x1 = 24
227 if y1 < 50 then y1 = 50
229 if y1 > 220 then y1 = 220

300 rem move bomb towards player 
301 rem (x2,y2) is bomb
302 rem (x1,y1) is player
310 if x2 > x1 then x2 = x2 - m2
315 if x2 < x1 then x2 = x2 + m2
320 if y2 > y1 then y2 = y2 - m2
330 if y2 < y1 then y2 =  y2 + m2

400 rem check collisions
401 rem 3 = 011 = S0 & S1 (guy & bomb)
402 rem 5 = 101 = S0 & S2 (guy & coin)
410 if (peek(v+30) and 3) = 3 then gosub 500
415 if (peek(v+30) and 5) = 5 then gosub 800     
420 goto 100

500 rem hit by bomb!  
502 rem relocate bomb
505 rem update/check lives left
508 for x = 1 to 30: POKE54296,0:POKE54296,15:gosub 920:next x
510 poke v+30,0                 :rem clear collision register
520 x2 = rnd(0)*225 + 24        :rem relocate bomb
530 y2 = rnd(0)*170 + 50
540 poke v+2,x2                         
550 poke v+3,y2                         
610 l = l - 1                   :rem dec lives
620 gosub 900
625 poke v+21, 7    
630 if l = 0 then goto 700
640 return

700 rem lives 0, game over
705 for x = 1 to 10
710 print""
720 next
730 for x = 1 to 15: print "";: next
740 print "game over..."
745 print "you got"; s; "coins"
746 print
748 print "press any key to play again"
750 POKE 198,0: WAIT 198,1 
760 l=5                                 :rem reset lives, score, speed
765 s=0
768 m2=0
770 gosub 900
780 goto 100

800 rem got coin!   Update score
801 gosub 940   :rem sound
802 s = s + 1
804 gosub 900   :rem update screen
810 rem relocate coin
811 x3 = rnd(0)*225 + 24 
812 y3 = rnd(0)*170 + 50
850 rem  speed up bomb every 3 coins
851 m = s - INT (S/3) * 3
852 if m = 0 then m2 = m2 + 2
861 if m2 > m1 then m2 = m1
870 return

900 rem refresh screen
901 print chr$(147)
902 print "lives = "; l
903 rem print "score = "; s
906 rem print peek(v+30)
910 return

920 rem show dead guy at (x1,y1)
921 poke v+21, 14    
922 poke v+6,x1                         
923 poke v+7,y1           
924 rem for x = 1 to 300: next x
935 return

939 rem dead sound
940 rem forx=54272to54296:poke x,0:next 
941 rem poke 54296,15 
942 poke54277,190 
943 poke54278,248 
944 poke54273,17:poke54272,37 
945 poke54276,17 
946 for x=1to150:next 
947 poke 54276,16
948 return
              

1000 :: rem sprite 1 / singlecolor / color: 1
1010 data 0,0,0,0,0,0,0,56,0,0,200,0,0,140,0,1
1020 data 132,0,1,4,0,1,12,0,1,216,0,0,32,0,0,32
1030 data 0,4,32,128,7,255,128,0,32,0,0,32,0,0,32,0
1040 data 0,96,0,0,240,0,3,12,0,6,7,0,0,0,0,1

2000 :: rem sprite 1 / singlecolor / color: 2
2010 data 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
2020 data 0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,12
2030 data 0,0,24,0,0,16,0,0,252,0,1,252,0,1,252,0
2040 data 1,252,0,1,252,0,1,252,0,0,252,0,0,248,0,2

3000 :: rem sprite 1 / singlecolor / color: 5
3010 data 0,0,0,0,0,0,0,0,0,1,254,0,6,3,128,12
3020 data 16,192,8,16,96,8,254,32,8,144,16,8,208,16,8,112
3030 data 16,8,28,48,8,20,32,4,20,32,4,124,32,6,16,32
3040 data 3,0,96,1,128,192,0,127,128,0,0,0,0,0,0,5

4050 :: rem sprite 2 / singlecolor / color: 1
4060 data 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
4070 data 0,0,0,0,0,0,0,0,0,0,16,96,192,16,216,64
4080 data 16,140,32,24,134,16,8,130,16,8,131,240,12,129,159,254
4090 data 131,16,8,198,48,12,124,96,6,0,192,2,0,0,0,1








