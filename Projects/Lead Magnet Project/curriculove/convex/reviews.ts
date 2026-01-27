import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

// Submit a new review
export const submitReview = mutation({
  args: {
    curriculumSlug: v.string(),
    curriculumName: v.string(),
    rawTranscript: v.string(),
    polishedReview: v.string(),
    rating: v.number(),
    highlights: v.array(v.string()),
    concerns: v.array(v.string()),
    bestFor: v.array(v.string()),
    userId: v.optional(v.string()),
    userEmail: v.optional(v.string()),
    userName: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const reviewId = await ctx.db.insert("reviews", {
      ...args,
      createdAt: Date.now(),
    });

    // Update user's review count if logged in
    if (args.userId) {
      const user = await ctx.db
        .query("users")
        .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.userId!))
        .first();

      if (user) {
        await ctx.db.patch(user._id, {
          reviewCount: user.reviewCount + 1,
          updatedAt: Date.now(),
        });
      }
    }

    return reviewId;
  },
});

// Get reviews for a specific curriculum
export const getReviewsForCurriculum = query({
  args: { curriculumSlug: v.string() },
  handler: async (ctx, args) => {
    const reviews = await ctx.db
      .query("reviews")
      .withIndex("by_curriculum", (q) => q.eq("curriculumSlug", args.curriculumSlug))
      .order("desc")
      .collect();
    return reviews;
  },
});

// Get all reviews (for admin/display)
export const getAllReviews = query({
  args: {},
  handler: async (ctx) => {
    const reviews = await ctx.db
      .query("reviews")
      .order("desc")
      .take(100);
    return reviews;
  },
});

// Get review count for a curriculum
export const getReviewCount = query({
  args: { curriculumSlug: v.string() },
  handler: async (ctx, args) => {
    const reviews = await ctx.db
      .query("reviews")
      .withIndex("by_curriculum", (q) => q.eq("curriculumSlug", args.curriculumSlug))
      .collect();
    return reviews.length;
  },
});

// Get average rating for a curriculum
export const getAverageRating = query({
  args: { curriculumSlug: v.string() },
  handler: async (ctx, args) => {
    const reviews = await ctx.db
      .query("reviews")
      .withIndex("by_curriculum", (q) => q.eq("curriculumSlug", args.curriculumSlug))
      .collect();

    if (reviews.length === 0) return null;

    const sum = reviews.reduce((acc, r) => acc + r.rating, 0);
    return sum / reviews.length;
  },
});
