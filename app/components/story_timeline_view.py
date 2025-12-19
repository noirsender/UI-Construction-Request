import reflex as rx
from app.states.news_state import NewsState, StoryPhase


def timeline_node(phase: StoryPhase, index: int) -> rx.Component:
    is_selected = NewsState.st_selected_phase_id == phase["id"]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.cond(
                    index > 0,
                    rx.el.div(
                        class_name="absolute top-1/2 right-full w-full h-0.5 bg-gray-200 -translate-y-1/2 z-0"
                    ),
                    rx.fragment(),
                ),
                rx.el.button(
                    rx.cond(
                        is_selected,
                        rx.el.div(class_name="w-3 h-3 bg-white rounded-full"),
                        rx.el.div(class_name="w-2 h-2 bg-white/80 rounded-full"),
                    ),
                    on_click=lambda: NewsState.set_st_phase(phase["id"]),
                    class_name=rx.cond(
                        is_selected,
                        "relative z-10 w-8 h-8 rounded-full bg-violet-600 shadow-lg shadow-violet-200 flex items-center justify-center transition-all scale-110",
                        "relative z-10 w-6 h-6 rounded-full bg-gray-300 hover:bg-violet-400 flex items-center justify-center transition-all",
                    ),
                ),
                class_name="relative flex items-center justify-center w-full",
            ),
            rx.el.div(
                rx.el.span(
                    phase["date"],
                    class_name="text-xs font-semibold text-violet-600 mb-1 block",
                ),
                rx.el.h4(
                    phase["phase_name"],
                    class_name=rx.cond(
                        is_selected,
                        "text-sm font-bold text-gray-900",
                        "text-sm font-medium text-gray-500",
                    ),
                ),
                class_name="mt-4 text-center w-32",
            ),
            class_name="flex flex-col items-center relative px-8",
        ),
        class_name="flex flex-col items-center",
    )


def phase_detail_panel() -> rx.Component:
    phase = NewsState.selected_phase
    return rx.cond(
        phase,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Selected Phase",
                        class_name="text-xs font-semibold text-gray-400 uppercase tracking-wider",
                    ),
                    rx.el.h3(
                        phase["phase_name"],
                        class_name="text-2xl font-bold text-gray-900 mt-2",
                    ),
                    rx.el.p(
                        phase["description"],
                        class_name="text-lg text-gray-600 mt-4 leading-relaxed",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            f"{phase['article_count']}",
                            class_name="text-3xl font-bold text-gray-900",
                        ),
                        rx.el.span("articles", class_name="text-sm text-gray-500 ml-2"),
                        class_name="flex items-baseline mb-2",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Read Analysis",
                            class_name="w-full py-3 bg-violet-600 hover:bg-violet-700 text-white rounded-xl font-medium transition-colors shadow-sm",
                        ),
                        rx.el.button(
                            "View Source Articles",
                            class_name="w-full py-3 bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 rounded-xl font-medium transition-colors mt-3",
                        ),
                        class_name="mt-6",
                    ),
                    class_name="bg-gray-50 rounded-2xl p-6 border border-gray-100",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-12",
            ),
            class_name="mt-16 animate-fade-in",
        ),
        rx.fragment(),
    )


def story_timeline_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Story Timeline", class_name="text-2xl font-bold text-gray-900 mb-1"
                ),
                rx.el.p(
                    NewsState.active_timeline["name"],
                    class_name="text-lg text-gray-500",
                ),
                class_name="mb-12 text-center",
            ),
            rx.el.div(
                rx.foreach(
                    NewsState.active_timeline["phases"],
                    lambda p, i: timeline_node(p, i),
                ),
                class_name="flex items-start justify-center relative",
            ),
            phase_detail_panel(),
            class_name="max-w-5xl mx-auto py-16 px-8",
        ),
        class_name="flex-1 ml-72 bg-white min-h-screen",
    )