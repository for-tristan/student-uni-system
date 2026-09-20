// ============================================================
// Smart University Assistant — shared mock academic data
// Realistic, restrained, no marketing fluff.
// ============================================================

export type Difficulty = "Introductory" | "Intermediate" | "Advanced";

export type Course = {
  code: string;
  name: string;
  category: string;
  credits: number;
  difficulty: Difficulty;
  prerequisites: string[];
  skills: string[];
  enrolled: number;
  capacity: number;
  matchScore?: number;
  matchReasons?: string[];
  status?: "completed" | "in-progress" | "available";
  grade?: string;
  semester?: string;
};

export const STUDENT = {
  id: "S-2023-1148",
  name: "Ahmed Samir",
  email: "ahmed.samir@uni.edu",
  major: "Computer Science",
  year: "Year 3",
  gpa: 3.74,
  creditsCompleted: 84,
  creditsRequired: 132,
  creditsInProgress: 12,
  graduation: "Spring 2026",
  interests: ["Artificial Intelligence", "Distributed Systems", "Data Engineering"],
  skills: [
    "Python",
    "Java",
    "Statistics",
    "Algorithms",
    "SQL",
    "Linux",
  ],
};

export const COURSES: Course[] = [
  {
    code: "CS-421",
    name: "Machine Learning",
    category: "AI",
    credits: 3,
    difficulty: "Advanced",
    prerequisites: ["CS-221", "MATH-204"],
    skills: ["Python", "Statistics", "Algorithms"],
    enrolled: 118,
    capacity: 130,
    matchScore: 92,
    matchReasons: [
      "Matches your AI interest",
      "Matches existing skills",
      "Prerequisites completed",
    ],
  },
  {
    code: "CS-432",
    name: "Data Mining",
    category: "AI",
    credits: 3,
    difficulty: "Advanced",
    prerequisites: ["CS-221", "MATH-204"],
    skills: ["Python", "Statistics", "SQL"],
    enrolled: 96,
    capacity: 110,
    matchScore: 88,
    matchReasons: [
      "Matches your AI interest",
      "Matches your Data Engineering interest",
    ],
  },
  {
    code: "CS-371",
    name: "Distributed Systems",
    category: "Systems",
    credits: 4,
    difficulty: "Advanced",
    prerequisites: ["CS-211", "CS-301"],
    skills: ["Java", "Linux", "Algorithms"],
    enrolled: 64,
    capacity: 70,
    matchScore: 84,
    matchReasons: [
      "Matches your Distributed Systems interest",
      "Prerequisites completed",
    ],
  },
  {
    code: "CS-352",
    name: "Database Systems II",
    category: "Data",
    credits: 3,
    difficulty: "Intermediate",
    prerequisites: ["CS-251"],
    skills: ["SQL", "Python", "Java"],
    enrolled: 88,
    capacity: 100,
    matchScore: 79,
    matchReasons: [
      "Matches your Data Engineering interest",
      "Matches existing skills",
    ],
  },
  {
    code: "CS-460",
    name: "Computer Vision",
    category: "AI",
    credits: 3,
    difficulty: "Advanced",
    prerequisites: ["CS-221", "MATH-204"],
    skills: ["Python", "Algorithms", "Statistics"],
    enrolled: 72,
    capacity: 80,
    matchScore: 74,
    matchReasons: ["Matches your AI interest", "Prerequisites completed"],
  },
  {
    code: "CS-385",
    name: "Cloud Computing",
    category: "Systems",
    credits: 3,
    difficulty: "Intermediate",
    prerequisites: ["CS-211"],
    skills: ["Linux", "Python", "Java"],
    enrolled: 102,
    capacity: 110,
    matchScore: 71,
    matchReasons: ["Matches your Distributed Systems interest"],
  },
  {
    code: "MATH-204",
    name: "Probability & Statistics",
    category: "Mathematics",
    credits: 3,
    difficulty: "Intermediate",
    prerequisites: ["MATH-103"],
    skills: ["Statistics"],
    enrolled: 240,
    capacity: 240,
    status: "completed",
    grade: "A-",
    semester: "Fall 2024",
  },
  {
    code: "CS-221",
    name: "Algorithms",
    category: "Computer Science",
    credits: 4,
    difficulty: "Intermediate",
    prerequisites: ["CS-101"],
    skills: ["Algorithms", "Java"],
    enrolled: 180,
    capacity: 180,
    status: "completed",
    grade: "A",
    semester: "Spring 2024",
  },
  {
    code: "CS-251",
    name: "Database Systems I",
    category: "Data",
    credits: 3,
    difficulty: "Intermediate",
    prerequisites: ["CS-101"],
    skills: ["SQL", "Java"],
    enrolled: 156,
    capacity: 160,
    status: "completed",
    grade: "A-",
    semester: "Fall 2024",
  },
  {
    code: "CS-101",
    name: "Introduction to Computing",
    category: "Computer Science",
    credits: 3,
    difficulty: "Introductory",
    prerequisites: [],
    skills: ["Python"],
    enrolled: 320,
    capacity: 320,
    status: "completed",
    grade: "A",
    semester: "Fall 2022",
  },
  {
    code: "CS-301",
    name: "Operating Systems",
    category: "Systems",
    credits: 4,
    difficulty: "Advanced",
    prerequisites: ["CS-211"],
    skills: ["Linux", "C", "Algorithms"],
    enrolled: 90,
    capacity: 90,
    status: "in-progress",
  },
  {
    code: "CS-322",
    name: "Software Engineering",
    category: "Computer Science",
    credits: 3,
    difficulty: "Intermediate",
    prerequisites: ["CS-221"],
    skills: ["Java", "Python"],
    enrolled: 110,
    capacity: 120,
    status: "in-progress",
  },
];

