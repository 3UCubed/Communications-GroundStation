# Communications

This is the code for reading in the files created by GNU radio. This code does not demodulate a revieved packet. 

gnuCode.cpp: this just generates the float to binary conversion

gnuCodeExtra.cpp: this generates the float to binary and splits the components including sign bit, exponent, and the mantissa

gnuCodeExtra2.cpp: //this generates the index and the float number into a file to be read by python code

gnuCodeExtra2.py: this is to plot the different points read from the cpp code

1kSig.bin: is the binary file from a 1k signal generated in GNU Radio Companion

data.csv: gives us the index and the value of that index on the wave. Output of gnuCodeExtra2.cpp, to be read by gnuCodeExtra2.py

GFSK_demod.bin: output of GFSK_Mod_DeMod.grc

GFSK_Mod_DeMod.grc: takes a wave and puts it through a GFSK modulating block and the corresponding demodulating block

sine_wave_generator.grc: generates a consistent 1k sine wave in GNU radio companion.
