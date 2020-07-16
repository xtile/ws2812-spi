#!/usr/bin/python

import time
import math

NumpyImported=False
try:
    #i=2
    import numpy 
    from numpy import sin, cos, pi
    NumpyImported=True
    print("numpy is ok")
except ImportError:
    print("Warning: no numpy found, routines will be slow")
    pass
"""
T0H: 0.35   -> 2p=0.31  3p=0.47
T0L: 0.80   -> 6p=0.94  5p=0.78
T1H: 0.70   -> 4p=0.625 5p=0.78
T1L: 0.60   -> 4p=0.625 3p=0.47
"""

def write2812_numpy8(spi,data):
    d=numpy.array(data).ravel()
    tx=numpy.zeros(len(d)*8, dtype=numpy.uint8)
    for ibit in range(8):
        #print ibit
        #print ((d>>ibit)&1)
        #tx[7-ibit::8]=((d>>ibit)&1)*0x18 + 0xE0   #0->3/5, 1-> 5/3 
        #tx[7-ibit::8]=((d>>ibit)&1)*0x38 + 0xC0   #0->2/6, 1-> 5/3
        tx[7-ibit::8]=((d>>ibit)&1)*0x78 + 0x80    #0->1/7, 1-> 5/3
        #print [hex(v) for v in tx]
    #print [hex(v) for v in tx]
    spi.xfer(tx.tolist(), int(8/1.25e-6))
    #spi.xfer(tx.tolist(), int(8e6))
    
def write2812_numpy4(spi,data):
    #print spi
    print("numpy4")
    d=numpy.array(data).ravel()
    tx=numpy.zeros(len(d)*4, dtype=numpy.uint8)
    for ibit in range(4):
        #print ibit
        #print ((d>>(2*ibit))&1), ((d>>(2*ibit+1))&1)
        tx[3-ibit::4]=((d>>(2*ibit+1))&1)*0x60 + ((d>>(2*ibit+0))&1)*0x06 +  0x88
        #print [hex(v) for v in tx]
    #print [hex(v) for v in tx]
    #not working on zero  spi.xfer3(tx.tolist(), int(4/1.25e-6)) #works, on Zero (initially didn't?)
    #not working on zero spi.xfer3(tx.tolist(), int(4/1.20e-6))  #works, no flashes on Zero, Works on Raspberry 3
    #not working on zero spi.xfer3(tx.tolist(), int(4/1.15e-6))  #works, no flashes on Zero
    #spi.xfer3(tx.tolist(), int(4/1.05e-6))  #works, no flashes on Zero
    spi.xfer3(tx.tolist(), int(4/.95e-6))  #works, no flashes on Zero
    #spi.xfer(tx.tolist(), int(4/.90e-6))  #works, no flashes on Zero
    #spi.xfer(tx.tolist(), int(4/.85e-6))  #doesn't work (first 4 LEDS work, others have flashing colors)
    #spi.xfer(tx.tolist(), int(4/.65e-6))  #doesn't work on Zero; Works on Raspberry 3
    #spi.xfer(tx.tolist(), int(4/.55e-6))  #doesn't work on Zero; Works on Raspberry 3
    #spi.xfer(tx.tolist(), int(4/.50e-6))  #doesn't work on Zero; Doesn't work on Raspberry 3 (bright colors)
    #spi.xfer(tx.tolist(), int(4/.45e-6))  #doesn't work on Zero; Doesn't work on Raspberry 3
    #spi.xfer(tx.tolist(), int(8e6))

def write2812_pylist8(spi, data):
    tx=[]
    for rgb in data:
        for byte in rgb: 
            for ibit in range(7,-1,-1):
                tx.append(((byte>>ibit)&1)*0x78 + 0x80)
    spi.xfer(tx, int(8/1.25e-6))

