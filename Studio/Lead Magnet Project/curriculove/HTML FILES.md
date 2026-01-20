<!-- Curriculum Discovery Swipe -->
<!DOCTYPE html>

<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Curriculove - Discovery Swipe</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        "primary": "#13ec80",
                        "background-light": "#f6f8f7",
                        "background-dark": "#102219",
                    },
                    fontFamily: {
                        "display": ["Plus Jakarta Sans"]
                    },
                    borderRadius: {"DEFAULT": "1rem", "lg": "2rem", "xl": "3rem", "full": "9999px"},
                },
            },
        }
    </script>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .fill-icon {
            font-variation-settings: 'FILL' 1;
        }
    </style>
<style>
    body {
      min-height: max(884px, 100dvh);
    }
  </style>
  </head>
<body class="bg-background-light dark:bg-background-dark font-display text-[#111814] dark:text-white min-h-screen flex flex-col">
<!-- Top Navigation -->
<header class="flex items-center bg-background-light dark:bg-background-dark p-4 pb-2 justify-between sticky top-0 z-50">
<div class="text-[#111814] dark:text-white flex size-12 shrink-0 items-center justify-center cursor-pointer" data-icon="menu">
<span class="material-symbols-outlined text-2xl">menu</span>
</div>
<h2 class="text-[#111814] dark:text-white text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pr-12">Curriculove</h2>
</header>
<!-- Progress Indicator -->
<div class="px-6 py-2">
<div class="flex flex-col gap-2">
<div class="flex justify-between items-center">
<p class="text-[#111814] dark:text-white text-sm font-medium leading-normal">Daily Discovery</p>
<p class="text-[#618975] dark:text-primary text-xs font-semibold leading-normal">1 of 12 matches</p>
</div>
<div class="h-1.5 w-full bg-[#dbe6e0] dark:bg-gray-700 rounded-full overflow-hidden">
<div class="h-full bg-primary rounded-full transition-all duration-500" style="width: 8%;"></div>
</div>
</div>
</div>
<!-- Discovery Card Stack Area -->
<main class="flex-1 flex flex-col items-center justify-center p-4 relative overflow-hidden">
<!-- Main Swiping Card -->
<div class="w-full max-w-md bg-white dark:bg-zinc-900 rounded-xl shadow-xl overflow-hidden flex flex-col border border-gray-100 dark:border-zinc-800">
<!-- Hero Image Section -->
<div class="relative w-full aspect-[4/5] bg-center bg-no-repeat bg-cover" data-alt="A beautiful flat-lay of nature-based homeschooling materials and books" style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuAPen01MHb_G58V0loUlEDtbtuETspJ2vc5b7Ld2Qc-UI0wlEMMb3_rURC6f34fzD9aiY9Pc4LcEmIjMbsj60ThgcIS1S5mEpw-pur1yfS_1RTsgkSlCGhnTkXKWBZlG2Ky8Pft8rP8qucXL2OIRHGNjXEtYl2UW2spG9tQBltua_qoy7pGybiwyFTCGZDTgkfcIw7etaE29wbR42C-Cd5cByWOJMZrqGgpQ7skK72ByyuDygMu4WVQT80lLLKDudjwvBfDuO0QTSyH");'>
<!-- Match Badge -->
<div class="absolute top-4 right-4 bg-primary text-background-dark px-3 py-1.5 rounded-full font-bold text-sm shadow-lg flex items-center gap-1">
<span class="material-symbols-outlined text-sm fill-icon">bolt</span>
                    94% Match
                </div>
<!-- Gradient Overlay for text readability at bottom of image -->
<div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
<!-- Title and Tagline on Image -->
<div class="absolute bottom-4 left-4 right-4 text-white">
<h1 class="text-3xl font-bold leading-tight">Blossom &amp; Root</h1>
<p class="text-white/90 text-sm font-medium italic">A creative, nature-based secular curriculum for wonder-led families.</p>
</div>
</div>
<!-- Content Details -->
<div class="p-5 flex flex-col gap-4">
<!-- Chips -->
<div class="flex gap-2 flex-wrap">
<div class="flex h-7 shrink-0 items-center justify-center gap-x-1 rounded-full bg-primary/20 dark:bg-primary/10 px-3 border border-primary/20">
<span class="material-symbols-outlined text-[14px] text-[#111814] dark:text-primary">payments</span>
<p class="text-[#111814] dark:text-primary text-xs font-bold leading-normal">$$</p>
</div>
<div class="flex h-7 shrink-0 items-center justify-center gap-x-1 rounded-full bg-gray-100 dark:bg-zinc-800 px-3 border border-gray-200 dark:border-zinc-700">
<span class="material-symbols-outlined text-[14px] text-gray-600 dark:text-gray-400">school</span>
<p class="text-gray-700 dark:text-gray-300 text-xs font-bold leading-normal">PreK - 5th</p>
</div>
<div class="flex h-7 shrink-0 items-center justify-center gap-x-1 rounded-full bg-gray-100 dark:bg-zinc-800 px-3 border border-gray-200 dark:border-zinc-700">
<span class="material-symbols-outlined text-[14px] text-gray-600 dark:text-gray-400">psychology</span>
<p class="text-gray-700 dark:text-gray-300 text-xs font-bold leading-normal">CM, Nature-Based</p>
</div>
</div>
<!-- Why it matches Section -->
<div class="flex flex-col gap-1.5">
<h3 class="text-primary text-xs font-bold uppercase tracking-wider">Why it matches you</h3>
<p class="text-[#618975] dark:text-gray-400 text-sm leading-relaxed">
                        Based on your preference for <span class="text-[#111814] dark:text-white font-semibold">nature-based learning</span> and the <span class="text-[#111814] dark:text-white font-semibold">Charlotte Mason philosophy</span>, this curriculum offers the flexible structure you love.
                    </p>
</div>
<!-- OpenEd Says Editorial Box -->
<div class="flex flex-col items-start justify-between gap-3 rounded-lg border border-[#dbe6e0] dark:border-zinc-700 bg-background-light dark:bg-background-dark p-4">
<div class="flex flex-col gap-1">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-primary text-xl">verified</span>
<p class="text-[#111814] dark:text-white text-sm font-bold leading-tight">OpenEd Expert Insight</p>
</div>
<p class="text-[#618975] dark:text-gray-400 text-xs leading-normal">
                            This curriculum excels at integrating arts with core sciences, perfect for creative learners who thrive outdoors.
                        </p>
</div>
<a class="text-xs font-bold leading-normal tracking-[0.015em] flex items-center gap-1 text-primary hover:underline" href="#">
                        Full Review
                        <span class="material-symbols-outlined text-sm">arrow_forward</span>
