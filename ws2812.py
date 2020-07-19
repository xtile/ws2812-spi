#!/usr/bin/python

import time
import math
import spidev
import time
import getopt
import sys



NumpyImported=False
try:
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

def i( x,y):
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



class Matrix2812:

    color_light_green = [30, 30, 0]
    color_orange= [20, 90, 0]
    color_yellow = [20,60, 0] 
    color_black  = [0,0,0]
    color_pink = [0, 30, 30]
    color_red = [0, 30, 0]
    color_green = [30, 0, 0]
    color_blue = [0, 0, 30]
    spi = None
    leds = None
    _nLEDs = 0


 



    def __init__(this, nLEDs = 8):
        this.spi = spidev.SpiDev()
        this.spi.open(0,0)
        #leds =  
        this.leds = [this.color_black]*nLEDs
        this._nLEDs = nLEDs

    def getLeds(this):
        return this.leds


    def write2812_numpy8(this):
        data = this.leds
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
        this.spi.xfer(tx.tolist(), int(8/1.25e-6))
        #spi.xfer(tx.tolist(), int(8e6))
    
    def write2812_numpy4(this, data = None):
        #print spi
        #print("numpy4")
        if data is None:
             data = this.leds
        d=numpy.array(data).ravel()
        print(data)
        tx=numpy.zeros(len(d)*4, dtype=numpy.uint8)
        for ibit in range(4):
            #print ibit
            #print ((d>>(2*ibit))&1), ((d>>(2*ibit+1))&1)
            tx[3-ibit::4]=((d>>(2*ibit+1))&1)*0x60 + ((d>>(2*ibit+0))&1)*0x06 +  0x88
            #print(tx)
            #print [hex(v) for v in tx]
        #print [hex(v) for v in tx]
        #not working on zero  spi.xfer3(tx.tolist(), int(4/1.25e-6)) #works, on Zero (initially didn't?)
        #not working on zero spi.xfer3(tx.tolist(), int(4/1.20e-6))  #works, no flashes on Zero, Works on Raspberry 3
        #not working on zero spi.xfer3(tx.tolist(), int(4/1.15e-6))  #works, no flashes on Zero
        #spi.xfer3(tx.tolist(), int(4/1.05e-6))  #works, no flashes on Zero
        this.spi.xfer3(tx.tolist(), int(4/.95e-6))  #works, no flashes on Zero
        #spi.xfer(tx.tolist(), int(4/.90e-6))  #works, no flashes on Zero
        #spi.xfer(tx.tolist(), int(4/.85e-6))  #doesn't work (first 4 LEDS work, others have flashing colors)
        #spi.xfer(tx.tolist(), int(4/.65e-6))  #doesn't work on Zero; Works on Raspberry 3
        #spi.xfer(tx.tolist(), int(4/.55e-6))  #doesn't work on Zero; Works on Raspberry 3
        #spi.xfer(tx.tolist(), int(4/.50e-6))  #doesn't work on Zero; Doesn't work on Raspberry 3 (bright colors)
        #spi.xfer(tx.tolist(), int(4/.45e-6))  #doesn't work on Zero; Doesn't work on Raspberry 3
        #spi.xfer(tx.tolist(), int(8e6))

    def write2812_pylist8(this):
        data = this.leds
        tx=[]
        for rgb in data:
            for byte in rgb: 
                for ibit in range(7,-1,-1):
                    tx.append(((byte>>ibit)&1)*0x78 + 0x80)
        this.spi.xfer(tx, int(8/1.25e-6))

    def write2812_pylist4(this,  data):
        data = this.leds
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
        this.spi.xfer3(tx, int(4/1.05e-6))


    if NumpyImported:
        write2812=write2812_numpy4
    else:
        write2812=write2812_pylist4  
        
        
    def i(this, x,y):
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


    def drawverticalline(this,  x, y, len, color):
        for j in range (len): 
            this.leds[this.i(x, y+j)] = color #leds[i(0,0)] #color
        #print("linever")
        #return leds


    def drawhorizontalline(this,  x, y, len, color):
        for j in range (len): 
            this.leds[this.i(x+j, y)] = color #leds[i(0,0)] #color
        #print("linehor")
        #return leds
    
    def clear(this ):
       this.leds = [this.color_black]*8*64
       #return leds

       #return leds

    def drawrect(this,  x,y, width, height, color):
        for j in range (width):
            this.drawverticalline( x+j, y, height, color)
        
        #return leds          


    def draw_let_a(this,  x, y, color):
        
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

        this.leds[i(x+1,y+4)] = color
        #leds[i(x+2,y+4)] = color
        this.leds[i(x+2,y+4)] = color
        this.leds[i(x+4,y+4)] = color

        this.leds[i(x+0,y+3)] = color
        this.leds[i(x+4,y+3)] = color
        this.leds[i(x+3,y+3)] = color

        this.leds[i(x+0,y+2)] = color
        this.leds[i(x+4,y+2)] = color

        this.leds[i(x+0,y+1)] = color
        this.leds[i(x+3,y+1)] = color
        this.leds[i(x+4,y+1)] = color

        this.leds[i(x+1,y+0)] = color
        #leds[i(x+2,y+0)] = color
        this.leds[i(x+2,y+0)] = color
        this.leds[i(x+4,y+0)] = color

        #return leds

    #i=2


    def draw_let_b(this,  x, y, color):
        
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

        this.leds[i(x,y+7)] = color
        this.leds[i(x,y+6)] = color
        this.leds[i(x,y+5)] = color
        
        this.leds[i(x,y+4)] = color

        this.leds[i(x+2,y+4)] = color
        this.leds[i(x+3,y+4)] = color

        this.leds[i(x,y+3)] = color
        this.leds[i(x+1,y+3)] = color
        this.leds[i(x+4,y+3)] = color
        
        this.leds[i(x,y+2)] = color
        this.leds[i(x+4,y+2)] = color


        this.leds[i(x,y+1)] = color
        this.leds[i(x+1,y+1)] = color
        this.leds[i(x+4,y+1)] = color

        this.leds[i(x+0,y+0)] = color
        this.leds[i(x+2,y+0)] = color
        #leds[i(x+3,y+0)] = color
        this.leds[i(x+3,y+0)] = color

        #return leds

    #i=2



    def draw_let_k(this,  x, y, color):
        
