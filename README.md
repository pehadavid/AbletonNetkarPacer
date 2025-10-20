# Nektar Pacer MIDI Remote Script for Ableton Live

MIDI Remote Script to control Ableton Live with Nektar Pacer foot controller.

**Note**: This script is designed primarily for **Session View** workflow (recording and triggering clips). The Nektar Pacer's built-in **Transport mode (Mackie protocol)** remains available and can be used alongside this script for transport controls.

## Features

### CC 20 - Recording (Toggle)
- **First press**: Arms the track and starts recording on the selected clip slot
- **Second press**: Stops recording and disarms the track

### CC 117 - Clip Play/Stop (Toggle)
- **Press**: Plays or stops the selected clip
- Does nothing if no clip is present

### CC 21 - Undo (Momentary)
- **Press**: Undoes the last action in Ableton Live

### CC 22 - Navigate Down (Momentary)
- **Press**: Moves the scene selection down (next clip slot below on the selected track)

### CC 23 - Navigate Up (Momentary)
- **Press**: Moves the scene selection up (previous clip slot above on the selected track)

### CC 24 - Navigate Left (Momentary)
- **Press**: Moves the track selection left (previous track)

### CC 25 - Navigate Right (Momentary)
- **Press**: Moves the track selection right (next track)

## Nektar Pacer Configuration

To use this script, you need to configure your Nektar Pacer footswitches to send the correct CC messages.

### Option 1: Import the SysEx file (Recommended)

A pre-configured preset is included in the `sysex/` folder:
- **File**: `nektar-pacer-surface.syx`
- Import this file using the Pacer Editor: **https://studiocode.dev/pacer-editor/#/**

This preset includes all CC mappings ready to use.

### Option 2: Manual Configuration

Use the online Pacer Editor to manually configure your footswitches with:
- **CC 20** for Recording (Toggle mode)
- **CC 117** for Clip Play/Stop (Toggle mode)
- **CC 21** for Undo (Momentary mode)
- **CC 22** for Navigate Down (Momentary mode)
- **CC 23** for Navigate Up (Momentary mode)
- **CC 24** for Navigate Left (Momentary mode)
- **CC 25** for Navigate Right (Momentary mode)

## Installation

1. Copy the entire repository content to a new folder named `NektarPacer` in your Ableton MIDI Remote Scripts directory:
   - **Windows:** `C:\ProgramData\Ableton\Live [version]\Resources\MIDI Remote Scripts\NektarPacer\`
   - **macOS:** `/Applications/Live [version]/Contents/App-Resources/MIDI Remote Scripts/NektarPacer/`

2. Restart Ableton Live

3. Go to **Preferences → Link/Tempo/MIDI**

4. Under **MIDI Ports**, select "NektarPacer" as a Control Surface

5. Set the appropriate Input and Output MIDI ports for your Nektar Pacer

## Nektar Pacer Configuration

Configure your Nektar Pacer footswitches with the following settings:

### Footswitch for Recording (CC 20)

```text
Mode:      CC Toggle
Channel:   Global
CC Number: 20
Data 2:    0    (value when OFF)
Data 3:    127  (value when ON)
```

### Footswitch for Clip Play/Stop (CC 117)

```text
Mode:      CC Toggle
Channel:   Global
CC Number: 117
Data 2:    0    (value when OFF)
Data 3:    127  (value when ON)
```

### Footswitch for Undo (CC 21)

```text
Mode:      CC Momentary
Channel:   Global
CC Number: 21
Data 2:    0    (value when OFF)
Data 3:    127  (value when ON)
```

### Footswitch for Navigate Down (CC 22)

```text
Mode:      CC Momentary
Channel:   Global
CC Number: 22
Data 2:    0    (value when OFF)
Data 3:    127  (value when ON)
```

### Footswitch for Navigate Up (CC 23)

```text
Mode:      CC Momentary
Channel:   Global
CC Number: 23
Data 2:    0    (value when OFF)
Data 3:    127  (value when ON)
```

### Footswitch for Navigate Left (CC 24)

```text
Mode:      CC Momentary
Channel:   Global
CC Number: 24
Data 2:    0    (value when OFF)
Data 3:    127  (value when ON)
```

### Footswitch for Navigate Right (CC 25)

```text
Mode:      CC Momentary
Channel:   Global
CC Number: 25
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

### Building a Loop Set with Navigation

1. Record first clip on Track 1 (CC 20)
2. Play first clip (CC 117)
3. Navigate to Track 2 (CC 25 - Navigate Right)
4. Navigate to desired scene (CC 22/23 - Navigate Down/Up)
5. Record second clip while first is playing (CC 20)
6. Toggle clips on/off as needed (CC 117)
7. Use CC 24/25 to move between tracks, CC 22/23 to move between scenes

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

- Verify Nektar Pacer is sending the correct CC numbers (20, 21, 22, 23, 24, 25, and 117)
- Check that "Data 3" is set to 127 (not 0) in your Pacer configuration
- Ensure the MIDI channel matches (Global = Channel 1)

### Recording doesn't start
- Make sure a track is selected
- Verify the track can be armed (audio/MIDI track, not Return/Master)
- Check that session recording is enabled in Ableton

### Clip doesn't play
- Ensure there's an actual clip in the selected slot
- Check the logs for "No clip in selected slot" message

## Logs and Debugging

The script outputs log messages visible in Ableton's Log.txt file:

- "Nektar Pacer Control loaded" - Script initialized successfully
- "Record ON track [name]" - Recording started
- "Record OFF track [name]" - Recording stopped
- "Auto-launching clip on [name] after recording" - Clip auto-play after recording
- "Clip PLAY on [name]" - Clip playback started
- "Clip STOP on [name]" - Clip playback stopped
- "No clip in selected slot" - No clip in selected slot
- "Undo triggered" - Undo action triggered successfully
- "Error during undo: [error]" - Undo action failed
- "Clip navigation: UP/DOWN to scene [number]" - Scene selection changed
- "Clip navigation: Already at top/bottom scene" - Cannot move further
- "Track navigation: LEFT/RIGHT to [track name]" - Track selection changed
- "Track navigation: Already at first/last track" - Cannot move further

## Version History

- **v1.3** - Track navigation added
  - CC 24: Navigate left (previous track)
  - CC 25: Navigate right (next track)
- **v1.2** - Scene navigation added
  - CC 22: Navigate down (next scene)
  - CC 23: Navigate up (previous scene)
- **v1.1** - Undo feature added
  - CC 21: Undo command
- **v1.0** - Initial release
  - CC 20: Track recording toggle
  - CC 117: Clip play/stop toggle

## License

This script is provided as-is for personal use.

## Credits

Created for use with Nektar Pacer MIDI foot controllers and Ableton Live.