</a>
</div>
</div>
</div>
</main>
<!-- Floating Action Buttons -->
<footer class="p-8 pb-12">
<div class="flex items-center justify-center gap-8">
<!-- Pass Button -->
<button class="w-16 h-16 rounded-full bg-white dark:bg-zinc-800 shadow-xl flex items-center justify-center border-4 border-red-50 text-red-500 hover:scale-110 active:scale-95 transition-all">
<span class="material-symbols-outlined text-3xl font-bold">close</span>
</button>
<!-- Save Button -->
<button class="w-20 h-20 rounded-full bg-primary shadow-xl flex items-center justify-center text-background-dark hover:scale-110 active:scale-95 transition-all">
<span class="material-symbols-outlined text-4xl fill-icon">favorite</span>
</button>
<!-- Info Button -->
<button class="w-16 h-16 rounded-full bg-white dark:bg-zinc-800 shadow-xl flex items-center justify-center border-4 border-blue-50 text-blue-500 hover:scale-110 active:scale-95 transition-all">
<span class="material-symbols-outlined text-3xl font-bold">info</span>
</button>
</div>
</footer>
</body></html>

<!-- Curriculum Full Details -->
<!DOCTYPE html>

<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Curriculum Full Details</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        "primary": "#13ec80",
                        "background-light": "#f6f8f7",
                        "background-dark": "#102219",
                    },
                    fontFamily: {
                        "display": ["Plus Jakarta Sans", "sans-serif"]
                    },
                    borderRadius: {"DEFAULT": "1rem", "lg": "2rem", "xl": "3rem", "full": "9999px"},
                },
            },
        }
    </script>
<style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; }
        .hide-scrollbar::-webkit-scrollbar { display: none; }
        .hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    </style>
<style>
    body {
      min-height: max(884px, 100dvh);
    }
  </style>
  </head>
<body class="bg-background-light dark:bg-background-dark text-[#111814] dark:text-white antialiased">
<div class="relative flex h-auto min-h-screen w-full flex-col group/design-root overflow-x-hidden">
<!-- TopAppBar -->
<header class="sticky top-0 z-50 flex items-center bg-white/80 dark:bg-background-dark/80 backdrop-blur-md p-4 justify-between border-b border-gray-100 dark:border-gray-800">
<button aria-label="Go back" class="text-[#111814] dark:text-white flex size-10 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800">
<span class="material-symbols-outlined">arrow_back</span>
</button>
<h2 class="text-[#111814] dark:text-white text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center">Curriculum Details</h2>
<div class="flex items-center justify-end">
<div class="bg-primary/20 px-3 py-1 rounded-full">
<p class="text-[#07882c] dark:text-primary text-sm font-bold leading-normal tracking-[0.015em] shrink-0">98% Match</p>
</div>
</div>
</header>
<main class="flex-1 pb-24">
<!-- HeaderImage -->
<div class="@container">
<div class="@[480px]:px-4 @[480px]:py-3">
<div class="w-full bg-center bg-no-repeat bg-cover flex flex-col justify-end overflow-hidden bg-white @[480px]:rounded-xl min-h-96 relative" data-alt="Modern homeschooling books and materials on a bright desk" style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuAwURoKK_WinfryLDMvzeBQN_l8x2uHFZTkCohG7tj453MSoHbbx5rzW4tE2T486Hc4mQSD_jvov4eQzmIvlpdGDYG8adZEohovc5cSBhkT7EG1DI4l9Wsc-Vco7EpUvwShbIFVXcV-WJrissg5fWBv6Iu8E6kL8V1anyCNW1g7t9_doCh1IblcmaFFpF_-sH1mckJ5y6e9GAmZorsYntr8OrCRjq_HbAubH-K5Ln53AMn99o9_02oJ8BGEbbYP-XiX2LxF5r-P4y7f");'>
<div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
<div class="relative p-6">
<!-- HeadlineText integrated into Hero -->
<h1 class="text-white tracking-light text-[32px] font-extrabold leading-tight">The Good and the Beautiful: Language Arts</h1>
<div class="flex gap-2 mt-2">
<span class="bg-white/20 backdrop-blur-sm text-white px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider">Grades K-8</span>
<span class="bg-white/20 backdrop-blur-sm text-white px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider">Literacy</span>
</div>
</div>
</div>
</div>
</div>
<!-- Stats / Quick Info -->
<div class="flex flex-wrap gap-4 p-4">
<div class="flex min-w-[158px] flex-1 flex-col gap-2 rounded-xl p-6 bg-white dark:bg-gray-800 shadow-sm border border-gray-100 dark:border-gray-700">
<p class="text-[#618975] dark:text-gray-400 text-sm font-medium leading-normal uppercase tracking-wider">Personal Match</p>
<div class="flex items-end gap-2">
<p class="text-[#111814] dark:text-white tracking-light text-3xl font-bold leading-tight">98%</p>
<p class="text-primary text-base font-bold leading-normal mb-1">+5% vs last week</p>
</div>
<p class="text-xs text-gray-500 dark:text-gray-400">Perfect for visual and kinesthetic learners like your children.</p>
</div>
</div>
<!-- SectionHeader: About -->
<div class="px-4">
<h2 class="text-[#111814] dark:text-white text-[22px] font-bold leading-tight tracking-[-0.015em] pb-3 pt-5">About this Curriculum</h2>
<div class="text-[#4f735d] dark:text-gray-300 text-base leading-relaxed space-y-4">
<p>
                        The Good and the Beautiful Language Arts is a comprehensive, open-and-go curriculum that focuses on high character and beautiful literature. It combines reading, writing, spelling, grammar, and art appreciation into a cohesive daily lesson.
                    </p>
<p>
                        Our unique approach eliminates the need for multiple separate programs by integrating all core language arts components. Each level is designed to be visually stunning, using fine art and nature photography to engage the child's imagination while building rigorous academic skills.
                    </p>
</div>
</div>
<!-- Pricing Details -->
<div class="px-4 pt-8">
<div class="bg-primary/5 dark:bg-primary/10 rounded-xl p-6 border border-primary/20">
<h3 class="text-[#111814] dark:text-white text-lg font-bold mb-4 flex items-center gap-2">
<span class="material-symbols-outlined text-primary">payments</span>
                        Pricing &amp; Options
                    </h3>
