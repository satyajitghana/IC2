function [HE] = CLAHE(Ihmf, tophat, bothat)
    img = (Ihmf + tophat) - bothat;
    HE = adapthisteq(img, 'clipLimit', 0.00002);
end