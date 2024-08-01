from datetime import date

from business_logic.controllers.category_controller import CategoryController
from business_logic.controllers.category_percentage_record_controller import CategoryPercentageRecordController
from business_logic.controllers.pocket_category_balance_record_controller import PocketCategoryBalanceRecordController
from business_logic.controllers.pocket_controller import PocketController
from business_logic.controllers.transaction_controller import TransactionController
from business_logic.controllers.transaction_type_controller import TransactionTypeController
from business_logic.controllers.transaction_type_strategy_controller import TransactionTypeStrategyController
from controller_manager import ControllerManager


def main():
    category_controller = CategoryController()
    category_percentage_record_controller = CategoryPercentageRecordController()
    pocket_category_balance_record_controller = PocketCategoryBalanceRecordController()
    pocket_controller = PocketController()
    transaction_controller = TransactionController()
    transaction_type_controller = TransactionTypeController()
    transaction_type_strategy_controller = TransactionTypeStrategyController()

    controller_manager = ControllerManager()
    controller_manager.register_controller('CategoryController', category_controller)
    controller_manager.register_controller('CategoryPercentageRecordController', category_percentage_record_controller)
    controller_manager.register_controller(
        'PocketCategoryBalanceRecordController',
        pocket_category_balance_record_controller
    )
    controller_manager.register_controller('PocketController', pocket_controller)
    controller_manager.register_controller('TransactionController', transaction_controller)
    controller_manager.register_controller('TransactionTypeController', transaction_type_controller)
    controller_manager.register_controller('TransactionTypeStrategyController', transaction_type_strategy_controller)

    # pocket_category_balance_record_controller.delete_all_records()
    pocket_category_balance_record_controller.update_last_12_months()
    # show_pocket_category_balance_records(pocket_category_balance_record_controller)
    # transaction_controller.delete_transaction_by_id(6)




def show_pocket_category_balance_records(
    pocket_category_balance_record_controller: PocketCategoryBalanceRecordController
):
    records = pocket_category_balance_record_controller.get_all_records()
    for record in records:
        print(record)


if __name__ == '__main__':
    main()
