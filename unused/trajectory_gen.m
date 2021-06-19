%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Support code for generation of desired trajectories for algorithmic music
% generation system. 
% Author: Stefan Ehrlich <stefan.ehrlich@tum.de>
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

% sweep from sad to happy
input.val = linspace(0,1,40)
input.aro = linspace(0,1,40)

save('sad_to_happy','input')

% sweep from sad to happy
input.val = linspace(1,0,40)
input.aro = linspace(1,0,40)

save('happy_to_sad','input')

% sweep from sad to happy
val1 = linspace(1,0,15)
aro1 = linspace(0,1,15)

val2 = linspace(0,1,10)
aro2 = linspace(1,0.95,10)

val3 = linspace(1,0,15)
aro3 = linspace(0.95,0,15)


input.val = [val1,val2,val3];
input.aro = [aro1,aro2,aro3];

input.val = smooth(input.val,5)
input.aro = smooth(input.aro,5)

save('seeWhatHappens','input')
