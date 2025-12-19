import reflex as rx
from app.states.news_state import NewsState


def sidebar_item(
    icon: str, label: str, view_name: str, description: str = ""
) -> rx.Component:
    """Renders a single sidebar navigation item."""
    is_active = NewsState.current_view == view_name
    return rx.el.div(
        rx.el.button(
            rx.icon(
                icon,
                class_name=rx.cond(
                    is_active, "w-5 h-5 text-violet-600", "w-5 h-5 text-gray-500"
                ),
            ),
            rx.el.div(
                rx.el.span(
                    label,
                    class_name=rx.cond(
                        is_active,
                        "font-semibold text-gray-900",
                        "font-medium text-gray-700",
                    ),
                ),
                rx.cond(
                    description != "",
                    rx.el.p(
                        description, class_name="text-xs text-gray-500 text-left mt-0.5"
                    ),
                    rx.fragment(),
                ),
                class_name="flex flex-col items-start ml-3",
            ),
            on_click=lambda: NewsState.set_current_view(view_name),
            class_name=rx.cond(
                is_active,
                "flex items-center w-full p-3 rounded-xl bg-violet-50 border border-violet-100 transition-all duration-200",
                "flex items-center w-full p-3 rounded-xl hover:bg-gray-50 transition-all duration-200",
            ),
        ),
        class_name="mb-1",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.icon("layers", class_name="w-8 h-8 text-violet-600"),
            rx.el.div(
                rx.el.h1(
                    "NewsCluster",
                    class_name="text-xl font-bold text-gray-900 leading-none",
                ),
                rx.el.span(
                    "Intelligence System",
                    class_name="text-xs font-medium text-violet-500 uppercase tracking-wider",
                ),
                class_name="flex flex-col ml-3",
            ),
            class_name="flex items-center px-6 py-6 border-b border-gray-100",
        ),
        rx.el.nav(
            rx.el.div(
                rx.el.p(
                    "DAILY MONITORING",
                    class_name="px-4 text-xs font-semibold text-gray-400 mb-2 mt-6 uppercase tracking-wider",
                ),
                sidebar_item(
                    "layout-list",
                    "Daily Briefing",
                    "daily_briefing",
                    description="Flat list of top stories",
                ),
                sidebar_item(
                    "layout-grid",
                    "Daily Topics",
                    "daily_topics",
                    description="Grouped by theme",
                ),
                class_name="px-2",
            ),
            rx.el.div(
                rx.el.p(
                    "ANALYSIS",
                    class_name="px-4 text-xs font-semibold text-gray-400 mb-2 mt-6 uppercase tracking-wider",
                ),
                sidebar_item("bar-chart-2", "Dominant News", "dominant_news"),
                sidebar_item("globe", "Topic Explorer", "topic_explorer"),
                class_name="px-2",
            ),
            rx.el.div(
                rx.el.p(
                    "INTELLIGENCE",
                    class_name="px-4 text-xs font-semibold text-gray-400 mb-2 mt-6 uppercase tracking-wider",
                ),
                sidebar_item("git_commit_vertical", "Story Timeline", "story_timeline"),
                sidebar_item("network", "Causal Network", "causal_network"),
                sidebar_item("repeat", "Recurring Patterns", "recurring_patterns"),
                class_name="px-2",
            ),
            class_name="flex-1 overflow-y-auto",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span("JD", class_name="text-sm font-medium text-white"),
                    class_name="w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center",
                ),
                rx.el.div(
                    rx.el.p("John Doe", class_name="text-sm font-medium text-gray-900"),
                    rx.el.p("Senior Analyst", class_name="text-xs text-gray-500"),
                    class_name="ml-3",
                ),
                class_name="flex items-center",
            ),
            class_name="p-4 border-t border-gray-100 bg-gray-50/50",
        ),
        class_name="flex flex-col w-72 h-screen bg-white border-r border-gray-200 shrink-0 fixed left-0 top-0 z-20",
    )