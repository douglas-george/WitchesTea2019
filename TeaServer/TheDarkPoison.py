import tkinter
from TeaServer.TeaScript import attendees
from TeaServer.TeaScript import game_states
from TeaServer.GameRunnerGui import GameRunnerGui
from TeaServer.TeaAnnouncer import TeaAnnouncer
from TeaServer.ServerListenerLink import TableListener, WandListener, FireplaceListener, ClickerListener
import time
from pygame import mixer


class TheDarkPoison:
    def __init__(self):
        self.gui = GameRunnerGui()
        self.announcer = TeaAnnouncer(time_between_heartbeats=0.1, current_game_state=game_states[0][0])
        self.table_listener = TableListener()
        self.fireplace_listener = FireplaceListener()
        self.wand_listener = WandListener()
        self.clicker_listener = ClickerListener()

        self.time_in_cast_state = None

        self.warmup_time = None

        self.last_initialized_state = None

        self.current_audio_clips_state = None

        self.num_wands_lit = 0

        self.last_wand_status = {}
        for attendee in attendees:
            self.last_wand_status[attendee] = ""

        mixer.init()

    def run(self):
        while True:
            try:
                self.gui.service()
                state_index = self.gui.get_index_of_current_state()
                self.current_state = game_states[state_index][0]
            except tkinter.TclError:
                break

            self.announcer.update_state(new_game_state=self.current_state)
            self.announcer.service()
            self.service_remote_devices()
            self.service_audio()
            self.service_current_state()

    def service_remote_devices(self):
        table_data = self.table_listener.service_table()
        if table_data is not None:
            table_heartbeat_id, table_state, sender_ip = table_data
            self.gui.table_status.update_hw_info(ip_addr=sender_ip, compile_date=None, compile_time=None)
            self.gui.table_status.heartbeat_received()
            self.gui.table_status.update_row_status(table_state)

            if (table_state == "SNAKE_DONE"):
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        fireplace_data = self.fireplace_listener.service_fireplace()
        if fireplace_data is not None:
            fireplace_heartbeat_id, fireplace_state, sender_ip = fireplace_data
            self.gui.ReginaFireplaceStatus.update_hw_info(ip_addr=sender_ip, compile_date=None, compile_time=None)
            self.gui.ReginaFireplaceStatus.heartbeat_received()
            self.gui.ReginaFireplaceStatus.update_row_status(fireplace_state)

        wand_data = self.wand_listener.service_wands()
        if wand_data is not None:
            message_id, wand_id, wand_state, compile_date, compile_time, sender_ip = wand_data
            self.gui.update_wand_status(message_id, wand_id, wand_state, compile_date, compile_time, sender_ip)
            self.last_wand_status[wand_id] = wand_state

        self.num_wands_lit = 0
        for wand_id in self.last_wand_status:
            if self.last_wand_status[wand_id] == "LIT":
                self.num_wands_lit += 1

        clicker_data = self.clicker_listener.service_clicker()
        if clicker_data is not None:
            message_id, clicker_id, clicker_state, compile_date, compile_time, sender_ip = clicker_data
            self.gui.ClickerStatus.update_hw_info(ip_addr=sender_ip, compile_date=None, compile_time=None)
            self.gui.ClickerStatus.heartbeat_received()
            self.gui.ClickerStatus.update_row_status(clicker_state)

    def start_new_audio_clip(self, clipPath):
        mixer.music.stop()
        mixer.music.load(clipPath)
        mixer.music.play()
        self.current_audio_clips_state = self.current_state

    def service_audio(self):
        if self.current_audio_clips_state is None:
            return

        if self.current_state != self.current_audio_clips_state:
            mixer.music.stop()
            self.current_audio_clips_state = None

    def service_current_state(self):
        if self.current_state == "SETTING_UP":
            if self.last_initialized_state != self.current_state:
                if self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                    pass
                else:
                    self.last_initialized_state = self.current_state
            elif self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "FAMILY_PICTURES":
            if self.last_initialized_state != self.current_state:
                if self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                    pass
                else:
                    self.last_initialized_state = self.current_state
            elif self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "GROUP_PICTURES":
            if self.last_initialized_state != self.current_state:
                if self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                    pass
                else:
                    self.last_initialized_state = self.current_state
            elif self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "REGINA_ARRIVES":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/bangingNoisesInFireplace.mp3')
            elif not mixer.music.get_busy():
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "REGINA_EXPLAINS":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/ReginaStuckInFireplace.mp3')
            elif not mixer.music.get_busy():
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "DINNER":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state

            if self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "FOGGER_WARMUP":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.warmup_time = time.time()
            elif time.time() > (self.warmup_time + 300):
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "FOGGER_COUNTDOWN":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state

        elif self.current_state == "POISONING":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state

            if self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "EVIL_ANNOUNCEMENT":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/evilAnnouncement.mp3')
            elif not mixer.music.get_busy():
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "CAST_PROHIBERE":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/ohNoYouAreGettingPoisonedDoProhiber.mp3')
                self.time_in_cast_state = time.time()
            elif (time.time() > (self.time_in_cast_state + 10)) and (not mixer.music.get_busy()):
                self.time_in_cast_state = None
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "WAIT_ON_PROHIBERE":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.time_state_started = time.time()
            elif (self.num_wands_lit > 15) or (time.time() > (self.time_state_started + 20)):
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "FOGGER_OFF":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.time_state_started = time.time()
            elif time.time() > (self.time_state_started + 5):
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "REGINAS_PLAN":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/drat_youHaveAllBeenPoisoned.mp3')
            elif not mixer.music.get_busy():
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "SPELL_BOOKS_APPEAR":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/frigidarium_someoneCheckTheFreezer.mp3')
            elif not mixer.music.get_busy():
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "PASS_OUT_BOOKS":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state

            if self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "ANTIDOTE_EXPLANATION":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/WitchWeeklyJustHadAnArticle.mp3')
            elif not mixer.music.get_busy():
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "REGINA_SUGGESTS_PUMPKIN_CAKE":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
            else:
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "EATING_PUMPKIN_CAKE":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state

            if self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "REGINA_SAYS_YOU_ARE_POISONED":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/TastedGoodAnyoneViolentlyIll.mp3')
            elif (not mixer.music.get_busy()) and (self.gui.ClickerStatus.last_gadget_status == "PROCEED"):
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "REGINA_ASKS_IF_YOU_HAVE_DESERT_TOAD":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/BestNextStepFindDesertToad.mp3')
            elif not mixer.music.get_busy():
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "WAIT_TO_FIND_TOAD":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state

            if self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "REGINA_SAYS_THE_BRAVEST_MUST_EAT_IT":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/OnlyOneToadFindTheBravest.mp3')
            elif not mixer.music.get_busy():
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "CAST_FORTISSIMI":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.time_in_cast_state = time.time()
            elif time.time() > (self.time_in_cast_state + 5):
                self.time_in_cast_state = None
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "WAIT_ON_FORTISSIMI":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
            elif self.last_wand_status["Isaac"] == "LIT":
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "EAT_TOAD":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/eatIt.mp3')
            elif (not mixer.music.get_busy()) and (self.gui.ClickerStatus.last_gadget_status == "PROCEED"):
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "REGINA_SUGGESTS_KOUING_AMAN":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/NeedSomethingWithBaneberrry.mp3')
            elif not mixer.music.get_busy():
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "EAT_KOUING_AMAN":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state

            if self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "REGINA_SUGGESTS_POPCORN":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/isWitchWeeklyHelping_FindHorklumpJuice.mp3')
            elif not mixer.music.get_busy():
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "EAT_POPCORN":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state

            if self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "REGINA_SUGGESTS_COCKROACH_CLUSTERS":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/FindPearlDustDontEatItYet.mp3')
            elif (not mixer.music.get_busy()) and (self.gui.ClickerStatus.last_gadget_status == "PROCEED"):
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "REGINA_EXPLAINS_RISUS_MAGNA":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/NotEnoughCastRisusMagna.mp3')
            elif not mixer.music.get_busy():
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "CAST_RISUS_MAGNA":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.time_in_cast_state = time.time()
            elif time.time() > (self.time_in_cast_state + 5):
                self.time_in_cast_state = None
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "WAIT_ON_RISUS_MAGNA":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state

            else:
                num_randalls_lit = 0
                if self.last_wand_status["Sam"] == "LIT":
                    num_randalls_lit += 1
                if self.last_wand_status["Erin"] == "LIT":
                    num_randalls_lit += 1
                if self.last_wand_status["Sariah"] == "LIT":
                    num_randalls_lit += 1
                if self.last_wand_status["Emma"] == "LIT":
                    num_randalls_lit += 1
                if self.last_wand_status["Hyrum"] == "LIT":
                    num_randalls_lit += 1

                if num_randalls_lit >= 3:
                    self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "HYSTERICAL_LAUGHING":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state

            if self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "REGINA_EXPLAINS_LINGUA_GUSTARE":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/IsThereAnyLichenPowder.mp3')
            elif not mixer.music.get_busy():
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "CAST_LINGUA_GUSTARE":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.time_in_cast_state = time.time()
            elif time.time() > (self.time_in_cast_state + 5):
                self.time_in_cast_state = None
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "WAIT_ON_LINGUA_GUSTARE":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.time_state_started = time.time()
            elif (self.num_wands_lit > 15) or (time.time() > (self.time_state_started + 20)):
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "EAT_CAULDRON_CAKES":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state

            if self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "REGINA_SAYS_FIND_DRAGONFLY_THORAX":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/IsThereAnyDragonflyThorax.mp3')
            elif not mixer.music.get_busy():
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "FINDING_DRAGONFLY_THORAX":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state

            if self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "NOT_ENOUGH_NEED_THE_BEST_CANTANTA_CANTICUM_SPELL":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/NotEnoughFindBestSingers.mp3')
            elif not mixer.music.get_busy():
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "CAST_CANTATA_CANTICUM":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.time_in_cast_state = time.time()
            elif time.time() > (self.time_in_cast_state + 5):
                self.time_in_cast_state = None
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "WAIT_ON_CANTATA_CANTICUM":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
            elif (self.last_wand_status["Amber"] == "LIT") and (self.last_wand_status["Alexis"] == "LIT"):
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "EAT_CHOCOLATE_KEYS":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/GoodGoAheadAndEatIt.mp3')
            elif not mixer.music.get_busy():
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "PEDERSENS_SING":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state

            if self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "REGINA_DEPARTS_IN_A_RUSH_SAYS_USE_DENTIS_FORTIS":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.start_new_audio_clip(clipPath='./audioClips/ScreamFindFairyTeeth.mp3')
            elif not mixer.music.get_busy():
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "CAST_DENTIS_FORTIS":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.time_in_cast_state = time.time()
            elif time.time() > (self.time_in_cast_state + 5):
                self.time_in_cast_state = None
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "WAIT_ON_DENTIS_FORTIS":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state
                self.time_state_started = time.time()
            elif (self.num_wands_lit > 15) or (time.time() > (self.time_state_started + 20)):
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "EAT_GOLD_ROCKS":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state

            if self.gui.ClickerStatus.last_gadget_status == "PROCEED":
                self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

        elif self.current_state == "CRAFT_CURE":
            if self.last_initialized_state != self.current_state:
                self.last_initialized_state = self.current_state






if __name__ == "__main__":
    tea = TheDarkPoison()

    tea.run()