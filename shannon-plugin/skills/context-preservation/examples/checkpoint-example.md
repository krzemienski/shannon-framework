# Context Preservation Example: Wave Checkpoint

## Scenario
User completes Wave 2 of e-commerce platform implementation, needs checkpoint before starting Wave 3.

## Input
```json
{
  "mode": "wave-checkpoint",
  "label": "wave-2-complete",
  "wave_number": 2,
  "include_files": true,
  "include_tests": true
}
```

## Process

### Step 1: Collect Context

**Active Context**:
- Wave 2 execution (Backend API implementation)
- Status: Complete
- Duration: 4 hours
- Agents used: backend-dev, test-dev

### Step 2: Gather Metadata

**Project Metadata**:
```json
{
  "name": "E-Commerce Platform",
  "root_path": "/Users/user/projects/ecommerce",
  "domains": ["frontend", "backend", "database"],
  "technologies": ["React", "Node.js", "PostgreSQL"],
  "file_count": 87
}
```

**Goals**:
```json
{
  "active_goals": [
    {
      "goal_id": "goal-1",
      "title": "Launch MVP by end of month",
      "criteria": ["User auth", "Product catalog", "Cart", "Checkout"],
      "progress": 65,
      "last_updated": "2025-11-03T14:00:00.000Z"
    }
  ]
}
```

**Wave History**:
```json
{
  "current_wave": 2,
  "wave_history": [
    {
      "wave_number": 1,
      "status": "complete",
      "completed_at": "2025-11-03T11:00:00.000Z",
      "deliverables_key": "shannon/waves/1/complete",
      "agents_used": ["frontend-dev", "backend-dev"],
      "deliverables": [
        "React component library",
        "Shopping cart UI",
        "Product catalog UI"
      ]
    },
    {
      "wave_number": 2,
      "status": "complete",
      "completed_at": "2025-11-03T14:00:00.000Z",
      "deliverables_key": "shannon/waves/2/complete",
      "agents_used": ["backend-dev", "test-dev"],
      "deliverables": [
        "JWT authentication API",
        "Product CRUD endpoints",
        "Cart management API",
        "Checkout workflow API"
      ]
    }
  ]
}
```

**Tasks**:
```json
{
  "total": 47,
  "completed": 35,
  "in_progress": 0,
  "blocked": 0,
  "remaining": 12
}
```

**Tests**:
```json
{
  "last_run": "2025-11-03T14:00:00.000Z",
  "platform": "web",
  "total_tests": 23,
  "passed": 23,
  "failed": 0,
  "no_mocks_compliant": true,
  "test_results_key": "shannon/tests/20251103T140000"
}
```

**Modified Files**:
```json
[
  {
    "path": "src/api/auth.ts",
    "last_modified": "2025-11-03T13:45:00.000Z",
    "change_summary": "JWT authentication implementation"
  },
  {
    "path": "src/api/products.ts",
    "last_modified": "2025-11-03T13:50:00.000Z",
    "change_summary": "Product CRUD endpoints"
  },
  {
    "path": "src/api/cart.ts",
    "last_modified": "2025-11-03T13:55:00.000Z",
    "change_summary": "Cart management API"
  },
  {
    "path": "tests/api/auth.test.ts",
    "last_modified": "2025-11-03T14:00:00.000Z",
    "change_summary": "Auth flow Puppeteer tests"
  }
]
```

### Step 3: Create Checkpoint Structure

**Checkpoint ID**: `SHANNON-W2-20251103T140000`

