"""
L2 槽位 Schema(DESIGN §5.5)。三业态各自一个 Pydantic 模型,工具入参直接复用。
"""
from .residential_slots import ResidentialSlots
from .office_slots import OfficeSlots
from .storefront_slots import StorefrontSlots

__all__ = ["ResidentialSlots", "OfficeSlots", "StorefrontSlots"]
