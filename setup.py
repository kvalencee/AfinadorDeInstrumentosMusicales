"""
Setup script for creating macOS .app bundle
"""
from setuptools import setup

APP = ['tuner_gui.py']
DATA_FILES = [('samples', ['samples/A4_440Hz.wav', 'samples/A4_435Hz_flat.wav', 'samples/A4_445Hz_sharp.wav', 
                           'samples/C4_262Hz_middle_c.wav', 'samples/E2_82Hz_guitar.wav', 'samples/G3_196Hz_violin.wav'])]
OPTIONS = {
    'argv_emulation': False,
    'packages': ['numpy', 'scipy', 'matplotlib', 'tkinter', 'pyaudio'],
    'includes': ['scipy.special._ufuncs_cxx', 'scipy.fft._pocketfft.pypocketfft'],
    'excludes': ['PyQt5', 'PyQt6'],
    'plist': {
        'CFBundleName': 'Afinador Musical',
        'CFBundleDisplayName': 'Afinador de Instrumentos Musicales',
        'CFBundleIdentifier': 'com.escom.afinadormusical',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSMicrophoneUsageDescription': 'Esta aplicación necesita acceso al micrófono para grabar y analizar notas musicales.',
    }
}

setup(
    name='AfinadorMusical',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
