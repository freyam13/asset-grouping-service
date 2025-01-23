from src.models.schemas import Asset, CloudAccount, GroupingCondition, GroupingRule, Tag


def test_auto_grouping_on_asset_creation(service, sample_asset, sample_rule):
    # create rule first
    service.create_rule(sample_rule)

    # create asset; should be automatically grouped
    created = service.create_asset(sample_asset)
    assert created.group_name == "production-instances"


def test_auto_grouping_on_rule_creation(service, sample_asset, sample_rule):
    # create asset first
    created_asset = service.create_asset(sample_asset)
    assert created_asset.group_name is None

    # create rule; should trigger grouping of existing asset
    service.create_rule(sample_rule)

    # verify asset was grouped
    updated_asset = service.get_asset(created_asset.id)
    assert updated_asset is not None
    assert updated_asset.group_name == "production-instances"


def test_complex_rule_matching(service):
    """
    Test scenario from code exercise email.

    ```
    Users should be able to provide multiple rules per grouping. For example, assets with
    type == "ec2-instance" and having a tag with key == "env" and value == "prod" OR "prod"
    in name should be assigned to group "production-instances".
    ```
    """
    # create a rule matching by type, name, and tag
    rule = GroupingRule(
        group_name="production-instances",
        description="Production Instances",
        conditions=[
            GroupingCondition(
                field="type",
                operator="equals",
                value="ec2-instance",
            ),
            GroupingCondition(
                field="name",
                operator="contains",
                value="prod",
            ),
            GroupingCondition(
                field="tag",
                operator="equals",
                tag_key="env",
                tag_value="prod",
            ),
        ],
    )
    service.create_rule(rule)

    # matching Asset
    asset_one = Asset(
        name="prod-instance",
        type="ec2-instance",
        tags=[Tag(key="env", value="prod")],
        cloud_account=CloudAccount(id="123", name="main"),
        owner_id="user1",
        region="us-east-1",
    )
    persisted_asset_one = service.create_asset(asset_one)
    assert persisted_asset_one.group_name == "production-instances"

    # non-matching Asset
    asset_two = Asset(
        name="dev-instance",
        type="ec2-instance",
        tags=[Tag(key="env", value="dev")],
        cloud_account=CloudAccount(id="123", name="main"),
        owner_id="user1",
        region="us-east-1",
    )
    persisted_asset_two = service.create_asset(asset_two)
    assert persisted_asset_two.group_name is None
