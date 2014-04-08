% fftex.m
% Example for computing FFT on a signal
 
%maxNumCompThreads(1)          % Limit the number of CPUs used to 4
Fs = 1000;                    % Sampling frequency
T = 1/Fs;                     % Sample time
L = 10;                     % Length of signal
t = (0:L-1)*T;                % Time vector
% Sum of a 50 Hz sinusoid and a 120 Hz sinusoid
x = 0.7*sin(2*pi*50*t) + sin(2*pi*120*t)
disp(x)
