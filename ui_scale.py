from PySide6.QtGui import QGuiApplication


class UIScale:
    """
    Scales the UI based on a 1920x1080 design resolution.
    """

    DESIGN_WIDTH = 1920
    DESIGN_HEIGHT = 1080

    _scale = 1.0

    @classmethod
    def initialize(cls):
        screen = QGuiApplication.primaryScreen()

        if screen is None:
            cls._scale = 1.0
            return

        size = screen.availableGeometry()

        scale_x = size.width() / cls.DESIGN_WIDTH
        scale_y = size.height() / cls.DESIGN_HEIGHT

        cls._scale = min(scale_x, scale_y)

        # Never become ridiculously small
        cls._scale = max(0.75, cls._scale)

        # Never become ridiculously large
        cls._scale = min(1.40, cls._scale)

    @classmethod
    def scale(cls, value):
        return int(value * cls._scale)

    @classmethod
    def factor(cls):
        return cls._scale