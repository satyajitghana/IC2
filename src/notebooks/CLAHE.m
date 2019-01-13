function [HE] = CLAHE(img)
    HE = adapthisteq(img, 'clipLimit', 0.00002);
end