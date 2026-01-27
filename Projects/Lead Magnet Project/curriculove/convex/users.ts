import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

// Get or create user from Clerk data
export const getOrCreateUser = mutation({
  args: {
    clerkId: v.string(),
    email: v.string(),
    name: v.optional(v.string()),
    imageUrl: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    // Check if user exists
    const existing = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .first();

    if (existing) {
      // Update user info if changed
      await ctx.db.patch(existing._id, {
        email: args.email,
        name: args.name,
        imageUrl: args.imageUrl,
        updatedAt: Date.now(),
      });
      return existing._id;
    }

    // Create new user
    const userId = await ctx.db.insert("users", {
      clerkId: args.clerkId,
      email: args.email,
      name: args.name,
      imageUrl: args.imageUrl,
      favorites: [],
      reviewCount: 0,
      createdAt: Date.now(),
      updatedAt: Date.now(),
    });

    return userId;
  },
});

// Get user by Clerk ID
export const getUser = query({
  args: { clerkId: v.string() },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .first();
  },
});

// Add a favorite curriculum
export const addFavorite = mutation({
  args: {
    clerkId: v.string(),
    curriculumSlug: v.string(),
  },
  handler: async (ctx, args) => {
    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .first();

    if (!user) return null;

    if (!user.favorites.includes(args.curriculumSlug)) {
      await ctx.db.patch(user._id, {
        favorites: [...user.favorites, args.curriculumSlug],
        updatedAt: Date.now(),
      });
    }

    return user._id;
  },
});

// Remove a favorite
export const removeFavorite = mutation({
  args: {
    clerkId: v.string(),
    curriculumSlug: v.string(),
  },
  handler: async (ctx, args) => {
    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .first();

    if (!user) return null;

    await ctx.db.patch(user._id, {
      favorites: user.favorites.filter((f) => f !== args.curriculumSlug),
      updatedAt: Date.now(),
    });

    return user._id;
  },
});

// Save quiz results
export const saveQuizResults = mutation({
  args: {
    clerkId: v.string(),
    primaryPhilosophy: v.string(),
    secondaryPhilosophies: v.array(v.string()),
  },
  handler: async (ctx, args) => {
    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .first();

    if (!user) return null;

    await ctx.db.patch(user._id, {
      primaryPhilosophy: args.primaryPhilosophy,
      secondaryPhilosophies: args.secondaryPhilosophies,
      updatedAt: Date.now(),
    });

    return user._id;
  },
});

// Get user's reviews
export const getUserReviews = query({
  args: { userId: v.string() },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("reviews")
      .withIndex("by_user", (q) => q.eq("userId", args.userId))
      .order("desc")
      .collect();
  },
});
