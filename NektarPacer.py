from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.SliderElement import SliderElement

class NektarPacer(ControlSurface):

    CC_RECORD = 20   # CC pour l'enregistrement
    CC_PLAY = 117    # CC pour play/stop
    CC_UNDO = 21     # CC pour undo
    CC_CLIP_DOWN = 22  # CC pour naviguer vers le clip du bas
    CC_CLIP_UP = 23    # CC pour naviguer vers le clip du haut
    CC_TRACK_LEFT = 24  # CC pour naviguer vers la piste de gauche
    CC_TRACK_RIGHT = 25  # CC pour naviguer vers la piste de droite

    def __init__(self, c_instance):
        super(NektarPacer, self).__init__(c_instance)
        with self.component_guard():
            self.log_message("Nektar Pacer Control loaded")
            
            # Créer un objet CC pour l'enregistrement (CC 20)
            self._cc_record = SliderElement(MIDI_CC_TYPE, 0, self.CC_RECORD)
            self._cc_record.add_value_listener(self._cc_record_value)
            
            # Créer un objet CC pour play/stop (CC 117)
            self._cc_play = SliderElement(MIDI_CC_TYPE, 0, self.CC_PLAY)
            self._cc_play.add_value_listener(self._cc_play_value)
            
            # Créer un objet CC pour undo (CC 21)
            self._cc_undo = SliderElement(MIDI_CC_TYPE, 0, self.CC_UNDO)
            self._cc_undo.add_value_listener(self._cc_undo_value)
            
            # Créer un objet CC pour navigation clip down (CC 22)
            self._cc_clip_down = SliderElement(MIDI_CC_TYPE, 0, self.CC_CLIP_DOWN)
            self._cc_clip_down.add_value_listener(self._cc_clip_down_value)
            
            # Créer un objet CC pour navigation clip up (CC 23)
            self._cc_clip_up = SliderElement(MIDI_CC_TYPE, 0, self.CC_CLIP_UP)
            self._cc_clip_up.add_value_listener(self._cc_clip_up_value)
            
            # Créer un objet CC pour navigation track left (CC 24)
            self._cc_track_left = SliderElement(MIDI_CC_TYPE, 0, self.CC_TRACK_LEFT)
            self._cc_track_left.add_value_listener(self._cc_track_left_value)
            
            # Créer un objet CC pour navigation track right (CC 25)
            self._cc_track_right = SliderElement(MIDI_CC_TYPE, 0, self.CC_TRACK_RIGHT)
            self._cc_track_right.add_value_listener(self._cc_track_right_value)

    def _cc_record_value(self, value):
        song = self.song()
        selected_track = song.view.selected_track
        
        # Obtenir l'index de la scène sélectionnée
        selected_scene_index = list(song.scenes).index(song.view.selected_scene)
        selected_slot = selected_track.clip_slots[selected_scene_index]

        if value > 0:
            # Activation : armer la piste et lancer l'enregistrement
            self.log_message("Record ON piste %s" % selected_track.name)
            
            # Armer la piste
            selected_track.arm = True
            
            # Activer l'enregistrement dans la session si nécessaire
            if not song.session_record:
                song.session_record = True
            
            # Lancer l'enregistrement sur le clip slot
            selected_slot.fire()
            
        else:
            # Désactivation : stopper le clip et désarmer la piste
            self.log_message("Record OFF piste %s" % selected_track.name)
            
            # Arrêter le clip s'il est en cours d'enregistrement
            if selected_slot.has_clip and selected_slot.clip.is_recording:
                # Stopper l'enregistrement
                selected_slot.stop()

                # Si le clip existe après l'arrêt, lancer sa lecture automatiquement
                # selected_slot.has_clip peut déjà être True ; on vérifie et on lance
                if selected_slot.has_clip:
                    try:
                        self.log_message("Lancement automatique du clip sur %s après enregistrement" % selected_track.name)
                        selected_slot.fire()
                    except Exception:
                        # Certains environnements Live peuvent exposer d'autres méthodes
                        # Si fire() n'est pas disponible, essayer via clip.playing_position / is_playing
                        try:
                            clip = selected_slot.clip
                            if not clip.is_playing:
                                clip.fire()  # tentative, selon API
                        except Exception:
                            # Rien de plus à faire ici; on laisse le clip arrêté
                            pass

            selected_track.arm = False

    def _cc_play_value(self, value):
        # Toggle play/stop du clip uniquement sur appui (valeur > 0)
        if value > 0:
            song = self.song()
            selected_track = song.view.selected_track
            
            # Obtenir l'index de la scène sélectionnée
            selected_scene_index = list(song.scenes).index(song.view.selected_scene)
            selected_slot = selected_track.clip_slots[selected_scene_index]
            
            # Vérifier si le slot a un clip
            if selected_slot.has_clip:
                clip = selected_slot.clip
                
                # Toggle play/stop du clip
                if clip.is_playing:
                    self.log_message("Clip STOP sur %s" % selected_track.name)
                    selected_slot.stop()
                else:
                    self.log_message("Clip PLAY sur %s" % selected_track.name)
                    selected_slot.fire()
            else:
                self.log_message("Pas de clip dans le slot sélectionné")

    def _cc_undo_value(self, value):
        # Déclencher undo uniquement sur appui (valeur > 0)
        if value > 0:
            self.log_message("Undo déclenché")
            try:
                self.song().undo()
            except Exception as e:
                self.log_message("Erreur lors de l'undo: %s" % str(e))

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

    def disconnect(self):
        self._cc_record.remove_value_listener(self._cc_record_value)
        self._cc_play.remove_value_listener(self._cc_play_value)
        self._cc_undo.remove_value_listener(self._cc_undo_value)
        self._cc_clip_down.remove_value_listener(self._cc_clip_down_value)
        self._cc_clip_up.remove_value_listener(self._cc_clip_up_value)
        self._cc_track_left.remove_value_listener(self._cc_track_left_value)
        self._cc_track_right.remove_value_listener(self._cc_track_right_value)
        super(NektarPacer, self).disconnect()
