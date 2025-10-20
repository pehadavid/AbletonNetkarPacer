# Nektar Pacer MIDI Remote Script for Ableton Live

A custom MIDI Remote Script that enables Nektar Pacer foot controllers to control recording and clip playback in Ableton Live.

## Features

This script provides two main control functions via MIDI CC messages:

### CC 20 - Track Recording (Toggle Mode)
Controls track arming and clip recording on the selected track.

**Behavior:**
- **First press** (CC 20 value > 0):
  - Arms the selected track
  - Enables session recording mode
  - Starts recording on the selected clip slot
  - Logs: "Record ON piste [track name]"

- **Second press** (CC 20 value = 0):
  - Stops the clip if currently recording
  - Disarms the selected track
  - Logs: "Record OFF piste [track name]"

**Use case:** Perfect for recording loops in session view. Press once to start recording, press again to stop and finalize the clip.

### CC 117 - Clip Play/Stop (Toggle Mode)
Controls playback of clips in the selected clip slot.

**Behavior:**
- **Press** (CC 117 value > 0):
  - If a clip exists in the selected slot:
    - **Clip is playing** → Stops the clip (Logs: "Clip STOP sur [track name]")
    - **Clip is stopped** → Starts the clip (Logs: "Clip PLAY sur [track name]")
  - If no clip exists in the selected slot:
    - Logs: "Pas de clip dans le slot sélectionné"

**Use case:** Toggle playback of recorded clips. Press to play, press again to stop.

## Installation

1. Copy the `NektarPacer` folder to your Ableton MIDI Remote Scripts directory:
   - **Windows:** `C:\ProgramData\Ableton\Live [version]\Resources\MIDI Remote Scripts\`
   - **macOS:** `/Applications/Live [version]/Contents/App-Resources/MIDI Remote Scripts/`

2. Restart Ableton Live

3. Go to **Preferences → Link/Tempo/MIDI**

4. Under **MIDI Ports**, select "NektarPacer" as a Control Surface

5. Set the appropriate Input and Output MIDI ports for your Nektar Pacer

## Nektar Pacer Configuration

Configure your Nektar Pacer footswitches with the following settings:

### Footswitch for Recording (CC 20)
```
Mode:      CC Toggle
Channel:   Global
CC Number: 20
Data 2:    0    (value when OFF)
Data 3:    127  (value when ON)
```

### Footswitch for Clip Play/Stop (CC 117)
```
Mode:      CC Toggle
Channel:   Global
CC Number: 117
Data 2:    0    (value when OFF)
Data 3:    127  (value when ON)
```

## Workflow Example

### Recording and Playing a Loop

1. **Select a track** in Ableton Live
2. **Select an empty clip slot** (scene)
3. **Press FS with CC 20** → Starts recording
4. Play your instrument/perform
5. **Press FS with CC 20 again** → Stops recording and creates the clip
6. **Press FS with CC 117** → Plays the recorded clip
7. **Press FS with CC 117 again** → Stops the clip

### Building a Loop Set

1. Record first clip on Track 1 (CC 20)
2. Play first clip (CC 117)
3. Select Track 2
4. Record second clip while first is playing (CC 20)
5. Toggle clips on/off as needed (CC 117)

## Technical Details

- **Framework:** Built using Ableton's `_Framework` module
- **Control Elements:** Uses `SliderElement` for MIDI CC input
- **MIDI Channel:** Channel 0 (MIDI Channel 1)
- **Python Version:** Compatible with Ableton Live's Python 2.7/3.x environment
- **Dependencies:** Managed via `component_guard()` context

## Troubleshooting

### Script doesn't load
- Check Ableton's Log.txt file for errors
- Verify the folder structure is correct
- Ensure `__init__.py` is present in the folder

### CC messages not working
- Verify Nektar Pacer is sending the correct CC numbers (20 and 117)
- Check that "Data 3" is set to 127 (not 0) in your Pacer configuration
- Ensure the MIDI channel matches (Global = Channel 1)

### Recording doesn't start
- Make sure a track is selected
- Verify the track can be armed (audio/MIDI track, not Return/Master)
- Check that session recording is enabled in Ableton

### Clip doesn't play
- Ensure there's an actual clip in the selected slot
- Check the logs for "Pas de clip dans le slot sélectionné" message

## Logs and Debugging

The script outputs log messages visible in Ableton's Log.txt file:
- "Nektar Pacer Control loaded" - Script initialized successfully
- "Record ON piste [name]" - Recording started
- "Record OFF piste [name]" - Recording stopped
- "Clip PLAY sur [name]" - Clip playback started
- "Clip STOP sur [name]" - Clip playback stopped
- "Pas de clip dans le slot sélectionné" - No clip in selected slot

## Version History

- **v1.0** - Initial release
  - CC 20: Track recording toggle
  - CC 117: Clip play/stop toggle

## License

This script is provided as-is for personal use.

## Credits

Created for use with Nektar Pacer MIDI foot controllers and Ableton Live.
