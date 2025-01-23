from typing import List

from fastapi import APIRouter, HTTPException, status

from src.models.schemas import (
    Asset,
    GroupingRule,
)
from src.services.grouping import GroupingService

router = APIRouter()
grouping_service = GroupingService()


################
# Asset routes #
################


@router.post("/assets", response_model=Asset, status_code=status.HTTP_201_CREATED)
async def create_asset(asset: Asset) -> Asset:
    """
    Create a new asset and automatically process it against existing rules.

    Arguments:
        asset: the asset to create

    Returns:
        Asset: newly created and processed asset

    Raises:
        HTTPException: if asset creation fails
    """
    try:
        return grouping_service.create_asset(asset)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/assets", response_model=List[Asset])
async def list_assets() -> List[Asset]:
    """
    Retrieve all assets.

    Returns:
        List[Asset]: list of all assets in the system
    """
    raise NotImplementedError("List assets endpoint to be implemented")


@router.get("/assets/{asset_id}", response_model=Asset)
async def get_asset(asset_id: str) -> Asset:
    """
    Retrieve a specific asset by its ID.

    Arguments:
        asset_id: unique identifier of the asset

    Returns:
        Asset: matching asset

    Raises:
        HTTPException: if asset is not found
    """
    asset = grouping_service.get_asset(asset_id)

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {asset_id} not found",
        )

    return asset


@router.patch("/assets/{asset_id}", response_model=Asset)
async def update_asset(asset_id: str, asset: Asset) -> Asset:
    """
    Update an existing asset and reprocess its grouping.

    Arguments:
        asset_id: unique identifier of the asset to update
        asset: updated asset data

    Returns:
        Asset: updated and reprocessed asset

    Raises:
        HTTPException: if asset is not found
    """
    updated_asset = grouping_service.update_asset(asset_id, asset)

    if not updated_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {asset_id} not found",
        )

    return updated_asset


@router.delete("/assets/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(asset_id: str) -> None:
    """
    Delete an asset from the system.

    Arguments:
        asset_id: unique identifier of the asset to delete
    """
    raise NotImplementedError("Delete asset endpoint to be implemented")


###############
# Rule routes #
###############


@router.post("/rules", response_model=GroupingRule, status_code=status.HTTP_201_CREATED)
async def create_rule(rule: GroupingRule) -> GroupingRule:
    """
    Create a new grouping rule and process existing assets.

    Arguments:
        rule: the rule to create

    Returns:
        GroupingRule: newly created rule

    Raises:
        HTTPException: if rule creation fails
    """
    try:
        return grouping_service.create_rule(rule)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/rules", response_model=List[GroupingRule])
async def list_rules() -> List[GroupingRule]:
    """
    Retrieve all grouping rules.

    Returns:
        List[GroupingRule]: list of all rules in the system
    """
    raise NotImplementedError("List rules endpoint to be implemented")


@router.get("/rules/{rule_id}", response_model=GroupingRule)
async def get_rule(rule_id: str) -> GroupingRule:
    """
    Retrieve a specific rule by its ID.

    Arguments:
        rule_id: unique identifier of the rule

    Returns:
        GroupingRule: matching rule
    """
    raise NotImplementedError("Get rule endpoint to be implemented")


@router.patch("/rules/{rule_id}", response_model=GroupingRule)
async def update_rule(rule_id: str, rule: GroupingRule) -> GroupingRule:
    """
    Update an existing rule and reprocess all assets.

    Arguments:
        rule_id: unique identifier of the rule to update
        rule: updated rule data

    Returns:
        GroupingRule: updated rule

    Raises:
        HTTPException: if rule is not found
    """
    updated_rule = grouping_service.update_rule(rule_id, rule)

    if not updated_rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule with ID {rule_id} not found",
        )

    return updated_rule


@router.delete("/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(rule_id: str) -> None:
    """
    Delete a rule and ungroup associated assets.

    Arguments:
        rule_id: unique identifier of the rule to delete
    """
    raise NotImplementedError("Delete rule endpoint to be implemented")
