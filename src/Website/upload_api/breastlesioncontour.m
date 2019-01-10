%% Clear things
clc
clear all

%% Load the Image and downscale it if needed
original_img = dicomread('000000.dcm');
%img = imresize(original_img, [256 256]);
img = original_img;
subplot(1, 2, 1)
imshow(img);
title('Original Image');

%% 1. PERFORM IMAGE PRE-PROCESSING

%% homomorphic filtering, output : G
% I(x, y) -> log_e -> high-pass filter -> exp -> I'(x, y)

I = im2double(img);
I = log(1 + I);
M = 2*size(I,1) + 1;
N = 2*size(I,2) + 1;
sigma = 10;
[X, Y] = meshgrid(1:N,1:M);
centerX = ceil(N/2);
centerY = ceil(M/2);
gaussianNumerator = (X - centerX).^2 + (Y - centerY).^2;
H = exp(-gaussianNumerator./(2*sigma.^2));
H = 1 - H;
H = fftshift(H);
If = fft2(I, M, N);
Iout = real(ifft2(repmat(H, [1, 1, 1]).*If));
Iout = Iout(1:size(I,1),1:size(I,2));
Ihmf = exp(Iout) - 1;
G = Ihmf;

%% top-hat transform, output : thf

se = strel('disk', 15);
tophatFiltered = imtophat(G, se);
thf = tophatFiltered;

%% dilate image, output : thfl -- ignore for now

dilatedImage = imdilate(thf, se);
% thinedImage = bwmorph(dilatedImage, 'thin', inf);
thfl = dilatedImage;

%% bot-hat transform, output : bhf

bothatFiltered = imbothat(thfl, se);
bhf = bothatFiltered;

%% adaptive histogram equalization, output : 

enimage = (G + thf) - bhf;
HE = adapthisteq(enimage);

%% pre-processed image
subplot(1, 2, 2)
imshow(HE)
title('Processed Image')

%% 2. PERFORM IMAGE SEGMENTATION

%% K-Means Clustering

% create a binary mask for clustering

binM = imbinarize(img, 0.6);
figure; imshow(binM); title('Binary Image')

%% 
Ero = bwareaopen(binM, 300);
Clab = bwlabel(Ero);
gray = double(img);
array = gray(:);

i = 0; j = 0;
tic
while(true)
    seed = mean(array);
    i = i + 1;
    while(true)
        j = j + 1;
        dist = sqrt((array - seed).^2);
        distth = sqrt(sum((array - seed).^2) / numel(array));
        qualified = dist < distth;
        newseed = mean(array(qualified));
        
        if isnan(newseed)
            break;
        end
        
        if seed == newseed || j > 10
            j = 0;
            array(qualified) = [];
            center(i) = newseed;
            break;
        end
        seed = newseed;
    end
    
    if isempty(array) || i > 10
        i = 0;
        break;
    end
    
end
toc

center = sort(center);
newcenter = diff(center);
intercluster = max(gray(:)/10);
center(newcenter <= intercluster) = [];

vector = repmat(gray(:), [1, numel(center)]);
centers = repmat(center, [numel(gray), 1]);

distance = (vector - centers).^2;
[~, lb] = min(distance, [], 2);
lb = reshape(lb, size(gray));

figure; imshow(lb, []); title('K-Means Clustered Image');

%%
mask = lb > max(max(lb) - 1);
bound = edge(mask, 'sobel');

figure; imshow(bound, []); title('Boundary Image');

% signature Frequency-Power Spectral Density, Geometrical features detection
AdR = regionprops(mask, 'All');
[B, L, N] = bwboundaries(mask);
figure; imshow(img); hold on;
title('Detected Boundary');
kh = 1;
for k = 1:length(AdR),
    boundary = B{k};
    plot(boundary(:, 2), ... 
        boundary(:, 1), 'r', 'LineWidth', 2);
    for sw = 1:length(boundary)
        Signature(kh) = abs(AdR(k).Centroid(1)-boundary(sw, 1));
        kh = kh + 1;
    end
end

Signature = Signature / max(Signature);
figure;
plot(Signature, 'LineWidth', 2);
title('Signature of boundary');

% Power Spectral Density estimate viw Welch's method
[pxx] = pwelch(Signature);
%%
figure; plot(10*log10(pxx), 'LineWidth', 3);
xlabel('Fractal Frequency (Hz)'); ylabel('PSD in dB');
title('Fractal PSD');

Aal = 0; Dal = 0;

%% Geomtric Features

for mx = 1:N
    % Area
    Ar = AdR(mx).Area;
    Aal = [Aal + Ar];
    
    % Diameter
    Di = AdR(mx).EquivDiameter;
    Dal = [Dal + Di];
    
    % PA Ratio
    PA_Ratio = AdR(mx).Perimeter/Ar;
    Major_ax_len = AdR(mx).MajorAxisLength;
    Minor_ax_len = AdR(mx).MinorAxisLength;
    
    % LS Ratio
    LS_Ratio = Major_ax_len / Minor_ax_len;
    
    % ENC Circumference
    ENC = pi * Di;
    GeoFeatures(mx, :) = [Ar Di PA_Ratio Major_ax_len Minor_ax_len LS_Ratio ENC];
    
end

N1 = 3; N2 = 3;
