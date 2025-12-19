import reflex as rx
from app.states.news_state import NewsState, NewsItem, Article, Relationship
from app.components.badges import relationship_badge, count_badge


def article_list_item(article: Article) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h4(
                article["title"],
                class_name="text-sm font-medium text-gray-900 group-hover:text-violet-600 transition-colors",
            ),
            rx.el.div(
                rx.el.span(article["source"], class_name="font-semibold text-gray-700"),
                rx.el.span(" • ", class_name="mx-1 text-gray-300"),
                rx.el.span(article["published_at"], class_name="text-gray-500"),
                class_name="text-xs mt-1 flex items-center",
            ),
            class_name="flex-1",
        ),
        rx.el.button(
            "Read",
            on_click=lambda: NewsState.open_article(article),
            class_name="text-xs font-medium text-violet-600 hover:bg-violet-50 px-3 py-1.5 rounded-md transition-colors opacity-0 group-hover:opacity-100",
        ),
        class_name="flex items-center p-3 rounded-lg hover:bg-gray-50 border border-transparent hover:border-gray-200 transition-all group cursor-pointer",
    )


def news_item_card(item: NewsItem) -> rx.Component:
    is_expanded = NewsState.expanded_news_ids.contains(item["id"])
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.span(item["emoji"], class_name="text-2xl"),
                        class_name="w-12 h-12 rounded-xl bg-gray-50 flex items-center justify-center shrink-0",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            item["title"],
                            class_name="text-lg font-semibold text-gray-900",
                        ),
                        rx.el.p(
                            item["summary"],
                            class_name="text-sm text-gray-500 mt-1 line-clamp-1",
                        ),
                        rx.el.div(
                            count_badge(item["article_count"]),
                            rx.foreach(
                                item["relationships"],
                                lambda r: relationship_badge(
                                    r["type"], r["description"]
                                ),
                            ),
                            class_name="flex flex-wrap gap-2 mt-2 items-center",
                        ),
                        class_name="ml-4 flex-1",
                    ),
                    class_name="flex items-start flex-1",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.cond(is_expanded, "Hide Articles", "View Articles"),
                        rx.icon(
                            "chevron-down",
                            class_name=rx.cond(
                                is_expanded,
                                "w-4 h-4 ml-2 rotate-180 transition-transform",
                                "w-4 h-4 ml-2 transition-transform",
                            ),
                        ),
                        on_click=lambda: NewsState.toggle_news_expanded(item["id"]),
                        class_name="flex items-center text-sm font-medium text-gray-500 hover:text-violet-600 transition-colors px-3 py-2 rounded-lg hover:bg-violet-50",
                    ),
                    class_name="ml-4 flex items-center",
                ),
                class_name="flex items-start justify-between p-6",
            ),
            rx.cond(
                is_expanded,
                rx.el.div(
                    rx.el.div(
                        rx.el.h4(
                            "Associated Coverage",
                            class_name="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3 pl-2",
                        ),
                        rx.el.div(
                            rx.foreach(item["articles"], article_list_item),
                            class_name="space-y-1",
                        ),
                        class_name="p-4 bg-gray-50/50 border-t border-gray-100 rounded-b-xl",
                    ),
                    class_name="animate-fade-in",
                ),
                rx.fragment(),
            ),
            class_name="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow",
        ),
        class_name="mb-4",
    )


def daily_briefing_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Top Stories", class_name="text-lg font-semibold text-gray-900 mb-4"
            ),
            rx.foreach(NewsState.news_items, news_item_card),
            rx.el.div(
                rx.el.div(
                    rx.icon("info", class_name="w-4 h-4 text-gray-400 mr-2"),
                    rx.el.span(
                        f"{NewsState.outliers_count} outlier articles excluded from clusters",
                        class_name="text-sm text-gray-500 font-medium",
                    ),
                    class_name="flex items-center justify-center py-4",
                ),
                class_name="mt-8 border-t border-gray-100 border-dashed",
            ),
            class_name="max-w-4xl mx-auto",
        ),
        class_name="animate-fade-in",
    )