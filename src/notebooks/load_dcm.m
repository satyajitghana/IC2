function [img] = load_dcm(name, varargin)
    %{
    loads dcm file
    
    :param name:     the name of the file
    :param varargin: the other arguments. valid arguments are:-
                        1) resize: a list containing new size
                        
    :return:         the image
    %}
    defaults = {false};
    idx = ~cellfun('isempty', varargin);
    defaults(idx) = varargin(idx);
    
    img = dicomread(strcat('../../res/images/', name));
    if defaults{1} ~= 0
       img = imresize(img, defaults{1}); 
    end
end