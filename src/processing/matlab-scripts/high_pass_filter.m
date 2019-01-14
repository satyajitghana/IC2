function [Iout] = high_pass_filter(img, sigma)
    M = 2*size(img,1) + 1;
    N = 2*size(img,2) + 1;
    [X, Y] = meshgrid(1:N,1:M);
    centerX = ceil(N/2);
    centerY = ceil(M/2);
    
    % gaussian low pass filter
    gaussianNumerator = (X - centerX).^2 + (Y - centerY).^2;
    H = exp(-gaussianNumerator./(2*sigma.^2));

    H = 1 - H; % converting to high pass filter
    alpha = 0.5;
    beta = 1.5;
    Hemphasis = alpha + beta*H; % high frequency emphasis filter

    % shift zero-frequency component to center (useful for visualizing a 
    % Fourier transform with the zero-frequency component in the middle of the spectrum.)
    % (in other words, shift the filter to the center)
    Hemphasis = fftshift(Hemphasis);

    If = fft2(img, M, N); % convert image to frequency domain. applying padding of MxN before conversion.
    Iout = real(ifft2(Hemphasis.*If)); % apply filter to If and apply inverse fourier transform 
    Iout = Iout(1:size(img,1),1:size(img,2)); % crop image (cuz it was padded)
end