"use client";

import { useState } from "react";
import BrowseRecommendations from "@/components/BrowseRecommendations";

export default function BrowsePage() {
  const [favorites, setFavorites] = useState<string[]>([]);

  const handleAddFavorite = (slug: string) => {
    setFavorites((prev) =>
      prev.includes(slug) ? prev : [...prev, slug]
    );
  };

  return (
    <BrowseRecommendations
      onAddFavorite={handleAddFavorite}
      favorites={favorites}
    />
  );
}