<div class="space-y-3">
<div class="flex justify-between items-center pb-2 border-b border-primary/10">
<span class="text-gray-600 dark:text-gray-400">Digital PDF Course (Full)</span>
<span class="font-bold text-[#111814] dark:text-white">FREE</span>
</div>
<div class="flex justify-between items-center pb-2 border-b border-primary/10">
<span class="text-gray-600 dark:text-gray-400">Physical Printed Set</span>
<span class="font-bold text-[#111814] dark:text-white">$120.98</span>
</div>
<div class="flex justify-between items-center">
<span class="text-gray-600 dark:text-gray-400">Teacher's Guide Only</span>
<span class="font-bold text-[#111814] dark:text-white">$45.00</span>
</div>
</div>
</div>
</div>
<!-- Recommendations Carousel -->
<div class="pt-8">
<h2 class="text-[#111814] dark:text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-4">Families like you also liked...</h2>
<div class="flex overflow-x-auto gap-4 px-4 pb-6 hide-scrollbar">
<!-- Carousel Item 1 -->
<div class="min-w-[200px] w-48 flex flex-col gap-3 group">
<div class="aspect-[4/5] w-full rounded-xl bg-cover bg-center shadow-md relative" data-alt="Children's nature study journal cover" style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuDVAcw_uw2Y6lh3SUpbX1L4WxFWO-LOTy5waksN67YrPz49HzxQD4KDX-natSQczDXoT3wtTQ6zfu1K6bFjkYp2hQAJ5OGv7tQiffOKpb_GoUOm6YllPuBVwLirFdT23KWjSysZDwhkJx6qJmUo4L_bWJu0Z6VAJ_fb8_DwL3QxHKrAziY5evos59MdF3Y2HdaEzfdrmlQWbxcWWRPOP8J4GyrvX-ZIcWtadJtAbYjoPcQfxKPWynyK6aHpADZMHuOQXFLB_QuInris");'>
<div class="absolute top-2 right-2 bg-primary px-2 py-0.5 rounded-full shadow-sm">
<span class="text-[10px] font-black text-white">95%</span>
</div>
</div>
<div>
<p class="font-bold text-sm line-clamp-1">Wildwood Nature</p>
<p class="text-xs text-gray-500">Science • Grade 1-5</p>
</div>
</div>
<!-- Carousel Item 2 -->
<div class="min-w-[200px] w-48 flex flex-col gap-3 group">
<div class="aspect-[4/5] w-full rounded-xl bg-cover bg-center shadow-md relative" data-alt="Colorful math manipulatives and blocks" style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuCXKl8p9bMDkfw4G0pT0UsawQCs-gvx-d0MZo3vUungrDeGXT00Zd1oN_ak3Rymj32t4b_XkswcffsjPeEOQyV1XbbKfVvF9MKb1BlQUXUaNnYN9so7dTxZjUT6NT-1z8Ur10AMHLOO2nQ92Cla2dK9TxNzeOAtT6hl9iQ9KF7LGWlwOjD0q8DED7StwMbSl2mQWfz_sF63sIMmqxYJzYwnyP6FCClM6B4uljrOUBhFvXG-prXL6Y3wtwmRRQsu5MERoriGdC1GswN2");'>
<div class="absolute top-2 right-2 bg-primary px-2 py-0.5 rounded-full shadow-sm">
<span class="text-[10px] font-black text-white">92%</span>
</div>
</div>
<div>
<p class="font-bold text-sm line-clamp-1">Simply Good Math</p>
<p class="text-xs text-gray-500">Math • Grade K-6</p>
</div>
</div>
<!-- Carousel Item 3 -->
<div class="min-w-[200px] w-48 flex flex-col gap-3 group">
<div class="aspect-[4/5] w-full rounded-xl bg-cover bg-center shadow-md relative" data-alt="Art history book and painting supplies" style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuAx0UVieH26Nuehf1iDC-nJkAljdN1nsI6qMuYLLI1hEPr7X5qhh_Oye-zjf3KIE0dpmBOsILch1i0zQ75tEBePScC9CkgZQg9Hipv_EtiLeggSqHUTjk3c1Rf9cQg319Dkf5nV9-UGft-Tz3cWpeR_gKqowU_G97fHMH-FV_YRcRbpciagX-xrhYwsDT-nkL99HHpxoLMAVYo98eWRN99zhv6PzSEZmw3kE2bsKTXhyyi0RDSa9SwniyawjrOmTaxeSX4ZFXga4W84");'>
<div class="absolute top-2 right-2 bg-primary px-2 py-0.5 rounded-full shadow-sm">
<span class="text-[10px] font-black text-white">88%</span>
</div>
</div>
<div>
<p class="font-bold text-sm line-clamp-1">Masterpiece Society</p>
<p class="text-xs text-gray-500">Art • All Ages</p>
</div>
</div>
</div>
</div>
</main>
<!-- Fixed Bottom CTA -->
<div class="fixed bottom-0 left-0 right-0 p-4 bg-white/80 dark:bg-background-dark/80 backdrop-blur-xl border-t border-gray-100 dark:border-gray-800 z-50">
<a class="flex items-center justify-center gap-2 bg-primary hover:bg-primary/90 text-white font-bold py-4 px-8 rounded-full shadow-lg shadow-primary/20 transition-all active:scale-95" href="#">
<span class="material-symbols-outlined">open_in_new</span>
                Visit Website
            </a>
</div>
</div>
</body></html>

<!-- Discovery Session Complete -->
<!DOCTYPE html>

