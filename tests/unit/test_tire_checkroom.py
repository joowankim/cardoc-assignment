from assertpy import assert_that

from src.tires.dto import Owner


def test_check_in_with_owner_and_trim_ids(tire_checkroom):
    owners = [
        Owner(id="cherry", trim_id=5000),
        Owner(id="banana", trim_id=9000),
        Owner(id="mango", trim_id=5000),
        Owner(id="cherry", trim_id=11000),
    ]
    tire_checkroom.check_in(owners)

    assert_that(tire_checkroom.uow.committed).is_equal_to(True)


def test_tires_of_with_owner_id(tire_checkroom):
    owners = [
        Owner(id="cherry", trim_id=5000),
        Owner(id="banana", trim_id=9000),
        Owner(id="mango", trim_id=5000),
        Owner(id="cherry", trim_id=11000),
    ]
    tire_checkroom.check_in(owners)

    tires = tire_checkroom.tires_of("cherry")
    assert_that(len(tires)).is_equal_to(4)


