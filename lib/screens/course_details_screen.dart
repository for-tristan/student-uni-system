// lib/screens/course_details_screen.dart
// Smart University Assistant — Course details.

import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../data/models.dart';
import '../widgets/primitives.dart';

class CourseDetailsScreen extends StatelessWidget {
  final String courseCode;
  const CourseDetailsScreen({super.key, required this.courseCode});

  @override
  Widget build(BuildContext context) {
    final course = findCourse(courseCode);
    if (course == null) {
      return const MobileScaffold(
        activeTab: 'courses',
        child: Center(child: Text('Course not found')),
      );
    }

    return MobileScaffold(
      activeTab: 'courses',
      child: Column(
        children: [
          // Back header
          Container(
            height: 48,
            decoration: const BoxDecoration(
              color: AppColors.background,
              border: Border(
                bottom: BorderSide(color: AppColors.border, width: 1),
              ),
            ),
            padding: const EdgeInsets.symmetric(horizontal: 12),
            child: Row(
              children: [
                IconButton(
                  icon: const Icon(Icons.chevron_left, size: 16),
                  onPressed: () => Navigator.pop(context),
                ),
                Text(course.code,
                  style: const TextStyle(
                    fontSize: 13, fontWeight: FontWeight.w500,
                    fontFeatures: [FontFeature.tabularFigures()],
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: ListView(
              padding: EdgeInsets.zero,
              children: [
                // Title block
                Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('${course.category} · ${course.credits} credits'.toUpperCase(),
                        style: const TextStyle(
                          fontSize: 11, fontWeight: FontWeight.w500,
                          letterSpacing: 0.66,
                          color: AppColors.textSecondary,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(course.name,
                        style: const TextStyle(
                          fontSize: 22, fontWeight: FontWeight.w600,
                          letterSpacing: -0.22,
                        ),
                      ),
                      const SizedBox(height: 8),
                      DifficultyTag(difficulty: course.difficulty),
                    ],
                  ),
                ),
                const HairlineDivider(),

                // Overview
                _Section(title: 'Overview', child:
                  const Text(
                    'An introduction to supervised, unsupervised, and reinforcement learning. '
                    'Covers linear models, decision trees, neural networks, and model evaluation. '
                    'Includes a semester-long applied project on a real dataset.',
                    style: TextStyle(fontSize: 13, height: 1.6),
                  ),
                ),
                const HairlineDivider(),

                // Prerequisites
                _Section(title: 'Prerequisites', child:
                  Column(
                    children: course.prerequisites.map((code) {
                      final p = findCourse(code);
                      final done = completedCourses.any((c) => c.code == code);
                      final grade = completedCourses
                          .where((c) => c.code == code)
                          .firstOrNull?.grade;
                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 10),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(p?.name ?? code,
                                  style: const TextStyle(
                                    fontSize: 13, fontWeight: FontWeight.w500,
                                  ),
                                ),
                                Text(code,
                                  style: const TextStyle(
                                    fontSize: 11, color: AppColors.textSecondary,
                                    fontFeatures: [FontFeature.tabularFigures()],
                                  ),
                                ),
                              ],
                            ),
                            if (done)
                              StatusPill(
                                kind: StatusKind.success,
                                label: grade != null ? 'Completed · $grade' : 'Completed',
                              )
                            else
                              const StatusPill(kind: StatusKind.warning, label: 'Not completed'),
                          ],
                        ),
                      );
                    }).toList(),
                  ),
                ),
                const HairlineDivider(),

                // Skills
                _Section(title: 'Skills', child:
                  Wrap(
                    spacing: 6, runSpacing: 6,
                    children: course.skills.map((s) => Container(
                      height: 24,
                      padding: const EdgeInsets.symmetric(horizontal: 8),
                      decoration: BoxDecoration(
                        color: AppColors.surface,
                        border: Border.all(color: AppColors.border),
                        borderRadius: BorderRadius.circular(AppRadii.md),
                      ),
                      alignment: Alignment.center,
                      child: Text(s, style: const TextStyle(fontSize: 12)),
                    )).toList(),
                  ),
                ),
                const HairlineDivider(),

                // Match
                _Section(title: 'Your match', child:
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.baseline,
                        children: [
                          Text('${course.matchScore ?? 0}%',
                            style: const TextStyle(
                              fontSize: 28, fontWeight: FontWeight.w600,
                              letterSpacing: -0.2,
                              fontFeatures: [FontFeature.tabularFigures()],
                            ),
                          ),
                          const SizedBox(width: 8),
                          const Text('based on skills & interests',
                            style: TextStyle(
                              fontSize: 11, color: AppColors.textSecondary,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      MatchMeter(value: course.matchScore ?? 0),
                      const SizedBox(height: 12),
                      const Text('Why this course appears here:',
                        style: TextStyle(
                          fontSize: 12, color: AppColors.textSecondary,
                        ),
                      ),
                      const SizedBox(height: 6),
                      ...?course.matchReasons?.map((r) => Padding(
                        padding: const EdgeInsets.symmetric(vertical: 2),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Padding(
                              padding: const EdgeInsets.only(top: 6),
                              child: Container(
                                width: 4, height: 4,
                                decoration: const BoxDecoration(
                                  color: AppColors.textPrimary,
                                  shape: BoxShape.circle,
                                ),
                              ),
                            ),
                            const SizedBox(width: 8),
                            Expanded(child: Text(r, style: const TextStyle(fontSize: 13))),
                          ],
                        ),
                      )),
                    ],
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(20, 16, 20, 16),
                  child: ElevatedButton(
                    onPressed: () {},
                    child: const Text('Add to next semester'),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _Section extends StatelessWidget {
  final String title;
  final Widget child;
  const _Section({required this.title, required this.child});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SectionHeader(label: title),
          child,
        ],
      ),
    );
  }
}
