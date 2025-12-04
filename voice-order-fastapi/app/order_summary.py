from __future__ import annotations

from typing import Iterable

from app.context import _load_all_catalog_data
from app.schemas import ChatMessage, OrderSummary, OrderItem


SUMMARY_KEYS = [
    "customerName",
    "customerAddress",
    "menuName",
    "menuStyle",
    "menuItems",
    "deliveryTime",
    "quantity",
    "couponCode",
    "useCoupon",
]


def _normalize_menu_key(value: str) -> str:
    if not value:
        return ""
    return " ".join(value.strip().split()).casefold()


def _extract_menu_key(entry: dict[str, str], candidate_fields: Iterable[str]) -> str:
    for field in candidate_fields:
        raw_value = entry.get(field)
        if raw_value:
            key = _normalize_menu_key(raw_value)
            if key:
                return key
    return ""


def _build_menu_item_guide() -> str:
    """Build menu item guide dynamically from catalog data."""
    catalog = _load_all_catalog_data()

    # Group menu items by normalized menu identifier (name or ID)
    menu_components = {}
    for item in catalog.menu_items:
        menu_key = _extract_menu_key(item, ("menu_id", "menu_name", "menu"))
        item_name = item.get("item_name", "").strip()

        # Skip non-food items (decorations, napkins, etc.) - only track items with prices
        if not item.get("unit_price"):
            continue

        if not menu_key:
            continue

        if menu_key not in menu_components:
            menu_components[menu_key] = []
        menu_components[menu_key].append(item_name)

    # Build guide text for each menu
    guide_lines = ["For the menuItems line, describe final quantities per component using comma-separated `항목=수량` pairs. Reflect any changes the customer requested. Use these component sets:"]

    for menu in catalog.menus:
        menu_key = _extract_menu_key(menu, ("menu_id", "name"))
        menu_name = menu.get("name", "").strip()

        if menu_key and menu_key in menu_components:
            components = ", ".join(menu_components[menu_key])
            guide_lines.append(f"- {menu_name}: {components}")

    guide_lines.append("If multiple 세트가 함께 주문되면 각 세트에 맞는 항목을 모두 포함하고, 언급되지 않은 항목은 `항목=미확인`으로 남기세요.")
    guide_lines.append("")
    guide_lines.append("IMPORTANT: When multiple menus are ordered, you must list each menu separately in the orderItems section below.")

    return "\n".join(guide_lines)


def _build_style_guide() -> str:
    """Provide available style names to encourage consistent menuStyle output."""
    catalog = _load_all_catalog_data()
    lines = ["Use one of these 서빙 스타일 이름(또는 null) for menuStyle:"]
    for style in catalog.styles:
        name = style.get("name", "").strip()
        if not name:
            continue
        description = style.get("description", "").strip() or "설명 없음"
        lines.append(f"- {name}: {description}")
    return "\n".join(lines)


def build_summary_prompt(history: Iterable[ChatMessage], final_message: str, assumed_date: str) -> list[dict]:
    conversation_lines = [
        f"{msg.role.upper()}: {msg.content}"
        for msg in history
    ]
    history_block = "\n".join(conversation_lines)
    menu_guide = _build_menu_item_guide()
    style_guide = _build_style_guide()

    prompt = [
        {
            "role": "system",
            "content": "\n".join(
                [
                    "You are an expert maître d' that produces structured order snapshots for Mr. Daebak Dinner.",
                    "Return plain text with the following structure:",
                    "",
                    "First, output these common fields (one per line):",
                    "customerName = <customer's name mentioned in conversation or greeting (e.g., '홍길동', '김철수') or null if not mentioned>",
                    "customerAddress = <value or null>",
                    "deliveryTime = <ISO 8601 datetime or null>",
                    "couponCode = <coupon code or coupon name mentioned by customer or null>",
                    "useCoupon = <true or false or null>",
                    "",
                    "Then, for the menu information:",
                    "- If only ONE menu is ordered, output these lines:",
                    "  menuName = <menu name>",
                    "  menuStyle = <style name or null>",
                    "  menuItems = <comma separated list of item=quantity>",
                    "  quantity = <integer number or null>",
                    "",
                    "- If MULTIPLE menus are ordered, output orderItems array instead:",
                    "  orderItems = [",
                    "    {menuName: '<menu name 1>', menuStyle: '<style or null>', menuItems: '<item=quantity pairs>', quantity: <number>},",
                    "    {menuName: '<menu name 2>', menuStyle: '<style or null>', menuItems: '<item=quantity pairs>', quantity: <number>}",
                    "  ]",
                    "",
                    "For orderItems: each menu must have its own entry with menuName, menuStyle (can be null), menuItems (can be null), and quantity.",
                    "When multiple menus are ordered, DO NOT use the single menuName/menuStyle/menuItems/quantity fields. Use orderItems array instead.",
                    "",
                    f"Use ISO 8601 format (YYYY-MM-DDTHH:mm:ss) for deliveryTime. Assume today is {assumed_date} and normalize any inferred delivery date to that day unless the customer explicitly requested another date.",
                    "For quantity: extract the number of menu sets ordered for EACH menu separately (e.g., '발렌타인 디너 2개' means quantity = 2 for that menu). If not mentioned, use 1.",
                    "For couponCode: extract the coupon code or name if the customer mentioned using a coupon (e.g., 'REGULAR10000', '단골 쿠폰', '쿠폰 사용'). If no coupon mentioned, use null.",
                    "For useCoupon: set to true if customer mentioned using a coupon, false if they explicitly said not to use one, null if not mentioned.",
                    "For deliveryTime: if customer mentioned a specific future date/time for delivery, set it here. If they want immediate delivery or didn't specify, use null.",
                    'Do not add extra lines or commentary. Use "null" (without quotes) for missing information. Use "true" or "false" (lowercase, without quotes) for boolean values.',
                    "When the conversation was in Korean, keep the values in Korean; otherwise mirror the customer language.",
                    "",
                    menu_guide,
                    "",
                    style_guide,
                ]
            ),
        },
        {
            "role": "user",
            "content": "\n".join(
                [
                    "다음은 고객과의 최종 주문 대화 내용입니다.",
                    "",
                    history_block,
                    "",
                    "최종 안내 메시지:",
                    final_message or "",
                    "",
                    "위 내용을 기준으로 주문 요약을 출력하세요.",
                ]
            ),
        },
    ]
    return prompt


