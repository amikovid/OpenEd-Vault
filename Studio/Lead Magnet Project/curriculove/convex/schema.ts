import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  reviews: defineTable({
    curriculumSlug: v.string(),
    curriculumName: v.string(),

    // Content
    rawTranscript: v.string(),
    polishedReview: v.string(),
    rating: v.number(),

    // AI-extracted metadata
    highlights: v.array(v.string()),
    concerns: v.array(v.string()),
    bestFor: v.array(v.string()),

    // User info
    userId: v.optional(v.string()),
    userEmail: v.optional(v.string()),
    userName: v.optional(v.string()),

    // Timestamps
    createdAt: v.number(),
  })
    .index("by_curriculum", ["curriculumSlug"])
    .index("by_user", ["userId"])
    .index("by_rating", ["rating"]),

  // User profiles for reviewer stats
  users: defineTable({
    clerkId: v.string(),
    email: v.string(),
    name: v.optional(v.string()),
    imageUrl: v.optional(v.string()),

    // Philosophy quiz results
    primaryPhilosophy: v.optional(v.string()),
    secondaryPhilosophies: v.optional(v.array(v.string())),

    // Favorites
    favorites: v.array(v.string()),

    // Stats
    reviewCount: v.number(),

    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_clerk_id", ["clerkId"])
    .index("by_email", ["email"]),
});
