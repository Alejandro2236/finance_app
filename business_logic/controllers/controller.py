from abc import ABC
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from controller_manager import ControllerManager


class Controller(ABC):
    def __init__(self):
        self._controller_manager: Optional['ControllerManager'] = None

    def set_controller_manager(self, controller_manager: 'ControllerManager') -> None:
        self._controller_manager = controller_manager
