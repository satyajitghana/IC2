function [img] = load_dcm(name, resize)
    %{
    loads dcm file
    
    :param name:     the name of the file
    :param resize:   False, if no need for resize, a cell otherwise
                        
    :return:         the image
    %}
    
    img = dicomread(strcat('../../res/images/', name));
    if iscell(resize)
       img = imresize(img, cell2mat(resize)); 
    end
end