<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Discovery Session Complete - Curriculove</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            colors: {
              "primary": "#13ec80",
              "background-light": "#f6f8f7",
              "background-dark": "#102219",
            },
            fontFamily: {
              "display": ["Plus Jakarta Sans", "sans-serif"]
            },
            borderRadius: {"DEFAULT": "1rem", "lg": "2rem", "xl": "3rem", "full": "9999px"},
          },
        },
      }
    </script>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .material-symbols-fill {
            font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
    </style>
<style>
    body {
      min-height: max(884px, 100dvh);
    }
  </style>
  </head>
<body class="bg-background-light dark:bg-background-dark font-display text-[#111814] dark:text-white transition-colors duration-300">
<div class="relative flex h-auto min-h-screen w-full flex-col group/design-root overflow-x-hidden max-w-[430px] mx-auto shadow-2xl bg-white dark:bg-background-dark">
<!-- Top Navigation -->
<div class="flex items-center p-4 pb-2 justify-between sticky top-0 bg-white/80 dark:bg-background-dark/80 backdrop-blur-md z-10">
<div class="text-[#111814] dark:text-white flex size-12 shrink-0 items-center justify-start">
<span class="material-symbols-outlined cursor-pointer">close</span>
</div>
<h2 class="text-[#111814] dark:text-white text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pr-12">Discovery Complete</h2>
</div>
<!-- Main Content Area -->
<div class="flex flex-col px-6 pt-8 pb-4 flex-grow">
<!-- Empty State / Celebratory Illustration -->
<div class="flex flex-col items-center gap-8">
<div class="relative w-full aspect-square max-w-[280px] flex items-center justify-center">
<!-- Abstract Decorative Background -->
<div class="absolute inset-0 bg-primary/10 dark:bg-primary/5 rounded-full blur-3xl"></div>
<!-- Main Illustration Component -->
<div class="relative w-full h-full rounded-xl bg-center bg-no-repeat bg-cover shadow-lg ring-4 ring-white dark:ring-[#1a3326]" data-alt="A joyful student celebrating learning achievements" style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuAL6jm1KBADWXA0DZBTvtw49MUlLBwc3pUCQcODKXHKezVFhsyzmXVb1UHAead9eq_gotCDlh8CS1zTQzw2v1VI6001sqQHKq-Tevl8RbIDtOCILESdf1PzXRLmTfwfgdtCQC3KYEgMp50cDFzY_jJBFssPq5gD1U9X9wcwde9jeccROKoukBOrWU8bUwjRvtaxJcb-B1A-lXPY__6BiS_bktruLuO8EjHggTI9wn-Ta9sXQQKbgpqZmeHcBFhh_7OKOXZUo5cslv2e");'>
</div>
<div class="absolute -bottom-4 -right-4 bg-primary p-3 rounded-full shadow-xl">
<span class="material-symbols-outlined text-white text-3xl material-symbols-fill">auto_awesome</span>
</div>
</div>
<div class="flex max-w-[480px] flex-col items-center gap-3">
<h1 class="text-[#111814] dark:text-white text-2xl font-extrabold leading-tight tracking-tight text-center">
                        You've seen all 12 matches!
                    </h1>
<p class="text-[#618975] dark:text-gray-400 text-base font-medium leading-normal max-w-[480px] text-center">
                        Great work! You've successfully swiped through your personalized curriculum recommendations for this session.
                    </p>
</div>
</div>
<!-- Summary Card -->
<div class="mt-10">
<div class="flex items-center justify-between gap-4 p-5 rounded-xl bg-primary/10 dark:bg-primary/5 border border-primary/20">
<div class="flex flex-col gap-1 flex-[2_2_0px]">
<p class="text-[#111814] dark:text-white text-lg font-bold leading-tight flex items-center gap-2">
<span class="material-symbols-outlined text-primary material-symbols-fill">favorite</span>
                            Saved: 5 curricula
                        </p>
<p class="text-[#618975] dark:text-gray-400 text-sm font-normal leading-normal">
                            These are waiting for you in your library to explore further.
                        </p>
</div>
<div class="w-20 h-20 bg-center bg-no-repeat bg-cover rounded-xl shadow-sm border-2 border-white dark:border-gray-800" data-alt="Collection of colorful books and educational materials" style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuCTXmSLSK9jadXGlzUEev67vkvntfqxGFHaUeySKmxVwtowFKHa5seU-0aMLWSfL0k6trUx7bEbF_Y1KQpRGHFv_NCX6wXCmNUl1FRzj3lhq2ITn94E1NrzEkDb0nzHm1wl6et8wl6JZHOXGOk_relk7M260QQLuNFX0KS1itHr0Wt_E71u9kZ2OhBE9l5XXE2g6HbhuQbIbDRiMBXGaI6LFsr3alZgm-rbhNuzqgBikNYzA_RUtMTyh3EFqMuLE3vCEkhPjbUSm6CM");'>
</div>
</div>
</div>
</div>
<!-- Action Buttons -->
<div class="px-6 py-6 mt-auto">
<div class="flex flex-col gap-3 w-full max-w-[480px] mx-auto">
<button class="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-14 px-5 bg-primary text-[#111814] text-base font-bold leading-normal tracking-[0.015em] w-full shadow-lg shadow-primary/20 hover:opacity-90 active:scale-95 transition-all">
<span class="truncate">View My Saves</span>
</button>
<button class="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-14 px-5 bg-transparent border-2 border-[#f0f4f2] dark:border-gray-700 text-[#111814] dark:text-white text-base font-bold leading-normal tracking-[0.015em] w-full hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
<span class="truncate">Retake Quiz</span>
</button>
</div>
</div>
<!-- Bottom Navigation Bar -->
<div class="flex gap-2 border-t border-[#f0f4f2] dark:border-gray-800 bg-white/90 dark:bg-background-dark/90 backdrop-blur-md px-4 pb-8 pt-3">
<a class="flex flex-1 flex-col items-center justify-end gap-1 rounded-full text-primary" href="#">
<div class="flex h-8 items-center justify-center">
<span class="material-symbols-outlined text-3xl material-symbols-fill">colors_spark</span>
</div>
<p class="text-xs font-bold leading-normal tracking-[0.015em]">Discover</p>
</a>
<a class="flex flex-1 flex-col items-center justify-end gap-1 text-[#618975] dark:text-gray-400" href="#">
<div class="flex h-8 items-center justify-center">
<span class="material-symbols-outlined text-3xl">favorite</span>
</div>
<p class="text-xs font-medium leading-normal tracking-[0.015em]">Saves</p>
</a>
<a class="flex flex-1 flex-col items-center justify-end gap-1 text-[#618975] dark:text-gray-400" href="#">
<div class="flex h-8 items-center justify-center">
<span class="material-symbols-outlined text-3xl">account_circle</span>
</div>
<p class="text-xs font-medium leading-normal tracking-[0.015em]">Profile</p>
</a>
</div>
</div>
</body></html>

<!-- My Saved Curricula -->
<!DOCTYPE html>

<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Curriculove - My Saved Curricula</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        "primary": "#13ec80",
                        "background-light": "#f6f8f7",
                        "background-dark": "#102219",
                    },
                    fontFamily: {
                        "display": ["Plus Jakarta Sans", "sans-serif"]
                    },
                    borderRadius: {"DEFAULT": "1rem", "lg": "2rem", "xl": "3rem", "full": "9999px"},
                },
            },
        }
    </script>
