import reflex as rx
from app.states.news_state import NewsState, NewsBurst


def timeline_chart(data: list[dict]) -> rx.Component:
    return rx.recharts.bar_chart(
        rx.recharts.bar(data_key="count", fill="#8b5cf6", radius=[2, 2, 0, 0]),
        data=data,
        width=100,
        height=40,
        margin={"top": 0, "right": 0, "bottom": 0, "left": 0},
    )


def news_burst_card(burst: NewsBurst) -> rx.Component:
    is_expanded = NewsState.expanded_news_ids.contains(burst["id"])
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(burst["emoji"], class_name="text-xl"),
                    class_name="w-10 h-10 rounded-lg bg-gray-50 flex items-center justify-center shrink-0 border border-gray-100",
                ),
                rx.el.div(
                    rx.el.h3(
                        burst["title"], class_name="text-lg font-semibold text-gray-900"
                    ),
                    rx.el.div(
                        rx.icon(
                            "calendar", class_name="w-3.5 h-3.5 text-gray-400 mr-1.5"
                        ),
                        rx.el.span(
                            f"{burst['start_date']} - {burst['end_date']}",
                            class_name="text-gray-600",
                        ),
                        rx.el.span(
                            f"({burst['duration_days']} days)",
                            class_name="text-gray-400 ml-1.5",
                        ),
                        class_name="flex items-center text-sm mt-1",
                    ),
                    class_name="ml-4 flex-1",
                ),
                class_name="flex items-center flex-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        f"{burst['coverage_percentage']}%",
                        class_name="text-xs font-semibold text-violet-700",
                    ),
                    rx.el.span("coverage", class_name="text-xs text-gray-500 ml-1"),
                    class_name="flex items-center justify-end mb-1.5",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name=f"h-full bg-violet-500 rounded-full",
                        style={"width": f"{burst['coverage_percentage']} %"},
                    ),
                    class_name="w-32 h-1.5 bg-gray-100 rounded-full overflow-hidden",
                ),
                class_name="flex flex-col items-end mx-6",
            ),
            rx.el.div(timeline_chart(burst["daily_counts"]), class_name="mx-6"),
            rx.el.div(
                rx.el.span(
                    f"{burst['article_count']}",
                    class_name="text-xl font-bold text-gray-900",
                ),
                rx.el.span("articles", class_name="text-xs text-gray-500 block"),
                class_name="text-right min-w-[60px]",
            ),
            rx.el.button(
                rx.icon(
                    "chevron-down",
                    class_name=rx.cond(
                        is_expanded,
                        "w-5 h-5 text-gray-400 transition-transform rotate-180",
                        "w-5 h-5 text-gray-400 transition-transform",
                    ),
                ),
                on_click=lambda: NewsState.toggle_news_expanded(burst["id"]),
                class_name="ml-4 p-1 hover:bg-gray-100 rounded-full transition-colors",
            ),
            class_name="flex items-center p-6",
        ),
        rx.cond(
            is_expanded,
            rx.el.div(
                rx.el.div(
                    rx.el.p(burst["summary"], class_name="text-gray-700 mb-4"),
                    rx.el.div(
                        rx.el.button(
                            "View Timeline",
                            on_click=lambda: NewsState.set_current_view(
                                "story_timeline"
                            ),
                            class_name="text-sm font-medium text-violet-600 hover:text-violet-700 hover:underline",
                        ),
                        class_name="flex items-center gap-4",
                    ),
                    class_name="p-6 bg-gray-50 border-t border-gray-100",
                ),
                class_name="animate-fade-in",
            ),
            rx.fragment(),
        ),
        class_name="bg-white border border-gray-200 rounded-xl hover:shadow-md transition-shadow mb-4",
    )


def dominant_news_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Dominant News", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "Date Range:",
                            class_name="text-sm font-medium text-gray-500 mr-3",
                        ),
                        rx.el.div(
                            rx.icon(
                                "calendar", class_name="w-4 h-4 text-gray-400 mr-2"
                            ),
                            rx.el.span(NewsState.dn_start_date),
                            rx.el.span("→", class_name="mx-2 text-gray-400"),
                            rx.el.span(NewsState.dn_end_date),
                            class_name="flex items-center bg-white border border-gray-200 rounded-lg px-3 py-1.5 text-sm font-medium text-gray-700",
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Sort by:",
                            class_name="text-sm font-medium text-gray-500 mr-3",
                        ),
                        rx.el.select(
                            rx.el.option("Article Count", value="count"),
                            rx.el.option("Duration", value="duration"),
                            rx.el.option("Recency", value="recent"),
                            value=NewsState.dn_sort_by,
                            on_change=NewsState.set_dn_sort,
                            class_name="bg-white border border-gray-200 rounded-lg px-3 py-1.5 text-sm font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-violet-500/20",
                        ),
                        class_name="flex items-center ml-6",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex items-center justify-between mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    "Top Stories by Coverage",
                    class_name="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-4",
                ),
                rx.foreach(NewsState.sorted_bursts, news_burst_card),
                class_name="space-y-1",
            ),
            class_name="max-w-5xl mx-auto py-8 px-8",
        ),
        class_name="flex-1 ml-72 bg-white min-h-screen",
    )