def write2812_pylist4(spi, data):
    print("pylist4")
    tx=[]
    for rgb in data:
        for byte in rgb: 
            for ibit in range(3,-1,-1):
                #print ibit, byte, ((byte>>(2*ibit+1))&1), ((byte>>(2*ibit+0))&1), [hex(v) for v in tx]
                tx.append(((byte>>(2*ibit+1))&1)*0x60 +
                          ((byte>>(2*ibit+0))&1)*0x06 +
                          0x88)
    #print [hex(v) for v in tx]
    spi.xfer3(tx, int(4/1.05e-6))


if NumpyImported:
    write2812=write2812_numpy4
else:
    write2812=write2812_pylist4    


if __name__=="__main__":
    
    import spidev
    import time
    import getopt
    import sys

<<<<<<< HEAD

    color_light_green = [30, 30, 0]
    color_orange= [20, 90, 0]
    color_yellow = [20,60, 0] 
    color_black  = [0,0,0]
    color_pink = [0, 30, 30]
    color_red = [0, 30, 0]
    color_green = [30, 0, 0]
    color_blue = [0, 0, 30]



    def i(x,y):
        if x < 0: 
            print("x<0")
            return
        if x > 63: 
            print("x>63")
            return 
        if y< 0:
            print("y<0")
            return 
        if y > 8: 
            print("y>8")
            return 
        if x%2:
            return x*8 + y
        else:
            return x*8 + 7 -y


    def drawverticalline(leds, x, y, len, color):
        #print(x)
        #print(y)
        #print(len)
        #print(color)
        for j in range (len): 
            leds[i(x, y+j)] = color #leds[i(0,0)] #color
        #print("linever")
        #print(leds)
        return leds


    def drawhorizontalline(leds, x, y, len, color):
        #print(x)
        #print(y)
        #print(len)
        #print(color)
        for j in range (len): 
            leds[i(x+j, y)] = color #leds[i(0,0)] #color
        #print("linehor")
        #print(leds)
        return leds
    
    def clear(leds ):
       leds = [color_black]*8*64
       return leds        

       return leds

    def drawrect(leds, x,y, width, height, color):
        for j in range (width):
            leds = drawverticalline(leds, x+j, y, height, color)
        
        return leds

    def draw_let_a(leds, x, y, color):
        
#    """
#
#
#
#     xxx x
#    x   xx
#    x    x
#    x   xx
#     xxx xx 
#    """

        leds[i(x+1,y+4)] = color
        #leds[i(x+2,y+4)] = color
        leds[i(x+2,y+4)] = color
        leds[i(x+4,y+4)] = color

        leds[i(x+0,y+3)] = color
        leds[i(x+4,y+3)] = color
        leds[i(x+3,y+3)] = color

        leds[i(x+0,y+2)] = color
        leds[i(x+4,y+2)] = color

        leds[i(x+0,y+1)] = color
        leds[i(x+3,y+1)] = color
        leds[i(x+4,y+1)] = color

        leds[i(x+1,y+0)] = color
        #leds[i(x+2,y+0)] = color
        leds[i(x+2,y+0)] = color
        leds[i(x+4,y+0)] = color

        return leds

    def draw_let_b(leds, x, y, color):
        
#'''
#x
#x
#x
#x xxx
#xx   x
#x    x
#xx   x
#x xxx
#'''

        leds[i(x,y+7)] = color
        leds[i(x,y+6)] = color
        leds[i(x,y+5)] = color
        
        leds[i(x,y+4)] = color

        leds[i(x+2,y+4)] = color
        #leds[i(x+3,y+4)] = color
        leds[i(x+3,y+4)] = color

        leds[i(x,y+3)] = color
        leds[i(x+1,y+3)] = color
        leds[i(x+4,y+3)] = color
        
        leds[i(x,y+2)] = color
        leds[i(x+4,y+2)] = color


        leds[i(x,y+1)] = color
        leds[i(x+1,y+1)] = color
        leds[i(x+4,y+1)] = color

        leds[i(x+0,y+0)] = color
        leds[i(x+2,y+0)] = color
        #leds[i(x+3,y+0)] = color
        leds[i(x+3,y+0)] = color

        return leds         

    def draw_let_c(leds, x, y, color):
        
