// lib/screens/home_screen.dart
// Smart University Assistant — Home screen.
// "What do I need to know right now?"

import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../data/models.dart';
import '../widgets/primitives.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final greeting = 'Good morning';
    final pct = (student.creditsCompleted / student.creditsRequired * 100).round();

    return MobileScaffold(
      activeTab: 'home',
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          // Greeting
          Padding(
            padding: const EdgeInsets.fromLTRB(20, 20, 20, 12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(greeting.toUpperCase(),
                  style: const TextStyle(
                    fontSize: 11, fontWeight: FontWeight.w500,
                    letterSpacing: 0.66,
                    color: AppColors.textSecondary,
                  ),
                ),
                const SizedBox(height: 2),
                Text(student.name,
                  style: const TextStyle(
                    fontSize: 22, fontWeight: FontWeight.w600,
                    letterSpacing: -0.22,
                  ),
                ),
                const SizedBox(height: 2),
                Text('${student.major} · ${student.year}',
                  style: const TextStyle(
                    fontSize: 12, color: AppColors.textSecondary,
                  ),
                ),
              ],
            ),
          ),
          const HairlineDivider(),

          // Academic progress
          Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SectionHeader(label: 'Academic progress'),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text('Credits',
                      style: TextStyle(
                        fontSize: 12, color: AppColors.textSecondary,
                      ),
                    ),
                    Text('${student.creditsCompleted} / ${student.creditsRequired}',
                      style: const TextStyle(
                        fontSize: 12, color: AppColors.textSecondary,
                        fontFeatures: [FontFeature.tabularFigures()],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                ClipRRect(
                  borderRadius: BorderRadius.circular(AppRadii.sm),
                  child: LinearProgressIndicator(
                    value: pct / 100,
                    minHeight: 6,
                    backgroundColor: AppColors.surfaceRaised,
                    valueColor: AlwaysStoppedAnimation(AppColors.accent),
                  ),
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    _Stat('GPA', student.gpa.toStringAsFixed(2)),
                    const SizedBox(width: 12),
                    _Stat('In progress', '${student.creditsInProgress} cr'),
                    const SizedBox(width: 12),
                    _Stat('Graduation', student.graduation),
                  ],
                ),
              ],
            ),
          ),
          const HairlineDivider(),

          // Current courses
          Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                SectionHeader(
                  label: 'Current courses',
                  right: TextButton(
                    onPressed: () {},
                    child: const Text('View all'),
                  ),
                ),
                ...inProgressCourses.map((c) => _CourseTile(course: c)),
              ],
            ),
          ),
          const HairlineDivider(),

          // Recommended
          Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                SectionHeader(
                  label: 'Recommended courses',
                  right: TextButton(
                    onPressed: () {},
                    child: const Text('See more'),
                  ),
                ),
                ...recommended.take(3).toList().asMap().entries.map(
                      (e) => _RecommendedTile(course: e.value, rank: e.key + 1, compact: true),
                    ),
              ],
            ),
          ),
          const HairlineDivider(),

          // Assistant prompt
          Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SectionHeader(label: 'Assistant'),
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: AppColors.surface,
                    border: Border.all(color: AppColors.border),
                    borderRadius: BorderRadius.circular(AppRadii.md),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Ask about courses, prerequisites, or university rules.',
                        style: TextStyle(fontSize: 13, height: 1.4),
                      ),
                      const SizedBox(height: 12),
                      Wrap(
                        spacing: 6,
                        runSpacing: 6,
                        children: [
                          _PromptChip('Prerequisites for Machine Learning?'),
                          _PromptChip('Which courses next semester?'),
                        ],
                      ),
                    ],
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

class _Stat extends StatelessWidget {
  final String label;
  final String value;
  const _Stat(this.label, this.value);

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(10),
        decoration: BoxDecoration(
          color: AppColors.surface,
          border: Border.all(color: AppColors.border),
          borderRadius: BorderRadius.circular(AppRadii.md),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label.toUpperCase(),
              style: const TextStyle(
                fontSize: 10, fontWeight: FontWeight.w500,
                letterSpacing: 0.6,
                color: AppColors.textSecondary,
              ),
            ),
            const SizedBox(height: 2),
            Text(value,
              style: const TextStyle(
                fontSize: 14, fontWeight: FontWeight.w500,
                fontFeatures: [FontFeature.tabularFigures()],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _PromptChip extends StatelessWidget {
  final String label;
  const _PromptChip(this.label);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 28,
      padding: const EdgeInsets.symmetric(horizontal: 10),
      decoration: BoxDecoration(
        color: AppColors.surface,
        border: Border.all(color: AppColors.border),
        borderRadius: BorderRadius.circular(AppRadii.md),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.chat_bubble_outline, size: 12, color: AppColors.textSecondary),
          const SizedBox(width: 4),
          Text(label, style: const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
        ],
      ),
    );
  }
}

class _CourseTile extends StatelessWidget {
  final Course course;
  const _CourseTile({required this.course});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 12),
      decoration: const BoxDecoration(
        border: Border(
          bottom: BorderSide(color: AppColors.border, width: 0.5),
        ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  crossAxisAlignment: CrossAxisAlignment.baseline,
                  textBaseline: TextBaseline.alphabetic,
                  children: [
                    Flexible(
                      child: Text(course.name,
                        style: const TextStyle(
                          fontSize: 14, fontWeight: FontWeight.w500,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const SizedBox(width: 8),
                    Text(course.code,
                      style: const TextStyle(
                        fontSize: 11, color: AppColors.textSecondary,
                        fontFeatures: [FontFeature.tabularFigures()],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 2),
                Text('${course.category} · ${course.credits} credits',
                  style: const TextStyle(
                    fontSize: 12, color: AppColors.textSecondary,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(width: 12),
          DifficultyTag(difficulty: course.difficulty),
        ],
      ),
    );
  }
}

class _RecommendedTile extends StatelessWidget {
  final Course course;
  final int rank;
  final bool compact;
  const _RecommendedTile({
    required this.course,
    required this.rank,
    this.compact = false,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 24,
            child: Text(rank.toString().padLeft(2, '0'),
              style: const TextStyle(
                fontSize: 12, fontWeight: FontWeight.w500,
                color: AppColors.textSecondary,
                fontFeatures: [FontFeature.tabularFigures()],
              ),
            ),
          ),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  crossAxisAlignment: CrossAxisAlignment.baseline,
                  textBaseline: TextBaseline.alphabetic,
                  children: [
                    Flexible(
                      child: Text(course.name,
                        style: const TextStyle(
                          fontSize: 14, fontWeight: FontWeight.w500,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const SizedBox(width: 8),
                    Text(course.code,
                      style: const TextStyle(
                        fontSize: 11, color: AppColors.textSecondary,
                        fontFeatures: [FontFeature.tabularFigures()],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 2),
                Text('${course.category} · ${course.difficultyLabel} · ${course.credits} credits',
                  style: const TextStyle(
                    fontSize: 12, color: AppColors.textSecondary,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(width: 12),
          SizedBox(
            width: 80,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('MATCH',
                  style: TextStyle(
                    fontSize: 10, fontWeight: FontWeight.w500,
                    letterSpacing: 0.6,
                    color: AppColors.textSecondary,
                  ),
                ),
                const SizedBox(height: 4),
                MatchMeter(value: course.matchScore ?? 0),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
