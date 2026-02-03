# Meta Ads Value Rules: Finding Higher-Value Customers & Improving ROAS

## Executive Summary

Value Rules allow you to signal to Meta's algorithm which conversions matter most to your business. Rather than treating all conversions equally, you can weight them based on customer attributes and behaviors. This shifts Meta's optimization from "lowest cost per conversion" to "highest value conversion," which typically improves ROI even if cost per result increases.

The core insight: **every lead gen client would pay double for better quality leads**. Value Rules automate this preference.

---

## What Value Rules Do

Value Rules tell Meta's algorithm that some conversions are worth more than others. When properly configured, Meta will:

1. **Prioritize valuable customers** - Optimize campaigns toward audiences and channels that historically deliver higher-value conversions
2. **Reweight optimization** - Shift from cost-per-result to value-per-result
3. **Improve ROI** - Even if cost per conversion increases, total business value typically increases

Value Rules are not audience exclusions—they're optimization weights. This is a critical distinction that prevents leaving money on the table.

---

## Weighting Dimensions

You can weight conversions based on customer and conversion attributes:

### Audience Attributes
- **Age range** (e.g., 30-40 year olds spend more, convert higher)
- **Gender**
- **Geographic location** (e.g., California vs rural states for shipping costs)

### Technical Attributes
- **Device type** (desktop vs mobile)
- **Operating system** (iOS vs Android)
- **Conversion location** (website vs Facebook)
- **Placement** (Instagram vs Facebook feed)

---

## When to Use Value Rules (With Examples)

### Lead Generation
If your analysis shows that 30-40 year old leads consistently convert to higher-value sales, weight toward that segment. This signals Meta to find more similar prospects.

**Mistake to avoid:** Don't exclude 29 or 41 year olds entirely. They still convert—just at a lower rate. Weight them down, not out.

### B2B Services
If desktop users convert better for your B2B offer (they're evaluating on computers, not phones), weight toward desktop rather than excluding mobile entirely.

**Why:** Mobile users may still be valuable; they're just your secondary target. Excluding them wastes potential inventory.

### E-commerce
If customers from California generate 2x AOV compared to rural areas (due to shipping economics, population density, or brand perception), weight heavily toward California while still showing ads to other regions.

### Location-Based Weighting
Prioritize geographic regions where:
- Shipping costs are lower
- Customer lifetime value is higher
- Local demand is strongest

---

## Step-by-Step Setup

### 1. Access Value Rules
Navigate to **Ads Manager → Advertising Settings → Value Rules**

### 2. Create Rule Set
Click **Create Rule Set**

### 3. Define Your Weights
Select the conversion attribute you want to weight, then assign relative values:

- Assign a baseline value (e.g., "1.0") to your control group
- Assign higher values to high-value segments (e.g., "1.5" or "2.0")
- Assign lower values to lower-value segments (e.g., "0.7")

### 4. Apply to Campaign
Assign the Value Rule Set to relevant campaigns

### 5. Monitor Results
Track cost per result vs. total business value over 1-2 weeks before making adjustments

---

## Strategic Guidelines

### Focus on ROI, Not Lowest Cost
The goal is not the lowest cost per conversion—it's the highest value per dollar spent. If Value Rules increase your cost per lead by 15% but increase lead quality by 40%, that's a win.

**Reframe the conversation:** "We're paying more per lead, but fewer leads are wasting our sales team's time."

### Use Weighting, Not Exclusion
Always weight toward better segments rather than excluding worse ones:

| Approach | Problem |
|----------|---------|
| Weight 30-40 year olds at 2.0, younger/older at 1.0 | ✓ Meta still shows ads to all ages, just optimizes harder for your best segment |
| Exclude anyone under 30 or over 40 | ✗ You lose valuable conversions and signal scarcity to the algorithm |

### Test One Dimension at a Time
Start with your highest-impact attribute (e.g., age if your data clearly shows an age sweet spot). Once you see improvement, test a second dimension (e.g., device type).

### Base Weights on Data
Don't guess. Analyze your conversion data to find:
- Which customer segments have highest lifetime value
- Which devices drive the best-quality conversions
- Which placements attract your target customer

### Weight Proportionally
If your best customers spend 2x more, weight them at 1.5-2.0, not 10.0. Extreme weights can confuse the algorithm.

---

## Common Mistakes

### 1. Mistaking Value Rules for Audience Exclusion
**Mistake:** "I'll set 45+ to 0.0 to exclude them."

**Why it fails:** You're telling Meta to waste ad spend on older users when it could show to them at reduced priority. This loses conversions.

**Correct approach:** Set 45+ to 0.8 or 0.9 if they're still slightly valuable.

### 2. Ignoring Cost Per Result Increases
**Mistake:** Implementing Value Rules, seeing cost per result go up 20%, and immediately pausing them.

**Why it fails:** Cost per result *should* increase if you're optimizing for value, not volume. The real metric is value per dollar.

**Correct approach:** Track: (Total Revenue - Ad Spend) / Ad Spend = True ROI.

### 3. Setting Weights Too Extreme
**Mistake:** Your best customer segment weights 10.0, everyone else is 0.1.

**Why it fails:** The algorithm becomes overly narrow and may struggle to find enough volume in your best segment.

**Correct approach:** Use a 2-3x range (e.g., 1.5x to 1.0 or 2.0 to 1.0).

### 4. Not Waiting Long Enough to Evaluate
**Mistake:** Implementing Value Rules Monday, reviewing results Wednesday.

**Why it fails:** Meta's algorithm needs time to learn and optimize. Two days isn't enough data.

**Correct approach:** Give it 1-2 weeks of data before making changes.

### 5. Weighting Low-Data Segments
**Mistake:** You have 50 conversions from iOS and 5 from Android, so you weight Android at 0.2.

**Why it fails:** Five conversions isn't enough data to determine if Android users are truly lower value.

**Correct approach:** Collect at least 20-30 conversions per segment before weighting.

---

## Summary

Value Rules are a powerful lever for improving ROAS by aligning Meta's optimization with your business definition of "valuable customer." They work best when you:

1. **Base them on data** - Know which segments actually convert higher value
2. **Use weighting, not exclusion** - Keep all audiences in play, just optimize harder for better ones
3. **Focus on ROI, not cost** - Accept higher cost per result if business value improves
4. **Test systematically** - One dimension at a time, with sufficient data
5. **Be patient** - Give the algorithm 1-2 weeks to learn and optimize

The result: campaigns that deliver higher-quality customers, even if they cost more per conversion.