def parse_summary_text(raw_text: str) -> OrderSummary:
    if not isinstance(raw_text, str) or not raw_text.strip():
        raise ValueError("요약 결과가 비어있습니다.")

    values: dict[str, str | int | bool | None] = {key: None for key in SUMMARY_KEYS}
    order_items: list[OrderItem] = []
    in_order_items = False
    current_item: dict[str, str | int] = {}

    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue

        # orderItems 배열 파싱
        if line.startswith("orderItems") and "=" in line:
            in_order_items = True
            # orderItems = [...] 형태 처리
            if "[" in line:
                continue
            elif line.strip() == "]":
                if current_item:
                    order_items.append(_parse_order_item(current_item))
                    current_item = {}
                in_order_items = False
                continue
        elif in_order_items:
            # orderItems 배열 내부 항목 파싱
            if line.startswith("{"):
                if current_item:
                    order_items.append(_parse_order_item(current_item))
                current_item = {}
                continue
            elif line.startswith("}"):
                if current_item:
                    order_items.append(_parse_order_item(current_item))
                    current_item = {}
                continue
            elif ":" in line:
                # {menuName: '...', menuStyle: '...'} 형태
                key, raw_value = line.split(":", 1)
                key = key.strip().rstrip(",").strip()
                raw_value = raw_value.strip().rstrip(",").strip()
                # 따옴표 제거
                if raw_value.startswith("'") and raw_value.endswith("'"):
                    raw_value = raw_value[1:-1]
                elif raw_value.startswith('"') and raw_value.endswith('"'):
                    raw_value = raw_value[1:-1]
                if raw_value.lower() in {"null", "-", "none", ""}:
                    current_item[key] = None
                elif key == "quantity":
                    try:
                        current_item[key] = int(raw_value)
                    except ValueError:
                        current_item[key] = 1
                else:
                    current_item[key] = raw_value
            continue

        # 기존 단일 필드 파싱
        if "=" not in line:
            continue
        key, raw_value = line.split("=", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if key not in values:
            continue
        if raw_value.lower() in {"null", "-", "none", ""}:
            values[key] = None
        elif key == "quantity":
            # 정수로 변환 시도
            try:
                values[key] = int(raw_value)
            except ValueError:
                values[key] = None
        elif key == "useCoupon":
            # 불린으로 변환
            if raw_value.lower() == "true":
                values[key] = True
            elif raw_value.lower() == "false":
                values[key] = False
            else:
                values[key] = None
        else:
            values[key] = raw_value

    # orderItems 배열이 비어있고 기존 필드가 있으면 하위 호환성 처리
    if not order_items and values.get("menuName"):
        # 단일 메뉴를 orderItems 배열로 변환
        order_items.append(OrderItem(
            menuName=values.get("menuName") or "",
            menuStyle=values.get("menuStyle"),
            menuItems=values.get("menuItems"),
            quantity=values.get("quantity") or 1
        ))

    return OrderSummary(orderItems=order_items, **values)


def _parse_order_item(item_dict: dict[str, str | int | None]) -> OrderItem:
    """orderItems 배열의 개별 항목을 OrderItem으로 변환"""
    menu_name = str(item_dict.get("menuName", ""))
    if not menu_name:
        raise ValueError("orderItem에 menuName이 없습니다.")
    
    menu_style = item_dict.get("menuStyle")
    if isinstance(menu_style, str) and menu_style.lower() in {"null", "-", "none", ""}:
        menu_style = None
    
    menu_items = item_dict.get("menuItems")
    if isinstance(menu_items, str) and menu_items.lower() in {"null", "-", "none", ""}:
        menu_items = None
    
    quantity = item_dict.get("quantity")
    if quantity is None:
        quantity = 1
    elif isinstance(quantity, str):
        try:
            quantity = int(quantity)
        except ValueError:
            quantity = 1
    
    return OrderItem(
        menuName=menu_name,
        menuStyle=menu_style,
        menuItems=menu_items,
        quantity=quantity
    )
