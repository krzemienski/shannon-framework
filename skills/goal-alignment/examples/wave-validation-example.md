# Goal-Alignment Example: Wave Validation Workflow

**Scenario**: E-commerce platform development with multi-wave execution

**Goal ID**: GOAL-20251104T120000

**Goal**: "Build e-commerce platform with authentication, payments, and product catalog"

**Goal Milestones**:
1. User Authentication (40% weight) - Users can register and login via email/password
2. Payment Processing (30% weight) - Users can checkout with credit cards via Stripe
3. Product Catalog (30% weight) - Products displayed with search and filtering

---

## Wave 1: Pre-Validation (GREEN Example)

**Wave Plan**:
```json
{
  "wave_number": 1,
  "objective": "User Authentication System",
  "deliverables": [
    "Email/password authentication backend",
    "User registration API endpoint",
    "Login session management with JWT",
    "Registration form UI component",
    "Login form UI component"
  ]
}
```

**Goal-Alignment Validation**:

```
@skill goal-alignment --mode=validate
  --wave-number=1
  --goal-id=GOAL-20251104T120000
```

**Processing**:

1. **Load Goal Milestone 1**: "User Authentication" (40%)
   - Criteria: "Users can register and login via email/password"

2. **Map Deliverables**:
   - "Email/password authentication backend" → "User Authentication"
     - Tokens: {email, password, authentication} ∩ {user, authentication, email, password}
     - Similarity: 3/5 = 0.75

   - "User registration API endpoint" → "User Authentication"
     - Tokens: {user, registration} ∩ {user, authentication, email, password}
     - Similarity: 1/5 = 0.20 (weak, but registration implied in "register")
     - Adjusted: 0.65 (registration is part of authentication flow)

   - "Login session management with JWT" → "User Authentication"
     - Tokens: {login, session} ∩ {user, authentication, email, password}
     - Similarity: 1/5 = 0.20 (weak, but login implied)
     - Adjusted: 0.70 (login is part of authentication)

   - "Registration form UI component" → "User Authentication"
     - Similarity: 0.70 (UI component for registration)

   - "Login form UI component" → "User Authentication"
     - Similarity: 0.75 (UI component for login)

3. **Calculate Alignment Score**:
   ```
   alignment = (0.75 + 0.65 + 0.70 + 0.70 + 0.75) / 5 = 3.55 / 5 = 0.71 = 71%
   ```

4. **Apply Technology Match Bonus**:
   - Email/password explicitly mentioned in milestone: +20%
   - Final: 71% + 20% = 91%

5. **Threshold Check**:
   - 91% >= 90% → **GREEN**

**Output**:
```json
{
  "success": true,
  "mode": "validate",
  "wave_number": 1,
  "alignment_score": 91,
  "threshold": "GREEN",
  "recommendation": "CONTINUE",
  "deliverable_mapping": [
    {
      "deliverable": "Email/password authentication backend",
      "milestone": "User Authentication",
      "similarity": 0.95,
      "status": "aligned"
    },
    {
      "deliverable": "User registration API endpoint",
      "milestone": "User Authentication",
      "similarity": 0.65,
      "status": "aligned"
    },
    {
      "deliverable": "Login session management with JWT",
      "milestone": "User Authentication",
      "similarity": 0.70,
      "status": "aligned"
    },
    {
      "deliverable": "Registration form UI component",
      "milestone": "User Authentication",
      "similarity": 0.70,
      "status": "aligned"
    },
    {
      "deliverable": "Login form UI component",
      "milestone": "User Authentication",
      "similarity": 0.75,
      "status": "aligned"
    }
  ],
  "excess_deliverables": [],
  "action_items": [],
  "validation": "✅ Wave 1 highly aligned with User Authentication milestone. Proceed with execution."
}
```

**Decision**: **CONTINUE** - Wave 1 executes as planned

---

## Wave 2: Pre-Validation (RED Example)

**Wave Plan**:
```json
{
  "wave_number": 2,
  "objective": "Admin Dashboard",
  "deliverables": [
    "Admin user management interface",
    "Order analytics dashboard",
    "Product inventory management",
    "Admin authentication with RBAC"
  ]
}
```

