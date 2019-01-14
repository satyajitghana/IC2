function [thf] = tophat_transform(img, se_type, se_size)
    se = strel(se_type, se_size);
    thf = imtophat(img, se);
end