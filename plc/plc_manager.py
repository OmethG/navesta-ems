from config.excel_loader import ExcelLoader


class PLCManager:
    """
    Manages all PLC communication for the application.

    The dashboard never communicates with the PLC directly.
    It communicates only with PLCManager.
    """

    def __init__(self, excel_path: str):

        self.loader = ExcelLoader(excel_path)

        # Load all PLC monitoring tags
        self.tags = self.loader.load_monitor_tags()

        # Snap7 client will be added later
        self.client = None

    # ---------------------------------------------------------

    def get_tags(self):
        """
        Returns all PLC tags.
        """

        return self.tags


# -------------------------------------------------------------
# Testing
# -------------------------------------------------------------

if __name__ == "__main__":

    manager = PLCManager("data/Details.xlsx")

    print("=" * 60)
    print(f"PLC Tags Loaded : {len(manager.get_tags())}")
    print("=" * 60)

    for tag in manager.get_tags()[:10]:
        print(tag)