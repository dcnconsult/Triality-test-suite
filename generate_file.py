import numpy as np
from scipy.io.wavfile import write

# --- Parameters ---
# Frequencies for the Trinity Chord and Schumann Resonance (Keynote)
freq_x = 0.306
freq_y = 42.0
freq_z = 131.95
freq_schumann = 7.83

# Audio settings
duration_seconds = 300  # 5 minutes
sample_rate = 44100     # CD quality
filename = "triality_chord.wav"

# --- Generation Process ---

# 1. Create a time array
num_samples = int(duration_seconds * sample_rate)
t = np.linspace(0, duration_seconds, num_samples, endpoint=False)

# 2. Generate each individual sine wave
# We'll give the very low frequencies a slightly higher amplitude to ensure their presence
# in the final mix before normalization.
wave_x = 0.4 * np.sin(2 * np.pi * freq_x * t)
wave_y = 0.2 * np.sin(2 * np.pi * freq_y * t)
wave_z = 0.2 * np.sin(2 * np.pi * freq_z * t)
wave_schumann = 0.2 * np.sin(2 * np.pi * freq_schumann * t)

# 3. Combine the waves (Additive Synthesis)
complex_wave = wave_x + wave_y + wave_z + wave_schumann

# 4. Normalize the audio to 16-bit integer range
# This prevents clipping and ensures it's a valid WAV file.
max_amplitude = np.max(np.abs(complex_wave))
if max_amplitude > 0:
    normalized_wave = complex_wave / max_amplitude
else:
    normalized_wave = complex_wave

scaled_wave = np.int16(normalized_wave * 32767)

# 5. Write the WAV file
write(filename, sample_rate, scaled_wave)

print(f"Successfully generated '{filename}'")
print(f"Duration: {duration_seconds} seconds")
print(f"Sample Rate: {sample_rate} Hz")