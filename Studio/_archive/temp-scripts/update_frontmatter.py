#!/usr/bin/env python3
"""
Update frontmatter in Master Content Database files to add tags for progressive disclosure.
Generated from analyze_master_content.py
"""

import re
import yaml
from pathlib import Path

updates = {
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/InfoCenter Improvements  March 2025.md": {
    "tags": [
      "career",
      "technology"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/A New Approach to Curriculum Access.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "curriculum"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/To Diploma or Not to Diploma.md": {
    "tags": [
      "art",
      "entrepreneurship",
      "career",
      "curriculum",
      "faith-based",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Montessori Curriculum for Homeschooling.md": {
    "tags": [
      "preschool",
      "career",
      "faith-based",
      "technology",
      "outdoor",
      "assessment",
      "science",
      "college-prep",
      "elementary",
      "project-based",
      "coding",
      "curriculum",
      "montessori",
      "high-school",
      "secular",
      "art",
      "music",
      "reading",
      "stem",
      "microschool",
      "entrepreneurship",
      "math",
      "middle-school",
      "writing",
      "socialization",
      "language",
      "history"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/What Resources Are Included In Your OpenEd UFA Package.md": {
    "tags": [
      "art",
      "college-prep",
      "math",
      "curriculum",
      "writing",
      "technology",
      "science"
    ],
    "tools": [
      "ixl"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Backyard Chickens The Ultimate Hands-On Homeschooling Projec.md": {
    "tags": [
      "entrepreneurship",
      "math",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/The Homeschool Socialization Question Lets Get Weird.md": {
    "tags": [
      "art",
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "curriculum",
      "roadschooling",
      "writing",
      "socialization",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/How to Create a Thriving Educational Micro-Community The Com.md": {
    "tags": [
      "career",
      "roadschooling",
      "technology",
      "outdoor",
      "college-prep",
      "science",
      "project-based",
      "coding",
      "curriculum",
      "montessori",
      "high-school",
      "art",
      "waldorf",
      "reading",
      "stem",
      "adhd",
      "microschool",
      "entrepreneurship",
      "math",
      "writing",
      "socialization",
      "assessment"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Best Homeschool Math Curriculum.md": {
    "tags": [
      "kindergarten",
      "career",
      "roadschooling",
      "gifted",
      "technology",
      "college-prep",
      "science",
      "elementary",
      "curriculum",
      "high-school",
      "secular",
      "art",
      "music",
      "reading",
      "stem",
      "math",
      "middle-school",
      "socialization",
      "assessment",
      "history"
    ],
    "tools": [
      "lego"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/The Homeschool Parents Guide to Dyslexia When to DIY vs When.md": {
    "tags": [
      "art",
      "history",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "language",
      "stem",
      "technology",
      "special-needs",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Homeschooling a Child with ADHD.md": {
    "tags": [
      "career",
      "roadschooling",
      "gifted",
      "technology",
      "college-prep",
      "science",
      "project-based",
      "coding",
      "curriculum",
      "high-school",
      "art",
      "music",
      "reading",
      "stem",
      "adhd",
      "entrepreneurship",
      "math",
      "middle-school",
      "writing",
      "socialization",
      "assessment"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Test html.md": {
    "tags": [
      "assessment",
      "curriculum"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Who is your childs best teacher.md": {
    "tags": [
      "secular",
      "art",
      "history",
      "career",
      "project-based",
      "math",
      "curriculum",
      "roadschooling",
      "gifted",
      "writing",
      "music",
      "reading",
      "socialization",
      "assessment",
      "high-school",
      "technology",
      "outdoor",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Playing with LEGO is More Valuable than Learning Algebra.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": [
      "lego"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/What is Open Education.md": {
    "tags": [
      "forest-school",
      "career",
      "roadschooling",
      "gifted",
      "faith-based",
      "technology",
      "outdoor",
      "science",
      "college-prep",
      "project-based",
      "nature-based",
      "coding",
      "curriculum",
      "montessori",
      "high-school",
      "waldorf",
      "unschooling",
      "stem",
      "adhd",
      "microschool",
      "classical-education",
      "math",
      "socialization",
      "assessment",
      "history"
    ],
    "tools": [
      "scratch"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/What Courses  Providers Are Included In Your OpenEd UFA Pack.md": {
    "tags": [
      "art",
      "college-prep",
      "entrepreneurship",
      "math",
      "coding",
      "curriculum",
      "socialization",
      "reading",
      "language",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Homeschool Kindergarten Without Walls Freedom as the Ultimat.md": {
    "tags": [
      "preschool",
      "kindergarten",
      "career",
      "gifted",
      "outdoor",
      "assessment",
      "college-prep",
      "science",
      "elementary",
      "coding",
      "curriculum",
      "charlotte-mason",
      "art",
      "reading",
      "stem",
      "math",
      "writing",
      "socialization",
      "language",
      "history"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/SmartPath The AI-Powered Homeschool Curriculum Finder That E.md": {
    "tags": [
      "college-prep",
      "entrepreneurship",
      "career",
      "curriculum",
      "roadschooling",
      "reading",
      "science",
      "stem",
      "technology",
      "microschool"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Stop Overscheduling Your Childs Learning  Matt Bowman.md": {
    "tags": [
      "art",
      "forest-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "curriculum",
      "writing",
      "reading",
      "assessment",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/OpenEd Day in the Life Brettani Shannons Slow-Morning AI-Pow.md": {
    "tags": [
      "art",
      "history",
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "gifted",
      "writing",
      "socialization",
      "reading",
      "language",
      "stem",
      "technology",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Beyond A to F.md": {
    "tags": [
      "college-prep",
      "kindergarten",
      "career",
      "curriculum",
      "coding",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Coming Soon OpenEds New Platform.md": {
    "tags": [
      "assessment",
      "career",
      "socialization",
      "curriculum"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Mike Rowes Case for Career and Technical Education.md": {
    "tags": [
      "art",
      "high-school",
      "college-prep",
      "career",
      "coding",
      "curriculum",
      "gifted",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/How OpenEd Teachers Master the Work-From-Home Juggle.md": {
    "tags": [
      "art",
      "preschool",
      "college-prep",
      "entrepreneurship",
      "career",
      "gifted",
      "socialization",
      "music",
      "reading",
      "language",
      "stem",
      "technology",
      "assessment",
      "science"
    ],
    "tools": [
      "zoom"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/OpenEd Communitys Favorite Educational Resources.md": {
    "tags": [
      "art",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "writing",
      "reading",
      "unschooling",
      "outdoor",
      "assessment",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/What the New York Times got wrong about homeschooling.md": {
    "tags": [
      "forest-school",
      "career",
      "roadschooling",
      "faith-based",
      "technology",
      "outdoor",
      "college-prep",
      "science",
      "project-based",
      "coding",
      "curriculum",
      "high-school",
      "charlotte-mason",
      "art",
      "reading",
      "unschooling",
      "stem",
      "adhd",
      "microschool",
      "entrepreneurship",
      "classical-education",
      "math",
      "socialization",
      "history"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/The World Has Changed.md": {
    "tags": [
      "curriculum",
      "roadschooling",
      "socialization",
      "writing",
      "technology",
      "microschool"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Kindergarten Homeschool Curriculum A Guide to Freedom-Based .md": {
    "tags": [
      "art",
      "waldorf",
      "college-prep",
      "kindergarten",
      "career",
      "math",
      "coding",
      "curriculum",
      "gifted",
      "writing",
      "socialization",
      "reading",
      "science",
      "language",
      "stem",
      "technology",
      "outdoor",
      "charlotte-mason"
    ],
    "tools": [
      "ixl"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/How to Start Homeschooling With Confidence Even If Youre Sca.md": {
    "tags": [
      "career",
      "math",
      "curriculum",
      "writing",
      "reading",
      "assessment",
      "outdoor",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Your Kids Will Be Alright What the New York Times Misses Abo.md": {
    "tags": [
      "high-school",
      "assessment",
      "college-prep",
      "kindergarten",
      "career",
      "entrepreneurship",
      "microschool",
      "math",
      "curriculum",
      "roadschooling",
      "writing",
      "socialization",
      "unschooling",
      "stem",
      "technology",
      "adhd",
      "science"
    ],
    "tools": [
      "lego"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Classical Education Understanding the Model and Approach.md": {
    "tags": [
      "career",
      "gifted",
      "faith-based",
      "technology",
      "assessment",
      "college-prep",
      "science",
      "elementary",
      "curriculum",
      "high-school",
      "art",
      "reading",
      "stem",
      "classical-education",
      "math",
      "middle-school",
      "writing",
      "socialization",
      "language",
      "history"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Best Homeschool Science Curriculum.md": {
    "tags": [
      "secular",
      "elementary",
      "high-school",
      "college-prep",
      "career",
      "project-based",
      "math",
      "coding",
      "curriculum",
      "middle-school",
      "writing",
      "reading",
      "assessment",
      "stem",
      "technology",
      "outdoor",
      "adhd",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Why Kids Lose Their Love of Learning And How to Prevent It.md": {
    "tags": [
      "art",
      "career",
      "writing",
      "reading",
      "stem",
      "microschool"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Why Traditional Schools Create Dependent Learners  Tyler Thi.md": {
    "tags": [
      "art",
      "elementary",
      "high-school",
      "forest-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "microschool",
      "curriculum",
      "reading",
      "stem",
      "outdoor",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/What neuroscience can teach us about homeschooling  Dr Clair.md": {
    "tags": [
      "art",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "writing",
      "reading",
      "language",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Your Kids Screen Was Built Like a Slot Machine.md": {
    "tags": [
      "art",
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "gifted",
      "socialization",
      "music",
      "assessment",
      "stem",
      "technology",
      "adhd",
      "science"
    ],
    "tools": [
      "outschool",
      "zoom"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/7 Uncomfortable Truths About Education from Award-Winning Te.md": {
    "tags": [
      "art",
      "history",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "gifted",
      "reading",
      "assessment",
      "stem",
      "special-needs",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/9 Future-Proof Career Prep Strategies for Homeschooled Teens.md": {
    "tags": [
      "art",
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "coding",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Why Kids Hate Mathand 20 Resources to Help Fix It.md": {
    "tags": [
      "elementary",
      "high-school",
      "career",
      "math",
      "curriculum",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": [
      "minecraft"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/12 Best Homeschool Podcasts for Personalized Education in 20.md": {
    "tags": [
      "career",
      "roadschooling",
      "gifted",
      "faith-based",
      "technology",
      "outdoor",
      "college-prep",
      "science",
      "project-based",
      "nature-based",
      "curriculum",
      "charlotte-mason",
      "secular",
      "art",
      "reading",
      "unschooling",
      "stem",
      "adhd",
      "microschool",
      "writing",
      "socialization"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/If you dread Back to School read this.md": {
    "tags": [
      "high-school",
      "career",
      "math",
      "coding",
      "curriculum",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/A Beginners Guide to Microschools  the Educational Trend Gro.md": {
    "tags": [
      "preschool",
      "career",
      "reggio-emilia",
      "roadschooling",
      "faith-based",
      "technology",
      "outdoor",
      "college-prep",
      "science",
      "project-based",
      "coding",
      "curriculum",
      "montessori",
      "art",
      "waldorf",
      "music",
      "stem",
      "entrepreneurship",
      "microschool",
      "math",
      "socialization",
      "assessment"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/The OpenEd Holiday Gift Guide 2025.md": {
    "tags": [
      "art",
      "high-school",
      "history",
      "college-prep",
      "10-14-years",
      "career",
      "math",
      "coding",
      "curriculum",
      "writing",
      "music",
      "reading",
      "socialization",
      "assessment",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": [
      "lego"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Small Schools Big Difference A Primer on Microschools.md": {
    "tags": [
      "kindergarten",
      "career",
      "roadschooling",
      "faith-based",
      "technology",
      "outdoor",
      "assessment",
      "science",
      "college-prep",
      "project-based",
      "nature-based",
      "curriculum",
      "montessori",
      "high-school",
      "secular",
      "art",
      "reading",
      "stem",
      "microschool",
      "entrepreneurship",
      "classical-education",
      "math",
      "socialization",
      "language",
      "history",
      "special-needs"
    ],
    "tools": [
      "zoom"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Free Homeschool Curriculum The OpenEd Complete Guide to Qual.md": {
    "tags": [
      "career",
      "gifted",
      "faith-based",
      "technology",
      "assessment",
      "college-prep",
      "science",
      "elementary",
      "curriculum",
      "high-school",
      "art",
      "music",
      "reading",
      "stem",
      "microschool",
      "entrepreneurship",
      "math",
      "writing",
      "socialization",
      "language",
      "history",
      "special-needs"
    ],
    "tools": [
      "khan-academy"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Coach Meg Thomas How I Built a Self-Managing Homeschool of 7.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "curriculum",
      "roadschooling",
      "socialization",
      "faith-based",
      "reading",
      "stem",
      "outdoor",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/Homeschool Art Curriculum  OpenEd.md": {
    "tags": [
      "kindergarten",
      "career",
      "technology",
      "outdoor",
      "assessment",
      "college-prep",
      "science",
      "elementary",
      "nature-based",
      "curriculum",
      "high-school",
      "charlotte-mason",
      "art",
      "waldorf",
      "music",
      "reading",
      "math",
      "middle-school",
      "writing",
      "socialization",
      "language",
      "history"
    ],
    "tools": [
      "outschool"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Blog Posts/When the Smartest Person in the World Called Out Our Schools.md": {
    "tags": [
      "history",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "reading",
      "assessment",
      "stem",
      "outdoor",
      "science"
    ],
    "tools": [
      "chatgpt"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Announcements/A Sneak Peek at the 2025 Marketplace.md": {
    "tags": [
      "career",
      "reading",
      "curriculum"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Announcements/What Returning Families Need To Know for the 25-26 School Ye.md": {
    "tags": [
      "art",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "language",
      "technology",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Announcements/Attention Class of 2026.md": {
    "tags": [
      "college-prep",
      "career",
      "curriculum",
      "high-school",
      "technology",
      "entrepreneurship"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Why Your ADHD Kid Wont Listen Its Not What You Think.md": {
    "tags": [
      "assessment",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "music",
      "reading",
      "language",
      "stem",
      "adhd",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/She Did Everything Right - Her Daughter Still Couldnt Read.md": {
    "tags": [
      "elementary",
      "high-school",
      "history",
      "college-prep",
      "kindergarten",
      "career",
      "math",
      "curriculum",
      "reading",
      "assessment",
      "stem",
      "technology",
      "special-needs",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Is Homeschooling the Wrong Word Were Only Home 3 Hours a Day.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "curriculum",
      "gifted",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "special-needs",
      "science"
    ],
    "tools": [
      "youtube",
      "audiobook"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Why Middle School Matters.md": {
    "tags": [
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "coding",
      "curriculum",
      "middle-school",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/The Hollywood Veterans Teaching Kids to Break Into Film.md": {
    "tags": [
      "art",
      "high-school",
      "history",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "curriculum",
      "writing",
      "socialization",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/I Let My Kids Skip School They Still Made Student Council.md": {
    "tags": [
      "college-prep",
      "entrepreneurship",
      "career",
      "project-based",
      "microschool",
      "curriculum",
      "roadschooling",
      "socialization",
      "reading",
      "language",
      "stem",
      "outdoor",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/How to Keep Your Kid in Music Lessons Without Forcing Them t.md": {
    "tags": [
      "art",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "middle-school",
      "music",
      "reading",
      "language",
      "high-school",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/What Makes a Thriving Homeschool Collective  Cassie Tinsmon.md": {
    "tags": [
      "kindergarten",
      "career",
      "roadschooling",
      "faith-based",
      "outdoor",
      "assessment",
      "college-prep",
      "science",
      "nature-based",
      "curriculum",
      "montessori",
      "high-school",
      "art",
      "reading",
      "unschooling",
      "stem",
      "entrepreneurship",
      "math",
      "socialization",
      "language",
      "special-needs"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/How to Raise Kids Who Actually Care About Others.md": {
    "tags": [
      "high-school",
      "history",
      "college-prep",
      "entrepreneurship",
      "career",
      "curriculum",
      "roadschooling",
      "socialization",
      "faith-based",
      "reading",
      "language",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": [
      "chatgpt"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Why Students Quit Online SchoolUntil This Stanford Pioneer M.md": {
    "tags": [
      "high-school",
      "college-prep",
      "kindergarten",
      "career",
      "entrepreneurship",
      "microschool",
      "math",
      "curriculum",
      "roadschooling",
      "gifted",
      "writing",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 008 - MARK HYATT.md": {
    "tags": [
      "career",
      "roadschooling",
      "faith-based",
      "technology",
      "assessment",
      "college-prep",
      "science",
      "curriculum",
      "high-school",
      "art",
      "music",
      "reading",
      "stem",
      "entrepreneurship",
      "math",
      "middle-school",
      "socialization",
      "language",
      "history"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/How to Homeschool Year-Round Without Burnout.md": {
    "tags": [
      "career",
      "math",
      "curriculum",
      "music",
      "reading",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 004 - The End of One-size-fits-all.md": {
    "tags": [
      "history",
      "college-prep",
      "entrepreneurship",
      "career",
      "microschool",
      "math",
      "coding",
      "curriculum",
      "gifted",
      "writing",
      "socialization",
      "reading",
      "faith-based",
      "assessment",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 018 - Is It Really Dyslexia.md": {
    "tags": [
      "high-school",
      "history",
      "college-prep",
      "career",
      "math",
      "coding",
      "curriculum",
      "roadschooling",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "special-needs",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Why a Public School Principal Told Me to Homeschool My Kids.md": {
    "tags": [
      "language",
      "high-school",
      "college-prep",
      "kindergarten",
      "career",
      "microschool",
      "math",
      "curriculum",
      "roadschooling",
      "socialization",
      "reading",
      "unschooling",
      "stem",
      "technology",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Dispelling Dyslexia Myths with the Science of Reading.md": {
    "tags": [
      "college-prep",
      "career",
      "reading",
      "outdoor",
      "stem",
      "special-needs",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Your kid will be weird and thats okay  TK Coleman on the hom.md": {
    "tags": [
      "college-prep",
      "entrepreneurship",
      "career",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/How to reclaim your teenagers affection.md": {
    "tags": [
      "high-school",
      "history",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "coding",
      "curriculum",
      "writing",
      "music",
      "reading",
      "socialization",
      "assessment",
      "stem",
      "outdoor",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Fund Families Not Systems How One Simple Change Could Fix Am.md": {
    "tags": [
      "history",
      "college-prep",
      "career",
      "microschool",
      "curriculum",
      "roadschooling",
      "gifted",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "zoom"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/5 Questions with Tuttle Twins Creator Connor Boyack.md": {
    "tags": [
      "college-prep",
      "entrepreneurship",
      "career",
      "project-based",
      "curriculum",
      "reading",
      "language",
      "stem",
      "assessment",
      "science"
    ],
    "tools": [
      "minecraft",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 011 - Unplugged and Unafraid The Nature Kids Connect.md": {
    "tags": [
      "entrepreneurship",
      "career",
      "nature-based",
      "curriculum",
      "socialization",
      "technology",
      "outdoor",
      "college-prep"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/The school that trusts parents to design their childs educat.md": {
    "tags": [
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "gifted",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "outschool"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 014 - Stop Outsourcing Your Childs Education.md": {
    "tags": [
      "college-prep",
      "entrepreneurship",
      "career",
      "microschool",
      "math",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 023 - The Apogee Approach to Modern Education A Form.md": {
    "tags": [
      "elementary",
      "college-prep",
      "career",
      "project-based",
      "microschool",
      "curriculum",
      "socialization",
      "reading",
      "unschooling",
      "stem",
      "outdoor",
      "assessment",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 015 - The Single Mom Who Fixed Her Kids Education Wi.md": {
    "tags": [
      "art",
      "college-prep",
      "kindergarten",
      "career",
      "math",
      "curriculum",
      "writing",
      "music",
      "reading",
      "socialization",
      "assessment",
      "stem",
      "technology",
      "adhd",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 017 - From Classroom Teacher to Homeschool Mom.md": {
    "tags": [
      "history",
      "college-prep",
      "kindergarten",
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "writing",
      "music",
      "reading",
      "socialization",
      "assessment",
      "high-school",
      "technology",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 024 - Why Poor Parents Trust Schools More Than Rich .md": {
    "tags": [
      "art",
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "curriculum",
      "roadschooling",
      "gifted",
      "middle-school",
      "writing",
      "reading",
      "socialization",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/College-for-All Is Breaking What Replaces It.md": {
    "tags": [
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "roadschooling",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/How to Homeschool Without Being the Teacher.md": {
    "tags": [
      "art",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "gifted",
      "socialization",
      "faith-based",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "microschool"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/The Lost Art of Play.md": {
    "tags": [
      "forest-school",
      "career",
      "roadschooling",
      "outdoor",
      "assessment",
      "science",
      "college-prep",
      "elementary",
      "nature-based",
      "coding",
      "curriculum",
      "high-school",
      "art",
      "reading",
      "unschooling",
      "stem",
      "microschool",
      "entrepreneurship",
      "math",
      "middle-school",
      "writing",
      "socialization",
      "language"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 010 - Relax and trust the process.md": {
    "tags": [
      "high-school",
      "history",
      "college-prep",
      "kindergarten",
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "writing",
      "music",
      "reading",
      "socialization",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/5 Myths Keeping Your Child From Reading Success And the 25-M.md": {
    "tags": [
      "history",
      "college-prep",
      "kindergarten",
      "career",
      "entrepreneurship",
      "math",
      "curriculum",
      "roadschooling",
      "gifted",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "special-needs",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 001 - Students Arent Standard.md": {
    "tags": [
      "elementary",
      "high-school",
      "history",
      "college-prep",
      "10-14-years",
      "entrepreneurship",
      "career",
      "project-based",
      "math",
      "curriculum",
      "montessori",
      "middle-school",
      "socialization",
      "unschooling",
      "stem",
      "technology",
      "assessment",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 021 - Why We Left School The Red Flags She Wishes Sh.md": {
    "tags": [
      "art",
      "preschool",
      "high-school",
      "history",
      "college-prep",
      "kindergarten",
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "gifted",
      "writing",
      "socialization",
      "reading",
      "faith-based",
      "assessment",
      "stem",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 009 - Daniella Park of Baketivity.md": {
    "tags": [
      "art",
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "coding",
      "curriculum",
      "roadschooling",
      "writing",
      "socialization",
      "reading",
      "language",
      "stem",
      "special-needs",
      "assessment",
      "science"
    ],
    "tools": [
      "baketivity",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 016  How to Transform Everyday Moments into Powerful.md": {
    "tags": [
      "college-prep",
      "kindergarten",
      "career",
      "math",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "adhd",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/How an 18-Year-Old Landed a Tech Sales Job Without a Degree.md": {
    "tags": [
      "college-prep",
      "career",
      "high-school",
      "technology",
      "entrepreneurship"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 006 - Deschooling Your Mind with Hannah Frankman.md": {
    "tags": [
      "kindergarten",
      "career",
      "roadschooling",
      "technology",
      "outdoor",
      "assessment",
      "college-prep",
      "science",
      "coding",
      "curriculum",
      "high-school",
      "music",
      "reading",
      "unschooling",
      "stem",
      "microschool",
      "entrepreneurship",
      "math",
      "middle-school",
      "writing",
      "socialization",
      "language",
      "history"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/From Viral Ads to Revolutionary Education A Conversation wit.md": {
    "tags": [
      "art",
      "history",
      "entrepreneurship",
      "career",
      "math",
      "curriculum",
      "socialization",
      "faith-based",
      "reading",
      "language",
      "high-school",
      "technology",
      "assessment",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/The School-to-Prescription Pipeline Ben Somers on How We Med.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "microschool",
      "curriculum",
      "socialization",
      "writing",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 012 - Kerry McDonald on Liberating Education.md": {
    "tags": [
      "art",
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "microschool",
      "math",
      "curriculum",
      "socialization",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": [
      "khan-academy",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/The 200-Year-Old Trap Breaking Down Part One of Open Educati.md": {
    "tags": [
      "high-school",
      "history",
      "college-prep",
      "entrepreneurship",
      "career",
      "project-based",
      "math",
      "curriculum",
      "gifted",
      "writing",
      "music",
      "reading",
      "socialization",
      "language",
      "stem",
      "technology",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Have We Been Teaching STEM Backwards The Case for Project-Ba.md": {
    "tags": [
      "art",
      "college-prep",
      "career",
      "project-based",
      "math",
      "curriculum",
      "writing",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/What Happens When a Teacher Tells Teens to Stop Going to Sch.md": {
    "tags": [
      "language",
      "high-school",
      "history",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "curriculum",
      "writing",
      "music",
      "reading",
      "socialization",
      "unschooling",
      "stem",
      "technology",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Whats behind the annual spike in youth anxiety  depression.md": {
    "tags": [
      "preschool",
      "kindergarten",
      "career",
      "roadschooling",
      "technology",
      "outdoor",
      "assessment",
      "college-prep",
      "science",
      "elementary",
      "curriculum",
      "high-school",
      "art",
      "music",
      "reading",
      "stem",
      "entrepreneurship",
      "math",
      "writing",
      "socialization",
      "language",
      "history"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/7 Things Career Expert Ken Coleman Says Parents Get Wrong An.md": {
    "tags": [
      "career",
      "math",
      "writing",
      "reading",
      "assessment",
      "college-prep"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Dont Quit Music Lessons Just Because Your Kid Wont Practice.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "curriculum",
      "socialization",
      "music",
      "reading",
      "language",
      "high-school",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/What kind of homeschool parent are you.md": {
    "tags": [
      "high-school",
      "10-14-years",
      "entrepreneurship",
      "career",
      "math",
      "coding",
      "middle-school",
      "music",
      "reading",
      "assessment",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Finding Your Childs Superpower Why Average Students Need Spe.md": {
    "tags": [
      "art",
      "high-school",
      "college-prep",
      "career",
      "coding",
      "gifted",
      "socialization",
      "music",
      "reading",
      "faith-based",
      "assessment",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 002 - When someone asks if you homeschool.md": {
    "tags": [
      "career",
      "faith-based",
      "technology",
      "outdoor",
      "assessment",
      "college-prep",
      "science",
      "project-based",
      "coding",
      "curriculum",
      "high-school",
      "art",
      "music",
      "reading",
      "entrepreneurship",
      "math",
      "middle-school",
      "writing",
      "socialization",
      "language",
      "history"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 022 - How This Working Mom Ditched Homework amp Tran.md": {
    "tags": [
      "kindergarten",
      "career",
      "roadschooling",
      "gifted",
      "technology",
      "outdoor",
      "assessment",
      "science",
      "college-prep",
      "elementary",
      "curriculum",
      "montessori",
      "high-school",
      "art",
      "waldorf",
      "music",
      "reading",
      "stem",
      "math",
      "middle-school",
      "writing",
      "socialization",
      "language",
      "history",
      "special-needs"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 007 - 5 Building Blocks of Open Education with Isaac.md": {
    "tags": [
      "career",
      "roadschooling",
      "technology",
      "outdoor",
      "college-prep",
      "science",
      "project-based",
      "curriculum",
      "montessori",
      "high-school",
      "art",
      "music",
      "reading",
      "unschooling",
      "stem",
      "entrepreneurship",
      "microschool",
      "classical-education",
      "writing",
      "assessment"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Your Kids Screen Was Built Like a Slot Machine.md": {
    "tags": [
      "preschool",
      "assessment",
      "college-prep",
      "career",
      "microschool",
      "math",
      "writing",
      "reading",
      "unschooling",
      "stem",
      "technology",
      "outdoor",
      "adhd",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Meg Thomass 3-Part Framework for Calm Homeschooling.md": {
    "tags": [
      "art",
      "career",
      "curriculum",
      "socialization",
      "music",
      "reading",
      "assessment",
      "charlotte-mason"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/The Genius We Engineer Away.md": {
    "tags": [
      "history",
      "college-prep",
      "career",
      "curriculum",
      "gifted",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 013 - Sidekick to Hero.md": {
    "tags": [
      "art",
      "high-school",
      "history",
      "college-prep",
      "entrepreneurship",
      "career",
      "curriculum",
      "roadschooling",
      "middle-school",
      "socialization",
      "reading",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/What to Do When Your Students Dont Respect You Michelle Rhee.md": {
    "tags": [
      "career",
      "microschool",
      "math",
      "music",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 019  QA ADHD Social Skills  Making Hard Choices in A.md": {
    "tags": [
      "high-school",
      "history",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "coding",
      "curriculum",
      "gifted",
      "middle-school",
      "writing",
      "reading",
      "socialization",
      "assessment",
      "stem",
      "technology",
      "adhd",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 003 - The Truth About Tech Careers in 2024 No Degree.md": {
    "tags": [
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "project-based",
      "coding",
      "curriculum",
      "socialization",
      "reading",
      "language",
      "stem",
      "technology",
      "assessment",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/The 1 life skill to turn your child into a confident learner.md": {
    "tags": [
      "high-school",
      "history",
      "college-prep",
      "entrepreneurship",
      "career",
      "curriculum",
      "socialization",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/The Etsy Effect How Not to Kill Your Childs Passions.md": {
    "tags": [
      "art",
      "college-prep",
      "career",
      "curriculum",
      "writing",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/He sold his house to homeschool in a 300-square-foot RV with.md": {
    "tags": [
      "college-prep",
      "career",
      "coding",
      "curriculum",
      "roadschooling",
      "socialization",
      "reading",
      "assessment",
      "special-needs",
      "adhd",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 005 - she almost gave up on education.md": {
    "tags": [
      "art",
      "high-school",
      "history",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "curriculum",
      "middle-school",
      "music",
      "reading",
      "socialization",
      "language",
      "stem",
      "technology",
      "outdoor",
      "assessment",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Episode 020 - The Secret to Not Ruining Your Homeschool Kids.md": {
    "tags": [
      "preschool",
      "kindergarten",
      "career",
      "gifted",
      "technology",
      "assessment",
      "college-prep",
      "science",
      "coding",
      "curriculum",
      "high-school",
      "art",
      "reading",
      "stem",
      "math",
      "writing",
      "socialization",
      "language",
      "history"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/College and Career Advice for Teens with Rose Ybaben ft Dani.md": {
    "tags": [
      "career",
      "assessment",
      "high-school",
      "technology",
      "outdoor",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Podcasts/Stop Limiting Your Childs Screen Time Do This Instead.md": {
    "tags": [
      "art",
      "college-prep",
      "entrepreneurship",
      "career",
      "microschool",
      "coding",
      "curriculum",
      "gifted",
      "socialization",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": [
      "outschool",
      "minecraft"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The 5-step formula for burnout 117.md": {
    "tags": [
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "outdoor"
    ],
    "tools": [
      "chatgpt",
      "ai-tutor"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Are we teaching STEM backwards.md": {
    "tags": [
      "high-school",
      "college-prep",
      "kindergarten",
      "career",
      "project-based",
      "math",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why your kids need you less.md": {
    "tags": [
      "reading",
      "math",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/ADHD and Homeschooling.md": {
    "tags": [
      "elementary",
      "high-school",
      "history",
      "assessment",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "curriculum",
      "middle-school",
      "music",
      "reading",
      "socialization",
      "faith-based",
      "language",
      "stem",
      "adhd",
      "science"
    ],
    "tools": [
      "minecraft",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/AI tutors are advancing quickly should you try one.md": {
    "tags": [
      "art",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "reading",
      "language",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "khan-academy",
      "ai-tutor"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The Weekly Rundown Learning Beyond School.md": {
    "tags": [
      "career",
      "curriculum",
      "coding",
      "music",
      "reading",
      "technology"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/108 - What happened in 2012.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "socialization",
      "reading",
      "stem",
      "technology",
      "microschool"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/058 - How to get your child to take you seriously as the tea.md": {
    "tags": [
      "career",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "microschool"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/046  Of Screen time and cliffhangers.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "nature-based",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/A psychologist explains why your kid is ignoring you.md": {
    "tags": [
      "art",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "socialization",
      "reading",
      "science",
      "assessment",
      "high-school",
      "adhd",
      "charlotte-mason"
    ],
    "tools": [
      "minecraft"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why Ansel Adams father pulled him out of school.md": {
    "tags": [
      "kindergarten",
      "career",
      "coding",
      "curriculum",
      "gifted",
      "socialization",
      "reading",
      "assessment",
      "history"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The boy who was supposed to fail.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "socialization",
      "reading",
      "stem",
      "special-needs",
      "adhd",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/She almost gave up on education.md": {
    "tags": [
      "art",
      "elementary",
      "high-school",
      "college-prep",
      "curriculum",
      "gifted",
      "middle-school",
      "writing",
      "reading",
      "music",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/When math finally clicks OED 109.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Handy guide to free curriculum.md": {
    "tags": [
      "career",
      "roadschooling",
      "gifted",
      "technology",
      "outdoor",
      "assessment",
      "college-prep",
      "science",
      "coding",
      "curriculum",
      "high-school",
      "art",
      "reading",
      "entrepreneurship",
      "math",
      "writing",
      "socialization",
      "language",
      "history",
      "special-needs"
    ],
    "tools": [
      "khan-academy",
      "outschool"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/097 - Dr Phil Just Mainstreamed Unschooling.md": {
    "tags": [
      "art",
      "waldorf",
      "career",
      "math",
      "socialization",
      "reading",
      "unschooling",
      "history",
      "technology",
      "assessment"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Everyone said hed fail He didnt.md": {
    "tags": [
      "art",
      "history",
      "career",
      "math",
      "writing",
      "socialization",
      "reading",
      "language",
      "high-school",
      "charlotte-mason"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Newton was right heres the proof.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "socialization",
      "writing",
      "reading",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The 228 IQ genius who warned us about schools.md": {
    "tags": [
      "math",
      "curriculum",
      "roadschooling",
      "reading",
      "assessment",
      "history"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/What we get wrong about socialization.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/082  Chores Before AP Scores.md": {
    "tags": [
      "art",
      "history",
      "college-prep",
      "career",
      "math",
      "writing",
      "music",
      "reading",
      "socialization",
      "assessment",
      "high-school",
      "technology",
      "adhd",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/A few questions about the launch of OpenEd.md": {
    "tags": [
      "career",
      "curriculum",
      "writing",
      "reading",
      "language",
      "technology",
      "college-prep"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Skip Stanford Buy a Business The New Success Formula 118.md": {
    "tags": [
      "entrepreneurship",
      "career",
      "math",
      "coding",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The false choice.md": {
    "tags": [
      "secular",
      "college-prep",
      "kindergarten",
      "career",
      "coding",
      "curriculum",
      "roadschooling",
      "middle-school",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "microschool"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/089 - When Teachers Stop Teaching.md": {
    "tags": [
      "classical-education",
      "college-prep",
      "career",
      "socialization",
      "writing",
      "reading",
      "assessment",
      "microschool"
    ],
    "tools": [
      "scratch"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/088 - The case against grammar worksheets and what to do ins.md": {
    "tags": [
      "history",
      "college-prep",
      "career",
      "project-based",
      "socialization",
      "reading",
      "language",
      "stem",
      "technology",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/080 - 3 words to transform conversations with your kids.md": {
    "tags": [
      "art",
      "high-school",
      "career",
      "math",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "college-prep"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Welcome to the OpenEd Daily.md": {
    "tags": [
      "preschool",
      "10-14-years",
      "entrepreneurship",
      "career",
      "microschool",
      "math",
      "curriculum",
      "reading",
      "assessment",
      "history",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The 5 fears killing your homeschool confidence.md": {
    "tags": [
      "college-prep",
      "career",
      "curriculum",
      "montessori",
      "socialization",
      "writing",
      "reading",
      "high-school",
      "microschool"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why art history grads are beating engineers.md": {
    "tags": [
      "art",
      "high-school",
      "history",
      "college-prep",
      "kindergarten",
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "montessori",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "khan-academy"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/037 - Obsessive interest can be a superpower.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "reading",
      "assessment",
      "history",
      "technology",
      "microschool"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Stop stressing Start designing A mom of 7 explains.md": {
    "tags": [
      "art",
      "high-school",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "montessori",
      "middle-school",
      "music",
      "reading",
      "science",
      "socialization",
      "assessment",
      "stem",
      "technology",
      "outdoor",
      "charlotte-mason"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Quick question for you.md": {
    "tags": [
      "assessment",
      "socialization",
      "reading",
      "curriculum"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/033 - ThoughtTrendTool Tldr Tuesday edition.md": {
    "tags": [
      "art",
      "forest-school",
      "entrepreneurship",
      "career",
      "socialization",
      "faith-based",
      "reading",
      "high-school",
      "technology",
      "outdoor",
      "college-prep"
    ],
    "tools": [
      "khan-academy",
      "ai-tutor"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/How to live a fulfilled life 136.md": {
    "tags": [
      "assessment",
      "high-school",
      "history",
      "reading"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/064 - Custom education for single and working parents.md": {
    "tags": [
      "art",
      "elementary",
      "history",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "steam",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "minecraft"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/When weird wins 129.md": {
    "tags": [
      "entrepreneurship",
      "career",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/What is a good job.md": {
    "tags": [
      "career",
      "coding",
      "reading",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The Great Enrollment Shuffle tldr Tuesday.md": {
    "tags": [
      "career",
      "microschool",
      "reading",
      "language",
      "stem",
      "technology",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Back-to-School Boost Brain Breaks  Resilient Kids.md": {
    "tags": [
      "art",
      "elementary",
      "career",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "technology"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/OpenEd Academy the school that adapts to YOUR child not the .md": {
    "tags": [
      "art",
      "high-school",
      "college-prep",
      "career",
      "math",
      "coding",
      "curriculum",
      "roadschooling",
      "writing",
      "music",
      "reading",
      "socialization",
      "language",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "outschool"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/107 - The death of labels in education.md": {
    "tags": [
      "entrepreneurship",
      "math",
      "curriculum",
      "gifted",
      "writing",
      "socialization",
      "reading",
      "unschooling",
      "high-school",
      "technology",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Science Doesnt Have to Be Boring.md": {
    "tags": [
      "career",
      "curriculum",
      "middle-school",
      "reading",
      "assessment",
      "high-school",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Skip College These Teens Already Have Their Degrees 130.md": {
    "tags": [
      "assessment",
      "college-prep",
      "entrepreneurship",
      "career",
      "microschool",
      "coding",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "language",
      "high-school",
      "technology",
      "adhd",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The conveyor belt to nowhere.md": {
    "tags": [
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "microschool",
      "curriculum",
      "middle-school",
      "writing",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Dyslexia guide two-hour school days and a 71B dropout.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "special-needs",
      "science"
    ],
    "tools": [
      "audiobook"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why learning should look like failing.md": {
    "tags": [
      "art",
      "career",
      "math",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "outdoor"
    ],
    "tools": [
      "chatgpt"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/A Stanford students take on AI vs Professors 122.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/105 - Kids arent lab rats.md": {
    "tags": [
      "elementary",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/22-year-old George Washingtons epic failure it didnt define .md": {
    "tags": [
      "art",
      "history",
      "math",
      "curriculum",
      "socialization",
      "music",
      "reading",
      "language",
      "high-school",
      "technology",
      "assessment",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/039 - Saying yes  cupcakes  recipe for success.md": {
    "tags": [
      "art",
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "coding",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "baketivity"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Raising kids who lead with compassion.md": {
    "tags": [
      "career",
      "curriculum",
      "roadschooling",
      "assessment",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Humans arent Model Ts.md": {
    "tags": [
      "career",
      "math",
      "science",
      "stem",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/084 - The real reason we assign homework.md": {
    "tags": [
      "classical-education",
      "career",
      "math",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/035 - Taste it Feel it Do it.md": {
    "tags": [
      "art",
      "career",
      "curriculum",
      "writing",
      "music",
      "assessment",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why Boys Are Falling Behind 126.md": {
    "tags": [
      "preschool",
      "college-prep",
      "entrepreneurship",
      "career",
      "microschool",
      "reading",
      "assessment",
      "technology",
      "adhd",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/067 - The perfect day is the enemy plus a 12-year-old built .md": {
    "tags": [
      "art",
      "career",
      "math",
      "curriculum",
      "socialization",
      "music",
      "reading",
      "language",
      "technology"
    ],
    "tools": [
      "duolingo",
      "minecraft",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/075 - How to create a high school transcript.md": {
    "tags": [
      "art",
      "history",
      "college-prep",
      "career",
      "curriculum",
      "roadschooling",
      "writing",
      "socialization",
      "reading",
      "language",
      "high-school",
      "outdoor",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/An open education day in the life.md": {
    "tags": [
      "career",
      "math",
      "curriculum",
      "reading",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/093 - Time isnt the teacher.md": {
    "tags": [
      "art",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "technology",
      "microschool"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The OpenEd Weekly Breaking Boundaries in Education.md": {
    "tags": [
      "high-school",
      "college-prep",
      "project-based",
      "coding",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Confession I played with LEGO instead of doing math.md": {
    "tags": [
      "career",
      "math",
      "curriculum",
      "reading",
      "assessment",
      "college-prep"
    ],
    "tools": [
      "lego"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/051  The 10-minute rule.md": {
    "tags": [
      "art",
      "forest-school",
      "career",
      "nature-based",
      "curriculum",
      "socialization",
      "reading",
      "high-school",
      "technology",
      "outdoor",
      "entrepreneurship"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Mark Twain summer reading edition.md": {
    "tags": [
      "art",
      "college-prep",
      "career",
      "socialization",
      "writing",
      "reading",
      "science"
    ],
    "tools": [
      "chatgpt"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why do we focus on the 10 when kids remember 95.md": {
    "tags": [
      "curriculum",
      "coding",
      "socialization",
      "reading",
      "language",
      "technology",
      "college-prep"
    ],
    "tools": [
      "ai-tutor",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/1 bestseller.md": {
    "tags": [
      "career",
      "curriculum",
      "montessori",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": [
      "khan-academy"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The 6-Hour School Day is a Lie.md": {
    "tags": [
      "assessment",
      "stem",
      "career",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why the trades pay 6 figures.md": {
    "tags": [
      "career",
      "curriculum",
      "reading",
      "high-school",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The Hidden Power of Feedback Loops 123.md": {
    "tags": [
      "college-prep",
      "career",
      "curriculum",
      "socialization",
      "reading",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/050 - The paradox of sacrifice.md": {
    "tags": [
      "art",
      "high-school",
      "forest-school",
      "college-prep",
      "career",
      "microschool",
      "nature-based",
      "curriculum",
      "socialization",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Mixed-age learning takes off 131.md": {
    "tags": [
      "waldorf",
      "montessori",
      "socialization",
      "reading",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Reading connects to everything.md": {
    "tags": [
      "college-prep",
      "career",
      "coding",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/061 - The ROI of Personalized Education.md": {
    "tags": [
      "career",
      "curriculum",
      "science",
      "assessment",
      "stem",
      "technology",
      "college-prep"
    ],
    "tools": [
      "khan-academy",
      "outschool",
      "time4learning"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Dave Ramsey Were fools about education.md": {
    "tags": [
      "entrepreneurship",
      "career",
      "curriculum",
      "socialization",
      "middle-school",
      "reading",
      "assessment",
      "high-school",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/3 kids 3 different schools 1 surprising lesson.md": {
    "tags": [
      "waldorf",
      "career",
      "roadschooling",
      "gifted",
      "montessori",
      "writing",
      "socialization",
      "reading",
      "technology",
      "outdoor",
      "entrepreneurship"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/095 - The Power of Yes And.md": {
    "tags": [
      "career",
      "socialization",
      "reading",
      "curriculum"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Study like a lion not like a cow.md": {
    "tags": [
      "career",
      "math",
      "reading",
      "language",
      "stem",
      "assessment",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Dont start with the chalkboard.md": {
    "tags": [
      "math",
      "curriculum",
      "roadschooling",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "outdoor",
      "college-prep"
    ],
    "tools": [
      "audiobook"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/074 - Try Different Not Harder.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "coding",
      "curriculum",
      "socialization",
      "music",
      "reading",
      "high-school",
      "adhd",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/What lawnmowers and baby cows can teach us.md": {
    "tags": [
      "entrepreneurship",
      "project-based",
      "math",
      "reading",
      "assessment",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Screens have taken over classrooms.md": {
    "tags": [
      "career",
      "math",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/099 - Your child doesnt hate learning heres whats really goi.md": {
    "tags": [
      "career",
      "curriculum",
      "coding",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "entrepreneurship"
    ],
    "tools": [
      "ai-tutor"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/College dropout becomes billionaire again.md": {
    "tags": [
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "coding",
      "roadschooling",
      "socialization",
      "reading",
      "assessment",
      "technology",
      "science"
    ],
    "tools": [
      "audiobook"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/How a 100000 bet against college created 11 billion-dollar c.md": {
    "tags": [
      "art",
      "career",
      "curriculum",
      "socialization",
      "reading",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The Great Phone Ban begins  115.md": {
    "tags": [
      "art",
      "history",
      "college-prep",
      "entrepreneurship",
      "career",
      "microschool",
      "coding",
      "steam",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Hands-on learning backyard chickens edition.md": {
    "tags": [
      "elementary",
      "college-prep",
      "entrepreneurship",
      "career",
      "project-based",
      "math",
      "curriculum",
      "gifted",
      "middle-school",
      "writing",
      "reading",
      "socialization",
      "assessment",
      "outdoor",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Have you considered not going to school.md": {
    "tags": [
      "high-school",
      "history",
      "college-prep",
      "career",
      "math",
      "socialization",
      "music",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Virtual school 10 vs 20 spot the difference.md": {
    "tags": [
      "art",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "gifted",
      "middle-school",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "science"
    ],
    "tools": [
      "outschool",
      "zoom",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The cure for childhood entitlement.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "socialization",
      "reading",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Deep Dive Classical Education Explained.md": {
    "tags": [
      "career",
      "roadschooling",
      "gifted",
      "faith-based",
      "technology",
      "assessment",
      "college-prep",
      "science",
      "elementary",
      "curriculum",
      "high-school",
      "art",
      "reading",
      "stem",
      "classical-education",
      "math",
      "middle-school",
      "writing",
      "socialization",
      "language",
      "history"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/038 - How to start a business with no ideas.md": {
    "tags": [
      "entrepreneurship",
      "career",
      "curriculum",
      "socialization",
      "writing",
      "technology",
      "outdoor",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Weekly Roundup Teen Success Stories 120.md": {
    "tags": [
      "high-school",
      "college-prep",
      "entrepreneurship",
      "microschool",
      "coding",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": [
      "chatgpt",
      "ai-tutor"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/087 - Screen Time Quality Over Quantity  SpaceXs Math Revolu.md": {
    "tags": [
      "career",
      "math",
      "gifted",
      "socialization",
      "reading",
      "assessment",
      "technology",
      "college-prep"
    ],
    "tools": [
      "ai-tutor"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Print books beat screens for memory.md": {
    "tags": [
      "career",
      "socialization",
      "writing",
      "reading",
      "language",
      "technology",
      "science"
    ],
    "tools": [
      "ai-tutor",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/4 post-COVID trends reshaping education.md": {
    "tags": [
      "history",
      "career",
      "curriculum",
      "socialization",
      "writing",
      "reading",
      "assessment",
      "stem",
      "technology",
      "outdoor"
    ],
    "tools": [
      "zoom"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/tldr Tuesday The New Science of Raising Happy Kids.md": {
    "tags": [
      "college-prep",
      "career",
      "curriculum",
      "reading",
      "assessment",
      "history",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/tldr Tuesday 100 million views and counting but.md": {
    "tags": [
      "assessment",
      "stem",
      "reading",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Is college the only path to success.md": {
    "tags": [
      "art",
      "history",
      "college-prep",
      "kindergarten",
      "career",
      "entrepreneurship",
      "math",
      "curriculum",
      "roadschooling",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/030 - Conditioning vs Education.md": {
    "tags": [
      "art",
      "waldorf",
      "forest-school",
      "college-prep",
      "career",
      "curriculum",
      "montessori",
      "socialization",
      "assessment",
      "technology",
      "outdoor",
      "microschool"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/041 - From dyslexic dropouts to doctoral degrees at 17.md": {
    "tags": [
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "coding",
      "curriculum",
      "writing",
      "reading",
      "assessment",
      "stem",
      "outdoor",
      "science"
    ],
    "tools": [
      "baketivity"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/When brain science meets education 135.md": {
    "tags": [
      "classical-education",
      "art",
      "college-prep",
      "career",
      "microschool",
      "math",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "language",
      "stem",
      "technology",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/What happens when a school actually trusts parents.md": {
    "tags": [
      "history",
      "career",
      "math",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/076 - The Four-Hour Revolution.md": {
    "tags": [
      "high-school",
      "career",
      "math",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/When not to quit music lessons.md": {
    "tags": [
      "career",
      "math",
      "music",
      "high-school",
      "technology"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Einstein had a tutor.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "curriculum",
      "gifted",
      "writing",
      "reading",
      "language",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "ai-tutor"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Protecting the Internal Spark.md": {
    "tags": [
      "art",
      "preschool",
      "high-school",
      "history",
      "college-prep",
      "kindergarten",
      "career",
      "math",
      "coding",
      "curriculum",
      "roadschooling",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "chatgpt"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/102 - Albert Einstein on his school and education system.md": {
    "tags": [
      "preschool",
      "history",
      "college-prep",
      "career",
      "coding",
      "curriculum",
      "socialization",
      "reading",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "outschool",
      "minecraft",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Thats not knowledge  MythBusters Adam Savage goes viral.md": {
    "tags": [
      "career",
      "gifted",
      "technology",
      "outdoor",
      "assessment",
      "college-prep",
      "science",
      "coding",
      "high-school",
      "charlotte-mason",
      "art",
      "music",
      "reading",
      "stem",
      "entrepreneurship",
      "math",
      "writing",
      "socialization",
      "language",
      "history"
    ],
    "tools": [
      "ai-tutor"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/How to make movies without a 200k degree 119.md": {
    "tags": [
      "art",
      "career",
      "curriculum",
      "gifted",
      "socialization",
      "reading",
      "assessment",
      "high-school"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/047 - Beyond mere choice.md": {
    "tags": [
      "art",
      "entrepreneurship",
      "career",
      "socialization",
      "reading",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Mommy did you get distracted too.md": {
    "tags": [
      "elementary",
      "kindergarten",
      "career",
      "middle-school",
      "music",
      "reading",
      "socialization",
      "assessment",
      "technology",
      "college-prep"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/094 - The fastest-growing trend in American education.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "curriculum",
      "middle-school",
      "socialization",
      "reading",
      "unschooling",
      "stem",
      "assessment",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/What happens when kids care.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "coding",
      "curriculum",
      "roadschooling",
      "middle-school",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/This mom turned a van into a microschool.md": {
    "tags": [
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "microschool",
      "coding",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Youre Not a Teacher Youre an Education Designer.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "curriculum",
      "writing",
      "socialization",
      "assessment",
      "stem",
      "technology",
      "adhd",
      "science"
    ],
    "tools": [
      "scratch"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/6 reasons kids say they hate school 135.md": {
    "tags": [
      "art",
      "forest-school",
      "history",
      "college-prep",
      "career",
      "project-based",
      "math",
      "curriculum",
      "gifted",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/049 - The necessary humility of Open Education.md": {
    "tags": [
      "art",
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "socialization",
      "reading",
      "unschooling",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/March 2020 The Month That Changed Everything 124.md": {
    "tags": [
      "history",
      "college-prep",
      "career",
      "microschool",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/George Washingtons epic failure.md": {
    "tags": [
      "art",
      "career",
      "math",
      "curriculum",
      "socialization",
      "music",
      "reading",
      "assessment",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Education needs a software update.md": {
    "tags": [
      "forest-school",
      "career",
      "roadschooling",
      "gifted",
      "technology",
      "outdoor",
      "college-prep",
      "science",
      "coding",
      "curriculum",
      "montessori",
      "high-school",
      "reading",
      "stem",
      "adhd",
      "entrepreneurship",
      "classical-education",
      "language",
      "math",
      "writing",
      "socialization",
      "assessment"
    ],
    "tools": [
      "scratch"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Steve Jobs cut 70 of products It saved Apple.md": {
    "tags": [
      "college-prep",
      "entrepreneurship",
      "career",
      "socialization",
      "writing",
      "reading",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why teen anxiety drops in May and spikes in August.md": {
    "tags": [
      "high-school",
      "forest-school",
      "assessment",
      "career",
      "nature-based",
      "math",
      "socialization",
      "reading",
      "language",
      "stem",
      "outdoor",
      "adhd",
      "college-prep"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Unbundling Education and Why It Matters.md": {
    "tags": [
      "art",
      "career",
      "project-based",
      "math",
      "coding",
      "curriculum",
      "roadschooling",
      "socialization",
      "reading",
      "assessment",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/CEO vs Gardener What kind of homeschool parent are you.md": {
    "tags": [
      "career",
      "curriculum",
      "reading",
      "unschooling",
      "high-school",
      "entrepreneurship"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Homeschooling year-round without burnout.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "curriculum",
      "reading",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/This school let its students design the campus 137.md": {
    "tags": [
      "art",
      "elementary",
      "forest-school",
      "career",
      "curriculum",
      "reading",
      "assessment",
      "outdoor"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The end of one-size-fits-all.md": {
    "tags": [
      "assessment",
      "stem",
      "reading",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Redefining Back-to-School.md": {
    "tags": [
      "career",
      "curriculum",
      "writing",
      "reading",
      "outdoor",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/031 - Weekly Roundup The Most-Watched Lesson Never Learned.md": {
    "tags": [
      "art",
      "worldschooling",
      "career",
      "microschool",
      "socialization",
      "reading",
      "unschooling",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why our book hit 1 hint thanks to you.md": {
    "tags": [
      "history",
      "career",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Shakespeare at 8 A neuroscientist explains 132.md": {
    "tags": [
      "classical-education",
      "college-prep",
      "career",
      "math",
      "writing",
      "reading",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Parenting Is a Learning Lab.md": {
    "tags": [
      "career",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/071 - Is reading a struggle Check for these signs.md": {
    "tags": [
      "art",
      "college-prep",
      "career",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "special-needs",
      "adhd",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Parents Guide to Homeschooling Students with Dyslexia.md": {
    "tags": [
      "art",
      "history",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "language",
      "stem",
      "technology",
      "special-needs",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/043 - The miracle ingredient in any environment.md": {
    "tags": [
      "art",
      "history",
      "college-prep",
      "career",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Parents as curators not classroom instructors.md": {
    "tags": [
      "microschool",
      "math",
      "curriculum",
      "roadschooling",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "khan-academy",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/073 - What comes first the lessons or the test.md": {
    "tags": [
      "career",
      "math",
      "coding",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "history",
      "technology"
    ],
    "tools": [
      "khan-academy",
      "ai-tutor"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Mythbusting one size fits all.md": {
    "tags": [
      "high-school",
      "assessment",
      "college-prep",
      "career",
      "curriculum",
      "middle-school",
      "writing",
      "reading",
      "socialization",
      "language",
      "stem",
      "technology",
      "outdoor",
      "adhd",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The 200-year-old mistake were still making.md": {
    "tags": [
      "art",
      "history",
      "college-prep",
      "career",
      "math",
      "assessment",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Personal tutors for all Sal Khans latest promise.md": {
    "tags": [
      "math",
      "writing",
      "reading",
      "language",
      "history",
      "technology",
      "assessment",
      "college-prep"
    ],
    "tools": [
      "khan-academy",
      "ai-tutor"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Open Education The Book Launch Countdown Begins.md": {
    "tags": [
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "microschool",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "faith-based",
      "unschooling",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "lego"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Will there be no more great physicists.md": {
    "tags": [
      "college-prep",
      "career",
      "reading",
      "language",
      "stem",
      "technology",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/060 - You dont need to find the right curriculum.md": {
    "tags": [
      "career",
      "curriculum",
      "reading",
      "assessment",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Stop raising well-rounded kids.md": {
    "tags": [
      "career",
      "math",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "entrepreneurship"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why kids forget what they learn in textbooks.md": {
    "tags": [
      "college-prep",
      "career",
      "curriculum",
      "socialization",
      "reading",
      "stem",
      "science"
    ],
    "tools": [
      "minecraft"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Balancing remote work and parenting.md": {
    "tags": [
      "career",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Tomorrow Break Free from One-Size-Fits-All Education Special.md": {
    "tags": [
      "high-school",
      "socialization",
      "reading",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/048 - From Moon Head to Main Character.md": {
    "tags": [
      "history",
      "career",
      "curriculum",
      "socialization",
      "reading",
      "high-school",
      "technology"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The 3-part remedy for burnout.md": {
    "tags": [
      "art",
      "career",
      "curriculum",
      "socialization",
      "music",
      "reading",
      "assessment",
      "charlotte-mason"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Tuttle Twins author on the two modes of learning.md": {
    "tags": [
      "high-school",
      "history",
      "college-prep",
      "entrepreneurship",
      "career",
      "microschool",
      "coding",
      "socialization",
      "reading",
      "stem",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/When to worry if your child is behind in reading.md": {
    "tags": [
      "waldorf",
      "college-prep",
      "kindergarten",
      "career",
      "curriculum",
      "roadschooling",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/No ChatGPT Until High School.md": {
    "tags": [
      "elementary",
      "high-school",
      "history",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "chatgpt",
      "ai-tutor"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/085 - The old man who outsmarted his bullies.md": {
    "tags": [
      "art",
      "history",
      "career",
      "coding",
      "montessori",
      "socialization",
      "music",
      "reading",
      "language",
      "high-school",
      "assessment",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Are we overcomplicating subtraction.md": {
    "tags": [
      "elementary",
      "preschool",
      "career",
      "math",
      "curriculum",
      "gifted",
      "socialization",
      "reading",
      "high-school"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Homeschooling doesnt mean what it used to.md": {
    "tags": [
      "art",
      "history",
      "microschool",
      "math",
      "curriculum",
      "writing",
      "music",
      "reading",
      "socialization",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "khan-academy"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Is Homeschooling the wrong word when youre only home 3 hours.md": {
    "tags": [
      "history",
      "college-prep",
      "career",
      "roadschooling",
      "socialization",
      "reading",
      "high-school",
      "special-needs",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Is a college degree still worth it.md": {
    "tags": [
      "entrepreneurship",
      "career",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/078 - Education  school.md": {
    "tags": [
      "art",
      "college-prep",
      "career",
      "math",
      "writing",
      "middle-school",
      "reading",
      "socialization",
      "assessment",
      "history",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/How to build a village so youre not doing it alone.md": {
    "tags": [
      "career",
      "technology",
      "outdoor",
      "assessment",
      "college-prep",
      "science",
      "elementary",
      "coding",
      "curriculum",
      "high-school",
      "charlotte-mason",
      "music",
      "reading",
      "stem",
      "math",
      "middle-school",
      "writing",
      "socialization",
      "language",
      "history"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Silicon Valleys education secret is leaking and its not codi.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "coding",
      "curriculum",
      "socialization",
      "reading",
      "unschooling",
      "technology",
      "assessment",
      "microschool"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/098 - What Einstein actually said about school.md": {
    "tags": [
      "history",
      "college-prep",
      "coding",
      "curriculum",
      "socialization",
      "reading",
      "unschooling",
      "stem",
      "assessment",
      "science"
    ],
    "tools": [
      "outschool",
      "minecraft"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/086 - The Element of Surprise.md": {
    "tags": [
      "elementary",
      "college-prep",
      "kindergarten",
      "career",
      "entrepreneurship",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "outdoor",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The hidden psychology of education shamers 112.md": {
    "tags": [
      "art",
      "high-school",
      "history",
      "college-prep",
      "career",
      "math",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/069 - Is your kid a night owl.md": {
    "tags": [
      "career",
      "math",
      "curriculum",
      "socialization",
      "reading",
      "assessment"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Kids begged for more math when teachers did this.md": {
    "tags": [
      "career",
      "math",
      "socialization",
      "music",
      "reading",
      "assessment",
      "outdoor"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The Lawnmower Fallacy.md": {
    "tags": [
      "high-school",
      "entrepreneurship",
      "career",
      "math",
      "reading",
      "assessment",
      "stem",
      "outdoor",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why weird kids win in adulthood.md": {
    "tags": [
      "college-prep",
      "career",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The Tebow Effect when being different pays off.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "curriculum",
      "gifted",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/We need to talk about educational autopilot.md": {
    "tags": [
      "high-school",
      "history",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "curriculum",
      "gifted",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/101 - When Builders Become Architects.md": {
    "tags": [
      "art",
      "high-school",
      "college-prep",
      "career",
      "socialization",
      "reading",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/090 - The 3 Rs Are All You Need.md": {
    "tags": [
      "high-school",
      "history",
      "college-prep",
      "career",
      "math",
      "coding",
      "curriculum",
      "gifted",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/When sit still stops working.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "roadschooling",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "adhd",
      "science"
    ],
    "tools": [
      "audiobook"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Matt Bowman  Youre a trailblazer.md": {
    "tags": [
      "career",
      "curriculum",
      "socialization",
      "science",
      "stem",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Valedictorians Confession Thats It The Empty Feeling at the .md": {
    "tags": [
      "college-prep",
      "career",
      "socialization",
      "reading",
      "assessment",
      "technology",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/From tree houses to chicken coops - learning by doing.md": {
    "tags": [
      "art",
      "history",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "socialization",
      "reading",
      "language",
      "stem",
      "technology",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Your child isnt broken but their chair might be.md": {
    "tags": [
      "socialization",
      "microschool",
      "reading",
      "curriculum"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/No One Right Way to Learn.md": {
    "tags": [
      "classical-education",
      "waldorf",
      "art",
      "career",
      "project-based",
      "coding",
      "curriculum",
      "montessori",
      "reading",
      "unschooling",
      "technology",
      "assessment"
    ],
    "tools": [
      "lego"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why your best ideas never come at a desk  110.md": {
    "tags": [
      "high-school",
      "forest-school",
      "college-prep",
      "kindergarten",
      "career",
      "entrepreneurship",
      "math",
      "coding",
      "curriculum",
      "socialization",
      "reading",
      "language",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/What OpenEd families are searching for in the marketplace.md": {
    "tags": [
      "career",
      "roadschooling",
      "faith-based",
      "technology",
      "assessment",
      "college-prep",
      "science",
      "elementary",
      "coding",
      "curriculum",
      "high-school",
      "art",
      "music",
      "reading",
      "stem",
      "microschool",
      "math",
      "middle-school",
      "socialization",
      "language",
      "history"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/A public school administrator shares the truth about homesch.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "curriculum",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/057 - Weekly Roundup.md": {
    "tags": [
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "adhd"
    ],
    "tools": [
      "khan-academy",
      "zoom",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/032 - The new success formula for teens.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "math",
      "coding",
      "curriculum",
      "assessment",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The math is broken Colleges ROI problem.md": {
    "tags": [
      "entrepreneurship",
      "career",
      "math",
      "reading",
      "high-school",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The OpenEd Weekly Rethinking Education from LeBron to Back-t.md": {
    "tags": [
      "art",
      "entrepreneurship",
      "career",
      "reading",
      "assessment",
      "stem",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": [
      "audiobook"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Is your child using outdated study habits 113.md": {
    "tags": [
      "career",
      "microschool",
      "math",
      "coding",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/070 - Yes youre qualified to teach your kids.md": {
    "tags": [
      "career",
      "coding",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "language",
      "high-school",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/079 - The Hidden Value of Chores.md": {
    "tags": [
      "history",
      "college-prep",
      "career",
      "gifted",
      "writing",
      "music",
      "reading",
      "socialization",
      "assessment",
      "high-school",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Can AI teach your kid to think.md": {
    "tags": [
      "art",
      "career",
      "math",
      "coding",
      "writing",
      "reading"
    ],
    "tools": [
      "khan-academy",
      "chatgpt",
      "ai-tutor"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Twain was right Dont let schooling interfere with your educa.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "coding",
      "roadschooling",
      "middle-school",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Weekly Roundup When Good Grades Hide Systemic Failure.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "coding",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "special-needs",
      "science"
    ],
    "tools": [
      "khan-academy",
      "chatgpt"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why Most Kids Hate Math and How to Fix It.md": {
    "tags": [
      "elementary",
      "career",
      "math",
      "curriculum",
      "middle-school",
      "socialization",
      "reading",
      "high-school",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/How schools fail the average kid.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "project-based",
      "math",
      "roadschooling",
      "gifted",
      "reading",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Stop overscheduling your childs learning.md": {
    "tags": [
      "math",
      "curriculum",
      "writing",
      "reading",
      "assessment",
      "high-school",
      "entrepreneurship"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Access 75000 free books without Amazon.md": {
    "tags": [
      "career",
      "curriculum",
      "reading",
      "assessment",
      "technology",
      "college-prep"
    ],
    "tools": [
      "youtube",
      "audiobook"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Mailbag Do You Need a Diploma for Success.md": {
    "tags": [
      "entrepreneurship",
      "career",
      "curriculum",
      "reading",
      "assessment",
      "high-school",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Nobel Prize winner I dont believe in honors.md": {
    "tags": [
      "assessment",
      "reading",
      "curriculum"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Minnesota AND Iowa  12 podcasts for busy parents.md": {
    "tags": [
      "art",
      "college-prep",
      "career",
      "microschool",
      "math",
      "nature-based",
      "socialization",
      "music",
      "reading",
      "assessment",
      "outdoor",
      "charlotte-mason"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why smart parents make bad education choices.md": {
    "tags": [
      "college-prep",
      "entrepreneurship",
      "career",
      "curriculum",
      "writing",
      "assessment",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/From 1 in 2500 to 1 in 31.md": {
    "tags": [
      "elementary",
      "career",
      "math",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "adhd",
      "college-prep"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Teaching outside the classroom.md": {
    "tags": [
      "art",
      "high-school",
      "career",
      "microschool",
      "curriculum",
      "music",
      "faith-based",
      "language",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The Power of Open Education.md": {
    "tags": [
      "art",
      "career",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "language",
      "technology",
      "outdoor",
      "assessment",
      "college-prep"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/He let his kids skip school They still made student council.md": {
    "tags": [
      "high-school",
      "entrepreneurship",
      "career",
      "roadschooling",
      "reading",
      "assessment",
      "stem",
      "college-prep"
    ],
    "tools": [
      "audiobook"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/No Kindle but heres another shot at winning.md": {
    "tags": [
      "career",
      "curriculum",
      "gifted",
      "socialization",
      "reading",
      "technology"
    ],
    "tools": [
      "kindle"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Skills Over Degrees The New Career Reality.md": {
    "tags": [
      "career",
      "technology",
      "outdoor",
      "assessment",
      "college-prep",
      "science",
      "coding",
      "curriculum",
      "montessori",
      "high-school",
      "charlotte-mason",
      "art",
      "reading",
      "stem",
      "entrepreneurship",
      "math",
      "writing",
      "socialization",
      "language",
      "history"
    ],
    "tools": [
      "ai-tutor"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/044 - The cliffhanger technique for read-alouds.md": {
    "tags": [
      "career",
      "socialization",
      "music",
      "reading",
      "assessment",
      "history",
      "technology",
      "charlotte-mason"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/This education trend has seen a 220 increase.md": {
    "tags": [
      "kindergarten",
      "career",
      "roadschooling",
      "technology",
      "outdoor",
      "assessment",
      "college-prep",
      "science",
      "curriculum",
      "montessori",
      "art",
      "waldorf",
      "music",
      "reading",
      "stem",
      "entrepreneurship",
      "microschool",
      "socialization",
      "language"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/092 - AI might be educations most patient assistant.md": {
    "tags": [
      "art",
      "career",
      "gifted",
      "socialization",
      "reading",
      "history",
      "technology"
    ],
    "tools": [
      "chatgpt",
      "ai-tutor"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/045 - Yes you are qualified to teach your child.md": {
    "tags": [
      "entrepreneurship",
      "career",
      "roadschooling",
      "socialization",
      "reading",
      "high-school",
      "technology",
      "college-prep"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Were spending billions to break something that came free.md": {
    "tags": [
      "career",
      "writing",
      "reading",
      "assessment",
      "stem",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/When parents go to jail for wanting better schools 111.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "coding",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Weekly Roundup How to build a self-managing family from a mo.md": {
    "tags": [
      "art",
      "high-school",
      "history",
      "college-prep",
      "career",
      "math",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "language",
      "stem",
      "technology",
      "special-needs",
      "assessment",
      "science"
    ],
    "tools": [
      "ai-tutor"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The OpenEd Weekly From LEGO learning to happy kids.md": {
    "tags": [
      "project-based",
      "math",
      "reading",
      "unschooling",
      "technology",
      "assessment",
      "science"
    ],
    "tools": [
      "lego"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/104 - 2025 The Year Learning Gets Personal.md": {
    "tags": [
      "math",
      "coding",
      "gifted",
      "socialization",
      "reading",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The 34 GPA Student Who Couldnt Read.md": {
    "tags": [
      "career",
      "math",
      "curriculum",
      "writing",
      "reading",
      "assessment",
      "stem",
      "technology",
      "special-needs",
      "science"
    ],
    "tools": [
      "khan-academy"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/My kids learned more when I backed off.md": {
    "tags": [
      "art",
      "elementary",
      "history",
      "kindergarten",
      "career",
      "math",
      "curriculum",
      "socialization",
      "music",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/103 - Boring businesses FTW.md": {
    "tags": [
      "entrepreneurship",
      "career",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Roadschoolers Rebels  Rooftop Classes.md": {
    "tags": [
      "art",
      "assessment",
      "college-prep",
      "career",
      "math",
      "coding",
      "curriculum",
      "roadschooling",
      "writing",
      "music",
      "reading",
      "socialization",
      "language",
      "history",
      "technology",
      "outdoor",
      "adhd",
      "science"
    ],
    "tools": [
      "khan-academy",
      "ai-tutor"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The Diploma Dilemma.md": {
    "tags": [
      "career",
      "curriculum",
      "roadschooling",
      "reading",
      "assessment",
      "high-school",
      "outdoor",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/068 - Why kids who learn at home dont get bullied as much.md": {
    "tags": [
      "career",
      "curriculum",
      "socialization",
      "reading",
      "technology",
      "microschool"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Breaking Writing Rules with Purpose 127.md": {
    "tags": [
      "college-prep",
      "coding",
      "curriculum",
      "gifted",
      "writing",
      "reading",
      "assessment",
      "technology",
      "special-needs",
      "microschool"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Its here.md": {
    "tags": [
      "history",
      "career",
      "math",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/How to influence your kid without controlling them.md": {
    "tags": [
      "music",
      "reading",
      "science",
      "stem",
      "microschool"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Tech-savvy teens will win the future.md": {
    "tags": [
      "high-school",
      "college-prep",
      "career",
      "microschool",
      "coding",
      "curriculum",
      "reading",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/034 - Pandemic Pods KaiPods and iPods.md": {
    "tags": [
      "career",
      "microschool",
      "curriculum",
      "music",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "outschool",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/083 - Is there life on MARS.md": {
    "tags": [
      "career",
      "project-based",
      "math",
      "coding",
      "curriculum",
      "roadschooling",
      "montessori",
      "writing",
      "socialization",
      "reading",
      "language",
      "stem",
      "technology",
      "special-needs",
      "assessment",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/She didnt know she couldnt do it.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "curriculum",
      "socialization",
      "assessment",
      "high-school",
      "microschool"
    ],
    "tools": [
      "khan-academy",
      "chatgpt"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Yes you are enough.md": {
    "tags": [
      "college-prep",
      "career",
      "curriculum",
      "socialization",
      "reading",
      "outdoor",
      "stem",
      "technology",
      "special-needs",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Deschooling vs Unschooling.md": {
    "tags": [
      "college-prep",
      "project-based",
      "writing",
      "unschooling",
      "stem",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Honey I Started a School The Microschool Revolution 143.md": {
    "tags": [
      "entrepreneurship",
      "career",
      "microschool",
      "curriculum",
      "socialization",
      "faith-based",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Create Before You Consume.md": {
    "tags": [
      "art",
      "history",
      "entrepreneurship",
      "career",
      "microschool",
      "coding",
      "curriculum",
      "roadschooling",
      "socialization",
      "reading",
      "language",
      "high-school",
      "technology",
      "assessment",
      "science"
    ],
    "tools": [
      "minecraft",
      "scratch",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Baby agency  transforming screen time 128.md": {
    "tags": [
      "career",
      "writing",
      "reading",
      "high-school",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/High school juniors landing 70k jobs.md": {
    "tags": [
      "entrepreneurship",
      "career",
      "roadschooling",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The case for MORE screens.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "coding",
      "curriculum",
      "roadschooling",
      "middle-school",
      "writing",
      "reading",
      "socialization",
      "assessment",
      "high-school",
      "technology",
      "science"
    ],
    "tools": [
      "outschool",
      "minecraft",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/When someone asks if you homeschool.md": {
    "tags": [
      "entrepreneurship",
      "math",
      "curriculum",
      "reading",
      "language",
      "technology",
      "outdoor",
      "college-prep"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Measure learning not teaching.md": {
    "tags": [
      "elementary",
      "career",
      "math",
      "curriculum",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": [
      "khan-academy",
      "ixl"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/072 - Weekly Roundup From Bullies to Night Owls.md": {
    "tags": [
      "career",
      "math",
      "coding",
      "curriculum",
      "socialization",
      "reading",
      "outdoor",
      "technology",
      "special-needs",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/054 - Why your GPA might not matter anymore according to Goo.md": {
    "tags": [
      "entrepreneurship",
      "career",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "technology",
      "adhd",
      "college-prep"
    ],
    "tools": [
      "zoom"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The Simple Formula Behind Reading Success 141.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "reading",
      "language",
      "stem",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/3 ways to cut teaching time in half without sacrificing resu.md": {
    "tags": [
      "art",
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "math",
      "coding",
      "curriculum",
      "writing",
      "music",
      "reading",
      "socialization",
      "language",
      "stem",
      "technology",
      "outdoor",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Im terrible at math but need to teach it one moms solution.md": {
    "tags": [
      "career",
      "math",
      "curriculum",
      "reading",
      "assessment",
      "history",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/New Jersey Governor Enough is Enough 114.md": {
    "tags": [
      "art",
      "history",
      "college-prep",
      "career",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "outdoor",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The factory model of education is dying.md": {
    "tags": [
      "art",
      "career",
      "writing",
      "socialization",
      "reading",
      "language",
      "stem",
      "college-prep"
    ],
    "tools": [
      "duolingo"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Is the school year obsolete.md": {
    "tags": [
      "elementary",
      "high-school",
      "history",
      "college-prep",
      "career",
      "project-based",
      "microschool",
      "coding",
      "curriculum",
      "roadschooling",
      "montessori",
      "middle-school",
      "writing",
      "reading",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/How to get a job without applying for one.md": {
    "tags": [
      "career",
      "curriculum",
      "socialization",
      "writing",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The future-proof career prep guide for teens.md": {
    "tags": [
      "high-school",
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "socialization",
      "reading",
      "assessment",
      "stem",
      "outdoor",
      "adhd",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Weekly Roundup The College ROI Question.md": {
    "tags": [
      "college-prep",
      "entrepreneurship",
      "career",
      "project-based",
      "math",
      "coding",
      "curriculum",
      "gifted",
      "writing",
      "socialization",
      "reading",
      "language",
      "high-school",
      "technology",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/055 - How do I know if were learning anything without grades.md": {
    "tags": [
      "art",
      "career",
      "roadschooling",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/My kid cant read yet Should I panic.md": {
    "tags": [
      "career",
      "math",
      "curriculum",
      "reading",
      "assessment",
      "technology",
      "college-prep"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/040 - How to encourage reluctant readers.md": {
    "tags": [
      "art",
      "college-prep",
      "math",
      "coding",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "language",
      "high-school",
      "technology",
      "assessment",
      "science"
    ],
    "tools": [
      "lego",
      "youtube",
      "audiobook"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/106 - The science behind movement and memory.md": {
    "tags": [
      "forest-school",
      "kindergarten",
      "career",
      "curriculum",
      "socialization",
      "reading",
      "stem",
      "outdoor",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The 3-day school week 116.md": {
    "tags": [
      "college-prep",
      "career",
      "socialization",
      "writing",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/How to teach calculus like a pro even if youre not a math pe.md": {
    "tags": [
      "preschool",
      "career",
      "gifted",
      "technology",
      "college-prep",
      "science",
      "elementary",
      "coding",
      "curriculum",
      "high-school",
      "art",
      "waldorf",
      "reading",
      "unschooling",
      "stem",
      "math",
      "socialization",
      "assessment",
      "history"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Worldschooling Without the Plane Ticket.md": {
    "tags": [
      "art",
      "career",
      "math",
      "reading",
      "assessment",
      "technology",
      "outdoor",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why kids lose their love of learning 134.md": {
    "tags": [
      "art",
      "elementary",
      "career",
      "microschool",
      "curriculum",
      "writing",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The morning routine thats tearing families apart 138.md": {
    "tags": [
      "career",
      "curriculum",
      "reading",
      "assessment",
      "technology",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The 4-minute video that teaches quadratic equations better t.md": {
    "tags": [
      "math",
      "reading",
      "assessment",
      "high-school",
      "special-needs"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why your explanations arent clicking and the simple fix.md": {
    "tags": [
      "career",
      "math",
      "curriculum",
      "reading",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/066 - Doing division with a Star Wars twist.md": {
    "tags": [
      "art",
      "college-prep",
      "career",
      "math",
      "writing",
      "reading",
      "language",
      "technology",
      "assessment",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/His Tremor Tanked His Art Then It Made Him.md": {
    "tags": [
      "art",
      "career",
      "microschool",
      "curriculum",
      "montessori",
      "socialization",
      "reading",
      "stem",
      "technology",
      "charlotte-mason"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Great writers think first.md": {
    "tags": [
      "college-prep",
      "entrepreneurship",
      "socialization",
      "writing",
      "reading",
      "assessment",
      "technology",
      "microschool"
    ],
    "tools": [
      "audiobook"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Bigfoot Wizard Cooking and a Minecraft Modding Class.md": {
    "tags": [
      "college-prep",
      "career",
      "microschool",
      "math",
      "coding",
      "curriculum",
      "socialization",
      "reading",
      "stem",
      "technology",
      "science"
    ],
    "tools": [
      "outschool",
      "minecraft",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why bored kids are winning.md": {
    "tags": [
      "career",
      "math",
      "curriculum",
      "socialization",
      "reading",
      "assessment",
      "charlotte-mason"
    ],
    "tools": [
      "minecraft"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Weekly Roundup A Brief Guide to Building Educational Micro-c.md": {
    "tags": [
      "high-school",
      "college-prep",
      "entrepreneurship",
      "career",
      "microschool",
      "math",
      "coding",
      "curriculum",
      "roadschooling",
      "writing",
      "music",
      "reading",
      "socialization",
      "language",
      "stem",
      "technology",
      "assessment",
      "science"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/081 - To shield or to share That is the question.md": {
    "tags": [
      "art",
      "entrepreneurship",
      "career",
      "math",
      "steam",
      "socialization",
      "music",
      "reading",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The OpenEd Store is now LIVE.md": {
    "tags": [
      "high-school",
      "history",
      "college-prep",
      "career",
      "microschool",
      "math",
      "curriculum",
      "gifted",
      "middle-school",
      "socialization",
      "assessment",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The 150k teenage side-hustle 119.md": {
    "tags": [
      "entrepreneurship",
      "career",
      "socialization",
      "middle-school",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "college-prep"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why classical education is making a comeback.md": {
    "tags": [
      "classical-education",
      "art",
      "history",
      "college-prep",
      "kindergarten",
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "gifted",
      "writing",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "technology",
      "charlotte-mason"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Matt Bowman  What if we graded LeBron James like a student.md": {
    "tags": [
      "career",
      "curriculum",
      "reading",
      "assessment",
      "college-prep"
    ],
    "tools": [
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/A fresh look at classical education 133.md": {
    "tags": [
      "art",
      "classical-education",
      "entrepreneurship",
      "career",
      "math",
      "curriculum",
      "gifted",
      "reading",
      "assessment",
      "technology",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/100 - Win a FREE family baking kit ends Friday.md": {
    "tags": [
      "math",
      "coding",
      "writing",
      "socialization",
      "reading",
      "unschooling",
      "high-school",
      "technology",
      "assessment",
      "college-prep"
    ],
    "tools": [
      "baketivity",
      "lego"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why John Taylor Gatto Quit.md": {
    "tags": [
      "art",
      "history",
      "career",
      "curriculum",
      "reading",
      "assessment",
      "stem",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/052 - I wish school had taught me that.md": {
    "tags": [
      "art",
      "career",
      "curriculum",
      "roadschooling",
      "socialization",
      "reading",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The four types of screen time.md": {
    "tags": [
      "entrepreneurship",
      "career",
      "roadschooling",
      "socialization",
      "reading",
      "assessment",
      "high-school",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/091 - We are in Kansas anymore.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "curriculum",
      "writing",
      "socialization",
      "reading",
      "language",
      "history",
      "technology",
      "assessment",
      "microschool"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why 15 million students are in microschools now.md": {
    "tags": [
      "career",
      "roadschooling",
      "faith-based",
      "technology",
      "outdoor",
      "assessment",
      "college-prep",
      "science",
      "elementary",
      "project-based",
      "nature-based",
      "curriculum",
      "montessori",
      "high-school",
      "secular",
      "reading",
      "unschooling",
      "stem",
      "entrepreneurship",
      "microschool",
      "math",
      "language",
      "special-needs"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/How savvy parents are tutoring their kids.md": {
    "tags": [
      "career",
      "socialization",
      "reading",
      "assessment",
      "special-needs",
      "science"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The Homeschool-to-Founder Pipeline.md": {
    "tags": [
      "college-prep",
      "entrepreneurship",
      "career",
      "curriculum",
      "coding",
      "reading",
      "language",
      "technology",
      "assessment",
      "microschool"
    ],
    "tools": [
      "audiobook"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/042 - What parents and teens think about screen time.md": {
    "tags": [
      "career",
      "math",
      "nature-based",
      "curriculum",
      "socialization",
      "reading",
      "high-school",
      "technology",
      "outdoor",
      "microschool"
    ],
    "tools": [
      "minecraft"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Textbooks vs Chromebooks.md": {
    "tags": [
      "career",
      "math",
      "curriculum",
      "socialization",
      "reading",
      "technology"
    ],
    "tools": [
      "audiobook"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/036 - Weekly Roundup The new success formula for teens.md": {
    "tags": [
      "college-prep",
      "career",
      "math",
      "curriculum",
      "roadschooling",
      "socialization",
      "assessment",
      "high-school",
      "technology",
      "microschool"
    ],
    "tools": [
      "outschool",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/The 5 real gaps homeschooling creates.md": {
    "tags": [
      "art",
      "career",
      "reading",
      "assessment",
      "high-school",
      "technology"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Are we making our kids more anxious by keeping them safe.md": {
    "tags": [
      "entrepreneurship",
      "career",
      "math",
      "curriculum",
      "socialization",
      "writing",
      "reading",
      "faith-based",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/063 - Math without the misery.md": {
    "tags": [
      "art",
      "math",
      "curriculum",
      "socialization",
      "music",
      "reading",
      "faith-based",
      "assessment",
      "high-school",
      "outdoor"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Print Your Own Diploma Weekly Roundup.md": {
    "tags": [
      "career",
      "roadschooling",
      "gifted",
      "technology",
      "assessment",
      "college-prep",
      "science",
      "coding",
      "curriculum",
      "high-school",
      "art",
      "reading",
      "unschooling",
      "stem",
      "math",
      "writing",
      "socialization",
      "language",
      "history"
    ],
    "tools": [
      "outschool",
      "youtube"
    ]
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Deep Dive How to Start Homeschooling With Confidence.md": {
    "tags": [
      "career",
      "math",
      "curriculum",
      "socialization",
      "writing",
      "reading",
      "assessment",
      "outdoor",
      "college-prep"
    ],
    "tools": []
  },
  "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Master Content Database/Daily Newsletters/Why are Tech CEOs sounding more like 90s homeschool moms.md": {
    "tags": [
      "elementary",
      "high-school",
      "career",
      "microschool",
      "curriculum",
      "roadschooling",
      "montessori",
      "middle-school",
      "writing",
      "reading",
      "stem",
      "technology",
      "science"
    ],
    "tools": []
  }
}

def update_file(file_path, tags, tools):
    """Update a single file's frontmatter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract existing frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if frontmatter_match:
            metadata = yaml.safe_load(frontmatter_match.group(1))
            body = content[frontmatter_match.end():]
        else:
            print(f"No frontmatter found in {file_path}")
            return False
        
        # Add tags right after title
        metadata['tags'] = tags
        if tools:
            metadata['tools'] = tools
        
        # Rebuild file with updated frontmatter
        # Order matters: title, tags, tools, then rest
        ordered_metadata = {'title': metadata.get('title', '')}
        ordered_metadata['tags'] = tags
        if tools:
            ordered_metadata['tools'] = tools
        
        # Add remaining fields
        for key, value in metadata.items():
            if key not in ['title', 'tags', 'tools']:
                ordered_metadata[key] = value
        
        # Write back
        new_content = "---\n"
        new_content += yaml.dump(ordered_metadata, default_flow_style=False, allow_unicode=True)
        new_content += "---\n"
        new_content += body
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"Error updating {file_path}: {str(e)}")
        return False

# Process updates
successful = 0
for file_path, data in updates.items():
    if update_file(file_path, data['tags'], data['tools']):
        successful += 1

print(f"Successfully updated {successful}/{len(updates)} files")