#'''
#
#
#
# xxxxx
#x
#x
#x
# xxxxx
#'''

        leds[i(x+1,y+4)] = color
        leds[i(x+2,y+4)] = color
        leds[i(x+3,y+4)] = color
        #leds[i(x+5,y+3)] = color
        leds[i(x+4,y+4)] = color

        leds[i(x,y+3)] = color

        leds[i(x,y+2)] = color

        leds[i(x,y+1)] = color

        leds[i(x+1,y+0)] = color
        leds[i(x+2,y+0)] = color
        leds[i(x+3,y+0)] = color
        leds[i(x+4,y+0)] = color


        return leds


    def draw_let_d(leds, x, y, color):
        
#'''
#x
#x
#x
#x xxx
#xx   x
#x    x
#xx   x
#x xxx
#'''
        leds[i(x+5,y+7)] = color
        leds[i(x+5,y+6)] = color
        leds[i(x+5,y+5)] = color

        leds[i(x+5,y+4)] = color

        leds[i(x+3,y+4)] = color
        leds[i(x+2,y+4)] = color
        leds[i(x+1,y+4)] = color

        leds[i(x+5,y+3)] = color
        leds[i(x+4,y+4)] = color
        leds[i(x+0,y+3)] = color

        leds[i(x,y+2)] = color
        leds[i(x+5,y+2)] = color

        leds[i(x,y+1)] = color
        leds[i(x+4,y+0)] = color
        leds[i(x+5,y+1)] = color

        leds[i(x+5,y+0)] = color
        leds[i(x+3,y+0)] = color
        leds[i(x+4,y+0)] = color
        leds[i(x+1,y+0)] = color

        return leds

    def draw_let_n(leds, x, y, color):
#'''
#
#
#
#x xx
#xx  x
#x   x
#x   x
#x   x
#'''
        leds[i(x+0,y+4)] = color
        leds[i(x+2,y+4)] = color
        leds[i(x+3,y+4)] = color

        leds[i(x+0,y+3)] = color
        leds[i(x+1,y+3)] = color

        leds[i(x+0,y+2)] = color
        leds[i(x+0,y+1)] = color
        leds[i(x+0,y+0)] = color
        leds[i(x+4,y+2)] = color
        leds[i(x+4,y+1)] = color
        leds[i(x+4,y+0)] = color

        return leds         


    def draw_let_r(leds, x, y, color):
#'''
#
#
#
#  xxx
# x
#x
#x
#x
#'''
        leds[i(x+2,y+4)] = color
        leds[i(x+3,y+4)] = color
        leds[i(x+4,y+4)] = color

        leds[i(x+1,y+3)] = color

        leds[i(x+0,y+2)] = color
        leds[i(x+0,y+1)] = color
        leds[i(x+0,y+0)] = color

        return leds         


    def draw_let_i(leds, x, y, color):
#'''
#
#  x
#
#  xx
#  x
#  x
#  x
#  xx
#'''
        leds[i(x+2,y+6)] = color
        leds[i(x+2,y+4)] = color
        leds[i(x+3,y+4)] = color

        leds[i(x+2,y+3)] = color

        leds[i(x+2,y+2)] = color
        leds[i(x+2,y+1)] = color
        leds[i(x+2,y+0)] = color

        leds[i(x+3,y+0)] = color

        return leds         


    def draw_let_p(leds, x, y, color):