export function getCourse(code: string): Course | undefined {
  return COURSES.find((c) => c.code === code);
}

export const RECOMMENDED = COURSES.filter((c) => c.matchScore)
  .sort((a, b) => (b.matchScore ?? 0) - (a.matchScore ?? 0));

export const COMPLETED = COURSES.filter((c) => c.status === "completed");
export const IN_PROGRESS = COURSES.filter((c) => c.status === "in-progress");

// ---- Admin (staff) data ------------------------------------

export const STAFF_STATS = {
  students: 1248,
  courses: 86,
  recommendationsToday: 312,
  activeConversations: 47,
  precisionAt5: 0.78,
  recallAt5: 0.64,
  avgCoverage: 0.81,
};

export const POPULAR_COURSES = [
  { code: "CS-101", name: "Introduction to Computing", enrolled: 320, trend: +6 },
  { code: "CS-221", name: "Algorithms", enrolled: 180, trend: +4 },
  { code: "MATH-204", name: "Probability & Statistics", enrolled: 240, trend: +2 },
  { code: "CS-421", name: "Machine Learning", enrolled: 118, trend: +18 },
  { code: "CS-352", name: "Database Systems II", enrolled: 88, trend: -3 },
];

export const RECOMMENDATION_TREND = [
  { day: "Mon", count: 218 },
  { day: "Tue", count: 244 },
  { day: "Wed", count: 312 },
  { day: "Thu", count: 286 },
  { day: "Fri", count: 271 },
  { day: "Sat", count: 152 },
  { day: "Sun", count: 119 },
];

export const STUDENTS = [
  {
    id: "S-2023-1148",
    name: "Ahmed Samir",
    major: "Computer Science",
    year: "Year 3",
    status: "Active",
    gpa: 3.74,
  },
  {
    id: "S-2022-0934",
    name: "Layla Hassan",
    major: "Computer Science",
    year: "Year 4",
    status: "Active",
    gpa: 3.88,
  },
  {
    id: "S-2023-2210",
    name: "Omar Khaled",
    major: "Data Science",
    year: "Year 3",
    status: "Active",
    gpa: 3.51,
  },
  {
    id: "S-2024-0512",
    name: "Mariam Tarek",
    major: "Software Engineering",
    year: "Year 2",
    status: "Probation",
    gpa: 2.41,
  },
  {
    id: "S-2022-0779",
    name: "Yousef Adel",
    major: "Computer Science",
    year: "Year 4",
    status: "Active",
    gpa: 3.62,
  },
  {
    id: "S-2023-1903",
    name: "Salma Nabil",
    major: "Data Science",
    year: "Year 3",
    status: "Inactive",
    gpa: 3.05,
  },
  {
    id: "S-2024-0887",
    name: "Karim Magdy",
    major: "Cybersecurity",
    year: "Year 2",
    status: "Active",
    gpa: 3.31,
  },
  {
    id: "S-2021-0644",
    name: "Nour Amr",
    major: "Computer Science",
    year: "Year 4",
    status: "Active",
    gpa: 3.95,
  },
  {
    id: "S-2023-3320",
    name: "Hana Mahmoud",
    major: "Software Engineering",
    year: "Year 3",
    status: "Active",
    gpa: 3.69,
  },
  {
    id: "S-2024-1190",
    name: "Ziad Tamer",
    major: "Cybersecurity",
    year: "Year 1",
    status: "Active",
    gpa: 3.10,
  },
];

