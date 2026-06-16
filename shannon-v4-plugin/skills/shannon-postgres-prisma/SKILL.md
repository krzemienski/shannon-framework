---
name: shannon-postgres-prisma
display_name: "Shannon PostgreSQL + Prisma"
description: "PostgreSQL database operations with Prisma ORM: schema design, migrations, queries, transactions, and optimization"
category: database
version: "4.0.0"
priority: 1
auto_activate: true
activation_condition: "domain_analysis.database >= 15% AND ('PostgreSQL' in tech_stack OR 'Prisma' in tech_stack)"
mcp_servers:
  required: [serena]
  recommended: [postgres, context7]
allowed_tools: [Write, Read, Edit, Glob, Grep, postgres_query, postgres_execute]
---

# Shannon PostgreSQL + Prisma

> **Database Operations**: Schema design, migrations, queries, transactions

## Capabilities

- Prisma schema design
- Migration workflows (dev, deploy, reset)
- CRUD operations
- Complex queries (joins, aggregations)
- Relations (one-to-one, one-to-many, many-to-many)
- Transactions
- Indexes and optimization
- Type-safe queries

## Patterns

**Schema Design**:
```prisma
// schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
  createdAt DateTime @default(now())

  @@index([authorId])
  @@index([published])
}
```

**Migration Workflow**:
```bash
# Development
npx prisma migrate dev --name add_user_posts

# Production
npx prisma migrate deploy

# Generate client
npx prisma generate
```

**Query Patterns**:
```typescript
// Basic CRUD
const user = await prisma.user.create({
  data: { email: 'user@example.com', name: 'User' }
});

const users = await prisma.user.findMany({
  where: { email: { contains: '@example.com' } },
  include: { posts: true }
});

// Relations
const userWithPosts = await prisma.user.findUnique({
  where: { id: 1 },
  include: { posts: { where: { published: true } } }
});

// Transactions
await prisma.$transaction([
  prisma.user.create({ data: {...} }),
  prisma.post.create({ data: {...} })
]);
```

**Testing (NO MOCKS)**:
- Real PostgreSQL database (Docker for tests)
- Real migrations
- Real queries
- No in-memory databases (unless production uses it)

## Integration

**Context7 MCP**: Load Prisma docs
```bash
context7 get "Prisma relations"
context7 get "Prisma transactions"
```

📚 Full patterns: [resources/PRISMA_PATTERNS.md](./resources/PRISMA_PATTERNS.md)
