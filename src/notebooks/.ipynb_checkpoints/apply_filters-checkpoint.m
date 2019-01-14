function [out] = apply_filters(img, img_name)
    fprintf("applying homomorphic filter...");
    Ihmf = homomorphic_filter(img, 10);
    fprintf("\napplying tophat transform...");
    tophat = tophat_transform(Ihmf, 'disk', 15);
    fprintf("\napplying bothat transform...");
    bothat = bothat_transform(Ihmf, 'disk', 15);
    fprintf("\napplying CLAHE...");
    out = CLAHE((Ihmf + tophat) - bothat);
    fprintf("\ndone.");
    
    %path="../../res/images/output/";
    %imwrite(Ihmf, strcat(path, img_name, "-MATLABHomomorphicFilter.jpg"))
    %imwrite(tophat, strcat(path, img_name,"-MATLABtophat.jpg"))
    %imwrite(bothat, strcat(path, img_name,"-MATLABbothat.jpg"))
    %imwrite(out, strcat(path, img_name,"-MATLABfinal.jpg"))
    
    montage([Ihmf, tophat; bothat, out]);
end