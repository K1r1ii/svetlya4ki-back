import uuid

from tests.user_utils import COMPANY_ID

CATEGORY_ID =  uuid.uuid4()

ITEM_1_ID =  uuid.uuid4()
ITEM_2_ID =  uuid.uuid4()


CATEGORY_1 = {
    "id": str(CATEGORY_ID),
    "company_id": str(COMPANY_ID),
    "name": "test"
}

CATEGORY_1_TUPLE = tuple(CATEGORY_1.values())

ITEM_1 = {
    "id": str(ITEM_1_ID),
    "company_id": str(COMPANY_ID),
    "category_id": str(CATEGORY_ID),
    "name": "test_item",
    "total_quantity": 10
}

ITEM_1_TUPLE = tuple(ITEM_1.values())
