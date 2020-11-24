

class SelectionMixin(object):

    def establish_connection(self):
        # call parent(base)'s establish connection from this mixin class
        super(SelectionMixin, self).establish_connection()



class PredictionMixin(object):

    def establish_connection(self):
        # call parent(base)'s establish connection from this mixin class
        super(PredictionMixin, self).establish_connection()