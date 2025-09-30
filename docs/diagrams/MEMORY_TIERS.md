# Shannon Framework - Memory Tier System

## 5-Tier Memory Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                   MEMORY TIER ARCHITECTURE                       │
│                                                                  │
│  Principle: Information theory-inspired memory management       │
│  Goal: Optimal storage efficiency with fast retrieval           │
└─────────────────────────────────────────────────────────────────┘

TIER 1: WORKING MEMORY
┌─────────────────────────────────────────────────────────────────┐
│  Duration:       0-1 minute                                      │
│  Compression:    NONE (raw data)                                │
│  Ratio:          1:1                                             │
│  Access Speed:   Instant (in-memory)                             │
│  Use Case:       Active task context                             │
│                                                                  │
│  ┌───────────────────────────────────────────────────────┐      │
│  │  Active Variables │ Current State │ Immediate Results │      │
│  └───────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼ Automatic transition after 1 minute
                            │
TIER 2: HOT MEMORY
┌─────────────────────────────────────────────────────────────────┐
│  Duration:       1 minute - 1 hour                               │
│  Compression:    SEMANTIC (embedding-based)                      │
│  Ratio:          5:1                                             │
│  Access Speed:   Very Fast (cached)                              │
│  Use Case:       Recent operations and patterns                  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────┐      │
│  │  Recent Tasks │ Pattern Cache │ Frequent Accesses    │      │
│  │                                                       │      │
│  │  Compression Method:                                  │      │
│  │  • Deduplication via MD5 hashing                      │      │
│  │  • Reference markers (@REF:hash)                      │      │
│  │  • LZ4 frame compression                              │      │
│  └───────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼ Automatic transition after 1 hour
                            │
TIER 3: WARM MEMORY
┌─────────────────────────────────────────────────────────────────┐
│  Duration:       1 hour - 24 hours                               │
│  Compression:    AST (Abstract Syntax Tree)                      │
│  Ratio:          10:1                                            │
│  Access Speed:   Fast (retrievable with overhead)                │
│  Use Case:       Daily operations and intermediate results       │
│                                                                  │
│  ┌───────────────────────────────────────────────────────┐      │
│  │  Session History │ AST Structures │ Parsed Context   │      │
│  │                                                       │      │
│  │  Compression Method:                                  │      │
│  │  • Parse to AST representation                        │      │
│  │  • Store only semantic nodes                          │      │
│  │  • Zstandard compression                              │      │
│  └───────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼ Automatic transition after 24 hours
                            │
TIER 4: COLD MEMORY
┌─────────────────────────────────────────────────────────────────┐
│  Duration:       24 hours - 7 days                               │
│  Compression:    HOLOGRAPHIC (distributed representation)        │
│  Ratio:          50:1                                            │
│  Access Speed:   Medium (reconstruction required)                │
│  Use Case:       Weekly patterns and historical data             │
│                                                                  │
│  ┌───────────────────────────────────────────────────────┐      │
│  │  Historical Patterns │ Key Insights │ Rare Access     │      │
│  │                                                       │      │
│  │  Compression Method:                                  │      │
│  │  • Holographic encoding (distributed)                 │      │
│  │  • Lossy but reconstructible                          │      │
│  │  • Maximum Zstandard compression                      │      │
│  └───────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼ Automatic transition after 7 days
                            │
TIER 5: ARCHIVE MEMORY
┌─────────────────────────────────────────────────────────────────┐
│  Duration:       > 7 days (long-term)                            │
│  Compression:    ARCHIVE (maximum compression)                   │
│  Ratio:          100:1                                           │
│  Access Speed:   Slow (full decompression needed)                │
│  Use Case:       Long-term storage and audit trails              │
│                                                                  │
│  ┌───────────────────────────────────────────────────────┐      │
│  │  Audit Logs │ Complete History │ Reference Archive   │      │
│  │                                                       │      │
│  │  Compression Method:                                  │      │
│  │  • Maximum Zstandard level (22)                       │      │
│  │  • Dictionary-based compression                       │      │
│  │  • Optional disk offload                              │      │
│  └───────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

