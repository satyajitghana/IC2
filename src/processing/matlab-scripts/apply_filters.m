function [out] = apply_filters(img)
    Ihmf = homomorphic_filter(img, 10);
    tophat = tophat_transform(Ihmf, 'disk', 15);
    bothat = bothat_transform(Ihmf, 'disk', 15);
    out = CLAHE(Ihmf,tophat, bothat);
    
end