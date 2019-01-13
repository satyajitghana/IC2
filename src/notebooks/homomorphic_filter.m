function [Ihmf] = homomorphic_filter(img, sigma)
    img = im2double(img);
    imgLog = log(1 + img);
    Iout = high_pass_filter(imgLog, sigma);
    Ihmf = exp(Iout) - 1;
end