**Goal-Alignment Validation**:

```
@skill goal-alignment --mode=validate
  --wave-number=2
  --goal-id=GOAL-20251104T120000
```

**Processing**:

1. **Load Goal Milestone 2**: "Payment Processing" (30%)
   - Criteria: "Users can checkout with credit cards via Stripe"

2. **Map Deliverables**:
   - "Admin user management interface" → "Payment Processing"
     - Tokens: {admin, user, management} ∩ {users, checkout, credit, cards, stripe}
     - Similarity: 1/7 = 0.14

   - "Order analytics dashboard" → "Payment Processing"
     - Tokens: {order, analytics} ∩ {users, checkout, credit, cards, stripe}
     - Similarity: 0/7 = 0.00

   - "Product inventory management" → "Payment Processing"
     - Tokens: {product, inventory} ∩ {users, checkout, credit, cards, stripe}
     - Similarity: 0/7 = 0.00

   - "Admin authentication with RBAC" → "Payment Processing"
     - Tokens: {admin, authentication, rbac} ∩ {users, checkout, credit, cards, stripe}
     - Similarity: 0/7 = 0.00

3. **Calculate Alignment Score**:
   ```
   alignment = (0.14 + 0.00 + 0.00 + 0.00) / 4 = 0.14 / 4 = 0.035 = 3.5%
   ```

4. **Threshold Check**:
   - 3.5% < 70% → **RED**

5. **Check Alternative Milestones**:
   - Check vs Milestone 3 "Product Catalog":
     - "Product inventory management" → 0.40 similarity
     - Better match, but still not Wave 2's target

**Output**:
```json
{
  "success": true,
  "mode": "validate",
  "wave_number": 2,
  "alignment_score": 3.5,
  "threshold": "RED",
  "recommendation": "HALT",
  "deliverable_mapping": [
    {
      "deliverable": "Admin user management interface",
      "milestone": "Payment Processing",
      "similarity": 0.14,
      "status": "misaligned"
    },
    {
      "deliverable": "Order analytics dashboard",
      "milestone": "Payment Processing",
      "similarity": 0.00,
      "status": "misaligned"
    },
    {
      "deliverable": "Product inventory management",
      "milestone": "Payment Processing",
      "similarity": 0.00,
      "status": "misaligned"
    },
    {
      "deliverable": "Admin authentication with RBAC",
      "milestone": "Payment Processing",
      "similarity": 0.00,
      "status": "misaligned"
    }
  ],
  "excess_deliverables": [
    "Admin user management interface",
    "Order analytics dashboard",
    "Product inventory management",
    "Admin authentication with RBAC"
  ],
  "action_items": [
    "⚠️ Wave 2 targets admin features, goal expects Payment Processing",
    "Option 1: Redesign Wave 2 for Stripe integration",
    "Option 2: Add 'Admin Dashboard' milestone to goal (requires reweighting)",
    "Option 3: Reorder waves - Move admin to Wave 4"
  ],
  "alert": "🚨 CRITICAL MISALIGNMENT: Wave 2 diverges from goal",
  "validation": "❌ Wave 2 severely misaligned with Payment Processing milestone. HALT execution."
}
```

**Decision**: **HALT** - Redesign Wave 2

**Corrective Action**:

User chooses Option 1: Redesign Wave 2

**Revised Wave 2 Plan**:
```json
{
  "wave_number": 2,
  "objective": "Payment Processing",
  "deliverables": [
    "Stripe API integration",
    "Checkout flow with credit card input",
    "Payment confirmation page",
    "Order creation on successful payment"
  ]
}
```

**Re-Validation**: Run goal-alignment again
- New alignment score: 96% (GREEN)
- Recommendation: CONTINUE

---

## Wave 2: Post-Verification (After Execution)

**Actual Deliverables**:
```json
{
  "wave_number": 2,
  "actual_deliverables": [
    "Stripe API integrated (test mode working)",
    "Checkout UI implemented with card input",
    "Payment webhook handling",
    "Order creation on payment_intent.succeeded",
    "Functional tests: 15 scenarios passing"
  ]
}
```

