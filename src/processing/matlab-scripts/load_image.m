function [img] = load_image(name, resize)
    %{
    loads dcm file
    
    :param name:     the name of the file
    :param resize:   False, if no need for resize, a cell otherwise
                        
    :return:         the image
    %}
    
    img = imread(strcat('../../res/images/', name));
    if iscell(resize)
       img = imresize(img, cell2mat(resize)); 
    end
end