class WarDogHardwareController:

    __INTIALISED = False

    def __init__(self):
        if type(self).__INTIALISED:
            raise RuntimeError(
                "Cannot create multiple instances of WarDogHardwareController")

        print("Initialized WarDogHardwareController")

        type(self).__INTIALISED = True

    def reset(self):

        type(self).__INTIALISED = False

        self.__init__()