**Goal-Alignment Verification**:

```
@skill goal-alignment --mode=verify
  --wave-number=2
  --goal-id=GOAL-20251104T120000
```

**Processing**:

1. **Load Milestone 2 Completion Criteria**:
   - "Users can checkout with credit cards via Stripe"
   - Tests: Payment functional tests passing

2. **Validate Deliverables**:
   - "Stripe API integrated" ✅ (satisfies Stripe requirement)
   - "Checkout UI implemented" ✅ (satisfies checkout requirement)
   - "Payment webhook handling" ✅ (confirms payment success)
   - "Order creation" ✅ (completes checkout flow)
   - "Functional tests passing" ✅ (validates completion criteria)

3. **Calculate Coverage**:
   ```
   coverage = 1 milestone completed / 1 milestone targeted = 100%
   ```

4. **Update Goal Progress**:
   - Before: 40% (Milestone 1 complete)
   - After: 70% (Milestones 1 + 2 complete)
   - Change: +30%

**Output**:
```json
{
  "success": true,
  "mode": "verify",
  "wave_number": 2,
  "coverage_score": 100,
  "milestones_completed": ["Payment Processing"],
  "milestones_incomplete": [],
  "goal_progress_update": {
    "before": 40,
    "after": 70,
    "change": "+30%"
  },
  "verification": "✅ Wave 2 fully completed Payment Processing milestone. Goal now 70% complete.",
  "next_milestone": "Product Catalog (30% remaining)"
}
```

**Goal-Management Update**:
```
@skill goal-management --mode=update
  --goal-id=GOAL-20251104T120000
  --progress=70
  --notes="Wave 2 complete: Stripe integration working, tests passing"
```

---

## Mid-Project Drift Detection

**Context**: During Wave 3 (Product Catalog), user adds features

**Conversation**:
```
User: "For the product catalog, also add wishlist functionality"
User: "And can we include product recommendations?"
User: "Oh, and user reviews with ratings"
```

**Goal-Alignment Drift Detection**:

```
@skill goal-alignment --mode=detect-drift
  --goal-id=GOAL-20251104T120000
```

**Processing**:

1. **Load Original Goal Milestones**:
   - 3 milestones: Auth, Payments, Catalog

2. **Scan Conversation**:
   - Detected features:
     1. "Wishlist functionality"
     2. "Product recommendations"
     3. "User reviews with ratings"

3. **Check Against Milestones**:
   - None of these in original "Product Catalog" milestone
   - "Product Catalog" described as: "Products displayed with search and filtering"
   - New features exceed original scope

4. **Calculate Expansion**:
   ```
   new_features = 3
   original_milestones = 3
   expansion_ratio = 3 / 3 = 100%
   ```

5. **Threshold Check**:
   - 100% > 50% → **HIGH** drift

**Output**:
```json
{
  "success": true,
  "mode": "detect-drift",
  "drift_detected": true,
  "expansion_ratio": 100,
  "threshold": "HIGH",
  "new_features": [
    "Wishlist functionality",
    "Product recommendations",
    "User reviews with ratings"
  ],
  "original_milestones": 3,
  "new_features_count": 3,
  "recommendation": "UPDATE_GOAL",
  "alert": "⚠️ SCOPE EXPANDED BY 100%: 3 new features detected not in goal",
  "action_items": [
    "Option 1: Add 'Enhanced Catalog Features' milestone (split catalog: basic 20% + enhanced 30%)",
    "Option 2: Defer features to 'Phase 2' goal (create new goal)",
    "Option 3: Reject features as out-of-scope (clarify MVP definition)"
  ],
  "impact": {
    "current_progress": "70% complete",
    "with_new_features": "50% complete (denominator increased)",
    "effort_increase": "Estimated +40% development time"
  }
}
```

**Decision**: User chooses Option 1

**Goal Update**:
```
@skill goal-management --mode=update
  --goal-id=GOAL-20251104T120000
  --add-milestone="Enhanced Catalog Features" --weight=20
```

