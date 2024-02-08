[y, fs] = audioread('seventh_measure/noutput7.wav');

% Make a column vector like y
[noise, fs2] = audioread('noise_delta_3.wav');
subplot(2, 1, 1);
plot(noise, 'b-');
grid on;
title('Noise Alone', 'FontSize', 20)

% Create noisy signal
subplot(2, 1, 2);
plot(y, 'b-');
grid on;
cur_snr = snr(y, noise);
caption = sprintf('Signal alone, result:  SNR = %.2f', cur_snr);
title(caption, 'FontSize', 20)