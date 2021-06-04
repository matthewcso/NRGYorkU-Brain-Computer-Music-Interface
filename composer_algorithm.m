%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Automatic music generation algorithm (Composer)
% Author: Stefan Ehrlich <stefan.ehrlich@tum.de>
% Last revised: September 2013
% 
% Code: Algorithmic Music Generation System used in closed loop affective 
% music BCI.
%
% Upon use, please cite / credit:
%
% Ehrlich, S. K., Agres, K. R., Guan, C., & Cheng, G. (2019). A closed-loop, 
% music-based brain-computer interface for emotion mediation. PloS one, 
% 14(3), e0213516. 
% URL/DOI: https://doi.org/10.1371/journal.pone.0213516
%
%
% MIT License
% 
% Copyright (c) 2021 Stefan Ehrlich
% 
% Permission is hereby granted, free of charge, to any person obtaining a copy
% of this software and associated documentation files (the "Software"), to deal
% in the Software without restriction, including without limitation the rights
% to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
% copies of the Software, and to permit persons to whom the Software is
% furnished to do so, subject to the following conditions:
% 
% The above copyright notice and this permission notice shall be included in all
% copies or substantial portions of the Software.
% 
% THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
% IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
% FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
% AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
% LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
% OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
% SOFTWARE.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


function composer_algorithm

% load trajectory
load trj_contentment_anger_happy_sad.mat

% load background image for visualization
img = imread('russel.png');


figure(1)
axis([-0.1 1.1 -0.1 1.1])
image('CData',img,'XData',[-0.1 1.1],'YData',[1.1 -0.1])
pause(5)

fprintf('ComposerState: Composer started\n');


info = mididevinfo;

%% open midi ports and set midi-settings

device = mididevice(0); % set here the midi port you want to push the data into
% port 0: OS internal virtual piano 

viz = 1; % visualize trajectory or just play music

%% defines variables

%load 'chordlist.txt' % chordlist contains all chords belonging to the C-major scale

% chordlist
chordlist =     [60,  64,  55,  59;
                62,  65,  57,  60;
                64,  55,  59,  62;
                60,  65,  57,  64;
                55,  59,  62,  65;
                57,  60,  64,  55;
                59,  62,  65,  57];

% set lydian mode
modeset(1,:,1) = chordlist(4,:);
modeset(2,:,1) = chordlist(7,:);
modeset(3,:,1) = chordlist(1,:);
modeset(4,:,1) = chordlist(4,:);

% set ionian mode
modeset(1,:,2) = chordlist(1,:);
modeset(2,:,2) = chordlist(4,:);
modeset(3,:,2) = chordlist(5,:);
modeset(4,:,2) = chordlist(1,:);

% set mixolydian mode
modeset(1,:,3) = chordlist(5,:);
modeset(2,:,3) = chordlist(1,:);
modeset(3,:,3) = chordlist(2,:);
modeset(4,:,3) = chordlist(5,:);

% set dorian mode
modeset(1,:,4) = chordlist(2,:);
modeset(2,:,4) = chordlist(5,:);
modeset(3,:,4) = chordlist(6,:);
modeset(4,:,4) = chordlist(2,:);

% set aeolian mode
modeset(1,:,5) = chordlist(6,:);
modeset(2,:,5) = chordlist(2,:);
modeset(3,:,5) = chordlist(3,:);
modeset(4,:,5) = chordlist(6,:);

% set phrygian mode
modeset(1,:,6) = chordlist(3,:);
modeset(2,:,6) = chordlist(6,:);
modeset(3,:,6) = chordlist(7,:);
modeset(4,:,6) = chordlist(3,:);

% set locrian mode
modeset(1,:,7) = chordlist(7,:);
modeset(2,:,7) = chordlist(3,:);
modeset(3,:,7) = chordlist(4,:);
modeset(4,:,7) = chordlist(7,:);


modeset = modeset-3; % pitch-down the complete modeset with 3 half-tones

low_loudness = 50;          % set minimal loudness



