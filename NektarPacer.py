from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.SliderElement import SliderElement

class NektarPacer(ControlSurface):

    CC_RECORD = 20   # CC for recording
    CC_PLAY = 117    # CC for play/stop
    CC_UNDO = 21     # CC for undo
    CC_CLIP_DOWN = 22  # CC for navigating to clip below
    CC_CLIP_UP = 23    # CC for navigating to clip above
    CC_TRACK_LEFT = 24  # CC for navigating to track on the left
    CC_TRACK_RIGHT = 25  # CC for navigating to track on the right
    CC_STOP_CLIP = 26  # CC for stopping the currently playing clip on selected track

    def __init__(self, c_instance):
        super(NektarPacer, self).__init__(c_instance)
        with self.component_guard():
            self.log_message("Nektar Pacer Control loaded")
            
            # Create CC object for recording (CC 20)
            self._cc_record = SliderElement(MIDI_CC_TYPE, 0, self.CC_RECORD)
            self._cc_record.add_value_listener(self._cc_record_value)
            
            # Create CC object for play/stop (CC 117)
            self._cc_play = SliderElement(MIDI_CC_TYPE, 0, self.CC_PLAY)
            self._cc_play.add_value_listener(self._cc_play_value)
            
            # Create CC object for undo (CC 21)
            self._cc_undo = SliderElement(MIDI_CC_TYPE, 0, self.CC_UNDO)
            self._cc_undo.add_value_listener(self._cc_undo_value)
            
            # Create CC object for clip navigation down (CC 22)
            self._cc_clip_down = SliderElement(MIDI_CC_TYPE, 0, self.CC_CLIP_DOWN)
            self._cc_clip_down.add_value_listener(self._cc_clip_down_value)
            
            # Create CC object for clip navigation up (CC 23)
            self._cc_clip_up = SliderElement(MIDI_CC_TYPE, 0, self.CC_CLIP_UP)
            self._cc_clip_up.add_value_listener(self._cc_clip_up_value)
            
            # Create CC object for track navigation left (CC 24)
            self._cc_track_left = SliderElement(MIDI_CC_TYPE, 0, self.CC_TRACK_LEFT)
            self._cc_track_left.add_value_listener(self._cc_track_left_value)
            
            # Create CC object for track navigation right (CC 25)
            self._cc_track_right = SliderElement(MIDI_CC_TYPE, 0, self.CC_TRACK_RIGHT)
            self._cc_track_right.add_value_listener(self._cc_track_right_value)
            
            # Create CC object for stop clip (CC 26)
            self._cc_stop_clip = SliderElement(MIDI_CC_TYPE, 0, self.CC_STOP_CLIP)
            self._cc_stop_clip.add_value_listener(self._cc_stop_clip_value)

    def _cc_record_value(self, value):
        # Trigger mode: only react to value > 0 (button press)
        if value > 0:
            song = self.song()
            selected_track = song.view.selected_track
            
            # Get the selected scene index
            selected_scene_index = list(song.scenes).index(song.view.selected_scene)
            selected_slot = selected_track.clip_slots[selected_scene_index]

            # Check current state: is track armed and recording?
            is_recording = selected_track.arm and selected_slot.has_clip and selected_slot.clip.is_recording
            
            if is_recording:
                # Currently recording → stop recording
                self.log_message("Record OFF track %s" % selected_track.name)
                
                # Stop the clip if it's currently recording
                selected_slot.stop()

                # If clip exists after stopping, launch it automatically
                if selected_slot.has_clip:
                    try:
                        self.log_message("Auto-launching clip on %s after recording" % selected_track.name)
                        selected_slot.fire()
                    except Exception:
                        # Some Live environments may expose other methods
                        try:
                            clip = selected_slot.clip
                            if not clip.is_playing:
                                clip.fire()
                        except Exception:
                            pass

                # Ne pas désarmer la piste pour éviter les conflits avec l'auto-arm
                # selected_track.arm = False
            else:
                # Not recording → start recording
                self.log_message("Record ON track %s" % selected_track.name)
                
                # Arm the track
                selected_track.arm = True
                
                # Enable session recording if needed
                if not song.session_record:
                    song.session_record = True
                
                # Start recording on the clip slot
                selected_slot.fire()

    def _cc_play_value(self, value):
        # Trigger mode: only react to value > 0 (button press)
        if value > 0:
            song = self.song()
            selected_track = song.view.selected_track
            
            # Get the selected scene index
            selected_scene_index = list(song.scenes).index(song.view.selected_scene)
            selected_slot = selected_track.clip_slots[selected_scene_index]
            
            # Check if the slot has a clip
            if selected_slot.has_clip:
                clip = selected_slot.clip
                
                # Check actual clip state and toggle
                if clip.is_playing:
                    self.log_message("Clip STOP on %s" % selected_track.name)
                    selected_slot.stop()
                else:
                    self.log_message("Clip PLAY on %s" % selected_track.name)
                    selected_slot.fire()
            else:
                self.log_message("No clip in selected slot")

    def _cc_undo_value(self, value):
        # Trigger undo only on press (value > 0)
        if value > 0:
            self.log_message("Undo triggered")
            try:
                self.song().undo()
            except Exception as e:
                self.log_message("Error during undo: %s" % str(e))

    def _cc_clip_down_value(self, value):
        # Navigate to the clip slot below on button press
        if value > 0:
            song = self.song()
            scenes = list(song.scenes)
            current_scene_index = scenes.index(song.view.selected_scene)
            
            # Move down if not at the bottom
            if current_scene_index < len(scenes) - 1:
                song.view.selected_scene = scenes[current_scene_index + 1]
                self.log_message("Clip navigation: DOWN to scene %d" % (current_scene_index + 2))
            else:
                self.log_message("Clip navigation: Already at bottom scene")

    def _cc_clip_up_value(self, value):
        # Navigate to the clip slot above on button press
        if value > 0:
            song = self.song()
            scenes = list(song.scenes)
            current_scene_index = scenes.index(song.view.selected_scene)
            
            # Move up if not at the top
            if current_scene_index > 0:
                song.view.selected_scene = scenes[current_scene_index - 1]
                self.log_message("Clip navigation: UP to scene %d" % current_scene_index)
            else:
                self.log_message("Clip navigation: Already at top scene")

    def _cc_track_left_value(self, value):
        # Navigate to the track on the left on button press
        if value > 0:
            song = self.song()
            tracks = list(song.tracks)
            current_track = song.view.selected_track
            
            # Check if current track is in the tracks list (not a return/master track)
            if current_track in tracks:
                current_track_index = tracks.index(current_track)
                
                # Move left if not at the first track
                if current_track_index > 0:
                    song.view.selected_track = tracks[current_track_index - 1]
                    self.log_message("Track navigation: LEFT to %s" % tracks[current_track_index - 1].name)
                else:
                    self.log_message("Track navigation: Already at first track")
            else:
                # If on return/master track, move to last regular track
                if len(tracks) > 0:
                    song.view.selected_track = tracks[-1]
                    self.log_message("Track navigation: LEFT to %s" % tracks[-1].name)

    def _cc_track_right_value(self, value):
        # Navigate to the track on the right on button press
        if value > 0:
            song = self.song()
            tracks = list(song.tracks)
            current_track = song.view.selected_track
            
            # Check if current track is in the tracks list (not a return/master track)
            if current_track in tracks:
                current_track_index = tracks.index(current_track)
                
                # Move right if not at the last track
                if current_track_index < len(tracks) - 1:
                    song.view.selected_track = tracks[current_track_index + 1]
                    self.log_message("Track navigation: RIGHT to %s" % tracks[current_track_index + 1].name)
                else:
                    self.log_message("Track navigation: Already at last track")
            else:
                # If on return/master track, move to first regular track
                if len(tracks) > 0:
                    song.view.selected_track = tracks[0]
                    self.log_message("Track navigation: RIGHT to %s" % tracks[0].name)

    def _cc_stop_clip_value(self, value):
        # Stop any playing clip on the selected track
        if value > 0:
            song = self.song()
            selected_track = song.view.selected_track
            
            # Find and stop any playing clip on this track
            clip_stopped = False
            for clip_slot in selected_track.clip_slots:
                if clip_slot.has_clip and clip_slot.clip.is_playing:
                    clip_slot.stop()
                    clip_stopped = True
                    self.log_message("Stopped playing clip on track %s" % selected_track.name)
                    break
            
            if not clip_stopped:
                self.log_message("No playing clip on track %s" % selected_track.name)

    def disconnect(self):
        self._cc_record.remove_value_listener(self._cc_record_value)
        self._cc_play.remove_value_listener(self._cc_play_value)
        self._cc_undo.remove_value_listener(self._cc_undo_value)
        self._cc_clip_down.remove_value_listener(self._cc_clip_down_value)
        self._cc_clip_up.remove_value_listener(self._cc_clip_up_value)
        self._cc_track_left.remove_value_listener(self._cc_track_left_value)
        self._cc_track_right.remove_value_listener(self._cc_track_right_value)
        self._cc_stop_clip.remove_value_listener(self._cc_stop_clip_value)
        super(NektarPacer, self).disconnect()