#'''
#xxxx
#x   x
#x   x
#x   x
#xxxx
#x
#x
#x
#'''
        leds[i(x+0,y+7)] = color
        leds[i(x+1,y+7)] = color
        leds[i(x+2,y+7)] = color
        leds[i(x+3,y+7)] = color

        leds[i(x+0,y+6)] = color
        leds[i(x+4,y+6)] = color

        leds[i(x+0,y+5)] = color
        leds[i(x+4,y+5)] = color

        leds[i(x+0,y+4)] = color
        leds[i(x+4,y+4)] = color

        leds[i(x+0,y+3)] = color
        leds[i(x+1,y+3)] = color
        leds[i(x+2,y+3)] = color
        leds[i(x+3,y+3)] = color

        leds[i(x+0,y+2)] = color

        leds[i(x+0,y+1)] = color
        leds[i(x+0,y+0)] = color

        return leds         



    def sine(leds, t):
       f = round(math.cos(t/10)*100)
       f = (f+100)/2

       print(f)
       #a1 = f*leds
       #a2 = numpy.true_divide(a1, 100)
       a2 = numpy.multiply(leds, f/100)
       #print(a2)
       leds2 = numpy.around(a2, 0).astype(numpy.uint8)
       #print(leds2)
       return leds2 

    def shift_right(leds):
        '''
        0 < 15
        1 < 14
        2 < 13
        3 < 12
        4 < 11
        5 < 10
        6 < 9
        7 < 8 
 
        8 < 23
        9 < 22
        10 < 21 
        11 < 20
        12 < 19
        13 < 18
        14 < 17
        15 < 16 

        '''
        for i in range(54*8, -1, -1):
            x = i // 8
            y = i % 8 
            #if x%2:
            #leds[55*8-1 - i] = 
            leds[ (i+16 -1 - 2*y)] = leds[ i] 
            #else:
            #    leds[i] = leds[i+8]
        return leds


    def shift_left(leds):
        '''
        0 < 15
        1 < 14
        2 < 13
        3 < 12
        4 < 11
        5 < 10
        6 < 9
        7 < 8 
 
        8 < 23
        9 < 22
        10 < 21 
        11 < 20
        12 < 19
        13 < 18
        14 < 17
        15 < 16 
        
        '''
        for i in range(55*8):
            x = i // 8
            y = i % 8 
            #if x%2:
            leds[i] = leds[i+16 -1 - 2*y]
            #else:
            #    leds[i] = leds[i+8]
        return leds

    def taxi_mode(spi):
        print("taxi_mode")
 #       leds = [color_black]*8*64

        #color_orange = [40, 150, 0]
        #color_black  = [0,0,0]
        leds = [color_black]*8*64


        i = 0
        while True:
            i = i+1
            if i%2: 
                color_1 = color_black
                color_2 = color_orange
                
            else:
                color_2 = color_black
                color_1 = color_orange
                 
 
           
