import reflex as rx
from app.components.sidebar import sidebar
from app.components.daily_briefing_view import daily_briefing_view
from app.components.daily_topics_view import daily_topics_view
from app.components.article_modal import article_detail_modal
from app.states.news_state import NewsState


def view_toggle() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon("layout-list", class_name="w-4 h-4 mr-2"),
            "Flat View",
            on_click=lambda: NewsState.set_view_mode("flat"),
            class_name=rx.cond(
                NewsState.is_flat_view,
                "flex items-center px-4 py-2 rounded-lg bg-white text-violet-700 shadow-sm text-sm font-semibold transition-all border border-gray-200",
                "flex items-center px-4 py-2 rounded-lg text-gray-500 hover:text-gray-900 hover:bg-gray-100 text-sm font-medium transition-all",
            ),
        ),
        rx.el.button(
            rx.icon("layout-grid", class_name="w-4 h-4 mr-2"),
            "Topic View",
            on_click=lambda: NewsState.set_view_mode("topic"),
            class_name=rx.cond(
                NewsState.is_topic_view,
                "flex items-center px-4 py-2 rounded-lg bg-white text-violet-700 shadow-sm text-sm font-semibold transition-all border border-gray-200",
                "flex items-center px-4 py-2 rounded-lg text-gray-500 hover:text-gray-900 hover:bg-gray-100 text-sm font-medium transition-all",
            ),
        ),
        class_name="flex items-center p-1 bg-gray-100 rounded-xl border border-gray-200/50",
    )


def date_navigator() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon("chevron-left", class_name="w-5 h-5"),
            class_name="p-2 rounded-lg hover:bg-gray-100 text-gray-500 transition-colors",
        ),
        rx.el.div(
            rx.icon("calendar", class_name="w-4 h-4 text-violet-500 mr-2"),
            rx.el.span(
                NewsState.current_date, class_name="font-semibold text-gray-900"
            ),
            class_name="flex items-center px-4 py-2 bg-white border border-gray-200 rounded-lg shadow-sm mx-2",
        ),
        rx.el.button(
            rx.icon("chevron-right", class_name="w-5 h-5"),
            class_name="p-2 rounded-lg hover:bg-gray-100 text-gray-500 transition-colors",
        ),
        class_name="flex items-center",
    )


from app.components.dominant_news_view import dominant_news_view
from app.components.topic_explorer_view import topic_explorer_view
from app.components.story_timeline_view import story_timeline_view
from app.components.causal_network_view import causal_network_view
from app.components.recurring_patterns_view import recurring_patterns_view


def daily_view_layout() -> rx.Component:
    return rx.el.main(
        rx.el.header(
            rx.el.div(
                date_navigator(),
                view_toggle(),
                class_name="flex items-center justify-between max-w-4xl mx-auto w-full",
            ),
            class_name="sticky top-0 z-10 bg-white/80 backdrop-blur-md border-b border-gray-100 py-4 px-8",
        ),
        rx.el.div(
            rx.cond(NewsState.is_flat_view, daily_briefing_view(), daily_topics_view()),
            class_name="p-8 min-h-[calc(100vh-80px)]",
        ),
        class_name="flex-1 ml-72 bg-white min-h-screen",
    )


def content_area() -> rx.Component:
    return rx.match(
        NewsState.current_view,
        ("daily_briefing", daily_view_layout()),
        ("daily_topics", daily_view_layout()),
        ("dominant_news", dominant_news_view()),
        ("topic_explorer", topic_explorer_view()),
        ("story_timeline", story_timeline_view()),
        ("causal_network", causal_network_view()),
        ("recurring_patterns", recurring_patterns_view()),
        daily_view_layout(),
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        content_area(),
        article_detail_modal(),
        class_name="flex w-full min-h-screen bg-white font-['Inter'] text-gray-900",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    ],
)
app.add_page(index, route="/")