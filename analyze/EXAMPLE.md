# Example: Quick Analysis of a Pricing Strategy

**Input:**
```bash
analyze quick "SaaS pricing: $49/mo starter, $199/mo pro, $499/mo enterprise"
```

---

**Output:**

# Quick Analysis: SaaS Pricing Strategy

**Mode**: Quick | **Domain**: Business | **Date**: 2026-01-28

## The Essence
A value-capture mechanism using tiered pricing to segment customers by willingness-to-pay and feature needs, creating revenue optimization through price discrimination.

## Verified Facts
- Three tiers: $49, $199, $499 (4.1x and 2.5x jumps)
- Domain: SaaS (subscription model)
- Confidence: Medium (stated structure, no supporting data)

## Key Points (Top 7)

1. **Pricing gaps are uneven** ($150 vs $300 jumps) → Middle tier is the "decoy" anchor making $199 look reasonable
2. **Missing: Feature differentiation** → Can't evaluate if price aligns with value delivered per tier
3. **4x Starter→Pro jump is aggressive** → Most SaaS use 2-3x multipliers; risk of sticker shock
4. **No annual discount mentioned** → Leaving 15-30% revenue on table (typical annual prepay incentive)
5. **Enterprise tier exists** → Signals custom pricing above $499, but $499 anchor may be too low if targeting large orgs
6. **Missing usage-based component** → Pure seat-based or flat pricing has lower expansion revenue than hybrid models
7. **Competitive context unknown** → Price positioning meaningless without competitor benchmarking

## Assumptions to Challenge

| Assumption | Evidence For | Evidence Against | Verdict |
|------------|-------------|------------------|---------|
| "Users will upgrade from $49 to $199" | Tier structure suggests it | 4x jump is steep; may need $99 tier | **VALIDATE** - Test with upgrade cohort data |
| "Enterprise starts at $499" | Listed as third tier | Enterprises typically spend $2k-50k+/year | **CHALLENGE** - Likely loses enterprise deals |
| "Customers value features, not usage" | Flat pricing suggests it | Modern SaaS trend toward usage-based | **VALIDATE** - Survey customer preference |
| "Annual/monthly pricing parity is fine" | Not mentioned | Industry standard: 20% discount for annual | **DISCARD** - Add annual option |

## What You Haven't Considered

1. **Psychological anchoring is working AGAINST you**: $499 "enterprise" tier anchors prospects low. Real enterprise buyers won't take you seriously. Consider removing public enterprise pricing entirely (→ "Contact Sales")

2. **Churn risk in Starter tier**: $49/mo customers have highest churn (low commitment). You're optimizing for acquisition over retention. Consider: raising to $79-99 (filters serious buyers) or making Starter annual-only.

3. **Revenue expansion ceiling**: Flat pricing = revenue grows only via seat expansion or tier upgrades. Usage-based component (API calls, storage, etc.) allows same customer to 10x spend without changing tier.

4. **Competitive response**: If you're undercutting competitors, they'll match. If you're premium, where's the justification? Price exists in a competitive system, not a vacuum.

## The Real Question

Not "are these prices right?" but:
1. **What's the LTV:CAC ratio by tier?** (Is Pro tier actually more profitable?)
2. **What % of revenue comes from expansion vs new?** (Pricing structure determines this)
3. **Where do customers cluster?** (If 80% choose Pro, Starter/Enterprise are poorly positioned)

## Quick Actions (Top 5)

- [ ] **Get competitor pricing data** (5 direct competitors) → Understand if you're premium/value/parity - 2h
- [ ] **Analyze current customer tier distribution** → If >70% in one tier, pricing is broken - 1h  
- [ ] **Add annual pricing** (20% discount) → Improve cash flow + reduce churn - 4h to implement
- [ ] **A/B test Starter at $49 vs $79** → Measure conversion rate change + churn at 30/60/90 days - 2 weeks
- [ ] **Remove public Enterprise pricing** → Replace with "Contact Sales" (increases deal size flexibility) - 1h

## Critical Risk to Watch

**Pricing too low initially** → Extremely difficult to raise later due to:
- Existing customer backlash (grandfather clauses trap you)
- Anchoring effect (market perceives you as "cheap")
- Brand perception (low price = low quality signal)

Start higher, offer discounts selectively. Far easier to discount than raise.

---

## Notes

This example demonstrates:
- ✅ First-principles decomposition (what pricing actually is)
- ✅ Challenging unstated assumptions
- ✅ Surfacing unconsidered factors (anchoring, churn, competitive response)
- ✅ Reframing to the real questions
- ✅ Specific, time-bound actions
- ✅ Evidence-based (marks confidence levels)
- ✅ Critical risk highlighted

**Time to generate**: ~45 seconds (Quick mode)
