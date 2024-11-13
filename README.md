# Isochronic Tone Generator

## Overview

The **Isochronic Tone Generator** is a desktop application that generates customizable isochronic tones. Isochronic tones are auditory pulses at specific frequencies often used in sound therapy and brainwave entrainment to promote relaxation, focus, meditation, and other mental states.

### Key Features

- **Custom Tone and Pulse Frequencies**: Set your own base tone and pulse frequency.
- **Ramp Mode**: Gradually transition the pulse frequency from a starting value to a final value over a specified time.
- **Random Frequency Variation**: Add dynamic variations to the pulse frequency within a user-defined range.
- **Brainwave Presets**: Choose from pre-configured settings for Delta, Theta, Alpha, Beta, and Gamma brainwave frequencies.
- **Volume and Audio Settings**: Control playback volume, sample rate, and buffer size for optimal performance.
- **Live Pulse Frequency Display**: Monitor the current pulse frequency in real-time during playback.

## Installation

### Download the Executable
For those who prefer a precompiled executable, you can download it from the [Releases page](https://github.com/jdolinschi/Isochronator/releases/tag/v1.0.0).

To run it with python:

1. **Ensure you have Python 3.x installed**. If not, download and install it from [python.org](https://www.python.org/).
2. **Install the required dependencies**:
   ```bash
   pip install pyaudio numpy
   ```
3. **Run the program**:
   Download the script and execute it using:
   ```bash
   python isochronic_tone_generator.py
   ```

## How to Use

### 1. **Presets**

- **Select a preset**: Choose from predefined brainwave settings such as Delta, Theta, Alpha, Beta, or Gamma waves using the dropdown menu.
- **Custom preset**: Select "Custom" to configure your own frequencies.

Each preset automatically sets the start and end pulse frequencies, along with a description of its effects (e.g., relaxation or focus).

---

### 2. **Tone and Pulse Settings**

- **Tone Frequency (Hz)**: The frequency of the base sound wave.
- **Start Pulse Frequency (Hz)**: The initial pulse frequency for modulation.
- **Final Pulse Frequency (Hz)**: The target pulse frequency to which the sound will ramp (if ramp mode is enabled).
- **Ramp Time (s)**: The duration for transitioning between the start and final pulse frequencies. Disable this by unchecking "Use Ramp."

---

### 3. **Random Frequency Variation**

- **Vary Randomly**: Enable to introduce dynamic changes to the pulse frequency.
- **Vary Interval (s)**: Define the time range (start and end) for how often the pulse frequency changes randomly.
- **Vary Amount (±Hz)**: Specify the range within which the frequency will vary.

---

### 4. **Audio Settings**

- **Volume**: Adjust the output volume of the tones using a slider.
- **Sample Rate**: Choose from common sample rates (e.g., 48000 Hz, 44100 Hz).
- **Buffer Size**: Select the buffer size for audio processing. Larger values improve stability but increase latency.

---

### 5. **Controls**

- **Play (▶)**: Starts generating tones.
- **Pause (⏸)**: Temporarily stops the tone while retaining the current state.
- **Stop (⏹)**: Stops playback and resets the settings.

---

### 6. **Real-Time Status**

- The **Current Pulse Frequency** is displayed at the bottom of the app, updating in real-time during playback.

## Example Use Cases

- **Meditation**: Use Theta waves (4–8 Hz) to enhance relaxation and creativity.
- **Focus**: Choose Beta waves (13–30 Hz) to improve concentration and mental alertness.
- **Deep Sleep**: Select Delta waves (0.5–4 Hz) to aid in achieving restorative sleep.

## Troubleshooting

- **No sound output**: Check your audio device configuration and ensure the volume is not muted.
- **Error on launch**: Ensure Python and the required libraries are installed correctly.

## Acknowledgments

This application provides an easy-to-use tool for exploring the effects of isochronic tones. Whether you're a sound therapy enthusiast or simply curious about brainwave entrainment, this generator offers a flexible way to experiment with sound and frequency settings.

<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="jdolinschi" data-color="#FFDD00" data-emoji=""  data-font="Poppins" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>