<style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .ios-blur {
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
    </style>
<style>
    body {
      min-height: max(884px, 100dvh);
    }
  </style>
  </head>
<body class="bg-background-light dark:bg-background-dark min-h-screen text-[#111814] dark:text-white">
<div class="relative mx-auto flex h-auto min-h-screen w-full max-w-[430px] flex-col overflow-x-hidden shadow-2xl bg-white dark:bg-background-dark">
<!-- Top Navigation Bar -->
<header class="sticky top-0 z-50 bg-white/80 dark:bg-background-dark/80 ios-blur px-4 pt-6 pb-2">
<div class="flex items-center justify-between">
<div class="flex size-10 items-center justify-center rounded-full bg-background-light dark:bg-white/10">
<span class="material-symbols-outlined text-2xl">person</span>
</div>
<h1 class="text-xl font-bold tracking-tight">My Saved Curricula</h1>
<div class="flex size-10 items-center justify-center">
<button class="relative">
<span class="material-symbols-outlined text-2xl">notifications</span>
<span class="absolute top-0 right-0 h-2 w-2 rounded-full bg-primary border-2 border-white dark:border-background-dark"></span>
</button>
</div>
</div>
</header>
<!-- Search Section -->
<section class="px-4 py-4">
<div class="relative flex items-center">
<div class="absolute left-4 text-slate-400">
<span class="material-symbols-outlined">search</span>
</div>
<input class="w-full h-12 rounded-xl bg-background-light dark:bg-white/5 border-none pl-12 pr-4 text-base focus:ring-2 focus:ring-primary/50 transition-all placeholder:text-slate-400" placeholder="Search saved curricula" type="text"/>
</div>
</section>
<!-- Filter Chips -->
<section class="px-4 pb-4">
<div class="flex gap-2 overflow-x-auto no-scrollbar">
<button class="flex items-center gap-1.5 px-4 py-2 rounded-full bg-primary text-black font-semibold text-sm whitespace-nowrap">
<span>Price</span>
<span class="material-symbols-outlined text-sm">keyboard_arrow_down</span>
</button>
<button class="flex items-center gap-1.5 px-4 py-2 rounded-full bg-background-light dark:bg-white/10 text-sm font-medium whitespace-nowrap">
<span>Grade</span>
<span class="material-symbols-outlined text-sm">keyboard_arrow_down</span>
</button>
<button class="flex items-center gap-1.5 px-4 py-2 rounded-full bg-background-light dark:bg-white/10 text-sm font-medium whitespace-nowrap">
<span>Philosophy</span>
<span class="material-symbols-outlined text-sm">keyboard_arrow_down</span>
</button>
<button class="flex items-center gap-1.5 px-4 py-2 rounded-full bg-background-light dark:bg-white/10 text-sm font-medium whitespace-nowrap">
<span class="material-symbols-outlined text-sm">tune</span>
<span>More</span>
</button>
</div>
</section>
<!-- List Content -->
<main class="flex-1 px-4 space-y-3 pb-24">
<!-- Item 1 -->
<div class="flex items-center gap-4 bg-white dark:bg-white/5 p-3 rounded-2xl border border-slate-100 dark:border-white/10 shadow-sm transition-transform active:scale-[0.98]">
<div class="relative shrink-0">
<div class="size-20 rounded-xl bg-cover bg-center" data-alt="Cover of a colorful elementary math textbook" style="background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuDAXqIrOsxnU984tZrfwusDR8xWbgsPFFt3_9IEZjTSkgfxw_9n0DFtBcX1C0arv-P6ntUXA4DKxMdoMDGaJ7iKrxbG5-ChRqRyLTKXtUFlZSM1EGswhcylKWgf2K81xDZxGypWOkOZoUJSmvPgjFOBzlnm9dunPej9tt9STTok5NuVnddgMkWI9WXQd0QYNxS5xwmBthLovE04KvPN5p_09B_mvUrDMwCBKBtfPSJMcFx5KTxyLaS91ksfZ3LB2Iw2GVaklk5LMFyP');"></div>
<div class="absolute -top-1 -left-1 flex size-7 items-center justify-center rounded-full bg-primary text-[10px] font-bold text-black border-2 border-white dark:border-background-dark">
                        98%
                    </div>
</div>
<div class="flex-1 min-w-0">
<h3 class="text-base font-bold truncate">The Good and the Beautiful - Math 1</h3>
<div class="flex items-center gap-2 mt-0.5">
<span class="text-xs font-medium px-2 py-0.5 rounded-full bg-primary/20 text-primary-dark">Reviewed</span>
<span class="text-xs text-slate-500 dark:text-slate-400">Grade 1 • Charlotte Mason</span>
</div>
</div>
<button class="shrink-0 text-slate-300">
<span class="material-symbols-outlined">chevron_right</span>
</button>
</div>
<!-- Item 2 -->
<div class="flex items-center gap-4 bg-white dark:bg-white/5 p-3 rounded-2xl border border-slate-100 dark:border-white/10 shadow-sm transition-transform active:scale-[0.98]">
<div class="relative shrink-0">
<div class="size-20 rounded-xl bg-cover bg-center" data-alt="Nature study science curriculum with forest illustrations" style="background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuD30J0JrUaphjGkdk5oXMr2F75NayPiD0rkPP6zRDR420yTUx47ukDCWfFJ539sFH3tSKMIcJ5x0_pDNLvSg_qLWat29jUWKirJ2ck3Whz-jTbF1AO0hHr-JVF9lSMkkDdIsN3cxcE6fEOA_Sv0-1NgLhbz4unyRwq82PZsd9IR7u9TQ8oRyenCcuhpwNzgTHiRfmAEM_MptByi_z-UJY0qbVcmol7OPovh37CdDqmLhKtB11kxfjOnMmZJf4fd8M_-JXTx0Om4uDN_');"></div>
<div class="absolute -top-1 -left-1 flex size-7 items-center justify-center rounded-full bg-primary text-[10px] font-bold text-black border-2 border-white dark:border-background-dark">
                        94%
                    </div>
</div>
<div class="flex-1 min-w-0">
<h3 class="text-base font-bold truncate">Blossom &amp; Root - Science</h3>
<div class="flex items-center gap-2 mt-0.5">
<span class="text-xs text-slate-500 dark:text-slate-400">Grade 2 • Secular • Nature-based</span>
</div>
</div>
<button class="shrink-0 text-slate-300">
<span class="material-symbols-outlined">chevron_right</span>
</button>
</div>
<!-- Item 3 -->
<div class="flex items-center gap-4 bg-white dark:bg-white/5 p-3 rounded-2xl border border-slate-100 dark:border-white/10 shadow-sm transition-transform active:scale-[0.98]">
<div class="relative shrink-0">
<div class="size-20 rounded-xl bg-cover bg-center" data-alt="Comic book style math curriculum with monsters" style="background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuCoaKfAridsNrjE3t8McWWmWwZTlXBBW7TmQYQCwoA4l0onOkdLnLUxHGNaCkTDRMkq63RmO_o5Jb56ImwSXsWN2wu2sNpq8IIJ2ULxH24YynI5WQma4grUS8kLuPKErRbWS4_CL4DFwGUxg_i2V3wDANlfgyekCLM9KF-NNx5viZRCGaHjmlVG2WJu7XesrCYUtRj80DgL6Nb7Ka3Q2dWDFbO_mkiWgvNSCKP7VU5JG7bjH02D3KTpmxA7OS5NqbPDlaVlHGoJCm_9');"></div>
<div class="absolute -top-1 -left-1 flex size-7 items-center justify-center rounded-full bg-primary text-[10px] font-bold text-black border-2 border-white dark:border-background-dark">
                        89%
                    </div>
</div>
<div class="flex-1 min-w-0">
<h3 class="text-base font-bold truncate">Beast Academy</h3>
<div class="flex items-center gap-2 mt-0.5">
<span class="text-xs text-slate-500 dark:text-slate-400">Level 3 • Mastery • Secular</span>
</div>
</div>
<button class="shrink-0 text-slate-300">
<span class="material-symbols-outlined">chevron_right</span>
</button>
</div>
<!-- Item 4 -->
<div class="flex items-center gap-4 bg-white dark:bg-white/5 p-3 rounded-2xl border border-slate-100 dark:border-white/10 shadow-sm transition-transform active:scale-[0.98]">
<div class="relative shrink-0">
<div class="size-20 rounded-xl bg-cover bg-center" data-alt="Classic literature and handwriting course" style="background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuCw5HFmzdzAczDb6i5jlTPV2sThAypItpAHxTIW8qWX4nsWFYzAf5EtrL4rDOah0HufsT6ujGntmo01Cju6tqDLcsiVHzWxzzdj-MZ06z7bsTtL3PjSTHtksVXExgTPQHBuojhtxxTUtc41fyj8A38LG_7-_yn37t-36hmC9q3Tt64x4jslYTUW-lzetH7SkbhMNRBDsrZ3xwdyKeP-aO_hgAc2z4lSojIKrgl2u2VMklJi-35xhndqUtuWD4xX4tOAyGWtIxmzudjL');"></div>
<div class="absolute -top-1 -left-1 flex size-7 items-center justify-center rounded-full bg-primary text-[10px] font-bold text-black border-2 border-white dark:border-background-dark">
                        82%
                    </div>
</div>
<div class="flex-1 min-w-0">
<h3 class="text-base font-bold truncate">Logos Latin I</h3>
<div class="flex items-center gap-2 mt-0.5">
<span class="text-xs font-medium px-2 py-0.5 rounded-full bg-primary/20 text-primary-dark">Reviewed</span>
<span class="text-xs text-slate-500 dark:text-slate-400">Classical • Language</span>
</div>
</div>
<button class="shrink-0 text-slate-300">
<span class="material-symbols-outlined">chevron_right</span>
</button>
</div>
<!-- Keep Swiping Prompt -->
<div class="py-8 text-center">
<p class="text-sm text-slate-400 mb-4 font-display">Looking for more inspiration?</p>
<button class="w-full py-4 rounded-2xl bg-primary text-black font-bold flex items-center justify-center gap-2 shadow-lg shadow-primary/20">
<span class="material-symbols-outlined">swipe</span>
                    Keep Swiping
                </button>
</div>
</main>
<!-- Bottom Navigation Bar (iOS Style) -->
<nav class="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-[430px] bg-white/90 dark:bg-background-dark/90 ios-blur border-t border-slate-100 dark:border-white/10 px-6 pt-3 pb-8 flex justify-between items-center">
<button class="flex flex-col items-center gap-1 text-slate-400">
<span class="material-symbols-outlined">explore</span>
<span class="text-[10px] font-bold">Discover</span>
</button>
<button class="flex flex-col items-center gap-1 text-primary">
<span class="material-symbols-outlined fill-[1]">favorite</span>
<span class="text-[10px] font-bold">Saves</span>
</button>
<button class="flex flex-col items-center gap-1 text-slate-400">
<span class="material-symbols-outlined">chat_bubble</span>
<span class="text-[10px] font-bold">Community</span>
</button>
<button class="flex flex-col items-center gap-1 text-slate-400">
<span class="material-symbols-outlined">settings</span>
<span class="text-[10px] font-bold">Settings</span>
</button>
</nav>
</div>
</body></html>
<!-- Curriculum Full Details -->
<!DOCTYPE html>
<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Curriculum Full Details</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;0,700;1,400&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        "primary": "#d4a373",
                        "sage": "#8d99ae",
                        "rose": "#e5989b",
                        "warm-gray": "#FAF9F6",
                        "background-light": "#fdfcfb",
                    },
                    fontFamily: {
                        "display": ["Crimson Pro", "serif"],
                        "sans": ["Plus Jakarta Sans", "sans-serif"]
                    },
                    borderRadius: {
                        "DEFAULT": "1.25rem",
                        "lg": "2.5rem",
                        "xl": "3.5rem",
                        "full": "9999px"
                    },
                },
            },
        }
    </script>
