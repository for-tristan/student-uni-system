// lib/data/models.dart
// Smart University Assistant — Dart models + mock data.

enum Difficulty { introductory, intermediate, advanced }
enum CourseStatus { completed, inProgress, available }

class Course {
  final String code;
  final String name;
  final String category;
  final int credits;
  final Difficulty difficulty;
  final List<String> prerequisites;
  final List<String> skills;
  final int enrolled;
  final int capacity;
  final int? matchScore;
  final List<String>? matchReasons;
  final CourseStatus? status;
  final String? grade;
  final String? semester;

  const Course({
    required this.code,
    required this.name,
    required this.category,
    required this.credits,
    required this.difficulty,
    required this.prerequisites,
    required this.skills,
    required this.enrolled,
    required this.capacity,
    this.matchScore,
    this.matchReasons,
    this.status,
    this.grade,
    this.semester,
  });

  String get difficultyLabel {
    switch (difficulty) {
      case Difficulty.introductory: return 'Introductory';
      case Difficulty.intermediate: return 'Intermediate';
      case Difficulty.advanced: return 'Advanced';
    }
  }
}

class Student {
  final String id;
  final String name;
  final String email;
  final String major;
  final String year;
  final double gpa;
  final int creditsCompleted;
  final int creditsRequired;
  final int creditsInProgress;
  final String graduation;
  final List<String> interests;
  final List<String> skills;

  const Student({
    required this.id,
    required this.name,
    required this.email,
    required this.major,
    required this.year,
    required this.gpa,
    required this.creditsCompleted,
    required this.creditsRequired,
    required this.creditsInProgress,
    required this.graduation,
    required this.interests,
    required this.skills,
  });
}

class AssistantMessage {
  final String role; // 'user' | 'assistant'
  final String content;
  final List<SourceRef>? sources;

  const AssistantMessage({required this.role, required this.content, this.sources});
}

class SourceRef {
  final String label;
  final String? code;
  const SourceRef({required this.label, this.code});
}

const student = Student(
  id: 'S-2023-1148',
  name: 'Ahmed Samir',
  email: 'ahmed.samir@uni.edu',
  major: 'Computer Science',
  year: 'Year 3',
  gpa: 3.74,
  creditsCompleted: 84,
  creditsRequired: 132,
  creditsInProgress: 12,
  graduation: 'Spring 2026',
  interests: ['Artificial Intelligence', 'Distributed Systems', 'Data Engineering'],
  skills: ['Python', 'Java', 'Statistics', 'Algorithms', 'SQL', 'Linux'],
);

