import reflex as rx
from app.states.news_state import NewsState, RecurringSeries, RecurringInstance


def instance_node(instance: RecurringInstance, is_last: bool) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    instance["date"],
                    class_name="text-xs font-semibold text-gray-500 mb-1 block whitespace-nowrap",
                ),
                rx.el.div(
                    rx.el.span(
                        instance["value"], class_name="text-xs font-bold text-gray-900"
                    ),
                    class_name="w-16 h-16 rounded-full bg-white border-2 border-violet-100 flex flex-col items-center justify-center shadow-sm z-10 relative hover:border-violet-500 hover:scale-105 transition-all cursor-pointer",
                ),
                rx.el.span(
                    instance["change"],
                    class_name=rx.cond(
                        instance["trend"] == "up",
                        "text-[10px] font-bold text-red-500 mt-1",
                        "text-[10px] font-bold text-green-500 mt-1",
                    ),
                ),
                class_name="flex flex-col items-center",
            ),
            rx.cond(
                ~is_last,
                rx.el.div(
                    rx.icon("arrow-right", class_name="w-4 h-4 text-gray-300"),
                    class_name="absolute top-1/2 left-full w-12 h-0.5 bg-gray-200 -translate-y-1/2 -ml-6 flex items-center justify-center",
                ),
                rx.fragment(),
            ),
            class_name="relative flex items-center mr-12 last:mr-0",
        ),
        class_name="flex items-center",
    )


def series_card(series: RecurringSeries) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(series["name"], class_name="text-lg font-bold text-gray-900"),
                rx.el.div(
                    rx.el.span(
                        series["company"],
                        class_name="text-xs font-medium text-gray-500 bg-gray-100 px-2 py-1 rounded-md mr-2",
                    ),
                    rx.el.span(
                        series["pattern_type"],
                        class_name="text-xs font-medium text-violet-600 bg-violet-50 px-2 py-1 rounded-md capitalize",
                    ),
                    class_name="flex items-center mt-2",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.span(
                    "Trend",
                    class_name="text-xs font-semibold text-gray-400 uppercase tracking-wider mr-2",
                ),
                rx.cond(
                    series["overall_trend"] == "up",
                    rx.el.span(
                        "Increasing ↗",
                        class_name="text-xs font-bold text-red-600 bg-red-50 px-2 py-1 rounded",
                    ),
                    rx.el.span(
                        "Decreasing ↘",
                        class_name="text-xs font-bold text-green-600 bg-green-50 px-2 py-1 rounded",
                    ),
                ),
                class_name="absolute top-6 right-6 flex items-center",
            ),
            class_name="relative",
        ),
        rx.el.div(
            rx.foreach(
                series["instances"],
                lambda inst, i: instance_node(
                    inst, i == series["instances"].length() - 1
                ),
            ),
            class_name="flex items-center overflow-x-auto pb-4 pt-2 no-scrollbar",
        ),
        rx.el.div(
            rx.icon("info", class_name="w-4 h-4 text-violet-500 mr-2 flex-shrink-0"),
            rx.el.p(
                f"Pattern identified with {series['instances'].length()} occurrences over the last period.",
                class_name="text-sm text-gray-600",
            ),
            class_name="mt-4 pt-4 border-t border-gray-100 flex items-start",
        ),
        class_name="bg-white border border-gray-200 rounded-xl p-6 shadow-sm hover:shadow-md transition-all mb-6",
    )


def recurring_patterns_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Recurring Patterns", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("All Patterns", value="all"),
                        rx.el.option("Monthly", value="monthly"),
                        rx.el.option("Quarterly", value="quarterly"),
                        value=NewsState.rp_selected_pattern_type,
                        on_change=NewsState.set_rp_pattern_type,
                        class_name="bg-white border border-gray-200 rounded-lg px-3 py-2 text-sm font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-violet-500/20 mr-3",
                    ),
                    rx.el.button(
                        rx.icon("download", class_name="w-4 h-4 mr-2"),
                        "Export",
                        on_click=NewsState.export_data,
                        class_name="flex items-center px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex items-center justify-between mb-8",
            ),
            rx.el.div(
                rx.cond(
                    NewsState.filtered_recurring_series.length() > 0,
                    rx.foreach(NewsState.filtered_recurring_series, series_card),
                    rx.el.div(
                        rx.icon("search", class_name="w-12 h-12 text-gray-300 mb-4"),
                        rx.el.h3(
                            "No patterns found",
                            class_name="text-lg font-medium text-gray-900",
                        ),
                        rx.el.p(
                            "Try adjusting your filters to see more results.",
                            class_name="text-gray-500",
                        ),
                        class_name="flex flex-col items-center justify-center py-16 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200",
                    ),
                ),
                class_name="flex flex-col",
            ),
            class_name="max-w-5xl mx-auto py-8 px-8",
        ),
        class_name="flex-1 ml-72 bg-white min-h-screen",
    )