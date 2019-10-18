from PiHat import PiHat
x


game_states = ( ("SETTING_UP", ""),
                ("FAMILY_PICTURES", ""),
                ("GROUP_PICTURES", ""),
                ("REGINA_ARRIVES", ""),
                ("REGINA_EXPLAINS", ""),
                ("DINNER", ""),
                ("FOGGER_WARMUP", ""),
                ("FOGGER_COUNTDOWN", ""),
                ("POISONING", ""),
                ("EVIL_ANNOUNCEMENT", ""),
                ("CAST_PROHIBERE", ""),
                ("WAIT_ON_PROHIBERE", ""),
                ("FOGGER_OFF", ""),
                ("REGINAS_PLAN", ""),
                ("SPELL_BOOKS_APPEAR", ""),
                ("PASS_OUT_BOOKS", ""),
                ("ANTIDOTE_EXPLANATION", ""),
                ("REGINA_SUGGESTS_PUMPKIN_CAKE", ""),
                ("EATING_PUMPKIN_CAKE", ""),
                ("CAST_AFFLICTO", ""),
                ("WAIT_ON_AFFLICTO", ""),
                ("REGINA_SAYS_YOU_ARE_POISONED", ""),
                ("REGINA_ASKS_IF_YOU_HAVE_DESERT_TOAD", ""),
                ("WAIT_TO_FIND_TOAD", ""),
                ("REGINA_SAYS_THE_BRAVEST_MUST_EAT_IT", ""),
                ("CAST_FORTISSIMI", ""),
                ("WAIT_ON_FORTISSIMI", ""),
                ("EAT_TOAD", ""),
                ("REGINA_SUGGESTS_KOUING_AMAN", ""),
                ("EAT_KOUING_AMAN", ""),
                ("REGINA_SUGGESTS_POPCORN", ""),
                ("EAT_POPCORN", ""),
                ("REGINA_SUGGESTS_COCKROACH_CLUSTERS", ""),
                ("REGINA_EXPLAINS_RISUS_MAGNA", ""),
                ("CAST_RISUS_MAGNA", ""),
                ("WAIT_ON_RISUS_MAGNA", ""),
                ("HYSTERICAL_LAUGHING", ""),
                ("REGINA_EXPLAINS_LINGUA_GUSTARE", ""),
                ("CAST_LINGUA_GUSTARE", ""),
                ("WAIT_ON_LINGUA_GUSTARE", ""),
                ("EAT_CAULDRON_CAKES", ""),
                ("REGINA_SAYS_FIND_DRAGONFLY_THORAX", ""),
                ("FINDING_DRAGONFLY_THORAX", ""),
                ("NOT_ENOUGH_NEED_THE_BEST_CANTANTA_CANTICUM_SPELL", ""),
                ("CAST_CANTATA_CANTICUM", ""),
                ("WAIT_ON_CANTATA_CANTICUM", ""),
                ("EAT_CHOCOLATE_KEYS", ""),
                ("PEDERSENS_SING", ""),
                ("REGINA_DEPARTS_IN_A_RUSH_SAYS_USE_DENTIS_FORTIS", ""),
                ("CAST_DENTIS_FORTIS", ""),
                ("WAIT_ON_DENTIS_FORTIS", ""),
                ("EAT_GOLD_ROCKS", ""),
                ("CRAFT_CURE", ""))



class Table(PiHat):
    TABLE_PORT = 10108

    def __init__(self):
        super().__init__(port=self.TABLE_PORT, client_id="Table")

    def service_current_state(self):
        if self.state_change_to_be_serviced:
            print("Servicing new game state: {}".format(self.current_game_state))
            self.state_change_to_be_serviced = False

            if ((self.current_game_state == "FOGGER_WARMUP") or
                (self.current_game_state == "FOGGER_COUNTDOWN") or
                (self.current_game_state == "POISONING") or
                (self.current_game_state == "EVIL_ANNOUNCEMENT")):
                self.SetRelay(1, True)
            else:
                self.SetRelay(1, False)


            if ((self.current_game_state == "POISONING") or
                (self.current_game_state == "EVIL_ANNOUNCEMENT")):
                self.SetRelay(2, True)
            else:
                self.SetRelay(2, False)


            if ((self.current_game_state == "FAMILY_PICTURES") or
                (self.current_game_state == "GROUP_PICTURES") or
                (self.current_game_state == "REGINA_ARRIVES") or
                (self.current_game_state == "REGINA_EXPLAINS") or
                (self.current_game_state == "DINNER") or
                (self.current_game_state == "FOGGER_WARMUP")):
                self.set_piHat_state(self.BLINK_STATE_WARM_TWINKLE)
            elif (self.current_game_state == "FOGGER_COUNTDOWN"):
                self.set_piHat_state(self.BLINK_STATE_RED_SNAKE)
            else:
                self.set_piHat_state(self.BLINK_STATE_OFF)
            


if __name__ == "__main__":
    table = Table()

    table.run()