## Memory Transition Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                AUTOMATIC TIER TRANSITIONS                        │
└─────────────────────────────────────────────────────────────────┘

Time-Based Transitions:
┌──────────┐    1 min     ┌──────────┐    1 hour    ┌──────────┐
│ WORKING  │─────────────▶│   HOT    │─────────────▶│   WARM   │
└──────────┘              └──────────┘              └──────────┘
                                                           │
                                                           │ 24 hours
                                                           ▼
┌──────────┐   7 days    ┌──────────┐
│ ARCHIVE  │◀────────────│   COLD   │
└──────────┘             └──────────┘

Access-Based Promotion:
┌──────────┐
│   COLD   │──────────▶ Accessed ──────▶ Promote to HOT
└──────────┘

┌──────────┐
│  ARCHIVE │──────────▶ Accessed ──────▶ Promote to WARM
└──────────┘

Compression Cascade:
┌──────────────────────────────────────────────────────────┐
│  Item creation                                           │
│         │                                                │
│         ▼                                                │
│  [WORKING] ──▶ No compression                            │
│         │                                                │
│         ▼ After 1 min                                    │
│  [HOT]     ──▶ Apply semantic compression (5:1)          │
│         │                                                │
│         ▼ After 1 hour                                   │
│  [WARM]    ──▶ Apply AST compression (10:1)              │
│         │                                                │
│         ▼ After 24 hours                                 │
│  [COLD]    ──▶ Apply holographic compression (50:1)      │
│         │                                                │
│         ▼ After 7 days                                   │
│  [ARCHIVE] ──▶ Apply maximum compression (100:1)         │
└──────────────────────────────────────────────────────────┘
```

## Memory Item Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    MEMORY ITEM ANATOMY                           │
└─────────────────────────────────────────────────────────────────┘

MemoryItem {
  ┌───────────────────────────────────────────────────────┐
  │ key: str                    ──▶ "task_result_abc123"  │
  │ content: Any                ──▶ Actual data           │
  │ tier: MemoryTier            ──▶ WORKING/HOT/WARM/...  │
  │ created_at: float           ──▶ Unix timestamp        │
  │ last_accessed: float        ──▶ Unix timestamp        │
  │ access_count: int           ──▶ Number of accesses    │
  │ compressed: bool            ──▶ True/False            │
  │ compression_type: Enum      ──▶ SEMANTIC/AST/...      │
  │ compressed_size: int        ──▶ Bytes after compress  │
  │ original_size: int          ──▶ Bytes before compress │
  │ metadata: Dict              ──▶ Additional info       │
  └───────────────────────────────────────────────────────┘
}

Metadata Examples:
┌───────────────────────────────────────────────────────────┐
│  {                                                        │
│    "agent_id": "AnalysisAgent_42_1234567890",            │
│    "task_type": "complexity_analysis",                   │
│    "priority": "high",                                   │
│    "tags": ["wave_1", "phase_analysis"],                │
│    "related_items": ["task_abc122", "task_abc124"]      │
│  }                                                        │
└───────────────────────────────────────────────────────────┘
```

## Compression Algorithms

