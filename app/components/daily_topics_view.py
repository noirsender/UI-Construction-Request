import reflex as rx
from app.states.news_state import NewsState, NewsItem, Topic
from app.components.badges import relationship_badge, count_badge
from app.components.daily_briefing_view import article_list_item


def topic_news_item(news_id: str) -> rx.Component:
    return rx.el.div(
        rx.foreach(
            NewsState.news_items,
            lambda item: rx.cond(
                item["id"] == news_id,
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(item["emoji"], class_name="text-lg mr-3"),
                            rx.el.span(
                                item["title"],
                                class_name="text-base font-medium text-gray-900",
                            ),
                            count_badge(item["article_count"]),
                            class_name="flex items-center gap-2",
                        ),
                        rx.el.div(
                            rx.foreach(
                                item["relationships"],
                                lambda r: rx.cond(
                                    r["type"] == "causal",
                                    rx.el.div(
                                        rx.icon(
                                            "corner-down-right",
                                            class_name="w-4 h-4 text-orange-400 mr-2 ml-6",
                                        ),
                                        rx.el.span(
                                            "Triggers: ",
                                            class_name="text-xs text-gray-400 mr-1",
                                        ),
                                        rx.el.span(
                                            r["description"],
                                            class_name="text-xs font-medium text-orange-600 bg-orange-50 px-2 py-1 rounded",
                                        ),
                                        class_name="flex items-center mt-2 w-full",
                                    ),
                                    rx.fragment(),
                                ),
                            )
                        ),
                        rx.el.button(
                            "View",
                            on_click=lambda: NewsState.toggle_news_expanded(item["id"]),
                            class_name="text-xs font-medium text-gray-400 hover:text-violet-600 ml-auto",
                        ),
                        class_name="flex items-center flex-wrap p-3 hover:bg-gray-50 rounded-lg transition-colors cursor-pointer",
                    ),
                    rx.cond(
                        NewsState.expanded_news_ids.contains(item["id"]),
                        rx.el.div(
                            rx.foreach(item["articles"], article_list_item),
                            class_name="pl-10 pr-4 pb-4 space-y-1 border-l-2 border-gray-100 ml-5 mt-1",
                        ),
                        rx.fragment(),
                    ),
                ),
                rx.fragment(),
            ),
        )
    )


def topic_group(topic: Topic) -> rx.Component:
    is_expanded = NewsState.expanded_topic_ids.contains(topic["id"])
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.el.div(
                    rx.el.span(
                        topic["emoji"],
                        class_name="text-2xl mr-4 grayscale opacity-80 group-hover:grayscale-0 group-hover:opacity-100 transition-all",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            topic["name"],
                            class_name="text-lg font-bold text-gray-800 group-hover:text-violet-700 transition-colors",
                        ),
                        rx.el.p(
                            f"{topic['total_articles']} total articles",
                            class_name="text-xs font-medium text-gray-400 text-left",
                        ),
                        class_name="flex flex-col items-start",
                    ),
                    class_name="flex items-center",
                ),
                rx.icon(
                    "chevron-down",
                    class_name=rx.cond(
                        is_expanded,
                        "w-5 h-5 text-gray-400 transform rotate-180 transition-transform",
                        "w-5 h-5 text-gray-400 transition-transform",
                    ),
                ),
                on_click=lambda: NewsState.toggle_topic_expanded(topic["id"]),
                class_name="w-full flex items-center justify-between p-6 bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md hover:border-violet-200 transition-all group mb-2 z-10 relative",
            ),
            rx.el.div(
                rx.cond(
                    is_expanded,
                    rx.el.div(
                        rx.el.div(
                            rx.foreach(topic["news_item_ids"], topic_news_item),
                            class_name="p-4 space-y-2",
                        ),
                        class_name="bg-white border-x border-b border-gray-200 rounded-b-xl -mt-2 pt-4 shadow-sm animate-slide-down origin-top",
                    ),
                    rx.fragment(),
                )
            ),
        ),
        class_name="mb-6",
    )


def daily_topics_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Thematic Overview",
                class_name="text-lg font-semibold text-gray-900 mb-4",
            ),
            rx.foreach(NewsState.topics, topic_group),
            class_name="max-w-4xl mx-auto",
        ),
        class_name="animate-fade-in",
    )