#        color_1 = color_black
#        color_2 = color_orange

       	    leds = drawhorizontalline(leds,0, 0, 4, color_1)
            leds = drawhorizontalline(leds,0, 1, 4, color_1)
            leds = drawhorizontalline(leds,0, 2, 4, color_1)
            leds = drawhorizontalline(leds,0, 3, 4, color_1)
            leds = drawhorizontalline(leds,0, 4, 4, color_2)
            leds = drawhorizontalline(leds,0, 5, 4, color_2)
            leds = drawhorizontalline(leds,0, 6, 4, color_2)
            leds = drawhorizontalline(leds,0, 7, 4, color_2)


            leds = drawhorizontalline(leds,4, 0, 4, color_2)
            leds = drawhorizontalline(leds,4, 1, 4, color_2)
            leds = drawhorizontalline(leds,4, 2, 4, color_2)
            leds = drawhorizontalline(leds,4, 3, 4, color_2)
            leds = drawhorizontalline(leds,4, 4, 4, color_1)
            leds = drawhorizontalline(leds,4, 5, 4, color_1)
            leds = drawhorizontalline(leds,4, 6, 4, color_1)
            leds = drawhorizontalline(leds,4, 7, 4, color_1)

            leds = drawhorizontalline(leds,8, 0, 4, color_1)
            leds = drawhorizontalline(leds,8, 1, 4, color_1)
            leds = drawhorizontalline(leds,8, 2, 4, color_1)
            leds = drawhorizontalline(leds,8, 3, 4, color_1)
            leds = drawhorizontalline(leds,8, 4, 4, color_2)
            leds = drawhorizontalline(leds,8, 5, 4, color_2)
            leds = drawhorizontalline(leds,8, 6, 4, color_2)
            leds = drawhorizontalline(leds,8, 7, 4, color_2)
	
	
            leds = drawhorizontalline(leds,12, 0, 4, color_2)
            leds = drawhorizontalline(leds,12, 1, 4, color_2)
            leds = drawhorizontalline(leds,12, 2, 4, color_2)
            leds = drawhorizontalline(leds,12, 3, 4, color_2)
            leds = drawhorizontalline(leds,12, 4, 4, color_1)
            leds = drawhorizontalline(leds,12, 5, 4, color_1)
            leds = drawhorizontalline(leds,12, 6, 4, color_1)
            leds = drawhorizontalline(leds,12, 7, 4, color_1)
	
            leds = drawhorizontalline(leds,16, 0, 4, color_1)
            leds = drawhorizontalline(leds,16, 1, 4, color_1)
            leds = drawhorizontalline(leds,16, 2, 4, color_1)
            leds = drawhorizontalline(leds,16, 3, 4, color_1)
            leds = drawhorizontalline(leds,16, 4, 4, color_2)
            leds = drawhorizontalline(leds,16, 5, 4, color_2)
            leds = drawhorizontalline(leds,16, 6, 4, color_2)
            leds = drawhorizontalline(leds,16, 7, 4, color_2)
	
            leds = drawhorizontalline(leds,20, 0, 4, color_2)
            leds = drawhorizontalline(leds,20, 1, 4, color_2)
            leds = drawhorizontalline(leds,20, 2, 4, color_2)
            leds = drawhorizontalline(leds,20, 3, 4, color_2)
            leds = drawhorizontalline(leds,20, 4, 4, color_1)
            leds = drawhorizontalline(leds,20, 5, 4, color_1)
            leds = drawhorizontalline(leds,20, 6, 4, color_1)
            leds = drawhorizontalline(leds,20, 7, 4, color_1)
	
            leds = drawhorizontalline(leds,24, 0, 4, color_1)
            leds = drawhorizontalline(leds,24, 1, 4, color_1)
            leds = drawhorizontalline(leds,24, 2, 4, color_1)
            leds = drawhorizontalline(leds,24, 3, 4, color_1)
            leds = drawhorizontalline(leds,24, 4, 4, color_2)
            leds = drawhorizontalline(leds,24, 5, 4, color_2)
            leds = drawhorizontalline(leds,24, 6, 4, color_2)
            leds = drawhorizontalline(leds,24, 7, 4, color_2)
	
            leds = drawhorizontalline(leds,28, 0, 4, color_2)
            leds = drawhorizontalline(leds,28, 1, 4, color_2)
            leds = drawhorizontalline(leds,28, 2, 4, color_2)
            leds = drawhorizontalline(leds,28, 3, 4, color_2)
            leds = drawhorizontalline(leds,28, 4, 4, color_1)
            leds = drawhorizontalline(leds,28, 5, 4, color_1)
            leds = drawhorizontalline(leds,28, 6, 4, color_1)
            leds = drawhorizontalline(leds,28, 7, 4, color_1)
            write2812(spi, leds)
            time.sleep(0.5)




                




    def test_turn_light_left(spi):
        print("turn light lefT")
        leds = [color_black]*8*64

        #print(leds)
        write2812(spi, leds)


        leds = drawhorizontalline(leds, 3, 4, 11, color_orange)   
        leds = drawhorizontalline(leds, 3, 5, 11, color_orange)   
        leds = drawhorizontalline(leds, 3, 6, 11, color_orange)   

        leds = drawverticalline(leds, 15, 0, 8, color_red)   
        leds = drawverticalline(leds, 18, 1, 5, color_blue)   


        #print(leds)

        write2812(spi, leds)

        time.sleep(2)


        leds = shift_left(leds)
        #print(leds)
        write2812(spi, leds)
        time.sleep(1)

        leds = shift_left(leds)
        write2812(spi, leds)
        time.sleep(0.05)

        leds = shift_left(leds)
        write2812(spi, leds)
        time.sleep(0.05)


        leds = shift_left(leds)
        write2812(spi, leds)
        time.sleep(0.05)

        leds = shift_left(leds)
        write2812(spi, leds)
        time.sleep(0.05)


        for i in range(4):
            leds = shift_left(leds)
            write2812(spi, leds) 
            time.sleep(0.1)

        time.sleep(1)

        for i in range(5):
            leds = shift_right(leds)
            write2812(spi, leds) 
            time.sleep(0.2)


        leds = clear( leds)
        write2812(spi, leds)
        time.sleep(1)
        



        leds = draw_let_p(leds, 0, 0, color_yellow)
        leds = draw_let_a(leds, 6, 0, color_yellow)
        leds = draw_let_r(leds, 12, 0, color_yellow)

        leds = draw_let_b(leds, 18, 0, color_yellow)

        leds = draw_let_i(leds, 22, 0, color_yellow)

        leds = draw_let_n(leds, 27, 0, color_yellow)

        write2812(spi, leds)


        time.sleep(1) 

        t = 0     
        while True:
            t = t +1.1
            leds2 = sine(leds, t)
            write2812(spi, leds2)
            #time.sleep(.05)






    def test_fixed(spi):
