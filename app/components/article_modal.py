import reflex as rx
from app.states.news_state import NewsState, Article


def article_detail_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "Article Details", class_name="hidden"
                ),
                rx.cond(
                    NewsState.selected_article,
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    NewsState.selected_article["source"],
                                    class_name="text-sm font-bold text-violet-600 uppercase tracking-wide",
                                ),
                                rx.el.span(" • ", class_name="text-gray-300 mx-2"),
                                rx.el.span(
                                    NewsState.selected_article["published_at"],
                                    class_name="text-sm text-gray-500",
                                ),
                                class_name="flex items-center mb-3",
                            ),
                            rx.el.h2(
                                NewsState.selected_article["title"],
                                class_name="text-2xl font-bold text-gray-900 leading-tight",
                            ),
                            class_name="mb-6 pb-6 border-b border-gray-100",
                        ),
                        rx.el.div(
                            rx.el.p(
                                NewsState.selected_article["full_text"],
                                class_name="text-lg text-gray-700 leading-relaxed font-serif",
                            ),
                            rx.el.div(
                                rx.el.a(
                                    "Read original source",
                                    rx.icon("external-link", class_name="w-4 h-4 ml-1"),
                                    href=NewsState.selected_article["url"],
                                    target="_blank",
                                    class_name="inline-flex items-center text-violet-600 hover:text-violet-700 font-medium mt-6",
                                ),
                                class_name="mt-4",
                            ),
                            class_name="prose prose-slate max-w-none",
                        ),
                    ),
                    rx.fragment(),
                ),
                rx.radix.primitives.dialog.close(
                    rx.el.button(
                        rx.icon(
                            "x", class_name="w-6 h-6 text-gray-400 hover:text-gray-600"
                        ),
                        class_name="absolute top-4 right-4 p-2 hover:bg-gray-100 rounded-full transition-colors",
                    )
                ),
                class_name="fixed left-[50%] top-[50%] z-50 w-full max-w-2xl translate-x-[-50%] translate-y-[-50%] bg-white p-8 shadow-2xl sm:rounded-2xl max-h-[85vh] overflow-y-auto focus:outline-none",
            ),
        ),
        open=NewsState.is_modal_open,
        on_open_change=NewsState.set_is_modal_open,
    )