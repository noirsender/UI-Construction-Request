# COMPLETE SYSTEM DOCUMENTATION

---

## PART 1: SYSTEM FLOW

---

### **Overview**

The system transforms raw news articles into a multi-level hierarchical structure that reveals:
- Individual distinct news items (Level 1)
- Same-day thematic groupings (Level 1.5)
- News bursts across time (Level 2)
- Cross-time topic groupings (Level 2.5)
- Story evolution, causal chains, and recurring patterns (Level 3)

**Core Philosophy:**
- Bottom-up processing (day-by-day, then across days)
- Controlled purity (micro-clusters first, then careful merging)
- Fixed medoids (birth medoids prevent drift)
- Similarity-sorted processing (high-confidence decisions first)
- Rejection sets (avoid transitivity errors)

---

### **LEVEL 0 + 1: SAME-DAY CLUSTERING**

**Input:** Raw articles for one day

**Process:**

1. **Deduplication**
   - Calculate content + title embeddings
   - Compare all pairs via cosine similarity
   - Threshold: >0.95 similarity = duplicate
   - Duplicates are marked but kept for tracking

2. **Micro-Cluster Formation (Phase 1: Auto-Merge)**
   - Build similarity matrix (content embeddings)
   - Generate candidate pairs (similarity ≥ 0.69)
   - Sort by similarity (descending)
   - Split into two queues:
     - **Auto-merge queue:** Content similarity ≥0.95 OR (Title similarity ≥0.95 AND Content ≥0.9)
     - **LLM candidate queue:** Everything else above threshold
   - Process auto-merge queue:
     - Union-Find structure merges articles
     - **Capture birth medoid** when two singletons merge (medoid = centroid of the pair)
   - Result: Initial seed clusters with high confidence

