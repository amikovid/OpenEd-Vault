import type { Metadata, Viewport } from "next";
import { Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";
import ConvexClientProvider from "@/components/ConvexClientProvider";
import ClerkClientProvider from "@/components/ClerkClientProvider";

const plusJakartaSans = Plus_Jakarta_Sans({
  variable: "--font-jakarta",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
});

export const metadata: Metadata = {
  title: "Curriculove - Find Your Homeschool Style",
  description: "Discover your homeschool philosophy and find curricula that match your values",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0"
        />
        {/* PWA manifest and icons */}
        <link rel="manifest" href="/manifest.json" />
        <link rel="icon" href="/icon-192.svg" type="image/svg+xml" />
        <link rel="apple-touch-icon" href="/icon-192.svg" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
        <meta name="apple-mobile-web-app-title" content="Curriculove" />
        <meta name="theme-color" content="#13ec80" />
      </head>
      <body className={`${plusJakartaSans.variable} antialiased`}>
        <ClerkClientProvider>
        {/* Desktop wrapper - shows branding on larger screens */}
        <div className="min-h-screen bg-[#102219] md:flex md:items-center md:justify-center">
          {/* Left branding panel - hidden on mobile */}
          <div className="hidden lg:flex lg:flex-col lg:items-end lg:justify-center lg:pr-12 lg:w-80">
            <div className="text-right">
              <h1 className="text-4xl font-extrabold text-white mb-2">
                Curricu<span className="text-[#13ec80]">love</span>
              </h1>
              <p className="text-white/60 text-sm mb-6">
                Find your perfect curriculum match
              </p>
              <div className="flex flex-col gap-3 items-end">
                <div className="flex items-center gap-2 text-white/80 text-sm">
                  <span className="material-symbols-outlined text-[#13ec80]">check_circle</span>
                  Personalized philosophy quiz
                </div>
                <div className="flex items-center gap-2 text-white/80 text-sm">
                  <span className="material-symbols-outlined text-[#13ec80]">check_circle</span>
                  AI-powered matching
                </div>
                <div className="flex items-center gap-2 text-white/80 text-sm">
                  <span className="material-symbols-outlined text-[#13ec80]">check_circle</span>
                  Expert curriculum insights
                </div>
              </div>
            </div>
          </div>

          {/* Mobile app container */}
          <div className="w-full max-w-[430px] mx-auto md:shadow-2xl md:rounded-3xl md:my-4 min-h-screen md:min-h-0 md:max-h-[90vh] md:h-[896px] md:overflow-y-auto md:overflow-x-hidden">
            <ConvexClientProvider>
              {children}
            </ConvexClientProvider>
          </div>

          {/* Right branding panel - hidden on mobile */}
          <div className="hidden lg:flex lg:flex-col lg:items-start lg:justify-center lg:pl-12 lg:w-80">
            <div className="text-left">
              <p className="text-white/40 text-xs uppercase tracking-wider mb-4">
                Powered by
              </p>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-full bg-[#13ec80]/20 flex items-center justify-center">
                  <span className="material-symbols-outlined text-[#13ec80]">school</span>
                </div>
                <div>
                  <p className="text-white font-bold">OpenEd</p>
                  <p className="text-white/60 text-xs">Alternative Education Experts</p>
                </div>
              </div>
              <div className="border-t border-white/10 pt-6">
                <p className="text-white/60 text-sm leading-relaxed">
                  Join thousands of homeschool families who've discovered their perfect curriculum match.
                </p>
              </div>
            </div>
          </div>
        </div>
        </ClerkClientProvider>
      </body>
    </html>
  );
}
