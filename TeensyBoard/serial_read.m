clear
close all
if exist('s', 'var') && isa(s, 'serialport') && isvalid(s)
    clear s;
end

s = serialport("COM3", 9600);
configureTerminator(s, "CR/LF");

allDataPoints = [];
timeStamps = [];

figure1 = figure;
figure2 = figure;
plot2 = plot(NaN, NaN);
grid on;

baseTimeStamp = now;
s.Timeout = 50;
while true
    str = readline(s);
    disp(str)
    splitData = regexp(str, '.{1,6}', 'match');
    numericArray = str2double(splitData);
    
    reshapedData = reshape(numericArray, 256, []);
    %pause(2);
    cur_TimeStamp = now;
    timeInterval = (cur_TimeStamp - baseTimeStamp) * 24 * 60 * 60;
    
    allDataPoints = [allDataPoints, reshapedData];
    timeStamps = [timeStamps, repmat(timeInterval, 1, size(reshapedData, 2))];
    
    figure(figure1);
    plot(timeStamps, allDataPoints);
    title('Figure Title');
    xlabel('X Axis Label');
    ylabel('Y Axis Label');
    grid on;
    drawnow;

    figure(figure2);
    set(plot2, 'XData', 1:length(numericArray), 'YData', numericArray);
    drawnow;
end

clear s
