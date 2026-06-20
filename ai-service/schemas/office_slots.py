"""商务办公装修槽位 — DESIGN §5.2 / §5.4.3。"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Tier = Literal["basic", "mid", "premium"]
Style = Literal["tech", "finance", "creative", "neutral"]   # 互联网/金融/创意/中性


class OfficeSlots(BaseModel):
    # 必填
    area_sqm: float | None = Field(None, ge=30, le=5000)
    headcount: int | None = Field(None, ge=2, le=500, description="工位数(含预留扩招)")
    includes_weak_current: bool | None = Field(None, description="是否含弱电")

    # 选填
    industry: str | None = None
    needs_reception_logo: bool | None = None
    meeting_room_large: int | None = Field(None, ge=0, le=10)
    meeting_room_small: int | None = Field(None, ge=0, le=20)
    needs_tea_room: bool | None = None
    needs_finance_room: bool | None = None
    needs_it_room: bool | None = None
    includes_furniture: bool | None = None
    has_vi_spec: bool | None = None
    style_pref: Style | None = None
    night_work_required: bool | None = Field(None, description="物业是否要求夜间施工")
    fire_system_modify: bool | None = Field(None, description="喷淋/烟感是否需要改造")
    budget_ceiling_yuan: float | None = Field(None, ge=30000)

    def required_filled(self) -> bool:
        return all(v is not None for v in (self.area_sqm, self.headcount, self.includes_weak_current))