// ---- Assistant conversation -------------------------------

export type AssistantMessage = {
  role: "user" | "assistant";
  content: string;
  sources?: { label: string; code?: string }[];
};

export const ASSISTANT_CONVERSATION: AssistantMessage[] = [
  {
    role: "user",
    content: "What are the prerequisites for Machine Learning?",
  },
  {
    role: "assistant",
    content:
      "Machine Learning (CS-421) requires the following prerequisites:\n\n1. Algorithms (CS-221) — you completed this with grade A.\n2. Probability & Statistics (MATH-204) — you completed this with grade A-.\n\nBoth prerequisites are satisfied, so you are eligible to enroll.",
    sources: [
      { label: "Course catalog", code: "CS-421" },
      { label: "Your transcript", code: "S-2023-1148" },
    ],
  },
  {
    role: "user",
    content: "Which courses can I take next semester?",
  },
  {
    role: "assistant",
    content:
      "Based on your completed courses and current skills, the following courses are available next semester:\n\n• Machine Learning (CS-421) — Advanced, 3 credits\n• Data Mining (CS-432) — Advanced, 3 credits\n• Distributed Systems (CS-371) — Advanced, 4 credits\n• Database Systems II (CS-352) — Intermediate, 3 credits\n\nYou can enroll in up to 18 credits without dean approval.",
    sources: [
      { label: "Course catalog", code: "Fall 2025" },
      { label: "Academic regulations", code: "§4.2" },
    ],
  },
];

export const SUGGESTED_PROMPTS = [
  "What are the prerequisites for Machine Learning?",
  "Which courses can I take next semester?",
  "What courses have I completed?",
  "Explain the Data Mining course to me.",
  "How many credits do I have left?",
];

// ---- Foundations / Typography helpers ---------------------

export const TYPE_SCALE = [
  { token: "display", size: "34 / 40", weight: 600, className: "text-[34px] leading-[40px] font-semibold tracking-[-0.01em]" },
  { token: "h1", size: "26 / 32", weight: 600, className: "text-[26px] leading-[32px] font-semibold tracking-[-0.01em]" },
  { token: "h2", size: "20 / 28", weight: 600, className: "text-[20px] leading-[28px] font-semibold" },
  { token: "h3", size: "16 / 24", weight: 600, className: "text-base font-semibold" },
  { token: "body", size: "14 / 22", weight: 400, className: "text-sm leading-[22px]" },
  { token: "small", size: "13 / 20", weight: 400, className: "text-[13px] leading-[20px]" },
  { token: "label", size: "12 / 16", weight: 500, className: "text-xs font-medium" },
  { token: "caption", size: "11 / 16", weight: 500, className: "text-[11px] font-medium uppercase tracking-[0.06em]" },
];

export const SPACING = [4, 8, 12, 16, 24, 32, 40, 48, 64, 80];

export const PALETTE = [
  { name: "Background", value: "#F7F7F5", usage: "Application background, behind everything" },
  { name: "Surface", value: "#FFFFFF", usage: "Cards, panels, tables" },
  { name: "Surface raised", value: "#FAFAF8", usage: "Hover rows, hover toolbar" },
  { name: "Border", value: "#E4E4E1", usage: "Separators, table lines, input borders" },
  { name: "Primary text", value: "#171717", usage: "Headlines, course names, key data" },
  { name: "Secondary text", value: "#666666", usage: "Metadata, captions, helper text" },
  { name: "Tertiary text", value: "#9A9A96", usage: "Placeholders, disabled" },
  { name: "Accent", value: "#315CFF", usage: "Primary actions, links, focus ring" },
  { name: "Accent surface", value: "#EEF1FF", usage: "Selected nav, subtle highlight" },
  { name: "Success", value: "#2F7D4A", usage: "Completed, prerequisites met" },
  { name: "Warning", value: "#A66A00", usage: "Probation, missing prerequisites" },
  { name: "Error", value: "#B42318", usage: "Fail, error states, destructive" },
];
