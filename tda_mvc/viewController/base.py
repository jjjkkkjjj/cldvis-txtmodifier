from ..model import Model
from ..view import *

class VCAbstractMixin(object):

    ### Attributes ###
    model: Model
    main: MainView
    menu: MenuBar

    ### property ###
    leftdock: LeftDockView
    central: CentralView
    rightdock: RightDockView

    def establish_connection(self):
        """
        Abstract method
        Returns
        -------

        """
        pass

    def updateModel(self):
        pass

    def updateAllUI(self):
        pass