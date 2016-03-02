# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey, String

from server.servbase import Base
from server.servparties import Partie
from util.utiltools import get_module_attributes
import voteMajoriteParams as pms
import voteMajoriteTexts as texts_VM


logger = logging.getLogger("le2m")


class PartieVM(Partie):
    __tablename__ = "partie_voteMajorite"
    __mapper_args__ = {'polymorphic_identity': 'voteMajorite'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsVM')

    def __init__(self, le2mserv, joueur):
        super(PartieVM, self).__init__("voteMajorite", "VM")
        self._le2mserv = le2mserv
        self.joueur = joueur
        self.VM_gain_ecus = 0
        self.VM_gain_euros = 0
        self._profile = None

    def set_profile(self, profile):
        self._profile = profile

    @defer.inlineCallbacks
    def configure(self):
        logger.debug(u"{} Configure".format(self.joueur))
        yield (self.remote.callRemote("configure", get_module_attributes(pms)))
        self.joueur.info(u"Ok")

    @defer.inlineCallbacks
    def newperiod(self, period):
        logger.debug(u"{} New Period".format(self.joueur))
        self.currentperiod = RepetitionsVM(period)
        self.currentperiod.VM_profil = self._profile
        self.currentperiod.VM_group = self.joueur.groupe
        self._le2mserv.gestionnaire_base.ajouter(self.currentperiod)
        self.repetitions.append(self.currentperiod)
        yield (self.remote.callRemote("newperiod", period))
        logger.info(u"{} Ready for period {}".format(self.joueur, period))

    @defer.inlineCallbacks
    def display_decision(self):
        logger.debug(u"{} Decision".format(self.joueur))
        debut = datetime.now()
        self.currentperiod.VM_decision = yield(self.remote.callRemote(
            "display_decision", pms.PROFILES.get(self._profile)))
        self.currentperiod.VM_decisiontime = (datetime.now() - debut).seconds
        self.joueur.info(u"{}".format(self.currentperiod.VM_decision))
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        logger.debug(u"{} Period Payoff".format(self.joueur))
        self.currentperiod.VM_periodpayoff = 0

        if self.currentperiod.VM_majority == pms.IN_FAVOR:  # pour
            self.currentperiod.VM_periodpayoff = \
                pms.PROFILES.get(self._profile)[self.currentperiod.VM_period - 1] - \
                pms.COUTS[self.currentperiod.VM_period - 1]

        # cumulative payoff since the first period
        if self.currentperiod.VM_period < 2:
            self.currentperiod.VM_cumulativepayoff = \
                self.currentperiod.VM_periodpayoff
        else: 
            previousperiod = self.periods[self.currentperiod.VM_period - 1]
            self.currentperiod.VM_cumulativepayoff = \
                previousperiod.VM_cumulativepayoff + \
                self.currentperiod.VM_periodpayoff

        # we store the period in the self.periodes dictionnary
        self.periods[self.currentperiod.VM_period] = self.currentperiod

        logger.debug(u"{} Period Payoff {}".format(
            self.joueur,
            self.currentperiod.VM_periodpayoff))

    @defer.inlineCallbacks
    def display_summary(self, *args):
        logger.debug(u"{} Summary".format(self.joueur))
        periods_content = [v.todict() for k, v in
                           sorted(self.periods.viewitems())]
        yield(self.remote.callRemote(
            "display_summary", periods_content, pms.PROFILES[self._profile]))
        self.joueur.info("Ok")
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def compute_partpayoff(self):
        logger.debug(u"{} Part Payoff".format(self.joueur))

        self.VM_gain_ecus = pms.DOTATION + self.currentperiod.VM_cumulativepayoff
        self.VM_gain_euros = float("{:.2f}".format(
            float(self.VM_gain_ecus) * float(pms.TAUX_CONVERSION)))

        yield (self.remote.callRemote(
            "set_payoffs", self.VM_gain_euros, self.VM_gain_ecus))

        logger.info(u'{} Payoff ecus {} Payoff euros {:.2f}'.format(
            self.joueur, self.VM_gain_ecus, self.VM_gain_euros))

    @defer.inlineCallbacks
    def display_additionalquestion(self):
        logger.debug(u"display_additionalquestion")
        for k in sorted(texts_VM.ADDITIONNAL_QUESTIONS.viewkeys()):
            tmp = yield (self.remote.callRemote(
                "display_additionalquestion", k))
            setattr(self.periods.get(1), "VM_question_{}".format(k), tmp)
        self.joueur.info(u"Ok")
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def display_questfinal(self):
        logger.debug(u"{} display_finalquest".format(self.joueur))
        inputs = yield (self.remote.callRemote("display_finalquest"))
        part_questfinal = self.joueur.get_part("questionnaireFinal")
        for k, v in inputs.viewitems():
            if k == "naissance_ville":
                setattr(self.currentperiod.get(1), "VM_{}".format(k), v)
            else:
                setattr(part_questfinal, k, v)
        self.joueur.info('ok')
        self.joueur.remove_waitmode()



class RepetitionsVM(Base):
    __tablename__ = 'partie_voteMajorite_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_voteMajorite.partie_id"))

    VM_period = Column(Integer)
    VM_treatment = Column(Integer)
    VM_group = Column(Integer)
    VM_profil = Column(String)
    VM_dotation = Column(Integer)
    VM_cout= Column(Integer)
    VM_decision = Column(Integer)
    VM_decisiontime = Column(Integer)
    VM_pour = Column(Integer)
    VM_contre = Column(Integer)
    VM_majority = Column(Integer)
    VM_periodpayoff = Column(Float)
    VM_cumulativepayoff = Column(Float)
    VM_question_1 = Column(Integer)
    VM_question_2 = Column(Integer)
    VM_naissance_ville = Column(String)

    def __init__(self, period):
        self.VM_treatment = pms.TREATMENT
        self.VM_period = period
        self.VM_cout = pms.COUTS[period-1]
        self.VM_dotation = pms.DOTATION
        self.VM_decisiontime = 0
        self.VM_periodpayoff = 0
        self.VM_cumulativepayoff = 0

    def todict(self, joueur=None):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if joueur:
            temp["joueur"] = joueur
        return temp

