from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.SliderElement import SliderElement

class NektarPacer(ControlSurface):

    CC_RECORD = 20   # CC pour l'enregistrement
    CC_PLAY = 117    # CC pour play/stop

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
                selected_slot.stop()
            
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

    def disconnect(self):
        self._cc_record.remove_value_listener(self._cc_record_value)
        self._cc_play.remove_value_listener(self._cc_play_value)
        super(NektarPacer, self).disconnect()