#'''
#x
#x
#x
#x  xx
#x x
#xx
#x x
#x  xx
#'''

        this.leds[i(x,y+7)] = color
        this.leds[i(x,y+6)] = color
        this.leds[i(x,y+5)] = color
        
        this.leds[i(x,y+4)] = color

        this.leds[i(x+4,y+4)] = color
        this.leds[i(x+3,y+4)] = color

        this.leds[i(x,y+3)] = color
        this.leds[i(x+2,y+3)] = color
        
        #this.leds[i(x+4,y+2)] = color
        
        this.leds[i(x,y+2)] = color
        this.leds[i(x+1,y+2)] = color


        this.leds[i(x,y+1)] = color
        this.leds[i(x+2,y+1)] = color
        #this.leds[i(x+4,y+1)] = color

        this.leds[i(x+0,y+0)] = color
        this.leds[i(x+3,y+0)] = color
        #leds[i(x+3,y+0)] = color
        this.leds[i(x+4,y+0)] = color

        #return leds

    #i=2





    def draw_let_c(this,  x, y, color):
        
#'''
#
#
#
# xxxx
#x
#x
#x
# xxxx
#'''

        this.leds[i(x+1,y+4)] = color
        this.leds[i(x+2,y+4)] = color
        this.leds[i(x+3,y+4)] = color
        #leds[i(x+5,y+3)] = color
        this.leds[i(x+4,y+4)] = color

        this.leds[i(x,y+3)] = color

        this.leds[i(x,y+2)] = color

        this.leds[i(x,y+1)] = color

        this.leds[i(x+1,y+0)] = color
        this.leds[i(x+2,y+0)] = color
        this.leds[i(x+3,y+0)] = color
        this.leds[i(x+4,y+0)] = color


        #return leds


    def draw_let_d(this,  x, y, color):
        
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

    def draw_let_n(this,  x, y, color):
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
        this.leds[i(x+0,y+4)] = color
        this.leds[i(x+2,y+4)] = color
        this.leds[i(x+3,y+4)] = color

        this.leds[i(x+0,y+3)] = color
        this.leds[i(x+1,y+3)] = color

        this.leds[i(x+0,y+2)] = color
        this.leds[i(x+0,y+1)] = color
        this.leds[i(x+0,y+0)] = color
        this.leds[i(x+4,y+2)] = color
        this.leds[i(x+4,y+1)] = color
        this.leds[i(x+4,y+0)] = color

        #return leds         


    def draw_let_r(this,  x, y, color):
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
        this.leds[i(x+2,y+4)] = color
        this.leds[i(x+3,y+4)] = color
        this.leds[i(x+4,y+4)] = color

        this.leds[i(x+1,y+3)] = color

        this.leds[i(x+0,y+4)] = color
        this.leds[i(x+0,y+3)] = color
        this.leds[i(x+0,y+2)] = color
        this.leds[i(x+0,y+1)] = color
        this.leds[i(x+0,y+0)] = color

        #return leds         


    def draw_let_i(this,  x, y, color):
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
        this.leds[i(x+2,y+6)] = color
        this.leds[i(x+2,y+4)] = color
        this.leds[i(x+3,y+4)] = color

        this.leds[i(x+2,y+3)] = color

        this.leds[i(x+2,y+2)] = color
        this.leds[i(x+2,y+1)] = color
        this.leds[i(x+2,y+0)] = color

        this.leds[i(x+3,y+0)] = color

        #return leds         


    def draw_let_p(this,  x, y, color):
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
        this.leds[i(x+0,y+7)] = color
        this.leds[i(x+1,y+7)] = color
        this.leds[i(x+2,y+7)] = color
        this.leds[i(x+3,y+7)] = color

        this.leds[i(x+0,y+6)] = color
        this.leds[i(x+4,y+6)] = color

        this.leds[i(x+0,y+5)] = color
        this.leds[i(x+4,y+5)] = color

        this.leds[i(x+0,y+4)] = color
        this.leds[i(x+4,y+4)] = color

        this.leds[i(x+0,y+3)] = color
        this.leds[i(x+1,y+3)] = color
        this.leds[i(x+2,y+3)] = color
        this.leds[i(x+3,y+3)] = color

        this.leds[i(x+0,y+2)] = color

        this.leds[i(x+0,y+1)] = color
        this.leds[i(x+0,y+0)] = color

        #return leds         




    def taxi_mode(this):
        print("taxi_mode")


        #this.leds = [this.color_black]*8*64
        this.clear()


        i = 0
        while True:
            i = i+1
            if i%2: 
                color_1 = this.color_black
                color_2 = this.color_orange
                
            else:
                color_2 = this.color_black
                color_1 = this.color_orange


            
            this.drawrect(0,0,4, 4, color_1)
            this.drawrect(0,4,4, 4, color_2)


            this.drawrect(4,0,4, 4, color_2)
            this.drawrect(4,4,4, 4, color_1)

            this.drawrect(8,0,4, 4, color_1)
            this.drawrect(8,4,4, 4, color_2)
	
	
            this.drawrect(12,0,4, 4, color_2)
            this.drawrect(12,4,4, 4, color_1)
	
            this.drawrect(16,0,4, 4, color_1)
            this.drawrect(16,4,4, 4, color_2)
	
            this.drawrect(20,0,4, 4, color_2)
            this.drawrect(20,4,4, 4, color_1)
	
            this.drawrect(24,0,4, 4, color_1)
            this.drawrect(24,4,4, 4, color_2)
	
            this.drawrect(28,0,4, 4, color_2)
            this.drawrect(28,4,4, 4, color_1)

            this.write2812()
            time.sleep(1.5)


    def sine(this,  t):
       f = round(math.cos(t/10)*100)
       f = (f+100)/2

       print(f)

       a2 = numpy.multiply(this.leds, f/100)

       leds2 = numpy.around(a2, 0).astype(numpy.uint8)

       #this.leds = leds2
       this.write2812(leds2)
       #return leds2 

    def taxi_flash(this ):

        this.drawrect(0,0,32, 8, this.color_orange)


        ind = 0
        t=0
        while True:
           ind = ind + 1
           t = t + 0.5 
           #sine = math.sin(t/10)*50 + 50
           #cosi = math.cos(t/10)*50 + 50
           sine = abs(math.sin(t/10))*math.sin(t/10)*100 
           if sine < 0:
               sine = 0
           cosi = -abs(math.sin(t/10))*math.sin(t/10)*100 
           if cosi < 0:
               cosi = 0
           print(sine)
           tt = numpy.ones((512,1)) #[1]*8*64

           for k in range(8):
               for j in range(32):
                   if (j//4)%2 ==0:
                       if k <4: 
                           tt[i(j,k)] = sine
                       else:
                           tt[i(j,k)] = cosi
                   else:
                       if k <4: 
                           tt[i(j,k)] = cosi
                       else:
                           tt[i(j,k)] = sine
           #tt.reshape(512, 1)                       

           temp = numpy.multiply(this.leds, tt/100)

           temp2 = numpy.around(temp, 0).astype(numpy.uint8)

           this.write2812(temp2)
           #time.sleep(0.01)


    def shift_right(this):
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

            this.leds[ (i+16 -1 - 2*y)] = this.leds[ i] 

        #return leds


    def shift_left(this):
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
            this.leds[i] = this.leds[i+16 -1 - 2*y]
            #else:
            #    leds[i] = leds[i+8]
        #return leds

# enfof Matrix2812


def test_turn_light_left(m):
    print("turn light lefT")
    m.clear()
    #leds = m.getLeds() #[color_black]*8*64


    #print(leds)
    m.write2812( )


     
    m.drawhorizontalline( 3, 4, 11, m.color_orange)   
    m.drawhorizontalline( 3, 5, 11, m.color_orange)   
    m.drawhorizontalline( 3, 6, 11, m.color_orange)   

    m.drawverticalline( 15, 0, 8, m.color_red)
    m.drawverticalline( 18, 1, 5, m.color_blue)



    m.write2812( )

    time.sleep(2)


    m.shift_left()
    #print(leds)
    m.write2812( )
    time.sleep(1)

    m.shift_left()
    m.write2812( )
    time.sleep(0.05)

    m.shift_left()
    m.write2812()
    time.sleep(0.05)


    m.shift_left()
    m.write2812()
    time.sleep(0.05)

    leds = m.shift_left()
    m.write2812()
    time.sleep(0.05)


    for i in range(4):
        leds = m.shift_left()
        m.write2812() 
        time.sleep(0.1)

    time.sleep(1)

    for i in range(5):
        leds = m.shift_right()
        m.write2812() 
        time.sleep(0.2)


    m.clear()
    m.write2812()
    time.sleep(1)
    



    leds = m.draw_let_p( 0, 0, m.color_yellow)
    leds = m.draw_let_a( 6, 0, m.color_yellow)
    leds = m.draw_let_r( 12, 0, m.color_yellow)

    leds = m.draw_let_k( 18, 0, m.color_yellow)

    leds = m.draw_let_i( 22, 0, m.color_yellow)

    leds = m.draw_let_n( 27, 0, m.color_yellow)

    m.write2812( )


    time.sleep(1)

    t = 0
    while True:
        t = t +1.1
        #leds2 = 
        m.sine( t)
        time.sleep(1)
        #m.write2812( )


def test_fixed(m):
#def test_fixed(spi, nLED):
    #write fixed pattern for 64 LEDs

    m.write2812( [
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

    m.write2812( leds)

def test_random(m, nLED):
    #   Black(off), White
    leds = [[0,0,0]]*nLED

    for i in range (nLED):
        leds[i][0] = rand(255)
        leds[i][1] = rand(255)
        leds[i][2] = rand(255)

    m.write2812( leds)



def test_off(m, nLED=8):
    #switch all nLED chips OFF.
    m.write2812( [[0,0,0]]*nLED)


def usage():
    print("usage: python ws2812-spi.py [-t] [-n] [-c], where -t or --test - run test with first 8 diodes in different colors, -c + -n - bright up first n diodes with given color, for example python ws2812.py -n 3 -c [100,100,0] ")

def main():
    print("==========================================================")
    print("WS2812 demo for xPI series")
    print("==========================================================")
    time.sleep(0.1)



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
        elif o in ("-l", "--lightturnleft"):
            print("1")
            testTurnLightLeft = True
        else:
            assert False, "unhandled option"


    m = Matrix2812(8*64)



    if color!=None:
        m.write2812( eval(color)*nLED)
        print(color) 
        print(eval(color))
    elif doTest:
        test_fixed(m)
    elif testTurnLightLeft:
        #test_turn_light_left(m)
        #m.taxi_mode()
        m.taxi_flash()
    else:
        usage()



if __name__ == "__main__":
    main()