idx = 1;
for ii=1:length(input.val)/4
      
        valence = input.val(idx);
        arousal = input.aro(idx);

        % update musical parameters
        mode = 7-round(valence*6); % set harmonic mode based on valence
        roughness = 1-arousal;      % set rhythmic roughness based on arousal
        velocity = arousal;         % set tempo based on arousal
        voicing = valence;          % set voicing based on valence
        loudness = (round(arousal*10))/10*40+60;   % set maximal loudness based on arousal

        for chord = 1:4

            valence = input.val(idx);
            arousal = input.aro(idx);
            
            disp(strcat('VAL: ',num2str(valence,'%.2f'),' - ARO: ',num2str(arousal,'%.2f')))
            
            if viz
            figure(1)
            axis([-0.1 1.1 -0.1 1.1])
            image('CData',img,'XData',[-0.1 1.1],'YData',[1.1 -0.1])
            hold on
            plot(input.val(1:idx),input.aro(1:idx),'bo-','LineWidth',2.5)
            hold off
            end

            
            roughness = 1-arousal;      % set rhythmic roughness based on arousal
            velocity = arousal;         % set tempo based on arousal
            voicing = valence;          % set voicing based on valence
            loudness = (round(arousal*10))/10*40+60;   % set maximal loudness based on arousal
            
            % create roughness
            activate1 = rand(1,8);
            for i=1:8
                if(activate1(i) < roughness)
                    activate1(i) = 0;
                else
                    activate1(i) = 1;
                end
            end
            
            % create roughness
            activate2 = rand(1,8);
            for i=1:8
                if(activate2(i) < roughness)
                    activate2(i) = 0;
                else
                    activate2(i) = 1;
                end
            end
            
            bright = rand(1,6);
            for i=1:6
                if(voicing < 0.5)
                    if(bright(i) > voicing*2)
                        bright(i) = -1;
                    else
                        bright(i) = 0;
                    end
                else
                    if(bright(i) < (voicing-0.5)*2)
                        bright(i) = 1;
                    else
                        bright(i) = 0;
                    end
                end
            end
            
            % Shut all down
            msg = midimsg('AllSoundOff',1); midisend(device,msg);
            msg = midimsg('AllSoundOff',2); midisend(device,msg);
            msg = midimsg('AllSoundOff',3); midisend(device,msg);
            
           
            % randomly create tone
            note = midimsg('NoteOn',1,modeset(chord,1,mode)+bright(1)*12,randi([low_loudness,loudness]));
            midisend(device,note)
            note = midimsg('NoteOn',2,modeset(chord,1,mode)+bright(1)*12,randi([low_loudness,loudness]));
            midisend(device,note)
            
            note = midimsg('NoteOn',1,modeset(chord,2,mode)+bright(2)*12, randi([low_loudness,loudness]));
            midisend(device,note)
            note = midimsg('NoteOn',2, modeset(chord,2,mode)+bright(2)*12, randi([low_loudness,loudness]));
            midisend(device,note)

            note = midimsg('NoteOn',1,modeset(chord,3,mode)+bright(3)*12, randi([low_loudness,loudness]));
            midisend(device,note)
            note = midimsg('NoteOn',2,modeset(chord,3,mode)+bright(3)*12, randi([low_loudness,loudness]));
            midisend(device,note)

          
            if(voicing > 0.5)
                note = midimsg('NoteOn',3,modeset(chord,1,mode)-12, randi([low_loudness,loudness]));
                midisend(device,note)
            else
                note = midimsg('NoteOn',3,modeset(chord,1,mode)-24, randi([low_loudness,loudness]));
                midisend(device,note)
            end
            
            for tone=1:8
                if(activate1(tone) == 1)
                    note = midimsg('NoteOn',1,modeset(chord,1,mode)+bright(5)*12, randi([low_loudness,loudness]));
                    midisend(device,note)
                end
                if(activate2(tone) == 1)
                    note = midimsg('NoteOn',1,modeset(chord,randi([2,3]),mode)+bright(6)*12, randi([low_loudness,loudness]));
                    midisend(device,note)
                end
                pause(0.3-velocity*0.15);
            end
            idx = idx+1;
        end
            % Shut all down
            msg = midimsg('AllSoundOff',1); midisend(device,msg);
            msg = midimsg('AllSoundOff',2); midisend(device,msg);
            msg = midimsg('AllSoundOff',3); midisend(device,msg);
    end

fprintf('ComposerState: Composer stopped\n');

end






 




