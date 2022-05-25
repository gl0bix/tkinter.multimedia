# Tkinter multimedia

- [Markdown](https://www.markdownguide.org/cheat-sheet) basics to edit the README
- write good [commit messages](https://chris.beams.io/posts/git-commit/), pls

# project-description

1. Thema: Multi-Media-Center
2. Technologie: TKinter
3. Team-Mitglieder: Daniel Schellenberg, Camillo Dobrovsky

#### Beschreibung:

Ziel ist es ein kleines Multi-Media-Center aufzubauen. Mit diesem sollen folgende Dinge möglich sein:

- Aufnehmen von Audio/Video aus Stream (So wie mit dem bereits gebauten Audiorecorder)
- Aufnehmen von Audio/Video/Bild mit Webcam
- Anzeigen/Sortieren/Filtern von vorhandenen Aufnahmen
- Abspielen von vorhandenen Aufnahmen

# Interfaces
## Sound 
### with mic

- file: sound_recording.py
- method: prepare_rec(device_id, filename)
- params:
    - **device_id** = index of device from sounddevice.query_devices()
    - **filename** = name of the file to safe (either with .wav or without (then added autom.))
- functionality:
  This function prepares the recording with the given device, chooses the correct samplerate and then starts recording
  in new thread. **To stop recording**, just set the global variable stop to value true.

## Video 
### with cam 

#### Beschreibung: 
Ziel ist es ein kleines Multi-Media-Center aufzubauen. Mit diesem sollen folgende Dinge möglich sein: 
- Aufnehmen von Audio/Video aus Stream (So wie mit dem bereits gebauten Audiorecorder) 
- Aufnehmen von Audio/Video/Bild mit Webcam 
- Anzeigen/Sortieren/Filtern von vorhandenen Aufnahmen 
- Abspielen von vorhandenen Aufnahmen 