3. **Micro-Cluster Growth (Phase 2: LLM Growth)**
   - Process LLM candidate queue (similarity-sorted)
   - Rules:
     - Skip if both articles already in same cluster
     - Skip if both articles in multi-article clusters (only grow clusters, don't merge large ones)
     - Skip if medoid pair in rejection set
   - For valid pairs:
     - Compare cluster medoids using Prompt 1 (same-day sameness)
     - If `same`: Merge clusters
     - If `separate_event`: Add medoid pair to rejection set
   - Result: Pure micro-clusters

4. **Iterative Merging (Multiple Iterations)**
   - Take micro-clusters as input
   - Calculate medoid-to-medoid similarities
   - Sort candidate pairs by similarity (descending)
   - Split into auto-merge and LLM queues (same thresholds)
   - Phase 1: Auto-merge high-confidence pairs
   - Phase 2: LLM-guided merging
   - **Critical:** Use BIRTH MEDOIDS throughout (prevent drift)
   - Repeat until convergence (no more merges possible)
   - Result: Final same-day clusters

**Output:**
- `merged_cluster_label` for each article
- `birth_medoids` dictionary: {cluster_label → medoid_article_index}
- Relationship flags: `compatible_related`, `causal_related`, `temporal_related` (from comparisons)

**File Saved:** `day_cluster_YYYY-MM-DD.csv`

---

### **LEVEL 1.5: SAME-DAY TOPIC GROUPING**

**Input:** Level 1 output (same-day clusters with flags)

**Process:**
- Extract all `compatible_related` flags from Level 1 comparisons
- Build graph: nodes = clusters, edges = compatible relationships
- Find connected components
- Each component = one topic group

**Output:**
- Topic groups for the day
- Mapping: {topic_id → [cluster_1, cluster_2, ...]}

**Purpose:** Optional view for users who want thematic organization of daily news

---

### **LEVEL 2: CROSS-DAY SAME-NEWS BRIDGING**

**Input:** All day-level clusters from Level 1 (multiple days)

**Process:**

1. **Sequential Processing**
   - Start with Day 1 clusters
   - For each cluster in Day 1:
     - Look forward to next 3 publication dates (days with articles, not calendar days)
     - Compare with clusters from Days 2, 3, 4
   - Move to Day 2, look forward to Days 3, 4, 5
   - Continue until end of dataset

2. **Comparison Strategy**
   - Use Prompt 2 (cross-day sameness)
   - **Critical:** Compare birth medoids, not random articles
   - Similarity pre-filter: Only compare if medoid similarity ≥ threshold
   - Sort candidate pairs by similarity (descending)

3. **Merging Logic**
   - If classification = `same`: Merge clusters into news burst
   - Track: start_date, end_date, article_count, medoid
   - News burst inherits earliest birth medoid

4. **Bridging Window**
   - Look forward 3 publication dates (configurable)
   - Reason: Captures delayed coverage, weekend gaps, reposts
   - Balance: Wide enough to catch same news, narrow enough to be efficient

**Output:**
- News bursts: {burst_id, start_date, end_date, article_count, articles, medoid}
- Each burst represents sustained coverage of one news event

**File Saved:** `news_bursts.csv`

---

### **LEVEL 2.5: CROSS-TIME TOPIC GROUPING**

**Input:** All news bursts from Level 2

**Process:**
- Extract ALL `compatible_related` flags across entire dataset
  - From Level 1 (same-day comparisons)
  - From Level 2 (cross-day comparisons)
- Build graph: nodes = news bursts, edges = compatible relationships
- Find connected components
- Each component = one topic group spanning time

**Output:**
- Topic groups: {topic_id → [burst_1, burst_2, ...]}
- Temporal span for each topic
- Can be filtered by time window (week/month) as needed

**Purpose:** Shows thematic relationships across time without direct temporal/causal links

---

### **LEVEL 3: TEMPORAL/CAUSAL/RECURRING LINKING**

**Input:** News bursts from Level 2

**Process:**

#### **3A: Temporal Linking (Story Progression)**

1. **Identify Candidates**
   - Pairs of bursts where later burst follows earlier
   - Time gap filter: Reasonable story evolution timeframe (configurable)
   - Thematic connection: Some content/keyword overlap

2. **Classification**
   - Use Prompt 3 (temporal linking)
   - Compare burst medoids
   - Classification: `temporal_related` = story progression

3. **Build Timeline**
   - Graph: nodes = bursts, edges = temporal links
   - Find paths (can be linear or branching)
   - Result: Story timelines showing evolution

**Example:** Policy Announced → Implementation Begins → Results Published

#### **3B: Causal Linking (Trigger Networks)**

1. **Identify Candidates**
   - Same as temporal, but look for reactive events
   - Flags from Level 1 (same-day causal) included

2. **Classification**
   - Use Prompt 3
   - Classification: `causal_related` = cause-effect

3. **Build Network**
   - Graph: nodes = bursts, edges = causal links
   - Can have forks (one event triggers multiple reactions)
   - Result: Causal networks

**Example:** Company Losses → CEO Resignation
**Example:** Policy Announcement → Protests + Opposition Response + Market Reaction (fork)

#### **3C: Recurring Patterns (Periodic Series)**

1. **Identify Candidates**
   - Bursts about similar topics at regular intervals
   - Look for: company name + announcement type patterns
   - Compare across entire dataset

2. **Classification**
   - Use Prompt 3
   - Classification: `recurring` = periodic pattern

3. **Build Series**
   - Graph: nodes = bursts, edges = recurring relationships
   - Find connected components
   - Each component = one recurring series
   - Sort by date within series

**Example:** March Prices → April Prices → May Prices
**Example:** Q1 Earnings → Q2 Earnings → Q3 Earnings

**Output:**
- Story timelines (temporal chains)
- Causal networks (cause-effect graphs)
- Recurring series (periodic sequences)

---

## PART 2: DATA STRUCTURES

---

### **Level 0+1 Output: Daily Clusters**

```
day_cluster_YYYY-MM-DD.csv:
├─ article_id (original index)
├─ title
├─ text
├─ full_article (title + text)
├─ url
├─ timestamp
├─ publish_date_only
├─ text_embeddings
├─ title_embeddings
├─ cluster_label (micro-cluster)
└─ merged_cluster_label (final cluster, -1 = outlier)

birth_medoids dictionary:
{
    0: 42,    # cluster 0's medoid is article 42
    1: 15,    # cluster 1's medoid is article 15
    2: 67,    # cluster 2's medoid is article 67
    ...
}

relationship_flags (stored during comparisons):
{
    (medoid_42, medoid_15): "compatible_related",
    (medoid_42, medoid_67): "causal_related",
    ...
}
```

---

### **Level 1.5 Output: Daily Topics**

```
daily_topics_YYYY-MM-DD:
{
    "Energy": [0, 2, 5],        # Topic contains clusters 0, 2, 5
    "Politics": [1, 3],          # Topic contains clusters 1, 3
    "Culture": [4],              # Topic contains cluster 4
    ...
}
```

---

### **Level 2 Output: News Bursts**

```
news_bursts.csv:
├─ burst_id
├─ start_date
├─ end_date
├─ duration_days
├─ article_count
├─ cluster_ids (list of original cluster IDs that merged)
├─ article_ids (list of all articles in burst)
├─ medoid_article_id
├─ title (from medoid)
├─ summary (from medoid or generated)
└─ dominant_keywords

Example row:
burst_id: 12
start_date: 2025-03-15
end_date: 2025-03-18
duration_days: 3
article_count: 47
cluster_ids: [Day1_Cluster_3, Day2_Cluster_5, Day3_Cluster_2, Day4_Cluster_1]
medoid_article_id: 156
title: "Helleniq Energy Reports Record Q4 Results"
```

---

### **Level 2.5 Output: Cross-Time Topics**

```
cross_time_topics:
{
    "Energy_Sector": {
        "burst_ids": [12, 27, 45, 63],
        "date_range": ("2025-03-01", "2025-03-31"),
        "total_articles": 234
    },
    "Political_Crisis": {
        "burst_ids": [8, 15, 29],
        "date_range": ("2025-03-05", "2025-03-20"),
        "total_articles": 156
    },
    ...
}
```

---

### **Level 3 Output: Relationships**

```
temporal_links:
[
    {
        "from_burst": 12,
        "to_burst": 27,
        "relationship": "temporal_related",
        "type": "story_progression"
    },
    ...
]

causal_links:
[
    {
        "from_burst": 8,
        "to_burst": 15,
        "relationship": "causal_related",
        "type": "reaction"
    },
    {
        "from_burst": 8,
        "to_burst": 29,
        "relationship": "causal_related",
        "type": "reaction"
    },
    ...
]

recurring_series:
[
    {
        "series_id": 1,
        "pattern_type": "monthly_prices",
        "bursts": [12, 45, 78, 102],  # Ordered by date
        "dates": ["2025-03-01", "2025-04-01", "2025-05-01", "2025-06-01"]
    },
    ...
]
```

---

## PART 3: UI VISUALIZATIONS

---

### **VIEW 1: DAILY BRIEFING (Flat)**

**Purpose:** "What were the top stories today?"

**Layout:**

```
┌─────────────────────────────────────────────────┐
│ Daily Briefing - March 15, 2025                 │
│ [Flat View] [Topic View]                  [←][→]│
├─────────────────────────────────────────────────┤
│                                                  │
│ Top Stories (7 distinct news)                   │
│                                                  │
│ 1. 📊 Helleniq Energy Q4 Results                │
│    5 articles • Most coverage today             │
│    [View Articles]                              │
│                                                  │
│ 2. 🎭 Festival "Roots of Gazi" Announced        │
│    3 articles                                   │
│    [View Articles]                              │
│                                                  │
│ 3. ⚡ Market Electricity Price Roundup          │
│    4 articles                                   │
│    [View Articles]                              │
│                                                  │
│ 4. 💰 DEI March Tariff Announcement             │
│    3 articles                                   │
│    [View Articles]                              │
│                                                  │
│ 5. 🏛️ Government Policy Update                  │
│    2 articles                                   │
│    [View Articles]                              │
│                                                  │
│ 6. 🏭 Factory Workers Strike                    │
│    2 articles • Causal: Related to #5          │
│    [View Articles]                              │
│                                                  │
│ 7. 🎪 Festival Family Activities                │
│    3 articles • Related to #2                  │
│    [View Articles]                              │
│                                                  │
│ 2 outliers (unrelated articles)                │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Interactions:**
- Click [View Articles] → Expands to show article list
- Hover over news item → Shows summary (medoid text preview)
- Click news title → Opens article detail modal
- Badges show relationships (🔗 Related, ⚡ Caused by, 📈 Part of trend)

---

### **VIEW 2: DAILY TOPICS (Grouped)**

**Purpose:** "What topics were covered today?"

**Layout:**

```
┌─────────────────────────────────────────────────┐
│ Daily Briefing - March 15, 2025                 │
│ [Flat View] [Topic View]                  [←][→]│
├─────────────────────────────────────────────────┤
│                                                  │
│ Topics Covered (3 topics, 12 articles total)    │
│                                                  │
│ [+] Energy Sector (3 news, 12 articles) 📈      │
│     │                                            │
│     ├─ Helleniq Energy Results (5 articles)     │
│     ├─ Market Price Roundup (4 articles)        │
│     └─ DEI Tariff Announcement (3 articles)     │
│                                                  │
│ [+] Cultural Events (2 news, 6 articles) 🎭     │
│     │                                            │
│     ├─ Festival Main Announcement (3 articles)  │
│     └─ Festival Family Activities (3 articles)  │
│                                                  │
│ [-] Government & Labor (2 news, 4 articles) 🏛️  │
│     │                                            │
│     ├─ Policy Update (2 articles)               │
│     └─ Strike Response (2 articles) ⚡          │
│         Causal link: Strike triggered by Policy │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Interactions:**
- Click [+] → Expands topic to show news items
- Click [-] → Collapses topic
- Click news item → Shows articles
- Badges show relationships within and across topics

---

### **VIEW 3: DOMINANT NEWS (Time Span)**

**Purpose:** "What stories got the most sustained coverage?"

**Layout:**

```
┌─────────────────────────────────────────────────┐
│ Dominant News                                    │
│ Date Range: [Mar 1, 2025] to [Mar 31, 2025] 🔍 │
│ Sort by: [Article Count ▼] [Duration] [Recent] │
├─────────────────────────────────────────────────┤
│                                                  │
│ Top 10 Stories by Coverage                      │
│                                                  │
│ 1. Helleniq Energy Q4 Results                   │
│    📊 47 articles | Mar 15-18 (3 days)          │
│    ████████████████░░░░ 80% coverage            │
│    [View Timeline] [View Articles]              │
│                                                  │
│ 2. Government Tax Policy Reform                 │
│    🏛️ 38 articles | Mar 5-12 (7 days)           │
│    ██████████████░░░░░░ 65% coverage            │
│    [View Timeline] [View Articles]              │
│    └─ 🔗 Linked: Tax Policy → Protests (Mar 8) │
│                                                  │
│ 3. Festival "Roots of Gazi"                     │
│    🎭 23 articles | Mar 15-16 (2 days)          │
│    ████████░░░░░░░░░░░░ 40% coverage            │
│    [View Timeline] [View Articles]              │
│                                                  │
│ 4. DEI Electricity Prices                       │
│    ⚡ 18 articles | Mar 10-12 (3 days)          │
│    ██████░░░░░░░░░░░░░░ 30% coverage            │
│    [View Timeline] [View Articles]              │
│    └─ 📈 Part of: Monthly Price Pattern         │
│                                                  │
│ [Show More]                                      │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Interactions:**
- Filter by date range
- Sort by article count, duration, or recency
- Click [View Timeline] → Shows daily article count graph
- Badges show relationships (linked stories, recurring patterns)

---

### **VIEW 4: TOPIC EXPLORER (Cross-Time)**

**Purpose:** "Explore a topic across time"

**Layout:**

```
┌─────────────────────────────────────────────────┐
│ Topic Explorer                                   │
│ Search: [energy sector____________] 🔍          │
│ Filters: [Company ▼] [Date Range] [Article Count]│
├─────────────────────────────────────────────────┤
│                                                  │
│ Energy Sector                                    │
│ 234 articles across 12 news bursts              │
│ Date range: Mar 1 - Mar 31, 2025                │
│                                                  │
│ Timeline View: [●──●─●────●──●────●──●─●] Mar  │
│                                                  │
│ News in this Topic:                              │
│                                                  │
│ • Helleniq Q4 Results (47 articles, Mar 15-18)  │
│   [View] [Related Topics: Finance, Oil]         │
│                                                  │
│ • Market Price Roundup (32 articles, Mar 10-15) │
│   [View] [Related Topics: Utilities]            │
│                                                  │
│ • DEI Tariff Changes (18 articles, Mar 10-12)   │
│   [View] [Part of: Monthly Price Pattern]       │
│                                                  │
│ • Renewable Energy Investments (15 articles, Mar 20-22) │
│   [View] [Linked to: Helleniq Results]          │
│                                                  │
│ [Load More]                                      │
│                                                  │
│ Related Topics:                                  │
│ [Finance (156)] [Utilities (89)] [Oil (67)]     │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Interactions:**
- Search topics by keyword
- Filter by company, date range, article count
- Timeline shows burst distribution
- Click news burst → View articles
- Related topics navigate to other explorations

---

### **VIEW 5: STORY TIMELINE (Evolution)**

**Purpose:** "How did this story evolve?"

**Layout:**

```
┌─────────────────────────────────────────────────┐
│ Story Timeline: Tax Policy Reform               │
│ [Linear View] [Network View]              [🔙] │
├─────────────────────────────────────────────────┤
│                                                  │
│         Policy            Implementation         │
│       Announced             Begins               │
│          │                    │                  │
│    Mar 5 ●─────────────────→ ●─────────────→    │
│         38 articles        15 articles           │
│                                                  │
│                            Results               │
│                          Published               │
│                              │                   │
│                          ─→ ● Mar 28             │
│                            8 articles            │
│                                                  │
│ [Timeline Controls: Play ▶ | Speed: 1x]         │
│                                                  │
│ Details:                                         │
│ ┌─────────────────────────────────────────────┐ │
│ │ Phase 1: Policy Announced (Mar 5-7)         │ │
│ │ 38 articles from 12 sources                 │ │
│ │                                             │ │
│ │ Key Points:                                 │ │
│ │ • 20% VAT reduction on essential goods     │ │
│ │ • €500M estimated impact                   │ │
│ │ • Implementation date: March 15            │ │
│ │                                             │ │
│ │ [View All Articles]                         │ │
│ └─────────────────────────────────────────────┘ │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Interactions:**
- Toggle between linear and network views
- Click node → Show burst details
- Play animation → Watch story unfold over time
- Hover edge → Show relationship type (temporal)

---

### **VIEW 6: CAUSAL NETWORK (Forks)**

**Purpose:** "What triggered what?"

**Layout:**

```
┌─────────────────────────────────────────────────┐
│ Causal Network: Tax Policy Announcement         │
│ [Linear View] [Network View]              [🔙] │
├─────────────────────────────────────────────────┤
│                                                  │
│              Policy                              │
│            Announced                             │
│            Mar 5 ●                               │
│                  │                               │
│         ┌────────┼────────┐                     │
│         │        │        │                      │
│         ▼        ▼        ▼                      │
│    Opposition  Protests  Market                 │
│    Response    Erupt    Reaction                │
│    Mar 6 ●    Mar 8 ●   Mar 6 ●                 │
│    12 art.    25 art.   8 art.                  │
│                  │                               │
│                  ▼                               │
│             Government                           │
│             Response                             │
│             Mar 10 ●                             │
│             15 art.                              │
│                                                  │
│ Legend: ● = News Burst | → = Causal Link       │
│                                                  │
│ Select a node to see details...                 │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Interactions:**
- Click node → Show burst details + articles
- Hover edge → Show causal relationship description
- Filter by: reaction type, time range, article count
- Export as image

---

### **VIEW 7: RECURRING PATTERNS (Series)**

**Purpose:** "Track periodic announcements"

**Layout:**

```
┌─────────────────────────────────────────────────┐
│ Recurring Patterns                               │
│ Type: [Monthly Prices ▼] [Quarterly Earnings]   │
│ Company: [All ▼] [DEI] [Helleniq]              │
├─────────────────────────────────────────────────┤
│                                                  │
│ Electricity Price Announcements (Monthly)        │
│ 6 instances • Pattern: 1st of each month        │
│                                                  │
│ Jan ●────→ Feb ●────→ Mar ●────→ Apr ●────→     │
│    15 art.    18 art.    18 art.    12 art.     │
│                                                  │
│ Trend: ↗ Prices increasing (+5% avg)            │
│                                                  │
│ ┌─────────────────────────────────────────────┐ │
│ │ March Prices (Mar 1-3)                      │ │
│ │ 18 articles from 8 sources                  │ │
│ │                                             │ │
│ │ Key Changes:                                │ │
│ │ • DEI: €0.154/kWh (+3% from Feb)           │ │
│ │ • Protergia: €0.148/kWh (+2%)              │ │
│ │ • Heron: €0.151/kWh (+4%)                  │ │
│ │                                             │ │
│ │ [View Articles] [Compare to February]       │ │
│ └─────────────────────────────────────────────┘ │
│                                                  │
│ Other Recurring Patterns:                        │
│ • Helleniq Quarterly Earnings (4 instances)     │
│ • Weekly Power Outage Schedules (12 instances)  │
│ • Daily Stock Market Reports (30 instances)     │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Interactions:**
- Filter by pattern type (monthly/quarterly/weekly/daily)
- Filter by company
- Click node → View that instance's articles
- [Compare to Previous] → Side-by-side comparison
- Trend analysis shows patterns over time

---

## PART 4: USER FLOWS

---

### **Flow 1: Daily News Monitoring**

**Persona:** Journalist checking daily coverage

**Steps:**
1. Land on View 1 (Daily Briefing - Flat)
2. See top 7 stories ranked by coverage
3. Click "Helleniq Energy Results" → Expand to see 5 articles
4. Hover over article → See preview
5. Click article → Open full text
6. Notice badge "Related to Festival" → Click
7. Navigate to Festival story
8. Toggle to View 2 (Topic View) → See Energy Sector grouping
9. Export daily report

**Goal Achieved:** Quick daily overview with ability to drill down

---

### **Flow 2: Trend Analysis**

**Persona:** Analyst tracking energy sector trends

**Steps:**
1. Navigate to View 3 (Dominant News)
2. Filter date range: Last 3 months
3. Sort by article count
4. See "Helleniq Q4 Results" as #1 (47 articles)
5. Click [View Timeline] → See coverage over 3 days
6. Notice badge "Part of: Quarterly Earnings Pattern"
7. Click → Navigate to View 7 (Recurring Patterns)
8. See Helleniq earnings: Q1, Q2, Q3, Q4
9. Click [Compare] → Side-by-side quarterly comparison
10. Export trend report

**Goal Achieved:** Identified and analyzed recurring pattern

---

### **Flow 3: Story Evolution Tracking**

**Persona:** Editor tracking policy story development

**Steps:**
1. Search "Tax Policy" in View 4 (Topic Explorer)
2. See 12 related news bursts
3. Notice timeline shows multiple phases
4. Click "Policy Announced" burst
5. See badge "Evolved into Implementation"
6. Click [View Timeline] → Navigate to View 5
7. See linear progression: Announcement → Implementation → Results
8. Click first node → See 38 articles
9. Play animation → Watch story unfold
10. Notice fork to View 6 (Causal Network)
11. Click → See protests triggered by policy
12. Export story evolution report

**Goal Achieved:** Tracked complete story arc with causal branches

---

### **Flow 4: Company Monitoring**

**Persona:** Investor tracking Helleniq Energy

**Steps:**
1. Navigate to View 4 (Topic Explorer)
2. Filter: Company = "Helleniq"
3. See all Helleniq news bursts (time-ordered)
4. See major stories:
   - Q4 Results (47 articles, Mar 15-18)
   - Drilling Decision (12 articles, Mar 16-17)
   - Renewable Investment (8 articles, Mar 20-21)
5. Notice "Q4 Results" and "Drilling Decision" overlap dates
6. Click both → See they're same news (different hooks)
7. Click "Renewable Investment" → See it's separate
8. Click related topic "Energy Sector"
9. See competitive context (DEI, other companies)
10. Export company report

**Goal Achieved:** Comprehensive company monitoring with context

---

### **Flow 5: Pattern Discovery**

**Persona:** Data scientist looking for patterns

**Steps:**
1. Navigate to View 7 (Recurring Patterns)
2. See suggested patterns: Monthly prices, Quarterly earnings
3. Filter: Type = Monthly, Company = All
4. See electricity price pattern (6 instances)
5. Notice trend: Prices increasing
6. Click [Compare] → See Jan vs Feb vs Mar prices
7. Export data
8. Switch to Topic Explorer
9. See all price-related bursts
10. Identify outliers (non-recurring price announcements)
11. Export analysis

**Goal Achieved:** Discovered and analyzed recurring patterns

---

## END OF DOCUMENTATION

---

**This complete system documentation covers:**
✅ Full algorithmic flow (5 levels)
✅ Data structures at each level
✅ 7 UI views with detailed mockups
✅ 5 user flows for key personas

**Ready for implementation!** 🚀