"""家装(精品家装)槽位 — DESIGN §5.2 / §5.4.1。"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Tier = Literal["basic", "mid", "premium"]
ContractType = Literal["clean", "half", "full"]   # 清包 / 半包 / 全包


class ResidentialSlots(BaseModel):
    # 必填
    area_sqm: float | None = Field(None, ge=10, le=2000, description="套内面积")
    layout: str | None = Field(None, description="户型,如 '三室两厅一卫'")
    tier: Tier | None = None

    # 选填
    contract_type: ContractType | None = None
    headcount: int | None = Field(None, ge=1, le=12)
    needs_kids_room: bool | None = None
    needs_elder_room: bool | None = None
    needs_study: bool | None = None
    style_pref: str | None = None
    has_furniture: bool | None = None
    has_central_ac: bool | None = None
    has_fresh_air: bool | None = None
    has_floor_heating: bool | None = None
    budget_ceiling_yuan: float | None = Field(None, ge=10000)

    def required_filled(self) -> bool:
        return all(v is not None for v in (self.area_sqm, self.layout, self.tier))
