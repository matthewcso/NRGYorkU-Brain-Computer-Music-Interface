import numpy as np
# %%
# define variables

# %load 'chordlist.txt' % chordlist contains all chords belonging to the C-major scale

# % chordlist

chordlist = [[60,  64,  55,  59],
             [62,  65,  57,  60],
             [64,  55,  59,  62],
             [60,  65,  57,  64],
             [55,  59,  62,  65],
             [57,  60,  64,  55],
             [59,  62,  65,  57]]

chordlist = np.asarray(chordlist)


# %%

modeset = np.zeros([4,4,7])
# % set lydian mode
modeset[0,:,0] = chordlist[3,:]
modeset[1,:,0] = chordlist[6,:]
modeset[2,:,0] = chordlist[0,:]
modeset[3,:,0] = chordlist[3,:]

# % set ionian mode
modeset[0,:,1] = chordlist[0,:]
modeset[1,:,1] = chordlist[3,:]
modeset[2,:,1] = chordlist[4,:]
modeset[3,:,1] = chordlist[0,:]

#% set mixolydian mode
modeset[0,:,2] = chordlist[4,:]
modeset[1,:,2] = chordlist[0,:]
modeset[2,:,2] = chordlist[1,:]
modeset[3,:,2] = chordlist[4,:]

#% set dorian mode
modeset[0,:,3] = chordlist[1,:]
modeset[1,:,3] = chordlist[4,:]
modeset[2,:,3] = chordlist[5,:]
modeset[3,:,3] = chordlist[1,:]

# % set aeolian mode
modeset[0,:,4] = chordlist[5,:]
modeset[1,:,4] = chordlist[1,:]
modeset[2,:,4] = chordlist[2,:]
modeset[3,:,4] = chordlist[5,:]

# % set phrygian mode
modeset[0,:,5] = chordlist[2,:]
modeset[1,:,5] = chordlist[5,:]
modeset[2,:,5] = chordlist[6,:]
modeset[3,:,5] = chordlist[2,:]

# % set locrian mode
modeset[0,:,6] = chordlist[6,:]
modeset[1,:,6] = chordlist[2,:]
modeset[2,:,6] = chordlist[3,:]
modeset[3,:,6] = chordlist[6,:]


modeset = modeset-3 # % pitch-down the complete modeset with 3 half-tones

modeset = modeset.astype('int32')

print('Modeset, similar to MATLAB print statement for debugging')
for i in range(7):
    print(modeset[:, :, i])