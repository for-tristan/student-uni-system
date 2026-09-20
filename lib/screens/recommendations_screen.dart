// lib/screens/recommendations_screen.dart
// Smart University Assistant — Recommended courses.

import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../data/models.dart';
import '../widgets/primitives.dart';

class RecommendationsScreen extends StatelessWidget {
  const RecommendationsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return MobileScaffold(
      activeTab: 'courses',
      child: Column(
        children: [
          const ScreenHeader(title: 'Recommended courses'),
          Expanded(
            child: ListView(
              padding: EdgeInsets.zero,
              children: [
                const Padding(
                  padding: EdgeInsets.fromLTRB(20, 16, 20, 12),
                  child: Text(
                    'Based on your courses, skills, and interests. Re-ranked nightly.',
                    style: TextStyle(
                      fontSize: 12, height: 1.5,
                      color: AppColors.textSecondary,
                    ),
                  ),
                ),
                ...recommended.asMap().entries.map((e) => _RecommendedRow(
                  course: e.value, rank: e.key + 1,
                )),
                Padding(
                  padding: const EdgeInsets.fromLTRB(20, 16, 20, 8),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('IMPROVE RECOMMENDATIONS',
                        style: TextStyle(
                          fontSize: 11, fontWeight: FontWeight.w500,
                          letterSpacing: 0.66,
                          color: AppColors.textSecondary,
                        ),
                      ),
                      const SizedBox(height: 8),
                      OutlinedButton.icon(
                        onPressed: () {},
                        icon: const Icon(Icons.add, size: 14),
                        label: const Text('Add interests and skills'),
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

class _RecommendedRow extends StatelessWidget {
  final Course course;
  final int rank;
  const _RecommendedRow({required this.course, required this.rank});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () => Navigator.pushNamed(context, '/course', arguments: course.code),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
        decoration: const BoxDecoration(
          border: Border(
            bottom: BorderSide(color: AppColors.border, width: 0.5),
          ),
        ),
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
                  const SizedBox(height: 8),
                  Wrap(
                    spacing: 6, runSpacing: 4,
                    children: course.skills.map((s) => Container(
                      height: 20,
                      padding: const EdgeInsets.symmetric(horizontal: 6),
                      decoration: BoxDecoration(
                        color: AppColors.surfaceRaised,
                        borderRadius: BorderRadius.circular(AppRadii.sm),
                      ),
                      alignment: Alignment.center,
                      child: Text(s,
                        style: const TextStyle(
                          fontSize: 11, color: AppColors.textSecondary,
                        ),
                      ),
                    )).toList(),
                  ),
                  const SizedBox(height: 8),
                  Text('Why: ${course.matchReasons?.first ?? ''}',
                    style: const TextStyle(fontSize: 12),
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
      ),
    );
  }
}
