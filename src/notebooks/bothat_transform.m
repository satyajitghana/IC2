function [bhf] = bothat_transform(img, se_type, se_size)
    se = strel(se_type, se_size);
    bhf = imbothat(img, se);
end