const courses = <Course>[
  Course(
    code: 'CS-421',
    name: 'Machine Learning',
    category: 'AI',
    credits: 3,
    difficulty: Difficulty.advanced,
    prerequisites: ['CS-221', 'MATH-204'],
    skills: ['Python', 'Statistics', 'Algorithms'],
    enrolled: 118, capacity: 130,
    matchScore: 92,
    matchReasons: [
      'Matches your AI interest',
      'Matches existing skills',
      'Prerequisites completed',
    ],
  ),
  Course(
    code: 'CS-432',
    name: 'Data Mining',
    category: 'AI',
    credits: 3,
    difficulty: Difficulty.advanced,
    prerequisites: ['CS-221', 'MATH-204'],
    skills: ['Python', 'Statistics', 'SQL'],
    enrolled: 96, capacity: 110,
    matchScore: 88,
    matchReasons: [
      'Matches your AI interest',
      'Matches your Data Engineering interest',
    ],
  ),
  Course(
    code: 'CS-371',
    name: 'Distributed Systems',
    category: 'Systems',
    credits: 4,
    difficulty: Difficulty.advanced,
    prerequisites: ['CS-211', 'CS-301'],
    skills: ['Java', 'Linux', 'Algorithms'],
    enrolled: 64, capacity: 70,
    matchScore: 84,
    matchReasons: [
      'Matches your Distributed Systems interest',
      'Prerequisites completed',
    ],
  ),
  Course(
    code: 'CS-352',
    name: 'Database Systems II',
    category: 'Data',
    credits: 3,
    difficulty: Difficulty.intermediate,
    prerequisites: ['CS-251'],
    skills: ['SQL', 'Python', 'Java'],
    enrolled: 88, capacity: 100,
    matchScore: 79,
    matchReasons: [
      'Matches your Data Engineering interest',
      'Matches existing skills',
    ],
  ),
  Course(
    code: 'CS-460',
    name: 'Computer Vision',
    category: 'AI',
    credits: 3,
    difficulty: Difficulty.advanced,
    prerequisites: ['CS-221', 'MATH-204'],
    skills: ['Python', 'Algorithms', 'Statistics'],
    enrolled: 72, capacity: 80,
    matchScore: 74,
    matchReasons: ['Matches your AI interest', 'Prerequisites completed'],
  ),
  Course(
    code: 'CS-385',
    name: 'Cloud Computing',
    category: 'Systems',
    credits: 3,
    difficulty: Difficulty.intermediate,
    prerequisites: ['CS-211'],
    skills: ['Linux', 'Python', 'Java'],
    enrolled: 102, capacity: 110,
    matchScore: 71,
    matchReasons: ['Matches your Distributed Systems interest'],
  ),
  Course(
    code: 'MATH-204',
    name: 'Probability & Statistics',
    category: 'Mathematics',
    credits: 3,
    difficulty: Difficulty.intermediate,
    prerequisites: ['MATH-103'],
    skills: ['Statistics'],
    enrolled: 240, capacity: 240,
    status: CourseStatus.completed, grade: 'A-', semester: 'Fall 2024',
  ),
  Course(
    code: 'CS-221',
    name: 'Algorithms',
    category: 'Computer Science',
    credits: 4,
    difficulty: Difficulty.intermediate,
    prerequisites: ['CS-101'],
    skills: ['Algorithms', 'Java'],
    enrolled: 180, capacity: 180,
    status: CourseStatus.completed, grade: 'A', semester: 'Spring 2024',
  ),
  Course(
    code: 'CS-251',
    name: 'Database Systems I',
    category: 'Data',
    credits: 3,
    difficulty: Difficulty.intermediate,
    prerequisites: ['CS-101'],
    skills: ['SQL', 'Java'],
    enrolled: 156, capacity: 160,
    status: CourseStatus.completed, grade: 'A-', semester: 'Fall 2024',
  ),
  Course(
    code: 'CS-101',
    name: 'Introduction to Computing',
    category: 'Computer Science',
    credits: 3,
    difficulty: Difficulty.introductory,
    prerequisites: [],
    skills: ['Python'],
    enrolled: 320, capacity: 320,
    status: CourseStatus.completed, grade: 'A', semester: 'Fall 2022',
  ),
  Course(
    code: 'CS-301',
    name: 'Operating Systems',
    category: 'Systems',
    credits: 4,
    difficulty: Difficulty.advanced,
    prerequisites: ['CS-211'],
    skills: ['Linux', 'C', 'Algorithms'],
    enrolled: 90, capacity: 90,
    status: CourseStatus.inProgress,
  ),
  Course(
    code: 'CS-322',
    name: 'Software Engineering',
    category: 'Computer Science',
    credits: 3,
    difficulty: Difficulty.intermediate,
    prerequisites: ['CS-221'],
    skills: ['Java', 'Python'],
    enrolled: 110, capacity: 120,
    status: CourseStatus.inProgress,
  ),
];

Course? findCourse(String code) {
  for (final c in courses) {
    if (c.code == code) return c;
  }
  return null;
}

List<Course> get recommended =>
    courses.where((c) => c.matchScore != null).toList()
      ..sort((a, b) => (b.matchScore ?? 0).compareTo(a.matchScore ?? 0));

List<Course> get completedCourses =>
    courses.where((c) => c.status == CourseStatus.completed).toList();

List<Course> get inProgressCourses =>
    courses.where((c) => c.status == CourseStatus.inProgress).toList();

const suggestedPrompts = [
  'What are the prerequisites for Machine Learning?',
  'Which courses can I take next semester?',
  'What courses have I completed?',
  'Explain the Data Mining course to me.',
  'How many credits do I have left?',
];

const assistantConversation = <AssistantMessage>[
  AssistantMessage(
    role: 'user',
    content: 'What are the prerequisites for Machine Learning?',
  ),
  AssistantMessage(
    role: 'assistant',
    content: 'Machine Learning (CS-421) requires the following prerequisites:\n\n1. Algorithms (CS-221) — you completed this with grade A.\n2. Probability & Statistics (MATH-204) — you completed this with grade A-.\n\nBoth prerequisites are satisfied, so you are eligible to enroll.',
    sources: [
      SourceRef(label: 'Course catalog', code: 'CS-421'),
      SourceRef(label: 'Your transcript', code: 'S-2023-1148'),
    ],
  ),
  AssistantMessage(
    role: 'user',
    content: 'Which courses can I take next semester?',
  ),
  AssistantMessage(
    role: 'assistant',
    content: 'Based on your completed courses and current skills, the following courses are available next semester:\n\n• Machine Learning (CS-421) — Advanced, 3 credits\n• Data Mining (CS-432) — Advanced, 3 credits\n• Distributed Systems (CS-371) — Advanced, 4 credits\n• Database Systems II (CS-352) — Intermediate, 3 credits\n\nYou can enroll in up to 18 credits without dean approval.',
    sources: [
      SourceRef(label: 'Course catalog', code: 'Fall 2025'),
      SourceRef(label: 'Academic regulations', code: '§4.2'),
    ],
  ),
];
