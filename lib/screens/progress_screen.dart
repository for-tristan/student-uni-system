// lib/screens/progress_screen.dart
// Smart University Assistant — Academic progress.

import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../data/models.dart';
import '../widgets/primitives.dart';

class ProgressScreen extends StatelessWidget {
  const ProgressScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final pct = (student.creditsCompleted / student.creditsRequired * 100).round();
    final remaining = student.creditsRequired - student.creditsCompleted;

    return MobileScaffold(
      activeTab: 'progress',
      child: Column(
        children: [
          const ScreenHeader(title: 'Progress'),
          Expanded(
            child: ListView(
              padding: EdgeInsets.zero,
              children: [
                Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const SectionHeader(label: 'Graduation progress'),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('Credits completed',
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
                          minHeight: 8,
                          backgroundColor: AppColors.surfaceRaised,
                          valueColor: AlwaysStoppedAnimation(AppColors.accent),
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text('$pct% complete · On track for ${student.graduation}',
                        style: const TextStyle(
                          fontSize: 11, color: AppColors.textSecondary,
                        ),
                      ),
                      const SizedBox(height: 16),
                      Row(
                        children: [
                          _Stat('GPA', student.gpa.toStringAsFixed(2)),
                          const SizedBox(width: 12),
                          _Stat('In progress', '${student.creditsInProgress} cr'),
                          const SizedBox(width: 12),
                          _Stat('Remaining', '$remaining cr'),
                        ],
                      ),
                    ],
                  ),
                ),
                const HairlineDivider(),
                Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const SectionHeader(label: 'Current courses'),
                      ...inProgressCourses.map((c) => _SimpleRow(course: c, isCompleted: false)),
                    ],
                  ),
                ),
                const HairlineDivider(),
                Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      SectionHeader(label: 'Completed · ${completedCourses.length}'),
                      ...completedCourses.map((c) => _SimpleRow(course: c, isCompleted: true)),
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

class _SimpleRow extends StatelessWidget {
  final Course course;
  final bool isCompleted;
  const _SimpleRow({required this.course, required this.isCompleted});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 10),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(course.name,
                  style: const TextStyle(
                    fontSize: 13, fontWeight: FontWeight.w500,
                  ),
                  overflow: TextOverflow.ellipsis,
                ),
                Text('${course.code}${course.semester != null ? ' · ${course.semester}' : ''}',
                  style: const TextStyle(
                    fontSize: 11, color: AppColors.textSecondary,
                    fontFeatures: [FontFeature.tabularFigures()],
                  ),
                ),
              ],
            ),
          ),
          if (isCompleted && course.grade != null)
            Text(course.grade!,
              style: const TextStyle(
                fontSize: 13, fontWeight: FontWeight.w500,
                fontFeatures: [FontFeature.tabularFigures()],
              ),
            )
          else
            const Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.access_time, size: 12, color: AppColors.textSecondary),
                SizedBox(width: 4),
                Text('In progress',
                  style: TextStyle(
                    fontSize: 12, color: AppColors.textSecondary,
                  ),
                ),
              ],
            ),
        ],
      ),
    );
  }
}