```
┌─────────────────────────────────────────────────────────────────┐
│              COMPRESSION ALGORITHM COMPARISON                    │
└─────────────────────────────────────────────────────────────────┘

SEMANTIC COMPRESSION (HOT tier, 5:1):
┌────────────────────────────────────────┐
│  Input: Text data                      │
│         │                              │
│         ▼                              │
│  Step 1: Split into lines             │
│         │                              │
│         ▼                              │
│  Step 2: Hash each line (MD5)          │
│         │                              │
│         ▼                              │
│  Step 3: Deduplicate using hash table  │
│         │                              │
│         ▼                              │
│  Step 4: Replace duplicates with @REF  │
│         │                              │
│         ▼                              │
│  Step 5: Apply LZ4 frame compression   │
│         │                              │
│         ▼                              │
│  Output: Compressed bytes (5:1 ratio)  │
└────────────────────────────────────────┘

AST COMPRESSION (WARM tier, 10:1):
┌────────────────────────────────────────┐
│  Input: Code or structured data       │
│         │                              │
│         ▼                              │
│  Step 1: Parse to AST                  │
│         │                              │
│         ▼                              │
│  Step 2: Extract semantic nodes        │
│         │                              │
│         ▼                              │
│  Step 3: Discard formatting/whitespace │
│         │                              │
│         ▼                              │
│  Step 4: Serialize minimal AST         │
│         │                              │
│         ▼                              │
│  Step 5: Zstandard compression         │
│         │                              │
│         ▼                              │
│  Output: Compressed bytes (10:1 ratio) │
└────────────────────────────────────────┘

HOLOGRAPHIC COMPRESSION (COLD tier, 50:1):
┌────────────────────────────────────────┐
│  Input: Historical data                │
│         │                              │
│         ▼                              │
│  Step 1: Extract key patterns          │
│         │                              │
│         ▼                              │
│  Step 2: Distributed encoding          │
│         │                              │
│         ▼                              │
│  Step 3: Lossy but reconstructible     │
│         │                              │
│         ▼                              │
│  Step 4: Maximum Zstandard level       │
│         │                              │
│         ▼                              │
│  Output: Compressed bytes (50:1 ratio) │
└────────────────────────────────────────┘

ARCHIVE COMPRESSION (ARCHIVE tier, 100:1):
┌────────────────────────────────────────┐
│  Input: Long-term storage data         │
│         │                              │
│         ▼                              │
│  Step 1: Dictionary-based analysis     │
│         │                              │
│         ▼                              │
│  Step 2: Maximum Zstandard (level 22)  │
│         │                              │
│         ▼                              │
│  Step 3: Optional disk offload         │
│         │                              │
│         ▼                              │
│  Output: Compressed bytes (100:1)      │
└────────────────────────────────────────┘
```

## Access Pattern Tracking

```
┌─────────────────────────────────────────────────────────────────┐
│                   ACCESS PATTERN MONITORING                      │
└─────────────────────────────────────────────────────────────────┘

Memory Access:
┌──────────────┐
│ get(key)     │
└──────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Update metadata:                    │
│  • last_accessed = now()             │
│  • access_count += 1                 │
│  • Record access pattern             │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Evaluate promotion:                 │
│                                      │
│  IF access_count > threshold         │
│  AND current_tier > HOT              │
│  THEN promote to HOT tier            │
└──────────────────────────────────────┘

Hot Item Detection:
┌──────────────────────────────────────┐
│  Criteria:                           │
│  • 5+ accesses in 5 minutes          │
│  • 10+ accesses in 1 hour            │
│  • Access frequency > 1/minute       │
│                                      │
│  Action: Promote to HOT tier         │
│         Keep uncompressed            │
└──────────────────────────────────────┘
```

## Storage Efficiency

```
┌─────────────────────────────────────────────────────────────────┐
│                STORAGE EFFICIENCY CALCULATION                    │
└─────────────────────────────────────────────────────────────────┘

Example Dataset: 1GB of wave execution data

Distribution across tiers:
┌──────────────────────────────────────────────────────────────┐
│  WORKING (10%):  100MB × 1:1    = 100MB                      │
│  HOT (20%):      200MB × 5:1    = 40MB                       │
│  WARM (30%):     300MB × 10:1   = 30MB                       │
│  COLD (30%):     300MB × 50:1   = 6MB                        │
│  ARCHIVE (10%):  100MB × 100:1  = 1MB                        │
│                                                              │
│  Total Storage: 177MB (82.3% reduction from 1GB)             │
└──────────────────────────────────────────────────────────────┘

Retrieval Performance:
┌──────────────────────────────────────────────────────────────┐
│  WORKING:    < 1ms    (instant)                              │
│  HOT:        < 5ms    (cached + decompression)               │
│  WARM:       < 20ms   (retrieval + AST reconstruction)       │
│  COLD:       < 100ms  (full decompression + reconstruction)  │
│  ARCHIVE:    < 500ms  (disk I/O + full decompression)        │
└──────────────────────────────────────────────────────────────┘
```