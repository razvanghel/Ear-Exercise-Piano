# Ear-Exercise-Piano: improve your note recognition skills
Interactive piano GUI with two available gamemodes: practice mode and test mode
# How to run the program
Run main.py
# Gamemodes and settings description
## Settings
### General settings
When a game is in progress, all the buttons of the menu are disabled, excepting the piano keys and the 'STOP GAME' button.
The piano has by default 4 octaves. The piano can be modified by changing the value PIANO_OCTAVE in configurations.py. Invariant: 1 <= PIANO_OCTAVE <= 8
### Game settings
Each gamemode has the following settings:
 - Starting octave (range: 1-8): the starting octave of the piano. The piano has by default 4 octaves (e.g. starting octave is 2, so you can play notes from octaves 2,3,4,5). 
 - One octave only: boolean that signals whether the games should use only one octave (the value of the octave is determined by starting octave)
 - Sounds per session: the length of a session. One game will play x amount of random notes, where x ∈ [5,50]. 
 - Show keys: boolean that signals whether the keys of the piano should display their note and octave
### Save settings 
In order to save the current game settings, press the button 'SAVE SETTINGS'.
## Practice mode 
A note is randomly played. After 5 seconds the piano key corresponding to the played note will be highlighted with red for 2 seconds, then the key return back to its original color.
## Test mode
A note is randomly played. When the user presses a piano key, the correct key will be displayed in the same manner as in practice mode.
