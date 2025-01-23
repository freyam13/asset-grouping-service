import logging
import uuid
from datetime import UTC, datetime
from typing import List, Optional

from src.models.schemas import (
    Asset,
    GroupingCondition,
    GroupingRule,
    Operator,
)

logger = logging.getLogger(__name__)


class GroupingService:
    def __init__(self):
        """
        Initialize the grouping service with empty storage.
        """
        # in a real application these would be stored in a database, but this works for demonstration purposes
        self.assets: dict[str, Asset] = {}
        self.rules: dict[str, GroupingRule] = {}

    def create_asset(self, asset: Asset) -> Asset:
        """
        Create a new asset and process it against existing rules.

        Arguments:
            asset: the asset configuration to create

        Returns:
            Asset: newly created asset with generated ID, timestamps, and group assignment
        """
        asset_id = str(uuid.uuid4())
        now = datetime.now(UTC)

        asset_data = asset.model_dump(
            exclude={"id", "group_name", "created_at", "updated_at"}
        )

        new_asset = Asset(id=asset_id, created_at=now, updated_at=now, **asset_data)

        group_name = self._evaluate_rules(new_asset)
        if group_name:
            new_asset.group_name = group_name

        self.assets[asset_id] = new_asset

        return new_asset

    def get_asset(self, asset_id: str) -> Optional[Asset]:
        """
        Retrieve an asset by its ID.

        Arguments:
            asset_id: unique identifier of the asset to retrieve

        Returns:
            Optional[Asset]: matching asset if found, None otherwise
        """
        return self.assets.get(asset_id)

    def list_assets(self) -> List[Asset]:
        """
        Retrieve all assets.

        Returns:
            List[Asset]: list of all assets in the system
        """
        raise NotImplementedError("List assets operation to be implemented")

    def update_asset(self, asset_id: str, asset: Asset) -> Optional[Asset]:
        """
        Update an existing asset and reprocess its grouping.

        Arguments:
            asset_id: unique identifier of the asset to update
            asset: updated asset configuration

        Returns:
            Optional[Asset]: updated asset if found, None otherwise
        """
        if asset_id not in self.assets:
            return None

        current_asset = self.assets[asset_id]
        current_data = current_asset.model_dump()

        update_data = asset.model_dump(
            exclude={"id", "created_at", "updated_at", "group_name"}
        )
        current_data.update(update_data)

        current_data["id"] = asset_id
        current_data["created_at"] = current_asset.created_at
        current_data["updated_at"] = datetime.now(UTC)

        updated_asset = Asset(**current_data)

        # TODO: show preference to manually set group_names; do not evaluate if present
        group_name = self._evaluate_rules(updated_asset)
        updated_asset.group_name = group_name

        self.assets[asset_id] = updated_asset

        return updated_asset

    def delete_asset(self, asset_id: str) -> bool:
        """
        Delete an asset from the system.

        Arguments:
            asset_id: unique identifier of the asset to delete

        Returns:
            bool: True if asset was deleted, False if not found
        """
        raise NotImplementedError("Delete asset operation to be implemented")

    def create_rule(self, rule: GroupingRule) -> GroupingRule:
        """
        Create a new grouping rule and process existing assets.

        Arguments:
            rule: the rule configuration to create

        Returns:
            GroupingRule: newly created rule with generated ID and timestamps
        """
        rule_id = str(uuid.uuid4())
        now = datetime.now(UTC)
        rule_data = rule.model_dump(exclude={"id", "created_at", "updated_at"})
        new_rule = GroupingRule(id=rule_id, created_at=now, updated_at=now, **rule_data)

        self.rules[rule_id] = new_rule

        self._process_existing_assets()

        return new_rule

    def get_rule(self, rule_id: str) -> Optional[GroupingRule]:
        """
        Retrieve a rule by its ID.

        Arguments:
            rule_id: unique identifier of the rule to retrieve

        Returns:
            Optional[GroupingRule]: matching rule if found, None otherwise
        """
        raise NotImplementedError("Get rule operation to be implemented")

    def list_rules(self) -> List[GroupingRule]:
        """
        Retrieve all grouping rules

        Returns:
            List[GroupingRule]: list of all rules in the system
        """
        raise NotImplementedError("List rules operation to be implemented")

    def update_rule(self, rule_id: str, rule: GroupingRule) -> Optional[GroupingRule]:
        """
        Update an existing rule and reprocess affected assets.

        Arguments:
            rule_id: unique identifier of the rule to update
            rule: updated rule configuration

        Returns:
            Optional[GroupingRule]: updated rule if found, None otherwise
        """
        if rule_id not in self.rules:
            return None

        current_rule = self.rules[rule_id]
        update_data = rule.model_dump(
            exclude={"id", "created_at", "updated_at"}, exclude_unset=True
        )

        updated_rule = GroupingRule(
            **current_rule.model_dump(), **update_data, updated_at=datetime.now(UTC)
        )

        self.rules[rule_id] = updated_rule

        self._process_existing_assets()

        return updated_rule

    def delete_rule(self, rule_id: str) -> bool:
        """
        Delete a rule and ungroup its associated assets.

        Arguments:
            rule_id: unique identifier of the rule to delete

        Returns:
            bool: True if rule was deleted, False if not found
        """
        raise NotImplementedError("Delete rule operation to be implemented")

    def _evaluate_rules(self, asset: Asset) -> Optional[str]:
        """
        Evaluate all rules against an asset to determine its group.

        Arguments:
            asset: the asset to evaluate

        Returns:
            Optional[str]: matching group name if any rule matches, None otherwise
        """
        for rule in self.rules.values():
            if all(
                self._evaluate_condition(asset, condition)
                for condition in rule.conditions
            ):
                return rule.group_name

        return None

    def _evaluate_condition(self, asset: Asset, condition: GroupingCondition) -> bool:
        """
        Evaluate a single condition against an asset.

        Arguments:
            asset: the asset to evaluate
            condition: the condition to check

        Returns:
            bool: True if condition matches, False otherwise
        """
        # TODO: add logging for better rule match debugging
        if condition.field == "type":
            if condition.operator == Operator.EQUALS:
                return asset.type == condition.value

            elif condition.operator == Operator.CONTAINS:
                return condition.value in asset.type

        elif condition.field == "name":
            if condition.operator == Operator.EQUALS:
                return asset.name == condition.value

            elif condition.operator == Operator.CONTAINS:
                return condition.value in asset.name

        elif condition.field == "tag":
            if condition.operator == Operator.EXISTS:
                return any(tag.key == condition.tag_key for tag in asset.tags)

            elif condition.operator == Operator.EQUALS:
                return any(
                    tag.key == condition.tag_key and tag.value == condition.tag_value
                    for tag in asset.tags
                )

        return False

    def _process_existing_assets(self) -> None:
        """
        Process all ungrouped assets against existing rules; updates group assignments for any assets that
        match new rules.
        """
        # TODO: update docstring as it is no longer accurate; only processes assets without group_name
        # potentially enqueue assets without group_name for asynchronous processing instead
        # consider flagging assets that match multiple rules or adding support for multiple group_names
        for asset in self.assets.values():
            if not asset.group_name:
                group_name = self._evaluate_rules(asset)

                if group_name:
                    asset.group_name = group_name
                    asset.updated_at = datetime.now(UTC)