=======
    def test_fixed(spi, nLED):
>>>>>>> 84ab35216413a008fd16b27afb491a6d4d4c123f
        #write fixed pattern for 8 LEDs
        #This will send the following colors:
        #   Red, Green, Blue,
        #   Purple, Cyan, Yellow,
<<<<<<< HEAD
        #   Black(off), White 
        write2812(spi, [
			[10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],

                        [10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],

                        [10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],

                        [10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],

                        [10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],

                        [10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],

                        [10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],

                        [10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],

                        [10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],


                        [10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],

                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],


                        [10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],

                        [10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [0,10,0], [0,0,10],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0], [10,10,10],
                        [10,0,0], [0,100,0], [0,0,100],
                        [0,10,10], [10,0,10], [10,10,0],
                        [10,0,0]


			])
=======
        #   Black(off), White
        leds = [[0,0,0]]*nLED
        
        for i in range nLED: 
            leds[i][0] = rand(255)
            leds[i][1] = rand(255)
            leds[i][2] = rand(255)
        
        write2812(spi, leds)
        
>>>>>>> 84ab35216413a008fd16b27afb491a6d4d4c123f
    def test_off(spi, nLED=8):
        #switch all nLED chips OFF.
        write2812(spi, [[0,0,0]]*nLED)
    def usage():
        print("usage: ...")
    
    def usage():
        print("usage: python ws2812-spi.py [-t] [-n] [-c], where -t or --test - run test with first 8 diodes in different colors, -c + -n - bright up first n diodes with given color, for example python ws2812.py -n 3 -c [100,100,0] "
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:c:t:l", ["help", "color=", "test", "lightturnleft"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err)) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    color=None
    nLED=8
    doTest=False
    print("2") 
    print(opts)
    testTurnLightLeft = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-c", "--color"):
            color=a
        elif o in ("-n", "--nLED"):
            nLED=int(a)
        elif o in ("-t", "--test"):
            doTest=True
<<<<<<< HEAD
        elif o in ("-l", "--lightturnleft"):
            print("1")
            testTurnLightLeft = True
=======
>>>>>>> 84ab35216413a008fd16b27afb491a6d4d4c123f
        else:
            assert False, "unhandled option"

    spi = spidev.SpiDev()
    spi.open(0,0)

    if color!=None:
        write2812(spi, eval(color)*nLED)
<<<<<<< HEAD
        print(color) 
        print(eval(color))
=======
           
>>>>>>> 84ab35216413a008fd16b27afb491a6d4d4c123f
    elif doTest:
        test_fixed(spi)
    elif testTurnLightLeft:
        test_turn_light_left(spi)
        #taxi_mode(spi)
    else:
        usage()


