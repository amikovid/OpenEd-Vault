# Meta Ads Strategy Reference

Consolidated from Ben Heath, Jamie Stenton, and Nathan Visser.

---

## The Two-Campaign Structure

Run two campaigns, not one:

| Campaign | Purpose | Budget Split |
|----------|---------|--------------|
| **Scaling** | Run proven winners at scale | 70-80% when profitable |
| **Testing** | Find next-generation winners | 20-30% (flip to 70-80% when unprofitable) |

**Why this works:** A single campaign starves new creative of budget once winners emerge. Separating them forces Meta to spend testing budget on new ads, revealing winners before you need them.

**Within each campaign:** One Ad Set with consolidated cold + warm audiences, open targeting. Meta blends them anyway - give it more data to optimize. Only segment by location if regional messaging differs significantly.

---

## Audience Targeting

**Default approach:** Start broad, let Meta learn.

- Location: Your market(s)
- Age: 18-65 unless clearly narrower
- Gender: All unless product-specific
- Interests: None or 2-3 very broad

**Build over time (after 50+ conversions):**
- **Custom Audiences:** Website visitors, customer email lists, video viewers, engaged followers
- **Lookalikes:** Start 1% (most similar), expand to 2-5% as you scale

**Avoid:** Stacking 5+ interests, behavior targeting, excluding broad groups, manual placements.

---

## Creative Strategy: The Creator Approach

Hire creators instead of making ads yourself.

**Where to find them:** Meta Creator Marketplace (free, under Engage Audience > All Tools)

**What to request:**
- 2-3 full video ads
- 10 hooks (first 3 seconds, different locations/openings)

**The math:** 2 ads + 10 hooks = 20+ variations for roughly the price of 3 ads. Creators charge based on time, not output - 10 hooks takes minimal extra time.

**Guidelines, not scripts:** Give brand guardrails but let creators use their voice. Over-scripting produces worse results.

---

## Value Rules (Finding Higher-Value Customers)

Value Rules tell Meta some conversions are worth more than others.

**Setup:** Ads Manager > Advertising Settings > Value Rules > Create Rule Set

**What you can weight:**
- Age ranges (e.g., 30-40 year olds spend more)
- Device (desktop vs mobile)
- Operating system (iOS vs Android)
- Placement (Instagram vs Facebook)
- Location (regions with higher AOV or lower shipping)

**Critical principle:** Weight toward better segments, don't exclude worse ones.

| Approach | Result |
|----------|--------|
| Weight 30-40 at 2.0, others at 1.0 | Meta still shows to all ages, optimizes harder for best segment |
| Exclude under-30 and over-40 | You lose conversions and signal scarcity to algorithm |

**Expect cost per result to increase.** That's the point - you're optimizing for value, not volume. Track ROI, not CPL.

---

## The Lead Gen System

Correct flow for service businesses:

```
Highly Targeted Ads
    ↓
Landing Page or Lead Form (not homepage)
    ↓
CRM Database (capture + organize)
    ↓
Email Nurture Flow (warm before contact)
    ↓
Manual Follow-Up (people buy from people)
    ↓
Retargeting (for non-responders)
    ↓
Booking → Sale → Ascension/Upsell
```

**Why boosting fails:** Reaches broad audiences with no qualification, no capture mechanism, no nurture, no follow-up system. Vanity metrics, not revenue.

**Key principle:** Leads are a numbers game. Know your unit economics - cost per lead, conversion rate, lifetime value, break-even point.

---

## Budget Guidelines

| Daily Budget | Expected Outcome |
|--------------|------------------|
| $10-20 | Minimal data, limited learning |
| $50+ | Solid data in 3-5 days |
| $100+ | Recommended for serious testing |

**Better to spend $50/day on one ad set than $10/day across five.**

**The learning phase:** Meta needs 3-7 days and ~50 conversions to optimize. Don't change settings during this period - it resets progress.

---

## Optimization Workflow

**Days 1-2:** Do nothing. Algorithm learning.

**Day 3:** Check for issues (pixel firing, traffic generating). Don't pause based on metrics yet.

**Day 5-7:** First real evaluation. Compare to benchmarks.

**Week 2+:** Make decisions based on full week of data.

**Scaling winners:** Increase budget 20-30% at a time, not doubling overnight.

**Managing fatigue:** Monitor frequency metric. Above 4 = audience seeing ad too often. Rotate creative or expand audience.

---

## Key Metrics

| Metric | What It Tells You | Target |
|--------|-------------------|--------|
| **Cost Per Result** | Efficiency per conversion | Depends on margins |
| **CTR** | Creative resonance | Above 1% |
| **ROAS** | Revenue per $1 spent | 3:1+ for profitability |
| **CPM** | Competition level | Lower = more efficient |
| **Frequency** | Ad fatigue risk | 1.5-3 ideal, above 4 = refresh needed |

---

## Common Mistakes

1. **Changing settings during learning phase** - Resets algorithm progress
2. **Spreading budget too thin** - 10 ad sets at $5/day each gets no optimization
3. **Targeting too narrow** - Let Meta find customers in broad audiences
4. **Single campaign trap** - New creative gets starved of budget
5. **DIY video when creators exist** - Hire expertise, don't become a video producer
6. **Expecting immediate results** - Judge after 3-7 days minimum
7. **Optimizing for wrong objective** - Use Sales/Leads, not Traffic, if you want conversions
8. **Static budget allocation** - Shift based on profitability, don't lock in ratios

---

## Quick Setup Checklist

**Before launching:**
- [ ] Meta Pixel installed and verified (use Pixel Helper extension)
- [ ] Conversion events configured (Purchase, Lead, etc.)
- [ ] Landing page ready (not homepage)
- [ ] 3-5 creative variations prepared
- [ ] CRM integration for lead capture

**Campaign structure:**
- [ ] Scaling Campaign created (proven winners)
- [ ] Testing Campaign created (new creative)
- [ ] One Ad Set per campaign (consolidated audiences)
- [ ] Budget set at $50+/day minimum
- [ ] Automatic placements enabled

**After launch:**
- [ ] Wait 3-7 days before changes
- [ ] Check pixel is tracking
- [ ] Document what's working
- [ ] Plan creative refresh for week 2

---

*Sources: Ben Heath (414K subs, $150M+ managed spend), Jamie Stenton, Nathan Visser (333 Agency)*
