# Repo Nexus - Updated Technical Specification

## Complete Technical Specification & Implementation Plan

**Version:** 3.0.0
**Platform:** iOS (React Native + Expo)
**Backend:** Python (FastAPI + PostgreSQL + Redis)
**Target:** iOS 17.0+
**Last Updated:** November 8, 2025

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Core Concept & User Flow](#core-concept--user-flow)
3. [Technology Stack](#technology-stack)
4. [Architecture Overview](#architecture-overview)
5. [Data Models](#data-models)
6. [API Specifications](#api-specifications)
7. [Screen-by-Screen Implementation](#screen-by-screen-implementation)
8. [Trending Algorithm Design](#trending-algorithm-design)
9. [Topic Suggestion Engine](#topic-suggestion-engine)
10. [Implementation Tasks](#implementation-tasks)

---

## 1. Executive Summary

### 1.1 Application Overview

**Repo Nexus** is a topic-first GitHub exploration platform that helps developers discover repositories through intelligent topic curation. The app analyzes users' starred repositories to suggest relevant topics they're not following, then surfaces trending and quality repositories within those topics.

### 1.2 Core Philosophy

**Topics First, Not Trending**: Unlike traditional GitHub explorers that focus on global trending repositories, Repo Nexus centers the experience around topics. Users follow topics that interest them, and the app intelligently surfaces the best repositories within those topics using custom trending algorithms.

### 1.3 Key Features

- 🏷️ **Topic-Centric Navigation** - App opens directly to your followed topics
- 🤖 **Intelligent Topic Suggestions** - Analyzes starred repos to suggest topics you're not following
- 🔍 **Topic Deep Dive** - Sort and filter repositories within topics
- 📈 **Topic-Specific Trending** - Custom algorithms for trending repos within each topic
- 🌟 **Explore Feed** - Discover trending repos from your followed topics
- 🔎 **Topic Search** - Search repositories within specific topics
- 📊 **Repository View** - GitHub-like repository detail pages

### 1.4 Key Metrics & Goals

MetricTargetApp Launch Time&lt; 2 secondsAPI Response Time&lt; 500ms (p95)Topic Suggestion Accuracy&gt; 80%User Topic Follow Rate&gt; 60%Test Coverage&gt; 85%Crash-Free Rate&gt; 99.5%

---

## 2. Core Concept & User Flow

### 2.1 Primary User Journey

```
┌─────────────────────────────────────────────────────────────┐
│                    USER ONBOARDING FLOW                      │
└─────────────────────────────────────────────────────────────┘

1. Sign in with GitHub OAuth
   ↓
2. App syncs starred repositories
   ↓
3. Backend analyzes starred repos for topics
   ↓
4. App suggests topics based on:
   - Topics in starred repos
   - Topics NOT currently followed
   - Topics with active repositories
   ↓
5. User selects topics to follow
   ↓
6. App opens to Topics screen (home screen)
```

### 2.2 Core Screens & Navigation

```
┌──────────────────────────────────────────────────────────────┐
│                     APP STRUCTURE                             │
└──────────────────────────────────────────────────────────────┘

(tabs)/
├── topics.tsx          ← PRIMARY (Home) - Opens here
│   └── Followed topics list
│   └── Topic management
│
├── explore.tsx         ← Trending from followed topics
│   └── Smart feed of repos from topics you follow
│   └── Trending algorithm-driven
│
├── search.tsx          ← Search within topics
│   └── Filter by topic
│   └── Search repos within topic
│
└── profile.tsx         ← User profile & settings
    └── Sync starred repos
    └── Topic suggestions
    └── Settings

repository/[id].tsx     ← Repository detail (GitHub-like)
topic/[name].tsx        ← Topic detail with repo list
```

### 2.3 Detailed User Flows

Flow 1: First Time User

```
1. Login with GitHub
2. Loading screen: "Analyzing your starred repositories..."
3. Backend processes:
   - Fetch all starred repos
   - Extract topics from each repo
   - Count topic frequency
   - Find topics user hasn't explicitly followed
   - Rank suggestions by relevance
4. Show "Suggested Topics" modal
   - "Based on your stars, you might like:"
   - Show top 10-15 suggested topics
   - User can toggle follow/ignore
5. Navigate to Topics screen (home)
```

Flow 2: Topics Screen (Home)

```
┌────────────────────────────────────────────────┐
│ Topics (Home)                          [+] [⚙] │
├────────────────────────────────────────────────┤
│                                                 │
│  📱 Your Followed Topics (12)                  │
│                                                 │
│  ┌──────────────────────────────────────────┐ │
│  │ 🎨 React                        Following │ │
│  │ 1,234 repositories                        │ │
│  │ Updated 2m ago                            │ │
│  └──────────────────────────────────────────┘ │
│                                                 │
│  ┌──────────────────────────────────────────┐ │
│  │ 🔧 TypeScript                   Following │ │
│  │ 892 repositories                          │ │
│  │ Updated 5m ago                            │ │
│  └──────────────────────────────────────────┘ │
│                                                 │
│  ┌──────────────────────────────────────────┐ │
│  │ 🤖 AI/ML                        Following │ │
│  │ 2,451 repositories                        │ │
│  │ Updated 10m ago                           │ │
│  └──────────────────────────────────────────┘ │
│                                                 │
│  [Pull to refresh]                             │
│                                                 │
└────────────────────────────────────────────────┘

Actions:
- Tap topic → Navigate to Topic Detail
- [+] → Browse/search all topics
- [⚙] → Manage topics (reorder, unfollow)
- Long press → Quick actions menu
```

Flow 3: Topic Detail Screen

```
┌────────────────────────────────────────────────┐
│ ← React                          [Following] ⭐│
├────────────────────────────────────────────────┤
│ A JavaScript library for building UIs          │
│ 1,234 repositories                             │
│                                                 │
│ Sort: [Most Stars ▼]  Filter: [All ▼]        │
├────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────────────────────────────┐ │
│  │ facebook/react                      ⭐ 228k│ │
│  │ The React library                         │ │
│  │ JavaScript • Updated 2 hours ago          │ │
│  │ #react #ui #javascript                    │ │
│  └──────────────────────────────────────────┘ │
│                                                 │
│  ┌──────────────────────────────────────────┐ │
│  │ vercel/next.js                      ⭐ 125k│ │
│  │ The React Framework                       │ │
│  │ JavaScript • Updated 4 hours ago          │ │
│  │ #react #nextjs #ssr                       │ │
│  └──────────────────────────────────────────┘ │
│                                                 │
└────────────────────────────────────────────────┘

Sort Options:
- Most Stars (default)
- Recently Updated
- Recently Created
- Most Forks
- Trending (custom algorithm)

Filter Options:
- All Languages
- By Language (JavaScript, TypeScript, etc.)
- Minimum Stars (1k+, 10k+, 50k+)
```

Flow 4: Explore Screen

```
┌────────────────────────────────────────────────┐
│ Explore                         Filter: [All ▼]│
├────────────────────────────────────────────────┤
│                                                 │
│  🔥 Trending from your topics                  │
│                                                 │
│  ┌──────────────────────────────────────────┐ │
│  │ tinygrad/tinygrad              ⭐ 24k (+200)│
│  │ You are like pytorch but smaller          │ │
│  │ From: AI/ML, Python                       │ │
│  │ Trending Score: 95/100                    │ │
│  └──────────────────────────────────────────┘ │
│                                                 │
│  ┌──────────────────────────────────────────┐ │
│  │ BuilderIO/mitosis              ⭐ 12k (+150)│
│  │ Write components once, run everywhere     │ │
│  │ From: React, WebDev                       │ │
│  │ Trending Score: 92/100                    │ │
│  └──────────────────────────────────────────┘ │
│                                                 │
│  ┌──────────────────────────────────────────┐ │
│  │ langchain-ai/langchain         ⭐ 89k (+120)│
│  │ Build LLM applications                    │ │
│  │ From: AI/ML, Python                       │ │
│  │ Trending Score: 88/100                    │ │
│  └──────────────────────────────────────────┘ │
│                                                 │
└────────────────────────────────────────────────┘

Filter Options:
- All Topics (default)
- By Specific Topic
- Time Range (Today, This Week, This Month)

Algorithm Factors:
- Star growth rate
- Recent commits
- Issue activity
- PR activity
- Community engagement
- Topic relevance score
```

Flow 5: Topic Suggestion Flow

```
Trigger: User syncs GitHub profile
         or manually requests suggestions

1. Backend Analysis:
   ┌──────────────────────────────────────────┐
   │ Analyze Starred Repositories             │
   │                                          │
   │ User has starred 250 repositories        │
   │ Extract topics from each                 │
   │                                          │
   │ Topic Frequency:                         │
   │ • typescript: 45 repos                   │
   │ • react: 38 repos                        │
   │ • ai: 32 repos                           │
   │ • python: 28 repos                       │
   │ • nextjs: 24 repos                       │
   │ • vue: 18 repos                          │
   │ ...                                      │
   │                                          │
   │ Currently Following: react, typescript   │
   │                                          │
   │ Suggestions (not following):             │
   │ • ai (32 repos) ← High recommendation   │
   │ • python (28 repos)                      │
   │ • nextjs (24 repos)                      │
   │ • vue (18 repos)                         │
   └──────────────────────────────────────────┘

2. Show Suggestions Modal:
   ┌──────────────────────────────────────────┐
   │ 🎯 Discover Topics You'll Love           │
   │                                          │
   │ Based on your 250 starred repos:         │
   │                                          │
   │  ┌────────────────────────────────────┐ │
   │  │ 🤖 AI/ML                    [Follow]│ │
   │  │ You've starred 32 AI repos          │ │
   │  │ 15,234 total repositories           │ │
   │  └────────────────────────────────────┘ │
   │                                          │
   │  ┌────────────────────────────────────┐ │
   │  │ 🐍 Python                   [Follow]│ │
   │  │ You've starred 28 Python repos      │ │
   │  │ 22,145 total repositories           │ │
   │  └────────────────────────────────────┘ │
   │                                          │
   │  ┌────────────────────────────────────┐ │
   │  │ ⚡ Next.js                  [Follow]│ │
   │  │ You've starred 24 Next.js repos     │ │
   │  │ 3,421 total repositories            │ │
   │  └────────────────────────────────────┘ │
   │                                          │
   │         [Skip]    [Follow Selected]     │
   └──────────────────────────────────────────┘
```

### 2.4 Key Differentiators

1. **No Global Trending**: We don't show GitHub's general trending. Instead, we show what's trending within topics YOU care about.
2. **Topic Suggestions, Not Recommendations**: We suggest topics based on YOUR starred repos, not generic popularity.
3. **Smart Discovery**: "You've starred 32 AI repos but aren't following the AI/ML topic. Here are hidden gems you might have missed."
4. **Contextual Trending**: Trending is calculated per-topic with custom algorithms, not just "most stars today."

---

## 3. Technology Stack

### 3.1 Frontend Stack

```json
{
  "react-native": "^0.75.0",
  "expo": "~52.0.0",
  "expo-router": "~4.0.0",
  "react": "18.3.1",
  "nativewind": "^5.0.0",
  "react-native-reanimated": "~4.0.0",
  "react-native-gesture-handler": "~2.20.0",
  "@tanstack/react-query": "^5.59.0",
  "zustand": "^5.0.0",
  "react-native-mmkv": "^3.0.0",
  "@shopify/flash-list": "1.7.1"
}
```

### 3.2 Backend Stack

```python
# requirements.txt
fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlalchemy==2.0.35
asyncpg==0.30.0
redis==5.2.0
celery==5.4.0
alembic==1.13.0
pydantic==2.9.0
python-jose[cryptography]==3.3.0
```

---

## 4. Architecture Overview

### 4.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    iOS APPLICATION                           │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         React Native + Expo (Hermes)                   │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │ │
│  │  │  Topics  │ │ Explore  │ │  Search  │ │ Profile  │ │ │
│  │  │  (Home)  │ │  Feed    │ │  Topics  │ │  Sync    │ │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────┬───────────────────────────────────────┬──────────┘
           │         HTTPS / WebSocket              │
           ▼                                        ▼
┌─────────────────────────────────────────────────────────────┐
│                 FASTAPI BACKEND SERVICES                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Auth Service  │  Topic Service   │  Suggestion Engine │ │
│  │  Sync Service  │  Trending Service│  Search Service    │ │
│  └────────────────────────────────────────────────────────┘ │
│                            │                                 │
│  ┌───────────────────┬─────┴──────┬────────────────────┐   │
│  │                   │            │                     │   │
│  ▼                   ▼            ▼                     ▼   │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐      ┌──────────┐│
│ │PostgreSQL│  │  Redis   │  │  Celery  │      │GitHub API││
│ │ Topics   │  │  Cache   │  │  Workers │      │          ││
│ │ UserTopics│  │ Trending │  │  - Sync  │      │          ││
│ │ Repos    │  │  Scores  │  │  - Suggest│     │          ││
│ └──────────┘  └──────────┘  └──────────┘      └──────────┘│
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Frontend Architecture

```
app/
├── (tabs)/                    # Main navigation
│   ├── topics.tsx            ← HOME: Followed topics
│   ├── explore.tsx           ← Trending from followed topics
│   ├── search.tsx            ← Search within topics
│   ├── profile.tsx           ← Profile & sync
│   └── _layout.tsx
├── (auth)/
│   ├── login.tsx
│   └── callback.tsx
├── repository/
│   └── [id].tsx              # Repository detail (GitHub-like)
├── topic/
│   └── [name].tsx            # Topic detail with repos
└── _layout.tsx

components/
├── ui/                        # Base components
├── topics/                    # Topic-specific components
│   ├── TopicCard.tsx
│   ├── TopicSuggestion.tsx
│   ├── TopicRepoList.tsx
│   └── TopicHeader.tsx
├── explore/
│   ├── TrendingCard.tsx
│   └── TrendingFeed.tsx
└── repository/
    ├── RepositoryCard.tsx
    ├── RepositoryHeader.tsx
    └── RepositoryStats.tsx

services/
├── api/
│   ├── topics.ts             # Topic APIs
│   ├── suggestions.ts        # Suggestion APIs
│   ├── trending.ts           # Trending APIs
│   └── sync.ts               # Sync APIs
└── algorithms/
    └── trendingScore.ts      # Client-side trending calculations
```

---

## 5. Data Models

### 5.1 Core Data Models

```typescript
// types/models.ts

export interface Topic {
  id: string;
  name: string;
  displayName: string;
  description?: string;
  icon?: string;
  repositoryCount: number;
  isFollowing: boolean;
  followOrder?: number;          // For user's custom ordering
  lastSyncedAt?: string;
  createdAt: string;
  updatedAt: string;
}

export interface UserTopic {
  id: string;
  userId: string;
  topicId: string;
  isFollowing: boolean;
  followOrder: number;           // Custom sort order
  notificationsEnabled: boolean;
  followedAt: string;
  unfollowedAt?: string;
}

export interface Repository {
  id: string;
  githubId: string;
  nameWithOwner: string;
  name: string;
  ownerLogin: string;
  description?: string;
  stargazerCount: number;
  forkCount: number;
  openIssuesCount: number;
  primaryLanguage?: string;
  languages: Record<string, number>;
  topics: string[];              // Array of topic names
  htmlUrl: string;
  createdAt: string;
  updatedAt: string;
  pushedAt?: string;
  lastFetchedAt: string;
  // Trending metrics
  trendingScore?: number;        // 0-100 score
  starGrowthRate?: number;       // Stars gained per day
  activityScore?: number;        // Commits, PRs, issues
}

export interface TopicSuggestion {
  topic: Topic;
  reason: string;
  relevanceScore: number;        // 0-100
  starredRepoCount: number;      // How many repos user starred with this topic
  sampleRepositories: Repository[]; // Top 3-5 example repos
  isFollowing: boolean;
  isDismissed: boolean;
}

export interface TrendingRepository {
  repository: Repository;
  trendingScore: number;         // Calculated trending score
  topicsSources: string[];       // Which of user's topics this came from
  scoreBreakdown: {
    starGrowth: number;
    activityGrowth: number;
    communityEngagement: number;
    recency: number;
  };
  rank?: number;
}

export interface StarredRepository {
  id: string;
  userId: string;
  repositoryId: string;
  starredAt: string;
  repository?: Repository;
}

export interface SyncStatus {
  id: string;
  userId: string;
  lastSyncAt: string;
  syncType: 'full' | 'incremental';
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  repositoriesSynced: number;
  topicsSuggested: number;
  error?: string;
}
```

### 5.2 Backend Models (SQLAlchemy)

```python
# app/models/topic.py

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base
import uuid
from datetime import datetime

class Topic(Base):
    __tablename__ = "topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String, nullable=True)
    repository_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_synced_at = Column(DateTime, nullable=True)


# app/models/user_topic.py

class UserTopic(Base):
    __tablename__ = "user_topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False, index=True)
    
    is_following = Column(Boolean, default=True)
    follow_order = Column(Integer, default=0)  # For custom sorting
    notifications_enabled = Column(Boolean, default=True)
    
    followed_at = Column(DateTime, default=datetime.utcnow)
    unfollowed_at = Column(DateTime, nullable=True)
    
    # Unique constraint: one user-topic relationship
    __table_args__ = (
        UniqueConstraint('user_id', 'topic_id', name='unique_user_topic'),
    )


# app/models/topic_suggestion.py

class TopicSuggestion(Base):
    __tablename__ = "topic_suggestions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False)
    
    relevance_score = Column(Integer, default=0)  # 0-100
    starred_repo_count = Column(Integer, default=0)  # Repos user starred with this topic
    reason = Column(Text, nullable=True)
    
    is_dismissed = Column(Boolean, default=False)
    is_followed = Column(Boolean, default=False)
    
    suggested_at = Column(DateTime, default=datetime.utcnow)
    dismissed_at = Column(DateTime, nullable=True)
    followed_at = Column(DateTime, nullable=True)


# app/models/repository_topic.py

class RepositoryTopic(Base):
    """Many-to-many relationship between repositories and topics"""
    __tablename__ = "repository_topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False, index=True)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False, index=True)
    
    added_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('repository_id', 'topic_id', name='unique_repo_topic'),
    )


# app/models/trending_score.py

class TrendingScore(Base):
    """Cached trending scores for repositories within topics"""
    __tablename__ = "trending_scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False, index=True)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False, index=True)
    
    # Trending metrics
    trending_score = Column(Integer, default=0)  # 0-100
    star_growth_rate = Column(Float, default=0.0)
    activity_score = Column(Integer, default=0)
    community_score = Column(Integer, default=0)
    recency_score = Column(Integer, default=0)
    
    # Metadata
    calculated_at = Column(DateTime, default=datetime.utcnow)
    time_window = Column(String, default='daily')  # daily, weekly, monthly
    
    __table_args__ = (
        Index('idx_trending_topic_score', 'topic_id', 'trending_score', postgresql_using='btree'),
    )
```

### 5.3 Database Schema

```
┌─────────────────────┐
│      Users          │
├─────────────────────┤
│ PK id               │
│    github_id        │
│    login            │
│    starred_count    │
└──────────┬──────────┘
           │
           │ 1:N
           │
┌──────────▼──────────┐        ┌──────────────────┐
│   User Topics       │   N:1  │     Topics       │
├─────────────────────┤◄───────┤──────────────────┤
│ PK id               │        │ PK id            │
│ FK user_id          │        │    name (unique) │
│ FK topic_id         │        │    display_name  │
│    is_following     │        │    description   │
│    follow_order     │        │    repo_count    │
│    followed_at      │        │    icon          │
└─────────────────────┘        └────────┬─────────┘
                                        │
           │ 1:N                        │ N:M
           │                            │
┌──────────▼──────────┐        ┌───────▼──────────┐
│ Topic Suggestions   │        │ Repository Topics│
├─────────────────────┤        ├──────────────────┤
│ PK id               │        │ PK id            │
│ FK user_id          │        │ FK repository_id │
│ FK topic_id         │        │ FK topic_id      │
│    relevance_score  │        └────────┬─────────┘
│    starred_repo_cnt │                 │
│    is_dismissed     │                 │ N:1
│    suggested_at     │                 │
└─────────────────────┘        ┌────────▼─────────┐
                               │   Repositories   │
           │ 1:N                ├──────────────────┤
           │                    │ PK id            │
┌──────────▼──────────┐        │    github_id     │
│ Starred Repos       │◄───────┤    name_with_own │
├─────────────────────┤   N:1  │    description   │
│ PK id               │        │    stars_count   │
│ FK user_id          │        │    topics (JSON) │
│ FK repository_id    │        │    language      │
│    starred_at       │        │    updated_at    │
└─────────────────────┘        └────────┬─────────┘
                                        │
                                        │ 1:N
                                        │
                               ┌────────▼─────────┐
                               │ Trending Scores  │
                               ├──────────────────┤
                               │ PK id            │
                               │ FK repository_id │
                               │ FK topic_id      │
                               │    trending_score│
                               │    star_growth   │
                               │    activity_score│
                               │    calculated_at │
                               └──────────────────┘
```

---

## 6. API Specifications

### 6.1 Topic APIs

```typescript
// GET /api/v1/topics
// Get all topics with optional filtering
Query Params:
  - search: string (search by name/description)
  - page: number
  - per_page: number
  - sort: "name" | "repo_count" | "popular"

Response:
{
  "data": [Topic[]],
  "pagination": {
    "total": 1000,
    "page": 1,
    "per_page": 20,
    "pages": 50
  }
}

// GET /api/v1/topics/{name}
// Get single topic by name
Response: Topic

// GET /api/v1/topics/{name}/repositories
// Get repositories within a topic
Query Params:
  - sort: "stars" | "updated" | "created" | "forks" | "trending"
  - language: string (filter by language)
  - min_stars: number
  - page: number
  - per_page: number

Response:
{
  "topic": Topic,
  "repositories": [Repository[]],
  "pagination": {...}
}

// GET /api/v1/users/me/topics
// Get user's followed topics
Query Params:
  - include_counts: boolean (include repo counts)

Response:
{
  "topics": [Topic[]],  // Sorted by follow_order
  "total_following": 12
}

// POST /api/v1/topics/{id}/follow
Headers: Authorization: Bearer {token}
Body: {
  "notifications_enabled": boolean
}
Response: UserTopic

// DELETE /api/v1/topics/{id}/follow
Headers: Authorization: Bearer {token}
Response: 204 No Content

// PATCH /api/v1/users/me/topics/reorder
Headers: Authorization: Bearer {token}
Body: {
  "topic_orders": [
    {"topic_id": "uuid", "order": 0},
    {"topic_id": "uuid", "order": 1},
    ...
  ]
}
Response: {
  "updated": number
}
```

### 6.2 Topic Suggestion APIs

```typescript
// GET /api/v1/suggestions/topics
// Get topic suggestions for current user
Headers: Authorization: Bearer {token}
Query Params:
  - limit: number (default: 10)
  - min_relevance: number (0-100, default: 50)

Response:
{
  "suggestions": [TopicSuggestion[]],
  "total": 15,
  "analysis": {
    "starred_repos_analyzed": 250,
    "unique_topics_found": 45,
    "currently_following": 8
  }
}

// POST /api/v1/suggestions/topics/{id}/dismiss
// Dismiss a topic suggestion
Headers: Authorization: Bearer {token}
Response: 204 No Content

// POST /api/v1/suggestions/topics/generate
// Trigger topic suggestion generation (manual sync)
Headers: Authorization: Bearer {token}
Response:
{
  "status": "queued" | "in_progress" | "completed",
  "sync_id": "uuid",
  "estimated_time": "30s"
}

// GET /api/v1/suggestions/topics/status/{sync_id}
// Check suggestion generation status
Headers: Authorization: Bearer {token}
Response:
{
  "status": "in_progress",
  "progress": 75,
  "repositories_analyzed": 188,
  "total_repositories": 250,
  "suggestions_found": 12
}
```

### 6.3 Trending & Explore APIs

```typescript
// GET /api/v1/explore/trending
// Get trending repos from user's followed topics
Headers: Authorization: Bearer {token}
Query Params:
  - time_window: "daily" | "weekly" | "monthly" (default: daily)
  - topic_filter: string (optional, filter by specific topic)
  - min_score: number (0-100, default: 70)
  - limit: number (default: 20)

Response:
{
  "trending": [TrendingRepository[]],
  "time_window": "daily",
  "topics_included": ["react", "typescript", "ai"],
  "updated_at": "2025-11-08T12:00:00Z"
}

// GET /api/v1/topics/{name}/trending
// Get trending repos within a specific topic
Query Params:
  - time_window: "daily" | "weekly" | "monthly"
  - limit: number

Response:
{
  "topic": Topic,
  "trending": [TrendingRepository[]],
  "algorithm_version": "v1.0"
}

// POST /api/v1/trending/calculate
// Admin: Trigger trending score calculation
Headers: Authorization: Bearer {admin_token}
Body: {
  "topics": ["react", "python"],  // Optional
  "time_window": "daily"
}
Response:
{
  "status": "queued",
  "job_id": "uuid"
}
```

### 6.4 Sync APIs

```typescript
// POST /api/v1/sync/starred
// Sync user's starred repositories from GitHub
Headers: Authorization: Bearer {token}
Body: {
  "full_sync": boolean  // true = fetch all, false = incremental
}
Response:
{
  "sync_id": "uuid",
  "status": "queued",
  "estimated_repositories": 250
}

// GET /api/v1/sync/status/{sync_id}
// Get sync status
Headers: Authorization: Bearer {token}
Response:
{
  "sync_id": "uuid",
  "status": "in_progress" | "completed" | "failed",
  "progress": {
    "current": 150,
    "total": 250,
    "percentage": 60
  },
  "repositories_added": 15,
  "repositories_updated": 135,
  "topics_extracted": 42,
  "started_at": "2025-11-08T12:00:00Z",
  "completed_at": null
}

// GET /api/v1/sync/history
// Get user's sync history
Headers: Authorization: Bearer {token}
Query Params:
  - limit: number (default: 10)

Response:
{
  "syncs": [SyncStatus[]],
  "last_successful_sync": "2025-11-08T10:30:00Z"
}
```

### 6.5 Search APIs

```typescript
// GET /api/v1/search/repositories
// Search repositories (optionally within topics)
Query Params:
  - q: string (required)
  - topics: string[] (optional, filter by topics)
  - language: string (optional)
  - min_stars: number (optional)
  - sort: "stars" | "updated" | "created"
  - page: number
  - per_page: number

Response:
{
  "repositories": [Repository[]],
  "total_count": 1250,
  "pagination": {...},
  "filters_applied": {
    "topics": ["react", "typescript"],
    "language": "JavaScript"
  }
}

// GET /api/v1/search/topics
// Search topics
Query Params:
  - q: string (required)
  - limit: number (default: 20)

Response:
{
  "topics": [Topic[]],
  "total_count": 45
}
```

---

## 7. Screen-by-Screen Implementation

### 7.1 Topics Screen (HOME)

**Route:** `app/(tabs)/topics.tsx`

```typescript
// Main Features:
// - Primary/home screen (opens here on launch)
// - List of followed topics
// - Drag to reorder
// - Pull to refresh
// - Topic suggestions indicator

import { FlashList } from '@shopify/flash-list';
import { useTopics, useReorderTopics } from '@/hooks/queries/useTopics';

export default function TopicsScreen() {
  const { data: topics, isLoading, refetch } = useTopics();
  const reorderMutation = useReorderTopics();
  
  // UI Elements:
  return (
    <View>
      {/* Header */}
      <Header>
        <Title>Topics</Title>
        <IconButton icon="plus" onPress={() => router.push('/browse-topics')} />
        <IconButton icon="settings" onPress={() => router.push('/manage-topics')} />
      </Header>
      
      {/* Topic Suggestions Banner (if available) */}
      {hasSuggestions && (
        <SuggestionBanner
          count={suggestionsCount}
          onPress={() => router.push('/suggestions')}
        />
      )}
      
      {/* Topics List */}
      <DraggableFlatList
        data={topics}
        onDragEnd={handleReorder}
        renderItem={({ item, drag }) => (
          <TopicCard
            topic={item}
            onPress={() => router.push(`/topic/${item.name}`)}
            onLongPress={drag}
          />
        )}
      />
    </View>
  );
}

// TopicCard Component:
function TopicCard({ topic, onPress, onLongPress }) {
  return (
    <Card onPress={onPress} onLongPress={onLongPress}>
      <View className="flex-row items-center">
        <TopicIcon icon={topic.icon} />
        <View className="flex-1">
          <Text className="font-semibold text-lg">{topic.displayName}</Text>
          <Text className="text-gray-500">{topic.repositoryCount} repositories</Text>
          <Text className="text-gray-400 text-sm">Updated {formatTimeAgo(topic.lastSyncedAt)}</Text>
        </View>
        <Badge>Following</Badge>
      </View>
    </Card>
  );
}

// API Calls:
// 1. GET /api/v1/users/me/topics - Load followed topics
// 2. PATCH /api/v1/users/me/topics/reorder - Save new order
// 3. GET /api/v1/suggestions/topics?limit=1 - Check for suggestions
```

### 7.2 Topic Detail Screen

**Route:** `app/topic/[name].tsx`

```typescript
// Main Features:
// - Topic header with follow button
// - Repository list with sorting/filtering
// - Search within topic
// - Sort: Most Stars, Recently Updated, Trending, etc.

export default function TopicDetailScreen() {
  const { name } = useLocalSearchParams();
  const { data: topic } = useTopic(name);
  const { data, fetchNextPage } = useTopicRepositories(name, {
    sort: sortOption,
    language: languageFilter,
  });
  
  return (
    <View>
      {/* Header */}
      <TopicHeader
        topic={topic}
        onFollowToggle={handleFollowToggle}
      />
      
      {/* Filters Bar */}
      <View className="flex-row p-4 gap-2">
        <SortDropdown
          value={sortOption}
          options={['stars', 'updated', 'created', 'forks', 'trending']}
          onChange={setSortOption}
        />
        <FilterDropdown
          value={languageFilter}
          options={['All', 'JavaScript', 'TypeScript', 'Python', ...]}
          onChange={setLanguageFilter}
        />
      </View>
      
      {/* Repositories List */}
      <FlashList
        data={repositories}
        renderItem={({ item }) => (
          <RepositoryCard
            repository={item}
            showTopics={false}  // Already in topic context
            onPress={() => router.push(`/repository/${item.id}`)}
          />
        )}
        onEndReached={fetchNextPage}
      />
    </View>
  );
}

// TopicHeader Component:
function TopicHeader({ topic, onFollowToggle }) {
  return (
    <View className="p-6 bg-gradient-to-r from-blue-500 to-purple-600">
      <View className="flex-row items-center justify-between">
        <View className="flex-1">
          <Text className="text-white text-3xl font-bold">{topic.displayName}</Text>
          <Text className="text-white/80 mt-2">{topic.description}</Text>
          <Text className="text-white/60 mt-1">{topic.repositoryCount} repositories</Text>
        </View>
        <FollowButton
          isFollowing={topic.isFollowing}
          onPress={onFollowToggle}
        />
      </View>
    </View>
  );
}

// API Calls:
// 1. GET /api/v1/topics/{name} - Load topic
// 2. GET /api/v1/topics/{name}/repositories?sort=stars - Load repos
// 3. POST /api/v1/topics/{id}/follow - Follow topic
// 4. DELETE /api/v1/topics/{id}/follow - Unfollow topic
```

### 7.3 Explore Screen

**Route:** `app/(tabs)/explore.tsx`

```typescript
// Main Features:
// - Shows trending repos from followed topics only
// - Trending algorithm scores visible
// - Filter by topic
// - Time window selection (daily/weekly/monthly)

export default function ExploreScreen() {
  const { data: trending, isLoading } = useExploreTrending({
    timeWindow: 'daily',
    topicFilter: selectedTopic,
  });
  
  return (
    <View>
      {/* Header */}
      <Header>
        <Title>Explore</Title>
        <TimeWindowSelector
          value={timeWindow}
          options={['daily', 'weekly', 'monthly']}
          onChange={setTimeWindow}
        />
      </Header>
      
      {/* Topic Filter */}
      <ScrollView horizontal className="px-4">
        <Chip
          label="All Topics"
          selected={!selectedTopic}
          onPress={() => setSelectedTopic(null)}
        />
        {followedTopics.map(topic => (
          <Chip
            key={topic.id}
            label={topic.displayName}
            selected={selectedTopic === topic.name}
            onPress={() => setSelectedTopic(topic.name)}
          />
        ))}
      </ScrollView>
      
      {/* Trending Feed */}
      <FlashList
        data={trending}
        renderItem={({ item }) => (
          <TrendingRepositoryCard
            item={item}
            onPress={() => router.push(`/repository/${item.repository.id}`)}
          />
        )}
      />
    </View>
  );
}

// TrendingRepositoryCard Component:
function TrendingRepositoryCard({ item, onPress }) {
  const { repository, trendingScore, scoreBreakdown, topicsSources } = item;
  
  return (
    <Card onPress={onPress}>
      {/* Repository Info */}
      <Text className="font-semibold text-lg">{repository.nameWithOwner}</Text>
      <Text className="text-gray-600 mt-1">{repository.description}</Text>
      
      {/* Stats */}
      <View className="flex-row items-center gap-4 mt-3">
        <View className="flex-row items-center">
          <Icon name="star" />
          <Text>{formatNumber(repository.stargazerCount)}</Text>
          <Text className="text-green-500 ml-1">+{item.scoreBreakdown.starGrowth}</Text>
        </View>
        <LanguageBadge language={repository.primaryLanguage} />
      </View>
      
      {/* Trending Info */}
      <View className="flex-row items-center justify-between mt-3 pt-3 border-t">
        <View className="flex-row items-center gap-2">
          <Icon name="fire" className="text-orange-500" />
          <Text className="text-sm text-gray-500">
            From: {topicsSources.join(', ')}
          </Text>
        </View>
        <TrendingScoreBadge score={trendingScore} />
      </View>
    </Card>
  );
}

// API Calls:
// 1. GET /api/v1/explore/trending?time_window=daily - Load trending
// 2. GET /api/v1/users/me/topics - Load followed topics for filter
```

### 7.4 Topic Suggestions Screen

**Route:** `app/suggestions.tsx`

```typescript
// Main Features:
// - Shows suggested topics based on starred repos
// - Displays relevance score and reasoning
// - Sample repositories from each topic
// - Follow/Dismiss actions

export default function SuggestionsScreen() {
  const { data: suggestions, isLoading } = useTopicSuggestions();
  const followMutation = useFollowTopic();
  const dismissMutation = useDismissSuggestion();
  
  return (
    <View>
      {/* Header */}
      <Header>
        <Title>🎯 Discover Topics</Title>
      </Header>
      
      {/* Analysis Info */}
      <InfoCard className="m-4">
        <Text className="text-gray-600">
          Based on your {suggestions?.analysis.starred_repos_analyzed} starred repositories,
          we found {suggestions?.total} topics you might love
        </Text>
      </InfoCard>
      
      {/* Suggestions List */}
      <FlashList
        data={suggestions?.suggestions}
        renderItem={({ item }) => (
          <SuggestionCard
            suggestion={item}
            onFollow={() => handleFollow(item)}
            onDismiss={() => handleDismiss(item)}
          />
        )}
      />
    </View>
  );
}

// SuggestionCard Component:
function SuggestionCard({ suggestion, onFollow, onDismiss }) {
  return (
    <Card className="m-4">
      {/* Topic Info */}
      <View className="flex-row items-start justify-between">
        <View className="flex-1">
          <Text className="font-bold text-xl">{suggestion.topic.displayName}</Text>
          <Text className="text-gray-600 mt-1">{suggestion.topic.description}</Text>
        </View>
        <RelevanceBadge score={suggestion.relevanceScore} />
      </View>
      
      {/* Reasoning */}
      <View className="mt-3 p-3 bg-blue-50 rounded-lg">
        <Text className="text-blue-900">
          💡 {suggestion.reason}
        </Text>
        <Text className="text-blue-700 mt-1 text-sm">
          You've starred {suggestion.starredRepoCount} repositories with this topic
        </Text>
      </View>
      
      {/* Sample Repositories */}
      <View className="mt-3">
        <Text className="font-semibold mb-2">Example repositories:</Text>
        {suggestion.sampleRepositories.map(repo => (
          <MiniRepositoryCard key={repo.id} repository={repo} />
        ))}
      </View>
      
      {/* Actions */}
      <View className="flex-row gap-2 mt-4">
        <Button
          variant="primary"
          onPress={onFollow}
          className="flex-1"
        >
          Follow Topic
        </Button>
        <Button
          variant="outline"
          onPress={onDismiss}
        >
          Not Interested
        </Button>
      </View>
    </Card>
  );
}

// API Calls:
// 1. GET /api/v1/suggestions/topics - Load suggestions
// 2. POST /api/v1/topics/{id}/follow - Follow topic
// 3. POST /api/v1/suggestions/topics/{id}/dismiss - Dismiss suggestion
```

### 7.5 Profile & Sync Screen

**Route:** `app/(tabs)/profile.tsx`

```typescript
// Main Features:
// - User profile info
// - Sync starred repos button
// - Sync status/history
// - View topic suggestions
// - Settings & logout

export default function ProfileScreen() {
  const { user } = useAuth();
  const { data: syncStatus } = useSyncStatus();
  const syncMutation = useSyncStarred();
  
  const handleSync = () => {
    syncMutation.mutate({ full_sync: false });
  };
  
  return (
    <ScrollView>
      {/* User Profile */}
      <UserProfileHeader user={user} />
      
      {/* Sync Section */}
      <Section title="GitHub Sync">
        <Card>
          <View className="flex-row items-center justify-between">
            <View>
              <Text className="font-semibold">Starred Repositories</Text>
              <Text className="text-gray-500">
                Last synced: {formatTimeAgo(syncStatus?.last_sync_at)}
              </Text>
            </View>
            <Button onPress={handleSync} loading={syncMutation.isLoading}>
              Sync Now
            </Button>
          </View>
          
          {syncMutation.isLoading && (
            <ProgressBar
              progress={syncStatus?.progress.percentage}
              label={`${syncStatus?.progress.current} / ${syncStatus?.progress.total}`}
            />
          )}
        </Card>
      </Section>
      
      {/* Topic Suggestions */}
      <Section title="Discover Topics">
        <Card onPress={() => router.push('/suggestions')}>
          <View className="flex-row items-center justify-between">
            <View>
              <Text className="font-semibold">🎯 New Suggestions Available</Text>
              <Text className="text-gray-500">
                {suggestionsCount} topics based on your stars
              </Text>
            </View>
            <Icon name="chevron-right" />
          </View>
        </Card>
      </Section>
      
      {/* Settings */}
      <Section title="Settings">
        <SettingsItem label="Notifications" onPress={() => {}} />
        <SettingsItem label="Theme" onPress={() => {}} />
        <SettingsItem label="About" onPress={() => {}} />
      </Section>
      
      {/* Sign Out */}
      <Button variant="destructive" onPress={handleSignOut}>
        Sign Out
      </Button>
    </ScrollView>
  );
}

// API Calls:
// 1. GET /api/v1/users/me - Load user data
// 2. GET /api/v1/sync/history - Load sync history
// 3. POST /api/v1/sync/starred - Trigger sync
// 4. GET /api/v1/sync/status/{id} - Poll sync status
// 5. GET /api/v1/suggestions/topics?limit=1 - Check suggestions
```

---

## 8. Trending Algorithm Design

### 8.1 Algorithm Overview

The trending algorithm calculates a score (0-100) for each repository within a topic, considering multiple factors.

```typescript
// Trending Score Components:

interface TrendingComponents {
  starGrowth: number;        // Weight: 35%
  activityGrowth: number;    // Weight: 25%
  communityEngagement: number; // Weight: 20%
  recency: number;           // Weight: 15%
  quality: number;           // Weight: 5%
}

// Final Score = Weighted sum of all components
```

### 8.2 Algorithm Implementation

```python
# app/services/trending_service.py

from datetime import datetime, timedelta
from typing import List, Dict
import math

class TrendingAlgorithm:
    """
    Custom trending algorithm for repositories within topics
    """
    
    # Weights for each component
    WEIGHTS = {
        'star_growth': 0.35,
        'activity_growth': 0.25,
        'community_engagement': 0.20,
        'recency': 0.15,
        'quality': 0.05
    }
    
    def calculate_trending_score(
        self,
        repo_id: str,
        topic_id: str,
        time_window: str = 'daily'
    ) -> Dict:
        """
        Calculate trending score for a repository within a topic
        """
        # Get time window
        end_time = datetime.utcnow()
        if time_window == 'daily':
            start_time = end_time - timedelta(days=1)
        elif time_window == 'weekly':
            start_time = end_time - timedelta(days=7)
        else:  # monthly
            start_time = end_time - timedelta(days=30)
        
        # Calculate each component
        star_growth_score = self._calculate_star_growth(
            repo_id, start_time, end_time
        )
        
        activity_score = self._calculate_activity_growth(
            repo_id, start_time, end_time
        )
        
        engagement_score = self._calculate_community_engagement(
            repo_id, start_time, end_time
        )
        
        recency_score = self._calculate_recency(repo_id, end_time)
        
        quality_score = self._calculate_quality(repo_id)
        
        # Calculate weighted final score
        final_score = (
            star_growth_score * self.WEIGHTS['star_growth'] +
            activity_score * self.WEIGHTS['activity_growth'] +
            engagement_score * self.WEIGHTS['community_engagement'] +
            recency_score * self.WEIGHTS['recency'] +
            quality_score * self.WEIGHTS['quality']
        )
        
        return {
            'trending_score': int(final_score),
            'components': {
                'star_growth': star_growth_score,
                'activity_growth': activity_score,
                'community_engagement': engagement_score,
                'recency': recency_score,
                'quality': quality_score
            }
        }
    
    def _calculate_star_growth(
        self,
        repo_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> float:
        """
        Calculate star growth rate (0-100)
        
        Formula: Log-scaled growth rate normalized
        """
        # Get star counts at start and end
        stars_start = self._get_stars_at_time(repo_id, start_time)
        stars_end = self._get_stars_at_time(repo_id, end_time)
        
        # Calculate growth
        growth = stars_end - stars_start
        
        if growth <= 0:
            return 0.0
        
        # Log scale (repos with 100 new stars vs 10 new stars)
        # Max expected daily growth: 1000 stars
        score = (math.log(growth + 1) / math.log(1001)) * 100
        
        return min(score, 100.0)
    
    def _calculate_activity_growth(
        self,
        repo_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> float:
        """
        Calculate activity growth (commits, PRs, issues)
        """
        # Get activity metrics
        commits = self._count_commits(repo_id, start_time, end_time)
        prs = self._count_prs(repo_id, start_time, end_time)
        issues = self._count_issues(repo_id, start_time, end_time)
        
        # Weighted activity score
        activity_score = (
            commits * 0.5 +
            prs * 0.3 +
            issues * 0.2
        )
        
        # Normalize (max expected daily activity: 100)
        score = (activity_score / 100) * 100
        
        return min(score, 100.0)
    
    def _calculate_community_engagement(
        self,
        repo_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> float:
        """
        Calculate community engagement (comments, reactions, discussions)
        """
        # Get engagement metrics
        pr_comments = self._count_pr_comments(repo_id, start_time, end_time)
        issue_comments = self._count_issue_comments(repo_id, start_time, end_time)
        discussions = self._count_discussions(repo_id, start_time, end_time)
        unique_contributors = self._count_unique_contributors(
            repo_id, start_time, end_time
        )
        
        # Engagement score
        engagement = (
            pr_comments * 0.3 +
            issue_comments * 0.3 +
            discussions * 0.2 +
            unique_contributors * 0.2
        )
        
        # Normalize (max expected: 200)
        score = (engagement / 200) * 100
        
        return min(score, 100.0)
    
    def _calculate_recency(self, repo_id: str, current_time: datetime) -> float:
        """
        Calculate recency score based on last update
        """
        last_push = self._get_last_push_time(repo_id)
        
        if not last_push:
            return 0.0
        
        hours_since_push = (current_time - last_push).total_seconds() / 3600
        
        # Decay function: 100 at 0 hours, 50 at 24 hours, 0 at 7 days
        if hours_since_push < 24:
            score = 100 - (hours_since_push / 24) * 50
        elif hours_since_push < 168:  # 7 days
            score = 50 - ((hours_since_push - 24) / 144) * 50
        else:
            score = 0
        
        return max(score, 0.0)
    
    def _calculate_quality(self, repo_id: str) -> float:
        """
        Calculate repository quality score
        """
        repo = self._get_repository(repo_id)
        
        # Quality indicators
        has_readme = repo.has_readme
        has_license = repo.has_license
        has_contributing = repo.has_contributing
        has_code_of_conduct = repo.has_code_of_conduct
        issue_response_time = repo.avg_issue_response_time  # hours
        
        score = 0.0
        
        # Basic quality checks
        if has_readme:
            score += 25
        if has_license:
            score += 20
        if has_contributing:
            score += 20
        if has_code_of_conduct:
            score += 15
        
        # Issue response time (faster is better)
        if issue_response_time:
            if issue_response_time < 24:
                score += 20
            elif issue_response_time < 72:
                score += 10
        
        return min(score, 100.0)


# Celery Task to calculate trending scores
@celery_app.task
def calculate_trending_scores_for_topic(topic_id: str, time_window: str = 'daily'):
    """
    Calculate trending scores for all repositories in a topic
    """
    algo = TrendingAlgorithm()
    
    # Get all repositories for topic
    repositories = get_repositories_for_topic(topic_id)
    
    for repo in repositories:
        try:
            # Calculate score
            result = algo.calculate_trending_score(
                repo.id,
                topic_id,
                time_window
            )
            
            # Save to database
            save_trending_score(
                repository_id=repo.id,
                topic_id=topic_id,
                trending_score=result['trending_score'],
                star_growth_rate=result['components']['star_growth'],
                activity_score=result['components']['activity_growth'],
                community_score=result['components']['community_engagement'],
                recency_score=result['components']['recency'],
                time_window=time_window
            )
            
        except Exception as e:
            logger.error(f"Error calculating trending for {repo.id}: {e}")
            continue
```

### 8.3 Caching Strategy

```python
# Trending scores are expensive to calculate
# Cache them in Redis with appropriate TTLs

class TrendingCache:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def get_trending_for_topic(
        self,
        topic_id: str,
        time_window: str = 'daily',
        limit: int = 20
    ) -> List[Dict]:
        """
        Get cached trending scores for a topic
        """
        cache_key = f"trending:{topic_id}:{time_window}"
        
        # Try to get from cache
        cached = self.redis.get(cache_key)
        
        if cached:
            return json.loads(cached)
        
        # Calculate and cache
        scores = self._calculate_and_cache(topic_id, time_window, limit)
        return scores
    
    def _calculate_and_cache(
        self,
        topic_id: str,
        time_window: str,
        limit: int
    ) -> List[Dict]:
        """
        Calculate trending scores and cache results
        """
        # Trigger async calculation
        task = calculate_trending_scores_for_topic.delay(topic_id, time_window)
        task.wait(timeout=30)
        
        # Get results from database
        scores = get_trending_scores_from_db(topic_id, time_window, limit)
        
        # Cache for appropriate time
        ttl = self._get_ttl(time_window)
        cache_key = f"trending:{topic_id}:{time_window}"
        self.redis.setex(
            cache_key,
            ttl,
            json.dumps(scores)
        )
        
        return scores
    
    def _get_ttl(self, time_window: str) -> int:
        """
        Get cache TTL based on time window
        """
        if time_window == 'daily':
            return 900  # 15 minutes
        elif time_window == 'weekly':
            return 3600  # 1 hour
        else:  # monthly
            return 7200  # 2 hours
```

---

## 9. Topic Suggestion Engine

### 9.1 Suggestion Algorithm

```python
# app/services/suggestion_service.py

from typing import List, Dict
from collections import Counter

class TopicSuggestionEngine:
    """
    Suggests topics to users based on their starred repositories
    """
    
    MIN_RELEVANCE_SCORE = 50  # Only suggest topics with score >= 50
    MIN_STARRED_REPOS = 3     # Need at least 3 starred repos with topic
    
    async def generate_suggestions(self, user_id: str) -> List[TopicSuggestion]:
        """
        Generate topic suggestions for a user
        """
        # Get user's starred repositories
        starred_repos = await self._get_user_starred_repos(user_id)
        
        if len(starred_repos) < 10:
            # Not enough data
            return []
        
        # Get topics user is already following
        following_topics = await self._get_user_following_topics(user_id)
        following_topic_names = {t.name for t in following_topics}
        
        # Extract topics from starred repos
        topic_counter = Counter()
        topic_to_repos = {}
        
        for repo in starred_repos:
            for topic_name in repo.topics:
                if topic_name not in following_topic_names:
                    topic_counter[topic_name] += 1
                    
                    if topic_name not in topic_to_repos:
                        topic_to_repos[topic_name] = []
                    topic_to_repos[topic_name].append(repo)
        
        # Generate suggestions
        suggestions = []
        
        for topic_name, count in topic_counter.most_common():
            if count < self.MIN_STARRED_REPOS:
                continue
            
            # Get topic details
            topic = await self._get_topic_by_name(topic_name)
            
            if not topic:
                continue
            
            # Calculate relevance score
            relevance_score = self._calculate_relevance_score(
                starred_count=count,
                total_starred=len(starred_repos),
                topic_popularity=topic.repository_count
            )
            
            if relevance_score < self.MIN_RELEVANCE_SCORE:
                continue
            
            # Get sample repositories
            sample_repos = sorted(
                topic_to_repos[topic_name],
                key=lambda r: r.stargazer_count,
                reverse=True
            )[:5]
            
            # Generate reason
            reason = self._generate_reason(count, len(starred_repos), topic_name)
            
            # Create suggestion
            suggestion = TopicSuggestion(
                topic=topic,
                relevance_score=relevance_score,
                starred_repo_count=count,
                reason=reason,
                sample_repositories=sample_repos,
                is_following=False,
                is_dismissed=False
            )
            
            suggestions.append(suggestion)
        
        # Sort by relevance
        suggestions.sort(key=lambda s: s.relevance_score, reverse=True)
        
        # Save to database
        await self._save_suggestions(user_id, suggestions)
        
        return suggestions
    
    def _calculate_relevance_score(
        self,
        starred_count: int,
        total_starred: int,
        topic_popularity: int
    ) -> int:
        """
        Calculate relevance score (0-100)
        
        Factors:
        - Percentage of starred repos with this topic (40%)
        - Absolute count of starred repos (30%)
        - Topic popularity (20%)
        - Diversity bonus (10%)
        """
        # Percentage score
        percentage = (starred_count / total_starred) * 100
        percentage_score = min(percentage * 2, 40)  # Cap at 40
        
        # Count score (log scale)
        count_score = (math.log(starred_count + 1) / math.log(51)) * 30
        
        # Popularity score (prefer active topics)
        # Topics with 100-10000 repos are ideal
        if 100 <= topic_popularity <= 10000:
            popularity_score = 20
        elif topic_popularity < 100:
            popularity_score = (topic_popularity / 100) * 20
        else:
            popularity_score = 20 - min((topic_popularity - 10000) / 10000 * 10, 10)
        
        # Diversity bonus (prefer topics user hasn't explored much)
        diversity_score = 10 if starred_count < 20 else 5
        
        total_score = percentage_score + count_score + popularity_score + diversity_score
        
        return int(min(total_score, 100))
    
    def _generate_reason(
        self,
        starred_count: int,
        total_starred: int,
        topic_name: str
    ) -> str:
        """
        Generate human-readable reason for suggestion
        """
        percentage = (starred_count / total_starred) * 100
        
        if percentage > 20:
            return f"You've starred {starred_count} {topic_name} repositories — that's {percentage:.0f}% of your stars!"
        elif starred_count > 10:
            return f"{starred_count} of your starred repos focus on {topic_name}. Discover more!"
        else:
            return f"You've shown interest in {topic_name} with {starred_count} starred repos"
    
    async def _get_user_starred_repos(self, user_id: str) -> List[Repository]:
        """Get all repositories user has starred"""
        # Implementation
        pass
    
    async def _get_user_following_topics(self, user_id: str) -> List[Topic]:
        """Get topics user is currently following"""
        # Implementation
        pass
    
    async def _get_topic_by_name(self, name: str) -> Topic:
        """Get topic by name"""
        # Implementation
        pass
    
    async def _save_suggestions(
        self,
        user_id: str,
        suggestions: List[TopicSuggestion]
    ):
        """Save suggestions to database"""
        # Implementation
        pass
```

### 9.2 Suggestion Triggers

```python
# When to generate suggestions:

# 1. After user signs in for first time
@router.post("/auth/callback")
async def auth_callback(code: str):
    # ... authenticate user ...
    
    # Queue suggestion generation
    generate_suggestions_task.delay(user.id)
    
    return {"user": user, "access_token": token}


# 2. After user syncs starred repos
@router.post("/sync/starred")
async def sync_starred(user: User = Depends(get_current_user)):
    # ... sync starred repos ...
    
    # Regenerate suggestions if significant changes
    if repos_added > 10:
        generate_suggestions_task.delay(user.id)
    
    return {"status": "completed"}


# 3. Periodically (weekly) for active users
@celery_app.task
def refresh_suggestions_for_active_users():
    """
    Refresh topic suggestions for users who haven't seen suggestions in a week
    """
    active_users = get_active_users()
    
    for user in active_users:
        last_suggestion = get_last_suggestion_date(user.id)
        
        if not last_suggestion or (datetime.utcnow() - last_suggestion).days > 7:
            generate_suggestions_task.delay(user.id)
```

---

## 10. Implementation Tasks

### Phase 1: Core Setup (100 tasks)

1.1 Project Setup (50 tasks)
1. 
   - [ ] Initialize Expo project
2. 
   - [ ] Configure TypeScript
3. 
   - [ ] Set up NativeWind v5
4. 
   - [ ] Install Expo Router (file-based routing)
5. 
   - [ ] Configure `app.json`
6. 
   - [ ] Set up iOS configuration
7. 
   - [ ] Install React Native Reanimated
8. 
   - [ ] Install Gesture Handler
9. 
   - [ ] Install TanStack Query
10. 
    - [ ] Install Zustand
11. 
    - [ ] Install MMKV storage
12. 
    - [ ] Install FlashList
13. 
    - [ ] Configure navigation structure
14. 
    - [ ] Create (tabs) layout
15. 
    - [ ] Create (auth) layout
16. 
    - [ ] Set up environment variables
17. 
    - [ ] Configure ESLint
18. 
    - [ ] Configure Prettier
19. 
    - [ ] Set up Git hooks
20. 
    - [ ] Initialize backend Python project
21. 
    - [ ] Set up FastAPI
22. 
    - [ ] Configure PostgreSQL
23. 
    - [ ] Configure Redis
24. 
    - [ ] Set up Alembic migrations
25. 
    - [ ] Create Docker compose file
26. 
    - [ ] Configure Celery
27. 
    - [ ] Set up Celery beat
28. 
    - [ ] Install pytest
29. 
    - [ ] Configure Jest
30. 
    - [ ] Set up Testing Library
31. 
    - [ ] **TEST**: Verify dev servers start
32. 
    - [ ] **BUILD**: Verify iOS simulator build
33. 
    - [ ] **CHECKPOINT**: Setup complete

1.2 Authentication (50 tasks)
1. 
   - [ ] Create auth store (Zustand)
2. 
   - [ ] Implement OAuth flow
3. 
   - [ ] Create login screen
4. 
   - [ ] Create callback handler
5. 
   - [ ] Configure GitHub OAuth app
6. 
   - [ ] Implement token storage (SecureStore)
7. 
   - [ ] Create auth service
8. 
   - [ ] Implement token refresh
9. 
   - [ ] Create backend auth endpoints
10. 
    - [ ] Implement JWT creation
11. 
    - [ ] Implement JWT verification
12. 
    - [ ] Create User model
13. 
    - [ ] Create user migration
14. 
    - [ ] Implement protected route middleware
15. 
    - [ ] Create auth context
16. 
    - [ ] Add biometric authentication
17. 
    - [ ] Add session timeout
18. 
    - [ ] Implement logout
19. 
    - [ ] Create auth error handling
20. 
    - [ ] Add rate limiting
21. 
    - [ ] Create audit logging
22. 
    - [ ] **TEST**: Login flow
23. 
    - [ ] **TEST**: Token persistence
24. 
    - [ ] **TEST**: Protected routes
25. 
    - [ ] **CHECKPOINT**: Auth complete

---

### Phase 2: Topic System (150 tasks)

2.1 Topic Models & API (75 tasks)
1. 
   - [ ] Create Topic model (backend)
2. 
   - [ ] Create UserTopic model
3. 
   - [ ] Create RepositoryTopic model
4. 
   - [ ] Create TopicSuggestion model
5. 
   - [ ] Run database migrations
6. 
   - [ ] Create topic schemas (Pydantic)
7. 
   - [ ] Create TopicService class
8. 
   - [ ] Implement GET /topics endpoint
9. 
   - [ ] Implement GET /topics/{name} endpoint
10. 
    - [ ] Implement GET /users/me/topics endpoint
11. 
    - [ ] Implement POST /topics/{id}/follow
12. 
    - [ ] Implement DELETE /topics/{id}/follow
13. 
    - [ ] Implement PATCH /users/me/topics/reorder
14. 
    - [ ] Create topic API client (frontend)
15. 
    - [ ] Create useTopics hook
16. 
    - [ ] Create useTopic hook
17. 
    - [ ] Create useFollowTopic mutation
18. 
    - [ ] Create useUnfollowTopic mutation
19. 
    - [ ] Create useReorderTopics mutation
20. 
    - [ ] Add topic caching strategy
21. 
    - [ ] Implement topic search
22. 
    - [ ] Create topic icons/assets
23. 
    - [ ] **TEST**: Topic CRUD operations
24. 
    - [ ] **TEST**: Topic following
25. 
    - [ ] **TEST**: Topic reordering
26. 
    - [ ] **CHECKPOINT**: Topic models complete

2.2 Topics Screen (Home) (75 tasks)
1. 
   - [ ] Create Topics screen layout
2. 
   - [ ] Create TopicCard component
3. 
   - [ ] Implement drag-to-reorder
4. 
   - [ ] Implement pull-to-refresh
5. 
   - [ ] Add loading states
6. 
   - [ ] Add empty state
7. 
   - [ ] Add error handling
8. 
   - [ ] Create topic suggestions banner
9. 
   - [ ] Implement topic sync
10. 
    - [ ] Add topic count display
11. 
    - [ ] Add last updated timestamp
12. 
    - [ ] Create topic quick actions menu
13. 
    - [ ] Implement topic unfollow
14. 
    - [ ] Add haptic feedback
15. 
    - [ ] Create add topic button
16. 
    - [ ] Create settings button
17. 
    - [ ] Implement topic navigation
18. 
    - [ ] Add animations
19. 
    - [ ] Optimize list performance
20. 
    - [ ] **TEST**: Topics list renders
21. 
    - [ ] **TEST**: Drag to reorder works
22. 
    - [ ] **TEST**: Pull to refresh works
23. 
    - [ ] **TEST**: Navigation works
24. 
    - [ ] **CHECKPOINT**: Topics screen complete

---

### Phase 3: Topic Detail & Repositories (120 tasks)

3.1 Repository Models (60 tasks)
1. 
   - [ ] Create Repository model
2. 
   - [ ] Create StarredRepository model
3. 
   - [ ] Run migrations
4. 
   - [ ] Create repository schemas
5. 
   - [ ] Create RepositoryService
6. 
   - [ ] Implement GET /topics/{name}/repositories
7. 
   - [ ] Add sorting (stars, updated, trending)
8. 
   - [ ] Add filtering (language, min stars)
9. 
   - [ ] Add pagination
10. 
    - [ ] Create useTopicRepositories hook
11. 
    - [ ] Create RepositoryCard component
12. 
    - [ ] Implement infinite scroll
13. 
    - [ ] Add repository caching
14. 
    - [ ] Create repository detail screen
15. 
    - [ ] Implement GET /repositories/{id}
16. 
    - [ ] Implement GET /repositories/{id}/readme
17. 
    - [ ] Create useRepository hook
18. 
    - [ ] Create RepositoryHeader component
19. 
    - [ ] Create RepositoryStats component
20. 
    - [ ] Create ReadmeViewer component
21. 
    - [ ] Add markdown rendering
22. 
    - [ ] Implement star/unstar
23. 
    - [ ] Add share functionality
24. 
    - [ ] Add open in browser
25. 
    - [ ] **TEST**: Repository list
26. 
    - [ ] **TEST**: Repository detail
27. 
    - [ ] **TEST**: README rendering
28. 
    - [ ] **CHECKPOINT**: Repositories complete

3.2 Topic Detail Screen (60 tasks)
1. 
   - [ ] Create Topic Detail screen layout
2. 
   - [ ] Create TopicHeader component
3. 
   - [ ] Add follow/unfollow button
4. 
   - [ ] Create sort dropdown
5. 
   - [ ] Create filter dropdown
6. 
   - [ ] Implement repository list
7. 
   - [ ] Add search within topic
8. 
   - [ ] Create loading states
9. 
   - [ ] Create empty states
10. 
    - [ ] Add pull to refresh
11. 
    - [ ] Implement infinite scroll
12. 
    - [ ] Add topic statistics
13. 
    - [ ] Display repository count
14. 
    - [ ] Add related topics section
15. 
    - [ ] Implement navigation
16. 
    - [ ] Add animations
17. 
    - [ ] Optimize performance
18. 
    - [ ] **TEST**: Topic detail renders
19. 
    - [ ] **TEST**: Sorting works
20. 
    - [ ] **TEST**: Filtering works
21. 
    - [ ] **TEST**: Follow/unfollow works
22. 
    - [ ] **CHECKPOINT**: Topic detail complete

---

### Phase 4: Trending & Explore (150 tasks)

4.1 Trending Algorithm (75 tasks)
1. 
   - [ ] Create TrendingScore model
2. 
   - [ ] Run migration
3. 
   - [ ] Create TrendingAlgorithm class
4. 
   - [ ] Implement star growth calculation
5. 
   - [ ] Implement activity growth calculation
6. 
   - [ ] Implement community engagement score
7. 
   - [ ] Implement recency score
8. 
   - [ ] Implement quality score
9. 
   - [ ] Create weighted scoring function
10. 
    - [ ] Create Celery task for trending calculation
11. 
    - [ ] Set up Celery beat schedule
12. 
    - [ ] Schedule daily trending calculation
13. 
    - [ ] Schedule weekly trending calculation
14. 
    - [ ] Schedule monthly trending calculation
15. 
    - [ ] Create TrendingCache class
16. 
    - [ ] Implement Redis caching
17. 
    - [ ] Set appropriate TTLs
18. 
    - [ ] Create cache invalidation
19. 
    - [ ] Implement GET /trending/topics/{name}
20. 
    - [ ] Implement GET /explore/trending
21. 
    - [ ] Create trending schemas
22. 
    - [ ] **TEST**: Trending calculation
23. 
    - [ ] **TEST**: Caching works
24. 
    - [ ] **TEST**: Score accuracy
25. 
    - [ ] **CHECKPOINT**: Trending algorithm complete

4.2 Explore Screen (75 tasks)
1. 
   - [ ] Create Explore screen layout
2. 
   - [ ] Create TrendingRepositoryCard component
3. 
   - [ ] Display trending score
4. 
   - [ ] Display score breakdown
5. 
   - [ ] Show topic sources
6. 
   - [ ] Add time window selector
7. 
   - [ ] Add topic filter chips
8. 
   - [ ] Implement useExploreTrending hook
9. 
   - [ ] Create loading states
10. 
    - [ ] Create empty states
11. 
    - [ ] Add pull to refresh
12. 
    - [ ] Implement infinite scroll
13. 
    - [ ] Display star growth
14. 
    - [ ] Add trending indicators
15. 
    - [ ] Create TrendingScoreBadge component
16. 
    - [ ] Add fire emoji for hot repos
17. 
    - [ ] Implement navigation
18. 
    - [ ] Add animations
19. 
    - [ ] Optimize performance
20. 
    - [ ] **TEST**: Explore screen renders
21. 
    - [ ] **TEST**: Time window selection
22. 
    - [ ] **TEST**: Topic filtering
23. 
    - [ ] **TEST**: Navigation works
24. 
    - [ ] **CHECKPOINT**: Explore screen complete

---

### Phase 5: Topic Suggestions (120 tasks)

5.1 Suggestion Engine (60 tasks)
1. 
   - [ ] Create TopicSuggestionEngine class
2. 
   - [ ] Implement generate_suggestions method
3. 
   - [ ] Implement starred repo analysis
4. 
   - [ ] Extract topics from starred repos
5. 
   - [ ] Count topic frequency
6. 
   - [ ] Calculate relevance scores
7. 
   - [ ] Generate suggestion reasons
8. 
   - [ ] Get sample repositories
9. 
   - [ ] Create suggestion ranking algorithm
10. 
    - [ ] Implement POST /suggestions/topics/generate
11. 
    - [ ] Implement GET /suggestions/topics
12. 
    - [ ] Implement POST /suggestions/topics/{id}/dismiss
13. 
    - [ ] Create Celery task for suggestion generation
14. 
    - [ ] Set up suggestion triggers
15. 
    - [ ] Trigger on first login
16. 
    - [ ] Trigger on starred sync
17. 
    - [ ] Trigger weekly for active users
18. 
    - [ ] Create suggestion caching
19. 
    - [ ] **TEST**: Suggestion generation
20. 
    - [ ] **TEST**: Relevance scoring
21. 
    - [ ] **TEST**: Trigger logic
22. 
    - [ ] **CHECKPOINT**: Suggestion engine complete

5.2 Suggestions Screen (60 tasks)
1. 
   - [ ] Create Suggestions screen layout
2. 
   - [ ] Create SuggestionCard component
3. 
   - [ ] Display topic info
4. 
   - [ ] Display relevance score
5. 
   - [ ] Display reasoning
6. 
   - [ ] Show starred repo count
7. 
   - [ ] Display sample repositories
8. 
   - [ ] Add follow button
9. 
   - [ ] Add dismiss button
10. 
    - [ ] Create useTopicSuggestions hook
11. 
    - [ ] Create useFollowSuggestion mutation
12. 
    - [ ] Create useDismissSuggestion mutation
13. 
    - [ ] Add loading states
14. 
    - [ ] Add empty state
15. 
    - [ ] Show analysis info
16. 
    - [ ] Implement batch actions
17. 
    - [ ] Add animations
18. 
    - [ ] Create success feedback
19. 
    - [ ] Implement navigation
20. 
    - [ ] **TEST**: Suggestions display
21. 
    - [ ] **TEST**: Follow from suggestions
22. 
    - [ ] **TEST**: Dismiss suggestions
23. 
    - [ ] **CHECKPOINT**: Suggestions screen complete

---

### Phase 6: GitHub Integration & Sync (100 tasks)

6.1 GitHub Service (50 tasks)
1. 
   - [ ] Create GitHubService class
2. 
   - [ ] Configure GitHub API client
3. 
   - [ ] Implement authentication
4. 
   - [ ] Implement rate limit handling
5. 
   - [ ] Implement fetch_user method
6. 
   - [ ] Implement fetch_starred_repos method
7. 
   - [ ] Handle pagination
8. 
   - [ ] Implement fetch_repository method
9. 
   - [ ] Implement fetch_readme method
10. 
    - [ ] Extract topics from repos
11. 
    - [ ] Create error handling
12. 
    - [ ] Add retry logic
13. 
    - [ ] Implement circuit breaker
14. 
    - [ ] Add request logging
15. 
    - [ ] Monitor rate limits
16. 
    - [ ] Create caching layer
17. 
    - [ ] **TEST**: GitHub API calls
18. 
    - [ ] **TEST**: Rate limiting
19. 
    - [ ] **TEST**: Error handling
20. 
    - [ ] **CHECKPOINT**: GitHub service complete

6.2 Sync System (50 tasks)
1. 
   - [ ] Create SyncStatus model
2. 
   - [ ] Run migration
3. 
   - [ ] Create SyncService class
4. 
   - [ ] Implement full sync
5. 
   - [ ] Implement incremental sync
6. 
   - [ ] Create Celery task for sync
7. 
   - [ ] Implement progress tracking
8. 
   - [ ] Implement POST /sync/starred
9. 
   - [ ] Implement GET /sync/status/{id}
10. 
    - [ ] Implement GET /sync/history
11. 
    - [ ] Create useSyncStarred mutation
12. 
    - [ ] Create useSyncStatus hook
13. 
    - [ ] Add sync progress display
14. 
    - [ ] Create progress bar
15. 
    - [ ] Add sync history
16. 
    - [ ] Implement background sync
17. 
    - [ ] Add sync notifications
18. 
    - [ ] Handle sync errors
19. 
    - [ ] Implement retry logic
20. 
    - [ ] Add sync locks (prevent concurrent)
21. 
    - [ ] **TEST**: Full sync
22. 
    - [ ] **TEST**: Incremental sync
23. 
    - [ ] **TEST**: Progress tracking
24. 
    - [ ] **CHECKPOINT**: Sync system complete

---

### Phase 7: Search & Profile (80 tasks)

7.1 Search Implementation (40 tasks)
1. 
   - [ ] Create Search screen
2. 
   - [ ] Create search bar component
3. 
   - [ ] Implement search API endpoint
4. 
   - [ ] Add topic filtering
5. 
   - [ ] Add language filtering
6. 
   - [ ] Add min stars filtering
7. 
   - [ ] Create useSearch hook
8. 
   - [ ] Implement debounced search
9. 
   - [ ] Create search results component
10. 
    - [ ] Add search history
11. 
    - [ ] Implement search suggestions
12. 
    - [ ] Add empty search state
13. 
    - [ ] Add no results state
14. 
    - [ ] Optimize search performance
15. 
    - [ ] Add search analytics
16. 
    - [ ] **TEST**: Search functionality
17. 
    - [ ] **TEST**: Filtering works
18. 
    - [ ] **CHECKPOINT**: Search complete

7.2 Profile & Settings (40 tasks)
1. 
   - [ ] Create Profile screen
2. 
   - [ ] Create UserProfileHeader component
3. 
   - [ ] Display user stats
4. 
   - [ ] Add sync section
5. 
   - [ ] Create sync button
6. 
   - [ ] Display sync status
7. 
   - [ ] Add suggestions section
8. 
   - [ ] Create settings section
9. 
   - [ ] Add notifications settings
10. 
    - [ ] Add theme settings
11. 
    - [ ] Add about section
12. 
    - [ ] Implement sign out
13. 
    - [ ] Add loading states
14. 
    - [ ] Create useAuth hook
15. 
    - [ ] **TEST**: Profile display
16. 
    - [ ] **TEST**: Sync from profile
17. 
    - [ ] **CHECKPOINT**: Profile complete

---

### Phase 8: Testing & QA (100 tasks)

8.1 Unit Tests (40 tasks)
1. 
   - [ ] Write tests for auth store
2. 
   - [ ] Write tests for topic hooks
3. 
   - [ ] Write tests for repository hooks
4. 
   - [ ] Write tests for suggestion hooks
5. 
   - [ ] Write tests for sync hooks
6. 
   - [ ] Write tests for TopicCard
7. 
   - [ ] Write tests for RepositoryCard
8. 
   - [ ] Write tests for SuggestionCard
9. 
   - [ ] Write tests for TrendingCard
10. 
    - [ ] Write backend service tests
11. 
    - [ ] Write algorithm tests
12. 
    - [ ] Set up code coverage
13. 
    - [ ] **RUN**: All unit tests
14. 
    - [ ] **VERIFY**: Coverage &gt; 85%
15. 
    - [ ] **CHECKPOINT**: Unit tests complete

8.2 Integration Tests (30 tasks)
1. 
   - [ ] Set up Detox
2. 
   - [ ] Write login flow test
3. 
   - [ ] Write topics flow test
4. 
   - [ ] Write explore flow test
5. 
   - [ ] Write suggestions flow test
6. 
   - [ ] Write sync flow test
7. 
   - [ ] Write offline tests
8. 
   - [ ] **RUN**: Integration tests
9. 
   - [ ] **CHECKPOINT**: Integration tests complete

8.3 E2E Tests (30 tasks)
1. 
   - [ ] Set up Maestro
2. 
   - [ ] Write critical user journeys
3. 
   - [ ] Write error handling tests
4. 
   - [ ] Write performance tests
5. 
   - [ ] Set up CI for E2E
6. 
   - [ ] **RUN**: E2E tests
7. 
   - [ ] **CHECKPOINT**: E2E tests complete

---

### Phase 9: Deployment (80 tasks)

9.1 Frontend Deployment (40 tasks)
1. 
   - [ ] Configure EAS Build
2. 
   - [ ] Set up iOS credentials
3. 
   - [ ] Configure environment variables
4. 
   - [ ] Build development version
5. 
   - [ ] Build preview version
6. 
   - [ ] Build production version
7. 
   - [ ] Submit to App Store Connect
8. 
   - [ ] Configure app metadata
9. 
   - [ ] Upload screenshots
10. 
    - [ ] Submit for review
11. 
    - [ ] Set up OTA updates
12. 
    - [ ] **BUILD**: Production build
13. 
    - [ ] **DEPLOY**: App Store
14. 
    - [ ] **CHECKPOINT**: Frontend deployed

9.2 Backend Deployment (40 tasks)
1. 
   - [ ] Set up production infrastructure
2. 
   - [ ] Deploy PostgreSQL
3. 
   - [ ] Deploy Redis
4. 
   - [ ] Deploy FastAPI app
5. 
   - [ ] Deploy Celery workers
6. 
   - [ ] Set up monitoring
7. 
   - [ ] Set up logging
8. 
   - [ ] Set up error tracking (Sentry)
9. 
   - [ ] Configure CI/CD
10. 
    - [ ] **DEPLOY**: Production backend
11. 
    - [ ] **VERIFY**: All services healthy
12. 
    - [ ] **CHECKPOINT**: Backend deployed

---

### Phase 10: Polish & Launch (50 tasks)

10.1 Optimization (25 tasks)
1. 
   - [ ] Optimize bundle size
2. 
   - [ ] Optimize API calls
3. 
   - [ ] Optimize database queries
4. 
   - [ ] Optimize images
5. 
   - [ ] Optimize animations
6. 
   - [ ] Implement caching everywhere
7. 
   - [ ] **TEST**: Performance metrics
8. 
   - [ ] **CHECKPOINT**: Optimizations complete

10.2 Final Polish (25 tasks)
1. 
   - [ ] Add haptic feedback
2. 
   - [ ] Implement dark mode
3. 
   - [ ] Add accessibility features
4. 
   - [ ] Create onboarding flow
5. 
   - [ ] Add app icon
6. 
   - [ ] Add splash screen
7. 
   - [ ] Final QA pass
8. 
   - [ ] **VERIFY**: Ready to launch
9. 
   - [ ] **LAUNCH**: 🚀

---

**Total Tasks**: 405
**Estimated Timeline**: 14-18 weeks
**Team Size**: 2-3 developers (1-2 iOS, 1 Backend)

---

## Success Metrics

### Technical

- App launch time &lt; 2s
- API response time &lt; 500ms (p95)
- Test coverage &gt; 85%
- Crash-free rate &gt; 99.5%

### Product

- Topic suggestion acceptance rate &gt; 60%
- Average topics followed per user &gt; 8
- Daily active user retention (D7) &gt; 40%
- User engagement (sessions per week) &gt; 5

---

This specification now accurately reflects the **topic-first, suggestion-driven** approach you described. The app opens to Topics (home), suggests topics based on starred repos, and shows trending repos only from topics users follow. Let me know if you'd like me to expand any section!