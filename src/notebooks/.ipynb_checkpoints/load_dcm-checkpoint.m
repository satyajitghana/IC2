function [img] = load_dcm(name, resize)
    %{
    loads dcm file
    
    :param name:     the name of the file
    :param varargin: the other arguments. valid arguments are:-
                        1) resize: a list containing new size
                        
    :return:         the image
    %}
    img = dicomread(strcat('../../res/images/', name));
    if iscell(resize)
       img = imresize(img, cell2mat(resize)); 
    end
end