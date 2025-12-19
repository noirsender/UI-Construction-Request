import reflex as rx
from typing import Literal


def relationship_badge(type_: str, text: str) -> rx.Component:
    """
    Renders a badge with color coding based on relationship type.
    """
    return rx.match(
        type_,
        (
            "causal",
            rx.el.span(
                rx.icon("zap", class_name="w-3 h-3 mr-1"),
                text,
                class_name="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-orange-100 text-orange-700 border border-orange-200",
            ),
        ),
        (
            "compatible",
            rx.el.span(
                rx.icon("link", class_name="w-3 h-3 mr-1"),
                text,
                class_name="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-blue-100 text-blue-700 border border-blue-200",
            ),
        ),
        (
            "trend",
            rx.el.span(
                rx.icon("trending-up", class_name="w-3 h-3 mr-1"),
                text,
                class_name="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-green-100 text-green-700 border border-green-200",
            ),
        ),
        (
            "temporal",
            rx.el.span(
                rx.icon("clock", class_name="w-3 h-3 mr-1"),
                text,
                class_name="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-purple-100 text-purple-700 border border-purple-200",
            ),
        ),
        rx.el.span(
            text,
            class_name="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-600",
        ),
    )


def count_badge(count: int) -> rx.Component:
    return rx.el.span(
        f"{count} articles",
        class_name="px-2 py-0.5 rounded-full bg-gray-100 text-gray-600 text-xs font-medium border border-gray-200",
    )