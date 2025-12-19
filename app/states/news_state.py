import reflex as rx
from typing import TypedDict, Optional


class Article(TypedDict):
    id: int
    title: str
    source: str
    preview: str
    full_text: str
    published_at: str
    url: str


class Relationship(TypedDict):
    type: str
    target_id: str
    description: str


class NewsItem(TypedDict):
    id: str
    title: str
    emoji: str
    article_count: int
    articles: list[Article]
    summary: str
    relationships: list[Relationship]
    coverage_percentage: int


class Topic(TypedDict):
    id: str
    name: str
    emoji: str
    news_item_ids: list[str]
    total_articles: int


class DailyCount(TypedDict):
    date: str
    count: int


class NewsBurst(TypedDict):
    id: str
    title: str
    emoji: str
    medoid_article_id: int
    article_count: int
    start_date: str
    end_date: str
    duration_days: int
    coverage_percentage: int
    summary: str
    related_topic_ids: list[str]
    linked_burst_ids: list[str]
    daily_counts: list[DailyCount]


class CrossTimeTopic(TypedDict):
    id: str
    name: str
    emoji: str
    burst_ids: list[str]
    total_articles: int
    date_range: str


class StoryPhase(TypedDict):
    id: str
    burst_id: str
    phase_name: str
    date: str
    description: str
    article_count: int


class StoryTimeline(TypedDict):
    id: str
    name: str
    phases: list[StoryPhase]


class CausalNode(TypedDict):
    id: str
    burst_id: str
    label: str
    date: str
    type: str
    article_count: int


class CausalLink(TypedDict):
    source: str
    target: str
    relationship: str


class RecurringInstance(TypedDict):
    id: str
    date: str
    value: str
    change: str
    trend: str
    article_count: int
    summary: str
    burst_id: str


class RecurringSeries(TypedDict):
    id: str
    name: str
    pattern_type: str
    company: str
    instances: list[RecurringInstance]
    overall_trend: str


