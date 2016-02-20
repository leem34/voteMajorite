# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from twisted.internet import defer
from util import utiltools
import voteMajoriteParams as pms
from voteMajoriteGui import DConfig
import random
from util.utili18n import le2mtrans
import voteMajoriteTexts as texts_VM


logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        # creation of the menu (will be placed in the "part" menu on the
        # server screen)
        actions = OrderedDict()
        actions[le2mtrans(u"Configure")] = self._configure
        actions[le2mtrans(u"Display parameters")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), le2mtrans(u"Parameters"))
        actions[le2mtrans(u"Start")] = lambda _: self._demarrer()
        actions[le2mtrans(u"Display payoffs")] = \
            lambda _: self._le2mserv.gestionnaire_experience.\
            display_payoffs_onserver("voteMajorite")
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            texts_VM.trans_VM(u"Majority Vote"), actions)

        self._profils = None

    def _configure(self):
        """
        To make changes in the parameters
        :return:
        """
        screen = DConfig(self._le2mserv.gestionnaire_graphique.screen)
        if screen.exec_():
            self._profils = screen.get_profiles()
            self._le2mserv.gestionnaire_graphique.infoserv(
                texts_VM.trans_VM(u"Profiles") + u": {}".format(self._profils))

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Start the part
        :return:
        """
        # check conditions =====================================================
        if not self._profils:
            self._le2mserv.gestionnaire_graphique.display_error(
                texts_VM.trans_VM(u"Profiles not defined, please configure the part"))
            return
        if len(self._profils) < \
            self._le2mserv.gestionnaire_joueurs.nombre_joueurs / pms.TAILLE_GROUPES:
            self._le2mserv.gestionnaire_graphique.display_error(
                texts_VM.trans_VM(u"There is not enougth profiles compared to groups"))
            return
        if self._le2mserv.gestionnaire_joueurs.nombre_joueurs % \
            pms.TAILLE_GROUPES != 0:
            self._le2mserv.gestionnaire_graphique.display_error(
                le2mtrans(u"The number of players is not compatible with the "
                          u"group size"))
            return

        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(le2mtrans(u"Start") + u" voteMajorite?")
        if not confirmation:
            return

        # init part ============================================================
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "voteMajorite", "PartieVM", "RemoteVM", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'voteMajorite')

        # configure part (player and remote)
        yield (self._le2mserv.gestionnaire_experience.run_step(
            le2mtrans(u"Configure"), self._tous, "configure"))

        # groups
        self._le2mserv.gestionnaire_groupes.former_groupes(
            self._le2mserv.gestionnaire_joueurs.get_players(),
            pms.TAILLE_GROUPES, forcer_nouveaux=True)

        # set profiles
        self._le2mserv.gestionnaire_graphique.infoserv(u"Groups - profiles")
        cpteur = 0
        for g, m in self._le2mserv.gestionnaire_groupes.get_groupes(
                "voteMajorite").iteritems():
            self._le2mserv.gestionnaire_graphique.infoserv(
                u"G{}: {} -> {}".format(g.split("_")[2], self._profils[cpteur],
                                        pms.PROFILES[self._profils[cpteur]]))
            for j in m:
                j.set_profile(self._profils[cpteur])
            cpteur += 1
    
        # Start part ===========================================================
        for period in xrange(1 if pms.NOMBRE_PERIODES else 0,
                        pms.NOMBRE_PERIODES + 1):

            if self._le2mserv.gestionnaire_experience.stop_repetitions:
                break

            # init period
            self._le2mserv.gestionnaire_graphique.infoserv(
                [None, le2mtrans(u"Period") + u" {}".format(period)])
            self._le2mserv.gestionnaire_graphique.infoclt(
                [None, le2mtrans(u"Period") + u" {}".format(period)],
                fg="white", bg="gray")
            yield (self._le2mserv.gestionnaire_experience.run_func(
                self._tous, "newperiod", period))
            
            # decision
            yield(self._le2mserv.gestionnaire_experience.run_step(
                le2mtrans(u"Decision"), self._tous, "display_decision"))

            # in favor of, against, majority
            self._le2mserv.gestionnaire_graphique.infoserv(u"Votes")
            votes_contre = sum([j.currentperiod.VM_decision for j in
                                self._le2mserv.gestionnaire_joueurs.get_players(
                                    "voteMajorite")])
            votes_pour = self._le2mserv.gestionnaire_joueurs.nombre_joueurs - \
                         votes_contre
            if votes_pour > votes_contre:
                majority = pms.IN_FAVOR
            elif votes_pour < votes_contre:
                majority = pms.AGAINST
            else:
                majority = random.randint(0, 1)
            for j in self._le2mserv.gestionnaire_joueurs.get_players(
                    "voteMajorite"):
                j.currentperiod.VM_pour = votes_pour
                j.currentperiod.VM_contre = votes_contre
                j.currentperiod.VM_majority = majority
            self._le2mserv.gestionnaire_graphique.infoserv(
                texts_VM.trans_VM(u"In favor") + u" {}, ".format(votes_pour) +
                texts_VM.trans_VM(u"Against") + u" {},".format(votes_contre) +
                texts_VM.trans_VM(u"Majority") + u" {}".format(
                    texts_VM.get_vote(majority)))

            # period payoffs
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "voteMajorite")

        # summary: only at the end of the part
        yield (self._le2mserv.gestionnaire_experience.run_step(
            le2mtrans(u"Summary"), self._tous, "display_summary"))
        
        # End of part ----------------------------------------------------------
        yield (self._le2mserv.gestionnaire_experience.finalize_part(
            "voteMajorite"))