<style type="text/tailwindcss">
        @layer base {
            body { 
                @apply bg-background-light font-sans text-[#4a4a4a] antialiased;
            }
            h1, h2, h3 {
                @apply font-display;
            }
        }
        .hide-scrollbar::-webkit-scrollbar { display: none; }
        .hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
        .hero-gradient {
            background: linear-gradient(to bottom, transparent 60%, #fdfcfb 100%);
        }
    </style>
<style>
    body {
      min-height: max(884px, 100dvh);
    }
  </style>
  </head>
<body class="min-h-screen">
<div class="relative flex h-auto min-h-screen w-full flex-col overflow-x-hidden">
<header class="fixed top-0 z-50 w-full flex items-center bg-white/40 backdrop-blur-md px-6 py-4 justify-between transition-all">
<button aria-label="Go back" class="text-gray-800 flex size-10 items-center justify-center rounded-full bg-white/80 shadow-sm border border-gray-100/50">
<span class="material-symbols-outlined text-xl">arrow_back</span>
</button>
<div class="flex items-center gap-1.5 bg-white/80 px-4 py-2 rounded-full shadow-sm border border-gray-100/50">
<span class="material-symbols-outlined text-rose text-lg fill-1">favorite</span>
<p class="text-gray-800 text-sm font-bold leading-none">98% Match</p>
</div>
</header>
<main class="flex-1 pb-32">
<div class="relative w-full h-[500px]">
<div class="absolute inset-0 bg-center bg-no-repeat bg-cover" style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuAwURoKK_WinfryLDMvzeBQN_l8x2uHFZTkCohG7tj453MSoHbbx5rzW4tE2T486Hc4mQSD_jvov4eQzmIvlpdGDYG8adZEohovc5cSBhkT7EG1DI4l9Wsc-Vco7EpUvwShbIFVXcV-WJrissg5fWBv6Iu8E6kL8V1anyCNW1g7t9_doCh1IblcmaFFpF_-sH1mckJ5y6e9GAmZorsYntr8OrCRjq_HbAubH-K5Ln53AMn99o9_02oJ8BGEbbYP-XiX2LxF5r-P4y7f");'>
<div class="absolute inset-0 hero-gradient"></div>
</div>
<div class="absolute bottom-0 left-0 right-0 px-8 pb-4">
<div class="flex gap-2 mb-4">
<span class="bg-white/40 backdrop-blur-md text-gray-700 border border-white/40 px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest">Grades K-8</span>
<span class="bg-white/40 backdrop-blur-md text-gray-700 border border-white/40 px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest">Literacy</span>
</div>
<h1 class="text-[#3d3d3d] text-4xl sm:text-5xl font-bold leading-[1.1] mb-2">
                        The Good and the Beautiful: Language Arts
                    </h1>
</div>
</div>
<div class="px-8 space-y-12">
<section class="mt-8">
<div class="bg-white rounded-[2.5rem] p-8 shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-gray-50">
<div class="flex items-center justify-between mb-4">
<p class="text-rose text-xs font-bold uppercase tracking-widest">Personal Match</p>
<span class="text-sage text-xs font-semibold">+5% vs last week</span>
</div>
<div class="flex items-baseline gap-3 mb-3">
<p class="text-[#3d3d3d] text-5xl font-display font-bold">98%</p>
<p class="text-gray-400 italic font-display text-lg">for your family</p>
</div>
<p class="text-gray-500 leading-relaxed text-sm">
                            Perfect for visual and kinesthetic learners like your children. The integration of art appreciation matches your Pinterest saves.
                        </p>
</div>
</section>
<section>
<h2 class="text-3xl text-[#3d3d3d] font-bold mb-6">About this Curriculum</h2>
<div class="text-gray-600 text-lg leading-relaxed space-y-6 font-light">
<p>
                            The Good and the Beautiful Language Arts is a comprehensive, open-and-go curriculum that focuses on high character and beautiful literature. It combines reading, writing, spelling, grammar, and art appreciation into a cohesive daily lesson.
                        </p>
<p>
                            Our unique approach eliminates the need for multiple separate programs by integrating all core language arts components. Each level is designed to be visually stunning, using fine art and nature photography to engage the child's imagination while building rigorous academic skills.
                        </p>
</div>
</section>
<section>
<div class="bg-[#f8f9fa] rounded-[2rem] p-8 border border-gray-100">
<div class="flex items-center gap-3 mb-8">
<div class="w-10 h-10 rounded-full bg-white flex items-center justify-center shadow-sm">
<span class="material-symbols-outlined text-rose text-xl">payments</span>
</div>
<h3 class="text-2xl text-[#3d3d3d] font-bold">Pricing &amp; Options</h3>
</div>
<div class="space-y-6">
<div class="flex justify-between items-center group">
<span class="text-gray-500 text-base">Digital PDF Course (Full)</span>
<div class="flex items-center gap-2">
<span class="h-px w-8 bg-gray-200"></span>
<span class="font-bold text-rose text-lg font-display">FREE</span>
</div>
</div>
<div class="flex justify-between items-center group">
<span class="text-gray-500 text-base">Physical Printed Set</span>
<div class="flex items-center gap-2">
<span class="h-px w-8 bg-gray-200"></span>
<span class="font-bold text-[#3d3d3d] text-lg font-display">$120.98</span>
</div>
</div>
<div class="flex justify-between items-center group">
<span class="text-gray-500 text-base">Teacher's Guide Only</span>
<div class="flex items-center gap-2">
<span class="h-px w-8 bg-gray-200"></span>
<span class="font-bold text-[#3d3d3d] text-lg font-display">$45.00</span>
</div>
</div>
</div>
</div>
</section>
<section class="-mx-8">
<h2 class="text-3xl text-[#3d3d3d] font-bold px-8 mb-6">More for you to love</h2>
<div class="flex overflow-x-auto gap-6 px-8 pb-8 hide-scrollbar">
<div class="min-w-[200px] w-52 flex flex-col gap-4">
<div class="aspect-[3/4] w-full rounded-[2rem] bg-cover bg-center shadow-lg relative overflow-hidden" style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuDVAcw_uw2Y6lh3SUpbX1L4WxFWO-LOTy5waksN67YrPz49HzxQD4KDX-natSQczDXoT3wtTQ6zfu1K6bFjkYp2hQAJ5OGv7tQiffOKpb_GoUOm6YllPuBVwLirFdT23KWjSysZDwhkJx6qJmUo4L_bWJu0Z6VAJ_fb8_DwL3QxHKrAziY5evos59MdF3Y2HdaEzfdrmlQWbxcWWRPOP8J4GyrvX-ZIcWtadJtAbYjoPcQfxKPWynyK6aHpADZMHuOQXFLB_QuInris");'>
<div class="absolute top-4 right-4 bg-white/90 backdrop-blur-md px-2.5 py-1 rounded-full shadow-sm">
<span class="text-[10px] font-bold text-rose">95%</span>
</div>
</div>
<div class="px-2">
<p class="font-display text-xl font-bold text-[#3d3d3d] leading-tight">Wildwood Nature</p>
<p class="text-xs text-gray-400 font-medium uppercase tracking-widest mt-1">Science • Grade 1-5</p>
</div>
</div>
<div class="min-w-[200px] w-52 flex flex-col gap-4">
<div class="aspect-[3/4] w-full rounded-[2rem] bg-cover bg-center shadow-lg relative overflow-hidden" style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuCXKl8p9bMDkfw4G0pT0UsawQCs-gvx-d0MZo3vUungrDeGXT00Zd1oN_ak3Rymj32t4b_XkswcffsjPeEOQyV1XbbKfVvF9MKb1BlQUXUaNnYN9so7dTxZjUT6NT-1z8Ur10AMHLOO2nQ92Cla2dK9TxNzeOAtT6hl9iQ9KF7LGWlwOjD0q8DED7StwMbSl2mQWfz_sF63sIMmqxYJzYwnyP6FCClM6B4uljrOUBhFvXG-prXL6Y3wtwmRRQsu5MERoriGdC1GswN2");'>
<div class="absolute top-4 right-4 bg-white/90 backdrop-blur-md px-2.5 py-1 rounded-full shadow-sm">
<span class="text-[10px] font-bold text-rose">92%</span>
</div>
</div>
<div class="px-2">
<p class="font-display text-xl font-bold text-[#3d3d3d] leading-tight">Simply Good Math</p>
<p class="text-xs text-gray-400 font-medium uppercase tracking-widest mt-1">Math • Grade K-6</p>
</div>
</div>
<div class="min-w-[200px] w-52 flex flex-col gap-4">
<div class="aspect-[3/4] w-full rounded-[2rem] bg-cover bg-center shadow-lg relative overflow-hidden" style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuAx0UVieH26Nuehf1iDC-nJkAljdN1nsI6qMuYLLI1hEPr7X5qhh_Oye-zjf3KIE0dpmBOsILch1i0zQ75tEBePScC9CkgZQg9Hipv_EtiLeggSqHUTjk3c1Rf9cQg319Dkf5nV9-UGft-Tz3cWpeR_gKqowU_G97fHMH-FV_YRcRbpciagX-xrhYwsDT-nkL99HHpxoLMAVYo98eWRN99zhv6PzSEZmw3kE2bsKTXhyyi0RDSa9SwniyawjrOmTaxeSX4ZFXga4W84");'>
<div class="absolute top-4 right-4 bg-white/90 backdrop-blur-md px-2.5 py-1 rounded-full shadow-sm">
<span class="text-[10px] font-bold text-rose">88%</span>
</div>
</div>
<div class="px-2">
<p class="font-display text-xl font-bold text-[#3d3d3d] leading-tight">Masterpiece Society</p>
<p class="text-xs text-gray-400 font-medium uppercase tracking-widest mt-1">Art • All Ages</p>
</div>
</div>
</div>
</section>
</div>
</main>
<div class="fixed bottom-8 left-0 right-0 px-8 z-50">
<a class="flex items-center justify-center gap-3 bg-rose hover:bg-rose/90 text-white font-bold py-5 px-8 rounded-full shadow-[0_15px_30px_rgba(229,152,155,0.4)] transition-all active:scale-95" href="#">
<span class="material-symbols-outlined text-xl">stylus_note</span>
<span class="text-lg">Visit Website</span>
</a>
</div>
</div>

</body></html>

<!-- Curriculum Discovery Swipe -->
<!DOCTYPE html>
<html class="light" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Curriculove - Discovery Swipe</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        "primary": "#d17a6a", // Warm earthy tone from Peanut/Pinterest inspiration
                        "accent-green": "#8fae92",
                        "background-cream": "#fdfaf7",
                        "card-bg": "#ffffff",
                    },
                    fontFamily: {
                        "display": ["Plus Jakarta Sans", "sans-serif"],
                        "serif": ["DM Serif Display", "serif"]
                    },
                    borderRadius: {
                        "DEFAULT": "1.25rem",
                        "lg": "2rem",
                        "xl": "2.5rem",
                        "full": "9999px"
                    },
                },
            },
        }
    </script>
