from ..model import Model
from ..view import MainView
class VCAbstractMixin(object):
    model: Model
    main: MainView
    def establish_connection(self):
        """
        Abstract method
        Returns
        -------

        """
        pass