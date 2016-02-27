# -*- coding: utf-8 -*-

from util.utiltools import get_pluriel
import voteMajoriteParams as pms
import os
import configuration.configparam as params
import gettext
import logging


logger = logging.getLogger("le2m")
localedir = os.path.join(params.getp("PARTSDIR"), "voteMajorite", "locale")
trans_VM = gettext.translation(
  "voteMajorite", localedir, languages=[params.getp("LANG")]).ugettext


VOTES = {
    pms.IN_FAVOR: trans_VM("In favor"),
    pms.AGAINST: trans_VM("Against")
}


def get_vote(code_or_name):
    logger.debug(u"get_vote with arg {}".format(code_or_name))
    if type(code_or_name) is int:
        return VOTES.get(code_or_name, None)
    elif type(code_or_name) is str:
        for k, v in VOTES.viewitems():
            if v.lower() == code_or_name.lower():
                return k
    return None



ADDITIONNAL_QUESTIONS = {
    1: {
        "text": trans_VM(u"En utilisant l'échelle ci-contre, indiquez votre "
                         u"niveau de certitude au moment où vous avez voté, "
                         u"sachant que<br />"
                         u"1=totalement incertain et 10=totalement certain"),
        "items": map(str, range(1, 11))
    },
    2: {
        "text": trans_VM(u"En utilisant l'échelle ci-contre, indiquez à quel "
                         u"point, <br />vous êtes heureux(se) en ce moment, "
                         u"sachant que<br />"
                         u"1=totalement triste et 7=totalement heureux(se)"),
        "items": map(str, range(1, 8))
    }
}


def get_text_question(num_question):
    return ADDITIONNAL_QUESTIONS.get(num_question)["text"]


def get_items_question(num_question):
    return ADDITIONNAL_QUESTIONS.get(num_question)["items"]


def get_histo_head():
    return [trans_VM(u"Policy"), trans_VM(u"Your vote"),
            trans_VM(u"The majority vote"), trans_VM(u"Your payoff")]


def get_text_summary(periods_content):
    txt = u""
    for line in periods_content:
        txt += \
            trans_VM(u"Policy {}: {} \"In favor\", {} \"Against\", "
                     u"Majority: \"{}\". ").format(
                line.get("VM_period"),
                get_pluriel(line.get("VM_pour"), trans_VM(u"people")),
                get_pluriel(line.get("VM_contre"), trans_VM(u"people")),
                get_vote(line.get("VM_majority")))

        txt += u" <strong>" + trans_VM(u"The policy is" + u" " + u"{}").format(
            trans_VM(u"applied") if \
            line.get("VM_majority") == pms.IN_FAVOR else
            trans_VM(u"is not applied")) + u".</strong><br />"

    gains = [line.get("VM_periodpayoff") for line in periods_content]
    txt += u"<br />" + trans_VM(u"Your payoff is equal to") + \
           u" {} + {} = {}, ".format(
               pms.DOTATION,
               " + ".join(map(str, gains)),
               get_pluriel(periods_content[-1].get(
                   "VM_cumulativepayoff") + pms.DOTATION, pms.MONNAIE)) + \
           trans_VM(u"which corresponds to") + \
           u" {}.".format(get_pluriel((periods_content[-1].get(
               "VM_cumulativepayoff") + pms.DOTATION) * pms.TAUX_CONVERSION,
                                      u"euro"))
    return txt


def get_text_explanation(period, profile):
    txt = trans_VM(u"Policy") + u" {}".format(period)
    txt += u"<br />" + \
           trans_VM(u"If the policy applies it will cost you {} "
                    u"and will provide you a payoff of {}.").format(
            get_pluriel(pms.COUTS[period-1], pms.MONNAIE),
            get_pluriel(profile[period-1], pms.MONNAIE))
    txt += u"<br />" + \
           trans_VM(u"You must vote either in favor of or against the "
                    u"policy.")
    return txt
