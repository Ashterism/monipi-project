


class Sensorstate:
    """
    Holds / controls state for sensor initialisation
    to support not initialising in dev mode (i.e. on
    a mac which doesn't support it), and avoiding
    repeatedly re-initialising.
    """

    def __init__(self):
        # None equates to not initialised yet
        self.pms = None

    def scd30(self):
        # code goes here
        ...

    def pms5003_initialise(self):
        # initialise PMS5003 device on serial
        # only in prod, not dev (not supported on mac)
        from pms5003 import PMS5003
        self.pms = PMS5003(device="/dev/serial0", baudrate=9600)

    def pms5003_check(self):
        # check if "nothing" initialised
        if self.pms is None:
            self.pms5003_initialise()
        else:
            return
