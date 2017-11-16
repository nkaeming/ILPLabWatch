% Small wrapper that plots data returned by importLabwatch
%
clear all 
close all

%% read data from exported text file
filename1 = 'getLogHum.txt';
[date_hum, hum] = importLabwatchData(filename1);

% Select data (should not be necessary)
ixh_ = hum > 28 & hum < 40;
date_hum = date_hum(ixh_);
hum = hum(ixh_);

%% Plot data
figure(1)
plot(date_hum, hum,'.')
hold off
grid on
legend({'humidity'})

%% Save data to .MAT file
clear *_
%save('labWatchTestData.mat')
