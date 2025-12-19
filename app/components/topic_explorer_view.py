import reflex as rx
from app.states.news_state import NewsState, CrossTimeTopic, NewsBurst
from app.components.dominant_news_view import news_burst_card


def topic_header() -> rx.Component:
    topic = NewsState.selected_topic
    return rx.cond(
        topic,
        rx.el.div(
            rx.el.div(
                rx.el.span(topic["emoji"], class_name="text-4xl mr-6"),
                rx.el.div(
                    rx.el.h2(
                        topic["name"],
                        class_name="text-3xl font-bold text-gray-900 mb-2",
                    ),
                    rx.el.div(
                        rx.el.span(
                            f"{topic['total_articles']} articles",
                            class_name="font-medium text-gray-900",
                        ),
                        rx.el.span("•", class_name="mx-2 text-gray-300"),
                        rx.el.span(topic["date_range"], class_name="text-gray-500"),
                        class_name="flex items-center text-sm",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center",
            ),
            class_name="bg-white border-b border-gray-100 p-8",
        ),
        rx.fragment(),
    )


def topic_explorer_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="w-5 h-5 text-gray-400 absolute left-4 top-3.5",
                    ),
                    rx.el.input(
                        placeholder="Search topics (e.g. 'Energy', 'Politics')...",
                        class_name="w-full pl-12 pr-4 py-3 bg-gray-50 border-transparent focus:bg-white focus:border-violet-500 focus:ring-0 rounded-xl transition-all placeholder-gray-500 text-gray-900",
                    ),
                    class_name="relative flex-1 max-w-2xl",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("filter", class_name="w-4 h-4 mr-2"),
                        "Filters",
                        class_name="flex items-center px-4 py-3 bg-white border border-gray-200 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50",
                    ),
                    class_name="ml-4",
                ),
                class_name="flex items-center p-8 border-b border-gray-100 bg-white/50 backdrop-blur-sm sticky top-0 z-10",
            ),
            topic_header(),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "News in this Topic",
                        class_name="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-6",
                    ),
                    rx.foreach(NewsState.selected_topic_bursts, news_burst_card),
                    class_name="max-w-5xl mx-auto",
                ),
                class_name="p-8 bg-gray-50/50 min-h-screen",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex-1 ml-72 bg-white min-h-screen",
    )