<style type="text/tailwindcss">
    @layer base {
        body {
            @apply bg-background-cream text-[#3e3431] font-display antialiased;
        }
    }
    .material-symbols-outlined {
        font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
    }
    .fill-icon {
        font-variation-settings: 'FILL' 1;
    }
    .organic-badge {
        background: #fdfaf7;
        border: 2px solid #e9dfd6;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        transform: rotate(2deg);
    }
    .pinterest-card {
        box-shadow: 0 10px 25px -5px rgba(62, 52, 49, 0.08);
    }
</style>
<style>
    body {
      min-height: max(884px, 100dvh);
    }
  </style>
  </head>
<body class="min-h-screen flex flex-col">
<header class="flex items-center p-6 pb-2 justify-between sticky top-0 z-50 bg-background-cream/80 backdrop-blur-md">
<div class="text-[#3e3431] flex size-10 items-center justify-center cursor-pointer" data-icon="menu">
<span class="material-symbols-outlined text-2xl">menu</span>
</div>
<h2 class="font-serif text-2xl text-[#3e3431] flex-1 text-center pr-10">Curriculove</h2>
</header>
<div class="px-8 py-2">
<div class="flex flex-col gap-1.5">
<div class="flex justify-between items-end px-1">
<p class="text-[#8c7e7a] text-xs font-semibold uppercase tracking-widest">Daily Discovery</p>
<p class="text-primary text-xs font-bold leading-normal">1 of 12 matches</p>
</div>
<div class="h-1 w-full bg-[#eee5df] rounded-full overflow-hidden">
<div class="h-full bg-primary rounded-full transition-all duration-500" style="width: 8%;"></div>
</div>
</div>
</div>
<main class="flex-1 flex flex-col items-center justify-center p-6 relative overflow-hidden">
<div class="pinterest-card w-full max-w-md bg-card-bg rounded-xl overflow-hidden flex flex-col border border-[#f0e8e0]">
<div class="relative w-full aspect-[4/5] bg-center bg-no-repeat bg-cover" data-alt="Curriculum on wooden desk" style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuAPen01MHb_G58V0loUlEDtbtuETspJ2vc5b7Ld2Qc-UI0wlEMMb3_rURC6f34fzD9aiY9Pc4LcEmIjMbsj60ThgcIS1S5mEpw-pur1yfS_1RTsgkSlCGhnTkXKWBZlG2Ky8Pft8rP8qucXL2OIRHGNjXEtYl2UW2spG9tQBltua_qoy7pGybiwyFTCGZDTgkfcIw7etaE29wbR42C-Cd5cByWOJMZrqGgpQ7skK72ByyuDygMu4WVQT80lLLKDudjwvBfDuO0QTSyH");'>
<div class="organic-badge absolute top-6 right-6 px-4 py-2 rounded-full flex flex-col items-center justify-center">
<span class="text-xs font-bold text-[#8c7e7a] uppercase tracking-tighter leading-none">Match</span>
<span class="text-lg font-serif text-primary leading-none">94%</span>
</div>
<div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent"></div>
<div class="absolute bottom-6 left-6 right-6 text-white">
<h1 class="font-serif text-4xl leading-tight mb-1">Blossom &amp; Root</h1>
<p class="text-white/95 text-sm font-medium italic opacity-90">A creative, nature-based secular curriculum for wonder-led families.</p>
</div>
</div>
<div class="p-6 flex flex-col gap-6">
<div class="flex gap-2 flex-wrap">
<div class="flex h-8 items-center justify-center gap-x-1.5 rounded-full bg-[#fdf2f0] px-4 border border-[#f5e1de]">
<span class="material-symbols-outlined text-[16px] text-primary">payments</span>
<p class="text-primary text-xs font-bold leading-normal">$$</p>
</div>
<div class="flex h-8 items-center justify-center gap-x-1.5 rounded-full bg-[#f4f7f5] px-4 border border-[#e4ece6]">
<span class="material-symbols-outlined text-[16px] text-accent-green">school</span>
<p class="text-accent-green text-xs font-bold leading-normal">PreK - 5th</p>
</div>
<div class="flex h-8 items-center justify-center gap-x-1.5 rounded-full bg-[#f7f5f2] px-4 border border-[#ece7e1]">
<span class="material-symbols-outlined text-[16px] text-[#8c7e7a]">spa</span>
<p class="text-[#8c7e7a] text-xs font-bold leading-normal">CM, Nature-Based</p>
</div>
</div>
<div class="flex flex-col gap-2">
<h3 class="text-primary text-[10px] font-bold uppercase tracking-widest px-1">Why it matches you</h3>
<p class="text-[#5d5451] text-sm leading-relaxed px-1">
                    Based on your preference for <span class="text-[#3e3431] font-semibold underline decoration-accent-green/30 decoration-2">nature-based learning</span> and the <span class="text-[#3e3431] font-semibold underline decoration-primary/30 decoration-2">Charlotte Mason philosophy</span>.
                </p>
</div>
<div class="flex flex-col items-start gap-3 rounded-2xl border border-[#f0e8e0] bg-background-cream/50 p-5">
<div class="flex flex-col gap-2">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-accent-green text-xl fill-icon">verified</span>
<p class="font-serif text-base text-[#3e3431]">Expert Insight</p>
</div>
<p class="text-[#5d5451] text-xs leading-relaxed italic">
                        "This curriculum excels at integrating arts with core sciences, perfect for creative learners who thrive outdoors."
                    </p>
</div>
<a class="text-xs font-bold leading-normal tracking-wider flex items-center gap-1.5 text-primary hover:opacity-80 transition-opacity" href="#">
                    READ FULL REVIEW
                    <span class="material-symbols-outlined text-sm">arrow_forward</span>
</a>
</div>
</div>
</div>
</main>
<footer class="p-8 pb-12">
<div class="flex items-center justify-center gap-8">
<button class="w-16 h-16 rounded-full bg-white shadow-lg flex items-center justify-center border border-[#eee5df] text-[#8c7e7a] hover:scale-110 active:scale-95 transition-all">
<span class="material-symbols-outlined text-3xl">close</span>
</button>
<button class="w-20 h-20 rounded-full bg-primary shadow-xl flex items-center justify-center text-white hover:scale-110 active:scale-95 transition-all">
<span class="material-symbols-outlined text-4xl fill-icon">favorite</span>
</button>
<button class="w-16 h-16 rounded-full bg-white shadow-lg flex items-center justify-center border border-[#eee5df] text-accent-green hover:scale-110 active:scale-95 transition-all">
<span class="material-symbols-outlined text-3xl">menu_book</span>
</button>
</div>
</footer>

</body></html>
