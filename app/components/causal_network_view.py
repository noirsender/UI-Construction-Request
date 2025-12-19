import reflex as rx
from app.states.news_state import NewsState, CausalNode


def node_card(
    node: CausalNode, is_selected: bool = False, is_main: bool = False
) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.el.div(
                rx.cond(
                    node["type"] == "trigger",
                    rx.icon("zap", class_name="w-4 h-4 text-orange-500 mr-2"),
                    rx.cond(
                        node["type"] == "outcome",
                        rx.icon("flag", class_name="w-4 h-4 text-green-500 mr-2"),
                        rx.icon("activity", class_name="w-4 h-4 text-blue-500 mr-2"),
                    ),
                ),
                rx.el.span(
                    node["label"],
                    class_name="font-medium text-gray-900 text-sm truncate",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.span(node["date"], class_name="text-xs text-gray-500"),
                rx.el.span(
                    f"{node['article_count']} articles",
                    class_name="text-xs font-semibold text-violet-600 bg-violet-50 px-1.5 py-0.5 rounded",
                ),
                class_name="flex items-center justify-between mt-2 w-full",
            ),
            on_click=lambda: NewsState.set_cn_node(node["id"]),
            class_name=rx.cond(
                is_selected,
                "w-full p-4 bg-white border-2 border-violet-500 shadow-md rounded-xl text-left transition-all scale-105 relative z-10",
                rx.cond(
                    is_main,
                    "w-full p-4 bg-violet-50 border border-violet-200 shadow-sm rounded-xl text-left hover:border-violet-300 transition-all",
                    "w-full p-3 bg-white border border-gray-200 shadow-sm rounded-xl text-left hover:border-gray-300 transition-all hover:shadow-md",
                ),
            ),
        ),
        rx.cond(is_main, rx.fragment(), rx.fragment()),
        class_name="relative w-full max-w-xs transition-all",
    )


def causal_network_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Causal Network Analysis",
                    class_name="text-2xl font-bold text-gray-900",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("download", class_name="w-4 h-4 mr-2"),
                        "Export Data",
                        on_click=NewsState.export_data,
                        class_name="flex items-center px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="flex items-center justify-between mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Triggers / Causes",
                        class_name="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-4 text-center",
                    ),
                    rx.el.div(
                        rx.cond(
                            NewsState.cn_parents.length() > 0,
                            rx.foreach(
                                NewsState.cn_parents,
                                lambda n: rx.el.div(
                                    node_card(n, False, False),
                                    rx.el.div(
                                        rx.icon(
                                            "arrow-right",
                                            class_name="w-5 h-5 text-gray-300",
                                        ),
                                        class_name="absolute -right-8 top-1/2 -translate-y-1/2 hidden md:block",
                                    ),
                                    class_name="relative mb-4",
                                ),
                            ),
                            rx.el.div(
                                "No direct triggers identified",
                                class_name="text-sm text-gray-400 italic text-center py-8",
                            ),
                        ),
                        class_name="flex flex-col gap-4",
                    ),
                    class_name="flex-1 min-w-[250px] p-6 bg-gray-50/50 rounded-2xl border border-gray-100 border-dashed",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Selected Event",
                        class_name="text-xs font-semibold text-violet-500 uppercase tracking-wider mb-4 text-center",
                    ),
                    rx.el.div(
                        rx.cond(
                            NewsState.cn_selected_node,
                            node_card(NewsState.cn_selected_node, True, True),
                            rx.fragment(),
                        ),
                        class_name="flex justify-center items-center h-full pb-20",
                    ),
                    class_name="flex-1 min-w-[280px] z-10",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Consequences / Reactions",
                        class_name="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-4 text-center",
                    ),
                    rx.el.div(
                        rx.cond(
                            NewsState.cn_children.length() > 0,
                            rx.foreach(
                                NewsState.cn_children,
                                lambda n: rx.el.div(
                                    rx.el.div(
                                        rx.icon(
                                            "arrow-right",
                                            class_name="w-5 h-5 text-gray-300",
                                        ),
                                        class_name="absolute -left-8 top-1/2 -translate-y-1/2 hidden md:block",
                                    ),
                                    node_card(n, False, False),
                                    class_name="relative mb-4",
                                ),
                            ),
                            rx.el.div(
                                "No direct consequences identified",
                                class_name="text-sm text-gray-400 italic text-center py-8",
                            ),
                        ),
                        class_name="flex flex-col gap-4",
                    ),
                    class_name="flex-1 min-w-[250px] p-6 bg-gray-50/50 rounded-2xl border border-gray-100 border-dashed",
                ),
                class_name="flex flex-col md:flex-row gap-8 justify-center items-stretch min-h-[500px]",
            ),
            rx.cond(
                NewsState.cn_selected_node,
                rx.el.div(
                    rx.el.h4(
                        "Event Details",
                        class_name="text-lg font-semibold text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "This event represents a significant cluster of news coverage. The causal links shown above are derived from temporal analysis and content similarity referencing.",
                            class_name="text-gray-600 mb-4",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "View Articles",
                                class_name="text-violet-600 font-medium hover:underline",
                            ),
                            class_name="flex items-center",
                        ),
                        class_name="p-6 bg-white border border-gray-200 rounded-xl shadow-sm",
                    ),
                    class_name="mt-12 animate-fade-in",
                ),
                rx.fragment(),
            ),
            class_name="max-w-6xl mx-auto py-8 px-8",
        ),
        class_name="flex-1 ml-72 bg-white min-h-screen",
    )