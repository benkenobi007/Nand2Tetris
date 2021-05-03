// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

//No. of words in screen memory map = (256*512)/16
@8192
D=A

@numScrWords
M=D

(LOOP)

    @i
    M=0

    @SCREEN
    D=A

    @scrAddr
    M=D
    
    @KBD
    D=M
    
    @WHITE
    D;JEQ

    (BLACK)
        // i == maxNumWords
        @i
        D=M

        @numScrWords
        D=D-M

        @END
        D;JGE

        // Colour the word black
        @i
        D=M

        @scrAddr
        A=D+M
        M=-1

        //i++
        @i
        M=M+1

        @BLACK
        0; JMP

    (WHITE)
        // i == maxNumWords
        @i
        D=M

        @numScrWords
        D=D-M

        @END
        D;JGE

        // Colour the word white
        @i
        D=M

        @scrAddr
        A=D+M
        M=0

        //i++
        @i
        M=M+1

        @WHITE
        0; JMP

    (END)
        @LOOP
        0;JMP