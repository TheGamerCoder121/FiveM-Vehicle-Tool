import sys
import logging
from PyQt6.QtWidgets import QApplication
from meta_tool_gui import MetaToolGUI

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('MetaTool')

def main():
    try:
        logger.info("Starting application")
        app = QApplication(sys.argv)
        logger.info("Created QApplication")

        window = MetaToolGUI()
        logger.info("Created main window")

        window.show()
        logger.info("Showing main window")

        return app.exec()
    except Exception as e:
        logger.exception("Fatal error in main loop")
        return 1

if __name__ == '__main__':
    sys.exit(main())