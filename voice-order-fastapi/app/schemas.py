from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field("user", pattern="^(system|user|assistant)$")
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    message: str
    orderConfirmed: bool = False
    orderId: Optional[str] = None
    order: Optional[OrderSummary] = None


class OrderConfirmRequest(BaseModel):
    history: List[ChatMessage]
    finalMessage: Optional[str] = None


class OrderChangeRequest(OrderConfirmRequest):
    orderId: str


class OrderItem(BaseModel):
    """주문 항목 - 여러 메뉴 주문을 지원하기 위한 구조"""
    menuName: str
    menuStyle: Optional[str] = None
    menuItems: Optional[str] = None  # 구성품 정보 (예: "에그 스크램블=1, 베이컨=2")
    quantity: int = 1


class OrderSummary(BaseModel):
    # 기존 필드 (하위 호환성을 위해 유지)
    customerName: Optional[str] = None
    customerAddress: Optional[str] = None
    menuName: Optional[str] = None  # deprecated: orderItems 사용 권장
    menuStyle: Optional[str] = None  # deprecated: orderItems 사용 권장
    menuItems: Optional[str] = None  # deprecated: orderItems 사용 권장
    deliveryTime: Optional[str] = None
    orderId: Optional[str] = None
    orderTime: Optional[str] = None
    quantity: Optional[int] = None  # deprecated: orderItems 사용 권장
    couponCode: Optional[str] = None
    useCoupon: Optional[bool] = None
    
    # 새로운 필드 - 여러 메뉴 주문 지원
    orderItems: List[OrderItem] = []


class OrderConfirmResponse(BaseModel):
    orderId: str
    confirmedAt: str
    order: OrderSummary