**Complete Checkpoint**:
```json
{
  "checkpoint_id": "SHANNON-W2-20251103T140000",
  "label": "wave-2-complete",
  "type": "wave-checkpoint",
  "timestamp": "2025-11-03T14:00:00.000Z",
  "shannon_version": "4.0.0",

  "context": {
    "conversation_summary": "Completed Wave 2: Backend API implementation with JWT auth, product CRUD, cart management, and checkout workflow. All tests passing (23/23). Ready for Wave 3: Frontend integration.",
    "user_intent": "Build e-commerce platform MVP by end of month",
    "current_phase": "implementation",
    "active_command": "/sh_wave 2"
  },

  "project": {
    "name": "E-Commerce Platform",
    "root_path": "/Users/user/projects/ecommerce",
    "domains": ["frontend", "backend", "database"],
    "technologies": ["React", "Node.js", "PostgreSQL"]
  },

  "specification": {
    "original_spec": "Build e-commerce platform with user authentication, product catalog, shopping cart, and checkout...",
    "complexity_score": 78,
    "analyzed_at": "2025-11-03T10:00:00.000Z",
    "spec_analysis_key": "shannon/specs/20251103T100000"
  },

  "goals": {
    "active_goals": [
      {
        "goal_id": "goal-1",
        "title": "Launch MVP by end of month",
        "criteria": ["User auth", "Product catalog", "Cart", "Checkout"],
        "progress": 65,
        "last_updated": "2025-11-03T14:00:00.000Z"
      }
    ],
    "goal_history_key": "shannon/goals/history"
  },

  "waves": {
    "current_wave": 2,
    "wave_history": [
      {
        "wave_number": 1,
        "status": "complete",
        "completed_at": "2025-11-03T11:00:00.000Z",
        "deliverables_key": "shannon/waves/1/complete",
        "agents_used": ["frontend-dev", "backend-dev"]
      },
      {
        "wave_number": 2,
        "status": "complete",
        "completed_at": "2025-11-03T14:00:00.000Z",
        "deliverables_key": "shannon/waves/2/complete",
        "agents_used": ["backend-dev", "test-dev"]
      }
    ]
  },

  "tasks": {
    "total": 47,
    "completed": 35,
    "in_progress": 0,
    "blocked": 0,
    "remaining": 12,
    "task_details_key": "shannon/tasks/current"
  },

  "tests": {
    "last_run": "2025-11-03T14:00:00.000Z",
    "platform": "web",
    "total_tests": 23,
    "passed": 23,
    "failed": 0,
    "no_mocks_compliant": true,
    "test_results_key": "shannon/tests/20251103T140000"
  },

  "files": {
    "modified_files": [
      {
        "path": "src/api/auth.ts",
        "last_modified": "2025-11-03T13:45:00.000Z",
        "change_summary": "JWT authentication implementation"
      },
      {
        "path": "src/api/products.ts",
        "last_modified": "2025-11-03T13:50:00.000Z",
        "change_summary": "Product CRUD endpoints"
      },
      {
        "path": "src/api/cart.ts",
        "last_modified": "2025-11-03T13:55:00.000Z",
        "change_summary": "Cart management API"
      },
      {
        "path": "tests/api/auth.test.ts",
        "last_modified": "2025-11-03T14:00:00.000Z",
        "change_summary": "Auth flow Puppeteer tests"
      }
    ],
    "file_count": 87,
    "has_project_index": true,
    "project_index_key": "shannon/project_index"
  },

  "mcps": {
    "required_available": ["serena", "sequential"],
    "recommended_available": ["context7", "puppeteer"],
    "conditional_available": ["postgres"],
    "missing_recommended": []
  },

  "metadata": {
    "size_bytes": 45623,
    "integrity_hash": "sha256:a7f2b3d4e5f6...",
    "compression": "gzip",
    "can_restore": true,
    "retention_days": 30
  },

  "restoration_hints": {
    "next_actions": [
      "Start Wave 3: Frontend integration with backend APIs",
      "Connect React components to auth API",
      "Integrate product catalog with backend",
      "Test complete shopping flow with Puppeteer"
    ],
    "context_dependencies": [
      "shannon/waves/2/complete",
      "shannon/specs/20251103T100000",
      "shannon/project_index"
    ]
  }
}
```

### Step 4: Store in Serena MCP

**Create Checkpoint Entity**:
```python
serena.create_entities([
    {
        "name": "SHANNON-W2-20251103T140000",
        "entityType": "checkpoint",
        "observations": [
            json.dumps(checkpoint_data),
            "label: wave-2-complete",
            "wave: 2",
            "type: wave-checkpoint",
            "status: complete"
        ]
    }
])
```

