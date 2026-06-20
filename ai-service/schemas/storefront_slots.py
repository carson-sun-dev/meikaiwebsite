"""门面房店铺装修槽位 — DESIGN §5.2 / §5.4.2(★ 核心业务)。"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Tier = Literal["basic", "mid", "premium"]


class StorefrontSlots(BaseModel):
    # 必填
    business_type: str | None = Field(None, description="业态:火锅/咖啡/眼镜店/服装/餐饮 ...")
    area_sqm: float | None = Field(None, ge=15, le=3000)
    tier: Tier | None = None

    # 选填(DESIGN §5.2)
    ceiling_height_m: float | None = Field(None, ge=2.4, le=6.0)
    is_franchise: bool | None = Field(None, description="是否品牌加盟(有总部 VI 手册)")
    brand_vi_locked: bool | None = Field(None, description="品牌 VI 是否已定")
    needs_kitchen_engineering: bool | None = Field(None, description="是否含厨房工程(排油/给排水)")
    includes_weak_current: bool | None = None
    fire_constraints: str | None = Field(None, description="商场/物业消防与施工硬限制摘要")
    rent_free_days: int | None = Field(None, ge=0, description="免租装修期天数")
    opening_deadline: str | None = Field(None, description="开业死线,YYYY-MM-DD")

    # §13.2 新增:门头是否纳入主报价(§8.4 决策驱动)
    door_facade_required: bool = False

    budget_ceiling_yuan: float | None = Field(None, ge=10000)

    def required_filled(self) -> bool:
        return all(v is not None for v in (self.business_type, self.area_sqm, self.tier))
