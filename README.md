# fireflies

A simple agent-based model of firefly motion and firing implemented in Python. Fireflies freely diffuse in a 3D space, with a low probability of lighting up at any given time step. The longer an individual bug hasn’t lit up, the higher it’s probability of lighting, but in general lighting probabilities per fly remain low. 

Flies that are within a set radius of a firing firefly light up with elevated probabilities. Once a fly has lit up, there is a brief recharge period in which it cannot light up again. Together, these properties create waves of lighting and darkness.

Plotting, diffusion, and radius calculation code adapted from code I have previously written during a rotation in the Johnson lab at Johns Hopkins University, where we applied diffusion models to transcription factor behavior. 


![grab-landing-page](https://github.com/andrew-bortvin/fireflies/blob/main/ff_trimmed.gif)


Repository includes firefly.py, which is the code for this simulation, and 13_ff.mp4, which is a representative movie generated by the simulation.
