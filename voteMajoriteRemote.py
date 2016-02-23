# -*- coding: utf-8 -*-

import logging
import random
from client.cltremote import IRemote
from twisted.internet import defer
import voteMajoriteParams as pms
import voteMajoriteTexts as texts_VM
from voteMajoriteGui import GuiDecision, DSummary, DEchelle, DQuestFinal


logger = logging.getLogger("le2m")


class RemoteVM(IRemote):
    def __init__(self, le2mclt):
        IRemote.__init__(self, le2mclt)
        self._histo_vars = [
            "VM_period", "VM_decision", "VM_majority", "VM_periodpayoff"]
        self.histo.append(texts_VM.get_histo_head())

    def remote_configure(self, params):
        logger.info(u"{} configure".format(self.le2mclt.uid))
        for k, v in params.iteritems():
            setattr(pms, k, v)

    def remote_newperiod(self, periode):
        logger.info(u"{} Period {}".format(self.le2mclt.uid, periode))
        self.currentperiod = periode
        if self.currentperiod == 1:
            del self.histo[1:]

    def remote_display_decision(self, profile):
        logger.info(u"{} Decision".format(self.le2mclt.uid))
        if self.le2mclt.simulation:
            decision = random.randint(0, 1)
            logger.info(u"{} Send back {}".format(self.le2mclt.uid, decision))
            return decision
        else: 
            defered = defer.Deferred()
            ecran_decision = GuiDecision(
                defered, self.le2mclt.automatique,
                self.le2mclt.screen, self.currentperiod, profile)
            ecran_decision.show()
            return defered

    def remote_display_summary(self, periods_content, profile):
        logger.info(u"{} Summary".format(self.le2mclt.uid))
        self.histo.extend(self._get_histo_content(periods_content))
        if self.le2mclt.simulation:
            return 1
        else:
            defered = defer.Deferred()
            ecran_recap = DSummary(
                defered, self.le2mclt.automatique, self.le2mclt.screen,
                text_summary=texts_VM.get_text_summary(periods_content),
                list_summary=self.histo, profile=profile)
            ecran_recap.show()
            return defered

    def _get_histo_content(self, periods_content):
        hc = []
        for line in periods_content:
            histo_line = []
            for v in self._histo_vars:
                if v in ["VM_decision", "VM_majority"]:
                    histo_line.append(texts_VM.get_vote(line.get(v)))
                else:
                    histo_line.append(line.get(v))
            hc.append(histo_line)
        return hc

    def remote_display_additionalquestion(self, num_question):
        logger.info(u"{} remote_display_additionalquestion({})".format(
            self.le2mclt.uid, num_question))
        if self.le2mclt.simulation:
            checked = random.choice(texts_VM.get_items_question(num_question))
            logger.info(u"{} send back {}".format(self.le2mclt.uid, checked))
            return int(checked)
        else:
            defered = defer.Deferred()
            screen = DEchelle(defered, self.le2mclt.automatique,
                              self.le2mclt.screen, num_question)
            screen.show()
            return defered

    def remote_display_finalquest(self):
        logger.info(u"{} remote_display_finalquest".format(self.le2mclt.uid))
        if self.le2mclt.simulation:
            from datetime import datetime
            inputs = {}
            today_year = datetime.now().year
            inputs['naissance'] = today_year - random.randint(16, 60)
            inputs['genre'] = random.randint(0, 1)
            inputs['nationalite'] = random.randint(1, 100)
            inputs['couple'] = random.randint(0, 1)
            inputs['etudiant'] = random.randint(0, 1)
            if inputs['etudiant']:
                inputs['etudiant_discipline'] = random.randint(1, 10)
                inputs['etudiant_niveau'] = random.randint(1, 6)
            inputs['experiences'] = random.randint(0, 1)
            inputs["fratrie_nombre"] = random.randint(0, 10)
            if inputs["fratrie_nombre"] > 0:
                inputs["fratrie_rang"] = random.randint(
                    1, inputs["fratrie_nombre"] + 1)
            else: inputs["fratrie_rang"] = 0
            # sportivité
            inputs["sportif"] = random.randint(0, 1)
            if inputs["sportif"]:
                inputs["sportif_type"] = random.randint(0, 1)
                inputs["sportif_competition"] = random.randint(0, 1)
            # religiosité
            inputs['religion_place'] = random.randint(1, 4)
            inputs['religion_croyance'] = random.randint(1, 4)
            inputs['religion_nom'] = random.randint(1, 6)
            # additional variables
            inputs["naissance_ville"] = random.choice(
                [u"Paris", u"Montpellier", u"Marseille", u"Nice", u"Toulouse"])
            logger.info(u"Renvoi: {}".format(inputs))
            return inputs
        else:
            defered = defer.Deferred()
            screen = DQuestFinal(defered, self.le2mclt.automatique,
                                   self.le2mclt.screen)
            screen.show()
            return defered
