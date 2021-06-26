# Original MATLAB code by Erlich. Translated to Python by Matthew So.
# TODO: Erlich's code doesn't separate music generation and music playing. 
# This is suboptimal because we can't do much in the same thread as the music playing, because it will screw up the music.
# So, I think it's important that we have some sort of threaded approach: music generation writes to a shared list.

def composer_process(valence_mp, arousal_mp, currently_running):
    global currently_playing
    import numpy as np
    import mido
    from time import sleep
    from chordlist import chordlist, modeset
    from random import randrange
    low_loudness = 50       #   % set minimal loudness

    ports = mido.get_output_names()
    print(ports)

    device =  mido.open_output('VirtualMIDISynth #1 0')

    currently_playing = []
    def randi(ls):# might be wrong
        return randrange(ls[0], ls[1]+1)


    def midimsg(t, channel, note=-1, velocity=None):
        global currently_playing
        note = int(note)
        if t == 'NoteOn':
            on_note = mido.Message(type='note_on', channel=channel, \
                note=note, velocity=velocity)
            device.send(on_note)
            currently_playing.append((channel, note, velocity))

        elif t == 'AllSoundOff':
            for channel, note, velocity in currently_playing:
                off_note = mido.Message(type='note_off', channel=channel, \
                    note=note, velocity = velocity)
                device.send(off_note)
            currently_playing=[]


    print('ComposerState: Composer started\n')
    idx = 0

    while True:
        with currently_running.get_lock():
            if not currently_running.value:
                break
        with valence_mp.get_lock():
            valence = valence_mp.value
        with arousal_mp.get_lock():
            arousal = arousal_mp.value
        #valence = input_val[idx]
        #arousal = input_aro[idx]

        # % update musical parameters
        mode = 6-round(valence*6) #; % set harmonic mode based on valence, 7 used to be the magic number but that was indexed +1
        roughness = 1-arousal #;      % set rhythmic roughness based on arousal
        velocity = arousal #;         % set tempo based on arousal
        voicing = valence #;          % set voicing based on valence
        loudness = (round(arousal*10))/10*40+60 #;   % set maximal loudness based on arousal
        for chord in range(4):
            with currently_running.get_lock():
                if not currently_running.value:
                    break
            with valence_mp.get_lock():
                valence = valence_mp.value
            with arousal_mp.get_lock():
                arousal = arousal_mp.value
    #        print('VAL: '+ str(round(valence,2)) + ' - ARO: ' + str(round(arousal,2)))
            
    #        if viz:
    #            clear_output(wait=True)

    #            plt.scatter(valence, arousal)
    #            plt.pause(0.00001) 
    #            plt.show()
                

            roughness = 1-arousal #;      % set rhythmic roughness based on arousal
            velocity = arousal #;         % set tempo based on arousal
            voicing = valence #;          % set voicing based on valence
            loudness = (round(arousal*10))/10*40+60 #;   % set maximal loudness based on arousal
                
            # % create roughness
            activate1 = np.random.random(8)
            for i in range(8):
                if(activate1[i] < roughness):
                    activate1[i] = 0
                else:
                    activate1[i] = 1

                
            #    % create roughness
            activate2 = np.random.random(8)
            for i in range(8):
                if(activate2[i] < roughness):
                    activate2[i] = 0
                else:
                    activate2[i] = 1           
            
                
            bright = np.random.random(6)
            for i in range(6):
                if(voicing < 0.5):
                    if(bright[i] > voicing*2):
                        bright[i] = -1
                    else:
                        bright[i] = 0
                else:
                    if(bright[i] < (voicing-0.5)*2):
                        bright[i] = 1
                    else:
                        bright[i] = 0

                
                # % Shut all down
                msg = midimsg('AllSoundOff',0)
                msg = midimsg('AllSoundOff',1)
                msg = midimsg('AllSoundOff',2)
                
            
                # % randomly create tone
                note = midimsg('NoteOn',0,modeset[chord,0,mode]+bright[0]*12,randi([low_loudness,loudness]))
                note = midimsg('NoteOn',1,modeset[chord,0,mode]+bright[0]*12,randi([low_loudness,loudness]))
                
                note = midimsg('NoteOn',0,modeset[chord,1,mode]+bright[1]*12, randi([low_loudness,loudness]))
                note = midimsg('NoteOn',1, modeset[chord,1,mode]+bright[1]*12, randi([low_loudness,loudness]))

                note = midimsg('NoteOn',0,modeset[chord,2,mode]+bright[2]*12, randi([low_loudness,loudness]))
                note = midimsg('NoteOn',1,modeset[chord,2,mode]+bright[2]*12, randi([low_loudness,loudness]))


            
            if(voicing > 0.5):
                note = midimsg('NoteOn',2,modeset[chord,0,mode]-12, randi([low_loudness,loudness]))
            else:

                note = midimsg('NoteOn',2,modeset[chord,0,mode]-24, randi([low_loudness,loudness]))
            
            for tone in range(8):
                if(activate1[tone] == 1):
                    note = midimsg('NoteOn',0,modeset[chord,0,mode]+bright[4]*12, randi([low_loudness,loudness]));

                if(activate2[tone] == 1):
                    note = midimsg('NoteOn',0,modeset[chord,randi([1,2]),mode]+bright[5]*12, randi([low_loudness,loudness]));
                sleep(0.3-velocity*0.15)

            idx = idx+1
            #   % Shut all down
            msg = midimsg('AllSoundOff',0)
            msg = midimsg('AllSoundOff',1)
            msg = midimsg('AllSoundOff',2)


    print('ComposerState: Composer stopped\n')
