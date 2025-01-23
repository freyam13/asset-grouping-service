import pytest

from src.models.schemas import (
    Asset,
    CloudAccount,
    GroupingCondition,
    GroupingRule,
    Operator,
    Tag,
)
from src.services.grouping import GroupingService


@pytest.fixture
def service():
    return GroupingService()


@pytest.fixture
def sample_asset() -> Asset:
    return Asset(
        name="test-instance-prod",
        type="ec2-instance",
        tags=[
            Tag(key="env", value="prod"),
            Tag(key="team", value="platform"),
        ],
        cloud_account=CloudAccount(id="123", name="main"),
        owner_id="user1",
        region="us-east-1",
    )


@pytest.fixture
def sample_rule() -> GroupingRule:
    return GroupingRule(
        group_name="production-instances",
        description="Production EC2 instances",
        conditions=[
            GroupingCondition(
                field="type",
                operator=Operator.EQUALS,
                value="ec2-instance",
            ),
            GroupingCondition(
                field="tag",
                operator=Operator.EQUALS,
                tag_key="env",
                tag_value="prod",
            ),
        ],
    )