**Create Relations**:
```python
serena.create_relations([
    {
        "from": "SHANNON-W2-20251103T140000",
        "to": "project:ecommerce",
        "relationType": "CHECKPOINT_FOR"
    },
    {
        "from": "SHANNON-W2-20251103T140000",
        "to": "SHANNON-W1-20251103T110000",
        "relationType": "FOLLOWS"
    },
    {
        "from": "SHANNON-W2-20251103T140000",
        "to": "wave-2-deliverables",
        "relationType": "CONTAINS"
    }
])
```

**Store Wave Deliverables**:
```python
serena.add_observations([
    {
        "entityName": "wave-2-deliverables",
        "contents": [
            "JWT authentication API implemented and tested",
            "Product CRUD endpoints (GET, POST, PUT, DELETE) working",
            "Cart management API with add/remove/update operations",
            "Checkout workflow API with order creation",
            "23 Puppeteer tests passing (NO MOCKS compliant)",
            "Backend integration complete and ready for frontend"
        ]
    }
])
```

### Step 5: User Notification

**Confirmation Message**:
```
✅ Checkpoint Created: SHANNON-W2-20251103T140000

📊 Checkpoint Summary:
- Label: wave-2-complete
- Wave: 2 (complete)
- Progress: 35/47 tasks (74%)
- Tests: 23/23 passed (100%)
- Files: 4 modified
- Size: 44.6 KB

🔄 To restore: /sh_restore SHANNON-W2-20251103T140000

📍 Storage: Serena MCP (shannon/checkpoints/SHANNON-W2-20251103T140000)
⏱️  Retention: 30 days (expires 2025-12-03)

🎯 Next Actions:
1. Start Wave 3: Frontend integration with backend APIs
2. Connect React components to auth API
3. Integrate product catalog with backend
4. Test complete shopping flow with Puppeteer
```

## Output

**Success Response**:
```json
{
  "success": true,
  "checkpoint_id": "SHANNON-W2-20251103T140000",
  "label": "wave-2-complete",
  "type": "wave-checkpoint",
  "size_bytes": 45623,
  "size_kb": "44.6 KB",
  "compression": "gzip",
  "storage_location": "serena://shannon/checkpoints/SHANNON-W2-20251103T140000",
  "restore_command": "/sh_restore SHANNON-W2-20251103T140000",
  "retention_days": 30,
  "expires_at": "2025-12-03T14:00:00.000Z",
  "integrity_hash": "sha256:a7f2b3d4e5f6...",

  "summary": {
    "wave": 2,
    "wave_status": "complete",
    "tasks_completed": 35,
    "tasks_total": 47,
    "tests_passed": 23,
    "tests_total": 23,
    "files_modified": 4
  },

  "next_actions": [
    "Start Wave 3: Frontend integration with backend APIs",
    "Connect React components to auth API",
    "Integrate product catalog with backend",
    "Test complete shopping flow with Puppeteer"
  ]
}
```

## Restoration Verification

To verify checkpoint works:
```bash
# Restore checkpoint
/sh_restore SHANNON-W2-20251103T140000

# Expected: Full context restored
# - Project: E-Commerce Platform
# - Goal: Launch MVP (65% complete)
# - Wave: 2 complete, ready for Wave 3
# - Tests: 23/23 passing
# - Next: Frontend integration
```

## Key Takeaways

1. **Rich Metadata**: Checkpoint includes goals, waves, tasks, tests, files - everything needed to resume
2. **Structured Storage**: Serena MCP with relations enables intelligent restoration
3. **Next Actions**: Clear guidance on what to do after restoration
4. **Validation**: Integrity hash ensures checkpoint not corrupted
5. **Wave Continuity**: Previous wave deliverables linked for context

This checkpoint enables user to:
- Close Claude Code and resume later
- Switch to different project and come back
- Recover from context compaction
- Hand off to another developer
- Review progress at any time