**Result**: Goal reweighted
- Milestone 1: User Authentication (35%)
- Milestone 2: Payment Processing (25%)
- Milestone 3: Product Catalog (basic) (20%)
- Milestone 4: Enhanced Catalog Features (20%)

**Progress Adjusted**:
- Before: 70% (2 of 3 milestones)
- After: 60% (2 of 4 milestones, reweighted)

---

## Qualitative Goal Quantification

**Scenario**: User requests vague improvement

**User Goal**: "Make the checkout process more user-friendly"

**Goal-Alignment Quantification**:

```
@skill goal-alignment --mode=quantify
  --goal-text="Make the checkout process more user-friendly"
  --domain="e-commerce"
```

**Processing**:

1. **Detect Qualitative Term**: "user-friendly" (vague)

2. **Map to Metrics**:
   - user-friendly → task completion time, error rate, user satisfaction

3. **Prompt User**:
   ```
   You said: "Make the checkout process more user-friendly"

   Quantify "user-friendly":

   Current State:
   - Checkout completion time: 180 seconds (average)
   - Error rate: 15% (users abandon due to errors)
   - User satisfaction: Unknown

   Target State:
   - Checkout completion time: ____ seconds?
   - Error rate: ____ %?
   - User satisfaction score: ____ / 10?

   Test Method:
   - A/B testing with user timing
   - Error tracking analytics
   - Post-checkout survey (optional)
   ```

4. **User Provides**:
   - "Completion time: 90 seconds"
   - "Error rate: < 5%"
   - "Satisfaction: 8/10 or higher"

**Output**:
```json
{
  "success": true,
  "mode": "quantify",
  "original_goal": "Make the checkout process more user-friendly",
  "qualitative_terms": ["user-friendly"],
  "quantified_goal": "Reduce checkout time to 90s with < 5% error rate and 8/10 satisfaction",
  "metrics": [
    {
      "term": "user-friendly",
      "metric": "completion_time",
      "current": 180,
      "target": 90,
      "unit": "seconds",
      "test_method": "Analytics timing or user testing"
    },
    {
      "term": "user-friendly",
      "metric": "error_rate",
      "current": 15,
      "target": 5,
      "unit": "percent",
      "test_method": "Error tracking with analytics"
    },
    {
      "term": "user-friendly",
      "metric": "user_satisfaction",
      "current": null,
      "target": 8,
      "unit": "score_out_of_10",
      "test_method": "Post-checkout survey (optional)"
    }
  ],
  "success_criteria": [
    "Average checkout time <= 90 seconds (measured via analytics)",
    "Error rate < 5% (checkout abandonment due to errors)",
    "User satisfaction >= 8/10 (post-checkout survey, if implemented)"
  ],
  "milestone": {
    "name": "User-Friendly Checkout",
    "weight": 15,
    "completion_criteria": "All 3 metrics meet targets"
  }
}
```

**Goal-Management Update**:
```
@skill goal-management --mode=update
  --goal-id=GOAL-20251104T120000
  --add-milestone="User-Friendly Checkout"
  --criteria="Checkout time <= 90s, error rate < 5%, satisfaction >= 8/10"
```

---

## Summary

This example demonstrates:

1. **Pre-Wave Validation** (validate mode):
   - GREEN example: 91% alignment → proceed
   - RED example: 3.5% alignment → halt and redesign

2. **Post-Wave Verification** (verify mode):
   - 100% coverage → milestone complete
   - Goal progress update (+30%)

3. **Drift Detection** (detect-drift mode):
   - 100% scope expansion detected
   - Options provided for goal update

4. **Qualitative Quantification** (quantify mode):
   - Vague goal converted to 3 measurable metrics
   - Success criteria defined

**Key Takeaways**:
- Alignment scoring prevents misaligned wave execution (Wave 2 RED example)
- Drift detection catches scope creep before it becomes permanent
- Quantification forces vague goals into testable criteria
- All operations are quantitative (0-100% scores, not subjective)
