clear a
a = arduino('com3', 'uno');
redLED = ('D9');
greenLED = ('D8');
vibrationSensor = ('D5');

vv= zeros(1,200);
for i = 1:200
% v(i)=readVoltage(a,'A0')
vv(i)=readDigitalPin(a,vibrationSensor);
end

if sum(vv==1)>10
    recObj=audiorecorder;
recDuration = 5 %5 sec recording time
disp("Begin speaking.")
recordblocking(recObj,recDuration);
disp("End of recording.")
play(recObj)
y = getaudiodata(recObj);
figure();
plot(y);
fs = 12000;
filename='voicerec.wav';
audiowrite(filename,y,fs);
%% recording analysis
scream = ('voicerec.wav');
[y,Fs] = audioread(scream);
%sound(y,Fs)
%loaded correctly heard scream
% taken out for my own sanity as I try this
Fs2 = Fs/2;
Ts=1/Fs2;
ts = 0:Ts:1;
dt=1/Fs2; % Nyquist frequency
y2 = y(:,1); %all of the rows in the first column
t=0:dt:(length(y)*dt)-dt;
figure;
plot(t,y)
title('Time Domain of Sound Sample')
xlabel('Time')
ylabel('Amplitude')

%% Measure the SPL of Audio Signal - should be done now :)
scream = 'voicerec.wav';
scope = timescope('SampleRate',Fs,'TimeSpanSource', 'property', 'YLimits', [20 120], 'AxesScaling','auto','ChannelNames',{'LAF','LAeq','LApeak','LAmax'});
sm = splMeter('TimeWeighting','Fast','FrequencyWeighting','A-weighting','SampleRate',Fs,'TimeInterval',2,'CalibrationFactor',1);
x=audioread(scream);
[LAF,LAeq,LApeak,LAmax]=sm(x(:,1));
scope([LAF,LAeq,LApeak,LAmax]);
M = max(LAF);%LAF is the entire plot used this value to get dB
DB = ['Maximum Decibels of this sample is ', num2str(M) ,' dB.'];
disp(DB)
if M>=85 %changed to be 85 for shouting
    disp('Output is not acceptable: Red :(')
else 
    disp('Output is acceptable: Green :)')
end

%old spectrogram section removed since it was not right
%% Spectrogram
scream = ('voicerec.wav');
[y,Fs] = audioread(scream);
Fs2 = Fs/2;
Ts=1/Fs2;
ts = 0:Ts:1;
dt=1/Fs2; % Nyquist frequency
win = 1024;
overlap = win/2;
%{tried the window and overlap values used in the lab 6 from 358}%
figure()
spectrogram(y(:,1),win,overlap,0:Fs/2, Fs,'yaxis')%unsure if this
%clim should be able to change the limits of the spectrogram color map
%would be helpful for easier analysis probably
%[S,F,T] = spectrogram(y(:,1), win, overlap, [],Fs);
% pks = findpeaks(screamfft); %next two lines are trying to figure out 
%the max frequency of the sample
% k = max(pks);
%% plot the signal spectrum
% spectral analysis
winlen = length(y);
win = blackman(winlen, 'periodic');
nfft = round(2*winlen);
[PS, f] = periodogram(y, win, nfft, Fs, 'power');
X = 10*log10(PS);
figure(2)
semilogx(f, X, 'r')
xlim([0 max(f)])
grid on
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14)
title('Spectrum of the signal')
xlabel('Frequency, Hz')
ylabel('Magnitude, dBV^2')

%% plot the signal spectrogram
% time-frequency analysis
winlen = 1024;
win = blackman(winlen, 'periodic');
hop = round(winlen/8);
nfft = round(2*winlen);
[~, F, T, STPS] = spectrogram(y, win, winlen-hop, nfft, Fs, 'power');
STPS = 10*log10(STPS);

% plot the spectrogram
figure;
surf(T, F, STPS)
shading interp
axis tight
box on
view(0, 90)
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14)
xlabel('Time, s')
ylabel('Frequency, Hz')
title('Spectrogram of the signal')

[~, cmax] = clim;
clim([max(-120, cmax-90), cmax])

hClbr = colorbar;
set(hClbr, 'FontName', 'Times New Roman', 'FontSize', 14)
ylabel(hClbr, 'Magnitude, dBV^2')
%%
figure();
[f0,loc]=pitch(y,Fs);
p1 = mean(f0);
P = ['The maximum pitch of this sample is ', num2str(p1),' Hz.'];
disp(P)
plot(loc,f0) 
xlabel('Location')
ylabel('Frequency (Hz)')
title('Pitch Estimate')
if mean(f0)>=255
    disp('Output is unacceptable: Red :(')
    for i = 0:5
    writeDigitalPin(a, redLED, 1);

    pause(5);

    writeDigitalPin(a, redLED, 0);

    pause(0.5);
    end
else 
    disp('Output is acceptable: Green :)')
    for i = 0:5
    writeDigitalPin(a, greenLED, 1);

    pause(5);

    writeDigitalPin(a, greenLED, 0);

    pause(0.5);
    end
end
end
%%

%%

%% recording using matlab