class NewsState(rx.State):
    current_view: str = "daily_briefing"
    current_view_mode: str = "flat"
    current_date: str = "March 15, 2025"
    dn_start_date: str = "2025-03-01"
    dn_end_date: str = "2025-03-31"
    dn_sort_by: str = "count"
    te_search_query: str = ""
    te_selected_topic_id: str = "topic_energy_cross"
    st_selected_timeline_id: str = "timeline_tax"
    st_selected_phase_id: str = "phase_1"
    cn_selected_node_id: str = "node_policy"
    rp_selected_pattern_type: str = "all"
    rp_selected_company: str = "all"
    rp_selected_series_id: str = "series_electricity"
    expanded_news_ids: list[str] = []
    expanded_topic_ids: list[str] = ["topic_energy", "topic_culture"]
    is_modal_open: bool = False
    selected_article: Optional[Article] = None
    _articles_pool: dict[int, Article] = {
        101: {
            "id": 101,
            "title": "Helleniq Energy reports record Q4 profits",
            "source": "Financial Times",
            "preview": "Helleniq Energy announced record-breaking Q4 results today...",
            "full_text": "Helleniq Energy announced record-breaking Q4 results today, driven by strong refining margins and increased export activity. The company reported EBITDA of €400M, exceeding analyst expectations by 15%. CEO John Doe attributed the success to operational efficiency and strategic hedging.",
            "published_at": "10:30 AM",
            "url": "#",
        },
        102: {
            "id": 102,
            "title": "Energy sector booms as Helleniq beats estimates",
            "source": "Bloomberg",
            "preview": "Markets reacted positively to Helleniq's earnings call...",
            "full_text": "Markets reacted positively to Helleniq's earnings call. Shares rose 5% in early trading. Analysts point to the robust demand in the Balkan region as a key driver for the company's performance this quarter.",
            "published_at": "11:15 AM",
            "url": "#",
        },
        103: {
            "id": 103,
            "title": "Refining margins boost Helleniq Q4",
            "source": "Reuters",
            "preview": "Strong refining margins were the primary driver...",
            "full_text": "Strong refining margins were the primary driver for Helleniq's Q4 success. The company also announced a new dividend policy that pleased shareholders.",
            "published_at": "09:45 AM",
            "url": "#",
        },
        104: {
            "id": 104,
            "title": "Analyst View: Helleniq Energy",
            "source": "Capital.gr",
            "preview": "Local analysts upgrade Helleniq stock to Buy...",
            "full_text": "Local analysts upgrade Helleniq stock to Buy following the earnings release. The long-term outlook remains positive despite volatility in oil prices.",
            "published_at": "02:00 PM",
            "url": "#",
        },
        105: {
            "id": 105,
            "title": "Helleniq dividend announcement details",
            "source": "Naftemporiki",
            "preview": "The board proposed a dividend of €0.50 per share...",
            "full_text": "The board proposed a dividend of €0.50 per share, payable in May. This represents a 10% increase year-over-year.",
            "published_at": "12:00 PM",
            "url": "#",
        },
        201: {
            "id": 201,
            "title": "Roots of Gazi Festival announced for June",
            "source": "Culture Now",
            "preview": "The annual Roots of Gazi festival returns this summer...",
            "full_text": "The annual Roots of Gazi festival returns this summer with a focus on urban folk music. Organizers promise the biggest lineup in the festival's history.",
            "published_at": "09:00 AM",
            "url": "#",
        },
        202: {
            "id": 202,
            "title": "Gazi Festival lineup revealed",
            "source": "Lifo",
            "preview": "Top headliners include...",
            "full_text": "Top headliners include traditional bands and modern fusion artists. Tickets go on sale next week.",
            "published_at": "10:00 AM",
            "url": "#",
        },
        203: {
            "id": 203,
            "title": "Summer culture calendar heats up",
            "source": "Kathimerini",
            "preview": "With the announcement of Roots of Gazi...",
            "full_text": "With the announcement of Roots of Gazi, the summer cultural calendar is filling up fast. The municipality expects record tourist attendance.",
            "published_at": "11:30 AM",
            "url": "#",
        },
        301: {
            "id": 301,
            "title": "Electricity prices for March released",
            "source": "Energy Press",
            "preview": "Providers have released their tariffs for March...",
            "full_text": "Providers have released their tariffs for March. Prices show a slight upward trend compared to February due to gas price fluctuations.",
            "published_at": "08:00 AM",
            "url": "#",
        },
        302: {
            "id": 302,
            "title": "DEI announces new Green tariff",
            "source": "News247",
            "preview": "DEI's green tariff set at 15 cents...",
            "full_text": "DEI's green tariff set at 15 cents per kWh. Consumers are advised to compare rates before locking in contracts.",
            "published_at": "08:15 AM",
            "url": "#",
        },
        303: {
            "id": 303,
            "title": "Market roundup: Energy costs rising",
            "source": "Euro2day",
            "preview": "A comprehensive look at the energy market...",
            "full_text": "A comprehensive look at the energy market shows a 3% average increase in consumer electricity costs for the upcoming month.",
            "published_at": "10:45 AM",
            "url": "#",
        },
        304: {
            "id": 304,
            "title": "Government Tax Policy Reform",
            "source": "Gov News",
            "preview": "New tax policy aims to simplify VAT...",
            "full_text": "New tax policy aims to simplify VAT structure for small businesses. The finance ministry expects this to boost compliance.",
            "published_at": "01:00 PM",
            "url": "#",
        },
        305: {
            "id": 305,
            "title": "Opposition slams tax reform",
            "source": "Political Daily",
            "preview": "Opposition leaders claim the new tax policy hurts the poor...",
            "full_text": "Opposition leaders claim the new tax policy hurts the poor and favors large corporations. They vow to fight the bill in parliament.",
            "published_at": "03:30 PM",
            "url": "#",
        },
        401: {
            "id": 401,
            "title": "Factory workers strike over wages",
            "source": "Labor News",
            "preview": "Thousands of workers walked off the job today...",
            "full_text": "Thousands of workers walked off the job today demanding better pay and working conditions. The strike has halted production at major industrial zones.",
            "published_at": "11:00 AM",
            "url": "#",
        },
        402: {
            "id": 402,
            "title": "Industrial zone paralyzed by strike",
            "source": "Local News",
            "preview": "Production standstill as negotiations fail...",
            "full_text": "Production standstill as negotiations fail between unions and management. The government has urged both sides to return to the table.",
            "published_at": "01:30 PM",
            "url": "#",
        },
        501: {
            "id": 501,
            "title": "Family activities at Gazi Festival",
            "source": "Kids in City",
            "preview": "Special zone for children announced...",
            "full_text": "Special zone for children announced for the upcoming festival, featuring workshops and puppet shows.",
            "published_at": "12:00 PM",
            "url": "#",
        },
        502: {
            "id": 502,
            "title": "Weekend guide: Festival preview",
            "source": "Timeout",
            "preview": "Get a sneak peek at the family events...",
            "full_text": "Get a sneak peek at the family events planned for the Gazi festival. Early bird tickets for families are now available.",
            "published_at": "04:00 PM",
            "url": "#",
        },
        503: {
            "id": 503,
            "title": "Cultural education workshops",
            "source": "Education Weekly",
            "preview": "Workshops to teach traditional instruments...",
            "full_text": "Workshops to teach traditional instruments will be part of the family activities zone.",
            "published_at": "02:15 PM",
            "url": "#",
        },
    }
    news_items: list[NewsItem] = [
        {
            "id": "news_1",
            "title": "Helleniq Energy Q4 Results",
            "emoji": "📊",
            "article_count": 5,
            "articles": [
                _articles_pool[101],
                _articles_pool[102],
                _articles_pool[103],
                _articles_pool[104],
                _articles_pool[105],
            ],
            "summary": "Helleniq Energy reports record Q4 profits driven by strong refining margins.",
            "relationships": [],
            "coverage_percentage": 80,
        },
        {
            "id": "news_2",
            "title": 'Festival "Roots of Gazi" Announced',
            "emoji": "🎭",
            "article_count": 3,
            "articles": [_articles_pool[201], _articles_pool[202], _articles_pool[203]],
            "summary": "Annual cultural festival returns with focus on urban folk music.",
            "relationships": [],
            "coverage_percentage": 40,
        },
        {
            "id": "news_3",
            "title": "Market Electricity Price Roundup",
            "emoji": "⚡",
            "article_count": 3,
            "articles": [_articles_pool[301], _articles_pool[302], _articles_pool[303]],
            "summary": "March electricity tariffs show slight increase across major providers.",
            "relationships": [
                {
                    "type": "trend",
                    "target_id": "monthly_price_pattern",
                    "description": "Part of monthly price pattern",
                }
            ],
            "coverage_percentage": 50,
        },
        {
            "id": "news_4",
            "title": "Government Policy Update",
            "emoji": "🏛️",
            "article_count": 2,
            "articles": [_articles_pool[304], _articles_pool[305]],
            "summary": "New tax policy reform announced amidst political debate.",
            "relationships": [],
            "coverage_percentage": 30,
        },
        {
            "id": "news_5",
            "title": "Factory Workers Strike",
            "emoji": "🏭",
            "article_count": 2,
            "articles": [_articles_pool[401], _articles_pool[402]],
            "summary": "Industrial action halts production over wage disputes.",
            "relationships": [
                {
                    "type": "causal",
                    "target_id": "news_4",
                    "description": "Union response to policy update",
                }
            ],
            "coverage_percentage": 25,
        },
        {
            "id": "news_6",
            "title": "Festival Family Activities",
            "emoji": "🎪",
            "article_count": 3,
            "articles": [_articles_pool[501], _articles_pool[502], _articles_pool[503]],
            "summary": "Special events for children announced for the upcoming festival.",
            "relationships": [
                {
                    "type": "compatible",
                    "target_id": "news_2",
                    "description": "Sub-event of Roots of Gazi",
                }
            ],
            "coverage_percentage": 35,
        },
    ]
    topics: list[Topic] = [
        {
            "id": "topic_energy",
            "name": "Energy Sector",
            "emoji": "📈",
            "news_item_ids": ["news_1", "news_3"],
            "total_articles": 8,
        },
        {
            "id": "topic_culture",
            "name": "Cultural Events",
            "emoji": "🎭",
            "news_item_ids": ["news_2", "news_6"],
            "total_articles": 6,
        },
        {
            "id": "topic_gov",
            "name": "Government & Labor",
            "emoji": "🏛️",
            "news_item_ids": ["news_4", "news_5"],
            "total_articles": 4,
        },
    ]
    outliers_count: int = 2

    @rx.event
    def set_view_mode(self, mode: str):
        self.current_view_mode = mode

    @rx.event
    def toggle_news_expanded(self, news_id: str):
        if news_id in self.expanded_news_ids:
            self.expanded_news_ids.remove(news_id)
        else:
            self.expanded_news_ids.append(news_id)

    @rx.event
    def toggle_topic_expanded(self, topic_id: str):
        if topic_id in self.expanded_topic_ids:
            self.expanded_topic_ids.remove(topic_id)
        else:
            self.expanded_topic_ids.append(topic_id)

    @rx.event
    def open_article(self, article: Article):
        self.selected_article = article
        self.is_modal_open = True

    @rx.event
    def close_modal(self):
        self.is_modal_open = False
        self.selected_article = None

    @rx.event
    def set_current_view(self, view: str):
        self.current_view = view
        if view == "daily_briefing":
            self.current_view_mode = "flat"
        elif view == "daily_topics":
            self.current_view_mode = "topic"

    @rx.event
    def set_dn_sort(self, sort_by: str):
        self.dn_sort_by = sort_by

    @rx.event
    def set_te_topic(self, topic_id: str):
        self.te_selected_topic_id = topic_id

    @rx.event
    def set_st_phase(self, phase_id: str):
        self.st_selected_phase_id = phase_id

    @rx.var
    def is_flat_view(self) -> bool:
        return self.current_view_mode == "flat"

    @rx.var
    def is_topic_view(self) -> bool:
        return self.current_view_mode == "topic"

    news_bursts: list[NewsBurst] = [
        {
            "id": "burst_1",
            "title": "Helleniq Energy Q4 Results",
            "emoji": "📊",
            "medoid_article_id": 101,
            "article_count": 47,
            "start_date": "Mar 15",
            "end_date": "Mar 18",
            "duration_days": 3,
            "coverage_percentage": 80,
            "summary": "Helleniq Energy reports record Q4 profits driven by strong refining margins.",
            "related_topic_ids": ["topic_energy_cross"],
            "linked_burst_ids": [],
            "daily_counts": [
                {"date": "15", "count": 20},
                {"date": "16", "count": 15},
                {"date": "17", "count": 8},
                {"date": "18", "count": 4},
            ],
        },
        {
            "id": "burst_2",
            "title": "Government Tax Policy Reform",
            "emoji": "🏛️",
            "medoid_article_id": 304,
            "article_count": 38,
            "start_date": "Mar 5",
            "end_date": "Mar 12",
            "duration_days": 7,
            "coverage_percentage": 65,
            "summary": "New tax policy reform announced amidst political debate and union opposition.",
            "related_topic_ids": ["topic_gov_cross"],
            "linked_burst_ids": ["burst_5"],
            "daily_counts": [
                {"date": "5", "count": 10},
                {"date": "6", "count": 12},
                {"date": "7", "count": 5},
                {"date": "8", "count": 8},
                {"date": "12", "count": 3},
            ],
        },
        {
            "id": "burst_3",
            "title": "Festival 'Roots of Gazi'",
            "emoji": "🎭",
            "medoid_article_id": 201,
            "article_count": 23,
            "start_date": "Mar 15",
            "end_date": "Mar 16",
            "duration_days": 2,
            "coverage_percentage": 40,
            "summary": "Annual cultural festival returns with focus on urban folk music.",
            "related_topic_ids": ["topic_culture_cross"],
            "linked_burst_ids": [],
            "daily_counts": [{"date": "15", "count": 15}, {"date": "16", "count": 8}],
        },
        {
            "id": "burst_4",
            "title": "DEI Electricity Prices",
            "emoji": "⚡",
            "medoid_article_id": 301,
            "article_count": 18,
            "start_date": "Mar 10",
            "end_date": "Mar 12",
            "duration_days": 3,
            "coverage_percentage": 30,
            "summary": "March electricity tariffs show slight increase across major providers.",
            "related_topic_ids": ["topic_energy_cross"],
            "linked_burst_ids": [],
            "daily_counts": [
                {"date": "10", "count": 10},
                {"date": "11", "count": 5},
                {"date": "12", "count": 3},
            ],
        },
        {
            "id": "burst_5",
            "title": "Factory Workers Strike",
            "emoji": "🏭",
            "medoid_article_id": 401,
            "article_count": 25,
            "start_date": "Mar 8",
            "end_date": "Mar 10",
            "duration_days": 3,
            "coverage_percentage": 45,
            "summary": "Industrial action halts production over wage disputes linked to new policy.",
            "related_topic_ids": ["topic_gov_cross"],
            "linked_burst_ids": ["burst_2"],
            "daily_counts": [
                {"date": "8", "count": 15},
                {"date": "9", "count": 8},
                {"date": "10", "count": 2},
            ],
        },
    ]
    cross_time_topics: list[CrossTimeTopic] = [
        {
            "id": "topic_energy_cross",
            "name": "Energy Sector",
            "emoji": "📈",
            "burst_ids": ["burst_1", "burst_4"],
            "total_articles": 65,
            "date_range": "Mar 1 - Mar 31",
        },
        {
            "id": "topic_gov_cross",
            "name": "Political Crisis",
            "emoji": "🏛️",
            "burst_ids": ["burst_2", "burst_5"],
            "total_articles": 63,
            "date_range": "Mar 5 - Mar 20",
        },
        {
            "id": "topic_culture_cross",
            "name": "Cultural Events",
            "emoji": "🎭",
            "burst_ids": ["burst_3"],
            "total_articles": 23,
            "date_range": "Mar 15 - Mar 16",
        },
    ]
    story_timelines: list[StoryTimeline] = [
        {
            "id": "timeline_tax",
            "name": "Tax Policy Reform",
            "phases": [
                {
                    "id": "phase_1",
                    "burst_id": "burst_2",
                    "phase_name": "Policy Announced",
                    "date": "Mar 5",
                    "description": "Government announces 20% VAT reduction plan.",
                    "article_count": 38,
                },
                {
                    "id": "phase_2",
                    "burst_id": "burst_5",
                    "phase_name": "Protests Erupt",
                    "date": "Mar 8",
                    "description": "Unions organize strikes in industrial zones.",
                    "article_count": 25,
                },
                {
                    "id": "phase_3",
                    "burst_id": "burst_x",
                    "phase_name": "Government Response",
                    "date": "Mar 10",
                    "description": "Minister calls for dialogue with union leaders.",
                    "article_count": 15,
                },
            ],
        }
    ]

    @rx.var
    def sorted_bursts(self) -> list[NewsBurst]:
        if self.dn_sort_by == "duration":
            return sorted(
                self.news_bursts, key=lambda x: x["duration_days"], reverse=True
            )
        elif self.dn_sort_by == "recent":
            return self.news_bursts
        else:
            return sorted(
                self.news_bursts, key=lambda x: x["article_count"], reverse=True
            )

    @rx.var
    def selected_topic(self) -> Optional[CrossTimeTopic]:
        for t in self.cross_time_topics:
            if t["id"] == self.te_selected_topic_id:
                return t
        return None

    @rx.var
    def selected_topic_bursts(self) -> list[NewsBurst]:
        topic = self.selected_topic
        if not topic:
            return []
        return [b for b in self.news_bursts if b["id"] in topic["burst_ids"]]

    @rx.var
    def active_timeline(self) -> Optional[StoryTimeline]:
        for t in self.story_timelines:
            if t["id"] == self.st_selected_timeline_id:
                return t
        return None

    @rx.var
    def selected_phase(self) -> Optional[StoryPhase]:
        timeline = self.active_timeline
        if not timeline:
            return None
        for p in timeline["phases"]:
            if p["id"] == self.st_selected_phase_id:
                return p
        return None

    causal_nodes: list[CausalNode] = [
        {
            "id": "node_policy",
            "burst_id": "burst_2",
            "label": "Tax Policy Announced",
            "date": "Mar 5",
            "type": "trigger",
            "article_count": 38,
        },
        {
            "id": "node_protest",
            "burst_id": "burst_5",
            "label": "Protests Erupt",
            "date": "Mar 8",
            "type": "reaction",
            "article_count": 25,
        },
        {
            "id": "node_market",
            "burst_id": "burst_mkt",
            "label": "Market Reaction",
            "date": "Mar 6",
            "type": "reaction",
            "article_count": 8,
        },
        {
            "id": "node_opp",
            "burst_id": "burst_opp",
            "label": "Opposition Response",
            "date": "Mar 6",
            "type": "reaction",
            "article_count": 12,
        },
        {
            "id": "node_gov",
            "burst_id": "burst_gov",
            "label": "Government Response",
            "date": "Mar 10",
            "type": "outcome",
            "article_count": 15,
        },
    ]
    causal_links: list[CausalLink] = [
        {"source": "node_policy", "target": "node_protest", "relationship": "Triggers"},
        {"source": "node_policy", "target": "node_market", "relationship": "Impacts"},
        {
            "source": "node_policy",
            "target": "node_opp",
            "relationship": "Criticized by",
        },
        {"source": "node_protest", "target": "node_gov", "relationship": "Forces"},
    ]
    recurring_series_list: list[RecurringSeries] = [
        {
            "id": "series_electricity",
            "name": "Electricity Price Announcements",
            "pattern_type": "monthly",
            "company": "Multiple",
            "overall_trend": "up",
            "instances": [
                {
                    "id": "inst_jan",
                    "date": "Jan 1",
                    "value": "€0.145/kWh",
                    "change": "+2%",
                    "trend": "up",
                    "article_count": 15,
                    "summary": "January tariffs announced with slight increase due to cold weather forecasts.",
                    "burst_id": "burst_jan",
                },
                {
                    "id": "inst_feb",
                    "date": "Feb 1",
                    "value": "€0.149/kWh",
                    "change": "+3%",
                    "trend": "up",
                    "article_count": 18,
                    "summary": "February prices continue upward trend as gas prices fluctuate.",
                    "burst_id": "burst_feb",
                },
                {
                    "id": "inst_mar",
                    "date": "Mar 1",
                    "value": "€0.154/kWh",
                    "change": "+3%",
                    "trend": "up",
                    "article_count": 18,
                    "summary": "March tariffs released showing sustained increase across all major providers.",
                    "burst_id": "burst_4",
                },
                {
                    "id": "inst_apr",
                    "date": "Apr 1",
                    "value": "€0.152/kWh",
                    "change": "-1%",
                    "trend": "down",
                    "article_count": 12,
                    "summary": "Projected April prices show first signs of stabilization.",
                    "burst_id": "burst_apr",
                },
            ],
        },
        {
            "id": "series_earnings",
            "name": "Helleniq Quarterly Earnings",
            "pattern_type": "quarterly",
            "company": "Helleniq Energy",
            "overall_trend": "up",
            "instances": [
                {
                    "id": "ear_q1",
                    "date": "May 15",
                    "value": "€320M",
                    "change": "+5%",
                    "trend": "up",
                    "article_count": 22,
                    "summary": "Q1 results show strong start to the year.",
                    "burst_id": "burst_q1",
                },
                {
                    "id": "ear_q2",
                    "date": "Aug 15",
                    "value": "€350M",
                    "change": "+9%",
                    "trend": "up",
                    "article_count": 25,
                    "summary": "Record tourism boosts Q2 fuel demand.",
                    "burst_id": "burst_q2",
                },
                {
                    "id": "ear_q3",
                    "date": "Nov 15",
                    "value": "€380M",
                    "change": "+8%",
                    "trend": "up",
                    "article_count": 28,
                    "summary": "Q3 outperforms expectations.",
                    "burst_id": "burst_q3",
                },
                {
                    "id": "ear_q4",
                    "date": "Mar 15",
                    "value": "€400M",
                    "change": "+5%",
                    "trend": "up",
                    "article_count": 47,
                    "summary": "Record Q4 profits driven by refining margins.",
                    "burst_id": "burst_1",
                },
            ],
        },
    ]

    @rx.event
    def set_cn_node(self, node_id: str):
        self.cn_selected_node_id = node_id

    @rx.event
    def set_rp_pattern_type(self, pattern_type: str):
        self.rp_selected_pattern_type = pattern_type

    @rx.event
    def set_rp_company(self, company: str):
        self.rp_selected_company = company

    @rx.event
    def set_rp_series(self, series_id: str):
        self.rp_selected_series_id = series_id

    @rx.event
    def export_data(self):
        """Simulate exporting data for the current view."""
        return rx.download(
            data=f"Exported data for {self.current_view} view.\nDate: {self.current_date}\nUser: John Doe",
            filename=f"{self.current_view}_export.txt",
        )

    @rx.var
    def cn_selected_node(self) -> Optional[CausalNode]:
        for node in self.causal_nodes:
            if node["id"] == self.cn_selected_node_id:
                return node
        return None

    @rx.var
    def cn_parents(self) -> list[CausalNode]:
        parent_ids = [
            link["source"]
            for link in self.causal_links
            if link["target"] == self.cn_selected_node_id
        ]
        return [node for node in self.causal_nodes if node["id"] in parent_ids]

    @rx.var
    def cn_children(self) -> list[CausalNode]:
        child_ids = [
            link["target"]
            for link in self.causal_links
            if link["source"] == self.cn_selected_node_id
        ]
        return [node for node in self.causal_nodes if node["id"] in child_ids]

    @rx.var
    def filtered_recurring_series(self) -> list[RecurringSeries]:
        series = self.recurring_series_list
        if self.rp_selected_pattern_type != "all":
            series = [
                s for s in series if s["pattern_type"] == self.rp_selected_pattern_type
            ]
        if self.rp_selected_company != "all":
            series = [
                s
                for s in series
                if self.rp_selected_company in s["company"]
                or s["company"] == "Multiple"
            ]
        return series