from business_logic.controllers.controller import Controller


class ControllerManager:
    def __init__(self):
        self.controllers: dict[str, Controller] = {}

    def register_controller(self, name: str, controller: Controller) -> None:
        self.controllers[name] = controller
        controller.set_controller_manager(self)

    def get_controller(self, name):
        return self.controllers.get(name)
