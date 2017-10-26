% Read data exported from LabWatch logger.
%
% Parameter:
%    filename    name of the log file [char]
%
% Returns: 
%    date       times of individual measurements [datetime]
%    value      measured values [double]
%
function [date, value] = importLabwatchData(filename)
    % check input
    p = inputParser;
    addRequired(p,'filename', ...
        @(x)validateattributes(x,{'char'},{'nonempty'}))
    parse(p,filename)
    if exist(filename, 'file')~=2
        error('file not found: %s', filename)
    end
    
    % read data file
    fileID = fopen(filename);
    C = textscan(fileID, '%s %f');
    fclose(fileID);

    % convert date string to datetime object
    for i = 1:numel(C{1})
        C{1}{i} = strrep(C{1}{i}, 'T', '_');
    end
    %%
    date = datetime([C{1}],'InputFormat','yyyy-MM-dd_HH:mm:ss');

    value = [C{2}];
end