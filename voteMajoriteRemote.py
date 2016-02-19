# -*- coding: utf-8 -*-

import logging
import random
from client.cltremote import IRemote
from twisted.internet import defer
import voteMajoriteParams as pms
import voteMajoriteTexts as texts_VM
from voteMajoriteGui import GuiDecision, DSummary


logger = logging.getLogger("le2m")


class RemoteVM(IRemote):
    def __init__(self, le2mclt):
        IRemote.__init__(self, le2mclt)
        self._histo_vars = [
            "VM_period", "VM_decision", "VM_majority", "VM_periodpayoff"]
        self.histo.append(texts_VM.get_histo_head())

    def remote_configure(self, params):
        logger.info(u"{} configure".format(self._le2mclt.uid))
        for k, v in params.iteritems():
            setattr(pms, k, v)

    def remote_newperiod(self, periode):
        logger.info(u"{} Period {}".format(self._le2mclt.uid, periode))
        self.currentperiod = periode
        if self.currentperiod == 1:
            del self.histo[1:]

    def remote_display_decision(self, profile):
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            decision = random.randint(0, 1)
            logger.info(u"{} Send back {}".format(self._le2mclt.uid, decision))
            return decision
        else: 
            defered = defer.Deferred()
            ecran_decision = GuiDecision(
                defered, self._le2mclt.automatique,
                self._le2mclt.screen, self.currentperiod, profile)
            ecran_decision.show()
            return defered

    def remote_display_summary(self, periods_content, profile):
        logger.info(u"{} Summary".format(self._le2mclt.uid))
        for line in periods_content:
            self.histo.append([line.get(k) for k in self._histo_vars])
        if self._le2mclt.simulation:
            return 1
        else:
            defered = defer.Deferred()
            ecran_recap = DSummary(
                defered, self._le2mclt.automatique, self._le2mclt.screen,
                text_summary=texts_VM.get_text_summary(periods_content),
                list_summary=self.histo, profile=profile)
            ecran_recap.show()
            return defered
