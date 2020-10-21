import models.station_obj as station_object
import models.well as well


class Station(station_object.StationObject):
    """
    """

    def __init__(self):
        self.well = well.Well()
