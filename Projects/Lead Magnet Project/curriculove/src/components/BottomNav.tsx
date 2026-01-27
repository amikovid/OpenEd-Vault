"use client";

interface BottomNavProps {
  activeTab: "discover" | "saves" | "profile";
  onTabChange: (tab: "discover" | "saves" | "profile") => void;
  savesCount?: number;
}

export default function BottomNav({
  activeTab,
  onTabChange,
  savesCount = 0,
}: BottomNavProps) {
  const tabs = [
    {
      id: "discover" as const,
      icon: "explore",
      label: "Discover",
    },
    {
      id: "saves" as const,
      icon: "favorite",
      label: "Saves",
      badge: savesCount,
    },
    {
      id: "profile" as const,
      icon: "person",
      label: "Profile",
    },
  ];

  return (
    <nav className="bottom-nav">
      <div className="bottom-nav-inner">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`bottom-nav-item ${activeTab === tab.id ? "active" : ""}`}
          >
            <div className="relative">
              <span
                className={`material-symbols-outlined text-2xl ${
                  activeTab === tab.id
                    ? "text-[var(--primary)]"
                    : "text-[var(--foreground-muted)]"
                }`}
              >
                {tab.icon}
              </span>
              {tab.badge && tab.badge > 0 && (
                <span className="absolute -top-1 -right-1 w-4 h-4 bg-[var(--primary)] text-[var(--background-dark)] text-[10px] font-bold rounded-full flex items-center justify-center">
                  {tab.badge > 9 ? "9+" : tab.badge}
                </span>
              )}
            </div>
            <span
              className={`text-xs font-medium ${
                activeTab === tab.id
                  ? "text-[var(--primary)]"
                  : "text-[var(--foreground-muted)]"
              }`}
            >
              {tab.label}
            </span>
          </button>
        ))}
      </div>
    </nav>
  );
}
