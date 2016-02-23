# -*- coding: utf-8 -*-

import logging
from PyQt4 import QtGui, QtCore
import voteMajoriteParams as pms
import voteMajoriteTexts as texts_VM
from voteMajoriteGuiSrc import VM_pol
from client.cltgui.cltguiwidgets import WExplication, WRadio, WListDrag, \
    WTableview, WLineEdit
from client.cltgui.cltguitablemodels import TableModelHistorique
from util.utili18n import le2mtrans
from client.cltgui.cltguidialogs import DQuestFinal


logger = logging.getLogger("le2m")


class WPolitics(QtGui.QWidget):
    def __init__(self, parent, profil, period):
        super(WPolitics, self).__init__(parent)
        self.ui = VM_pol.Ui_Form()
        self.ui.setupUi(self)

        stylesheet_normal = "border: 1px solid black; font-weight: bold; " \
                            "color: black; font-size:1.2em;"
        stylesheet_period = "border: 1px solid blue; font-weight: bold; " \
                            "color: blue; font-size:1.2em;"

        for i in range(1, 5):
            getattr(self.ui, "label_pol_{}".format(i)).setText(
                texts_VM.trans_VM(u"Policy") + u" {}".format(i))
            getattr(self.ui, "label_val_{}".format(i)).setText(str(profil[i-1]))
            if i == period:
                getattr(self.ui, "label_pol_{}".format(i)).setStyleSheet(
                    stylesheet_period)
                getattr(self.ui, "label_val_{}".format(i)).setStyleSheet(
                    stylesheet_period)
            else:
                getattr(self.ui, "label_pol_{}".format(i)).setStyleSheet(
                    stylesheet_normal)
                getattr(self.ui, "label_val_{}".format(i)).setStyleSheet(
                    stylesheet_normal)


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, periode, profil):
        """

        :param defered:
        :param automatique:
        :param parent:
        :param periode:
        :param profil: only the table
        :return:
        """
        super(GuiDecision, self).__init__(parent)

        # variables
        self._defered = defered
        self._automatique = automatique

        self._layout = QtGui.QVBoxLayout(self)

        # Explanation
        self._wexplanation = WExplication(
            text=texts_VM.get_text_explanation(periode, profil), parent=self,
            size=(450, 80))
        self._layout.addWidget(self._wexplanation)

        # Politics
        self._wpolitics = WPolitics(self, profil, periode)
        self._layout.addWidget(self._wpolitics)

        # Vote
        votes = tuple([v for k, v in sorted(texts_VM.VOTES.viewitems())])
        self._wvote = WRadio(
            label=texts_VM.trans_VM(u"You vote"), texts=votes,
            automatique=self._automatique, parent=self)
        self._layout.addWidget(self._wvote)

        # buttons
        self._buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        self._buttons.accepted.connect(self._accept)
        self._layout.addWidget(self._buttons)

        # title and size
        self.setWindowTitle(le2mtrans(u"Decision"))
        self.adjustSize()
        self.setFixedSize(self.size())

        # automatic
        if self._automatique:
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(
                self._buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer_automatique.start(7000)
                
    def reject(self):
        pass
    
    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass

        try:
            decision = self._wvote.get_checkedbutton()
        except ValueError:
            return QtGui.QMessageBox.warning(
                self, le2mtrans(u"Warning"),
                texts_VM.trans_VM(u"You must vote"))

        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, le2mtrans(u"Confirmation"),
                le2mtrans(u"Do you confirm your choice?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes: 
                return

        logger.info(u"Send back: {}".format(decision))
        self.accept()
        self._defered.callback(decision)


class DSummary(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, profile, text_summary,
                 list_summary):
        super(DSummary, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique

        layout = QtGui.QVBoxLayout(self)

        wexplanation = WExplication(
            text=text_summary, parent=self, size=(600, 100))
        layout.addWidget(wexplanation)

        wprofiles = WPolitics(
            parent=self, profil=profile, period=0)
        layout.addWidget(wprofiles)

        model_summary = TableModelHistorique(list_summary)
        wsummary = WTableview(
            parent=self, tablemodel=model_summary, size=(600, 160))
        wsummary.ui.tableView.verticalHeader().setResizeMode(
            QtGui.QHeaderView.Stretch)
        layout.addWidget(wsummary)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(le2mtrans(u"Summary"))
        self.adjustSize()
        self.setFixedSize(self.size())

        if self._automatique:
            self._timerauto = QtCore.QTimer()
            self._timerauto.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timerauto.start(7000)

    def _accept(self):
        try:
            self._timerauto.stop()
        except AttributeError:
            pass
        self.accept()
        self._defered.callback(True)

    def reject(self):
        pass


class DConfig(QtGui.QDialog):
    def __init__(self, parent):
        super(DConfig, self).__init__(parent)
        layout = QtGui.QVBoxLayout(self)

        self._wexplanation = WExplication(
            text=texts_VM.trans_VM(
                u"Select in the list on the left the profiles you want in "
                u"the session and put it in the list on the right."),
            parent=self, size=(400, 80))
        layout.addWidget(self._wexplanation)

        self._wlistdrag = WListDrag(
            parent=self, size=(120, 150))
        profils = sorted(pms.PROFILES.viewkeys())
        self._wlistdrag.ui.listWidget_left.addItems(profils)
        layout.addWidget(self._wlistdrag)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Cancel |QtGui.QDialogButtonBox.Ok)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setWindowTitle(le2mtrans(u"Configure"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def get_profiles(self):
        return self._wlistdrag.get_rightitems()


class DEchelle(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, num_question):
        super(DEchelle, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique

        layout = QtGui.QVBoxLayout(self)

        self._radios = WRadio(
            parent=self, automatique=self._automatique,
            label=texts_VM.get_text_question(num_question),
            texts=texts_VM.get_items_question(num_question))
        layout.addWidget(self._radios)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(le2mtrans(u"Question"))
        self.adjustSize()
        self.setFixedSize(self.size())

        if self._automatique:
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer_automatique.start(7000)

    def reject(self):
        pass

    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass

        try:
            checked = self._radios.get_checkedbutton()
        except ValueError:
            return QtGui.QMessageBox.warning(
                self, le2mtrans(u"Warning"),
                texts_VM.trans_VM(u"You must select one item"))

        if not self._automatique:
            confirm = QtGui.QMessageBox.question(
                self, le2mtrans(u"Confirmation"),
                le2mtrans(u"Do you confirm your choice?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirm != QtGui.QMessageBox.Yes:
                return

        logger.info(u"Send back: {}".format(checked))
        self.accept()
        self._defered.callback(checked)


class DQuestFinalVM(DQuestFinal):
    def __init__(self, defered, automatique, parent):
        DQuestFinal.__init__(self, defered, automatique, parent)

        self._naissance_ville = WLineEdit(
            parent=self, automatique=self._automatique,
            label=texts_VM.trans_VM(u"Town of birth"),
            list_of_possible_values=[u"Paris", u"Marseille", u"Lyon",
                                     u"Montpellier"])
        self._gridlayout.addWidget(self._naissance_ville, 0, 2)

        self.adjustSize()
        self.setFixedSize(self.size())

    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass
        inputs = self._get_inputs()
        if inputs:

            try:
                inputs["naissance_ville"] = self._naissance_ville.get_text()
            except ValueError:
                return QtGui.QMessageBox.warning(
                    self, le2mtrans(u"Warning"),
                    le2mtrans(u"You must answer to all the questions"))

            if not self._automatique:
                if QtGui.QMessageBox.question(
                    self, le2mtrans(u"Confirmation"),
                    le2mtrans(u"Do you confirm your answers?"),
                    QtGui.QMessageBox.No | QtGui.QMessageBox.Yes) != \
                        QtGui.QMessageBox.Yes: return

            logger.info(u"Send back: {}".format(inputs))
            self.accept()
            self._defered.callback(inputs)

        else:
            return