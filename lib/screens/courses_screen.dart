// lib/screens/courses_screen.dart
// Smart University Assistant — Course browsing.

import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../data/models.dart';
import '../widgets/primitives.dart';

class CoursesScreen extends StatefulWidget {
  const CoursesScreen({super.key});

  @override
  State<CoursesScreen> createState() => _CoursesScreenState();
}

class _CoursesScreenState extends State<CoursesScreen> {
  String _filter = 'All';
  final _filters = ['All', 'AI', 'Systems', 'Data', 'Mathematics'];

  @override
  Widget build(BuildContext context) {
    final list = _filter == 'All'
        ? courses
        : courses.where((c) => c.category == _filter).toList();

    return MobileScaffold(
      activeTab: 'courses',
      child: Column(
        children: [
          const ScreenHeader(title: 'Courses'),
          Expanded(
            child: ListView(
              padding: EdgeInsets.zero,
              children: [
                Padding(
                  padding: const EdgeInsets.fromLTRB(20, 16, 20, 12),
                  child: TextField(
                    decoration: InputDecoration(
                      hintText: 'Search by name, code, or skill',
                      prefixIcon: const Icon(Icons.search,
                        size: 14, color: AppColors.textSecondary),
                      contentPadding: EdgeInsets.zero,
                      isDense: true,
                    ),
                  ),
                ),
                SizedBox(
                  height: 32,
                  child: ListView.separated(
                    scrollDirection: Axis.horizontal,
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    itemCount: _filters.length + 1,
                    separatorBuilder: (_, __) => const SizedBox(width: 8),
                    itemBuilder: (context, i) {
                      if (i == _filters.length) {
                        return _FilterChip(
                          label: 'Filters',
                          icon: Icons.filter_list,
                          active: false,
                          onTap: () {},
                        );
                      }
                      final f = _filters[i];
                      return _FilterChip(
                        label: f,
                        active: f == _filter,
                        onTap: () => setState(() => _filter = f),
                      );
                    },
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(20, 12, 20, 4),
                  child: Text('${list.length} COURSES',
                    style: const TextStyle(
                      fontSize: 11, fontWeight: FontWeight.w500,
                      letterSpacing: 0.66,
                      color: AppColors.textSecondary,
                    ),
                  ),
                ),
                ...list.map((c) => _CourseRow(course: c)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _FilterChip extends StatelessWidget {
  final String label;
  final IconData? icon;
  final bool active;
  final VoidCallback onTap;
  const _FilterChip({
    required this.label,
    this.icon,
    required this.active,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        height: 28,
        padding: const EdgeInsets.symmetric(horizontal: 10),
        decoration: BoxDecoration(
          color: active ? AppColors.textPrimary : AppColors.surface,
          border: Border.all(
            color: active ? AppColors.textPrimary : AppColors.border,
          ),
          borderRadius: BorderRadius.circular(AppRadii.md),
        ),
        alignment: Alignment.center,
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (icon != null) ...[
              Icon(icon, size: 12,
                color: active ? AppColors.background : AppColors.textSecondary),
              const SizedBox(width: 4),
            ],
            Text(label,
              style: TextStyle(
                fontSize: 12,
                color: active ? AppColors.background : AppColors.textSecondary,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _CourseRow extends StatelessWidget {
  final Course course;
  const _CourseRow({required this.course});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () {
        Navigator.pushNamed(context, '/course',
          arguments: course.code);
      },
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
                  if (course.prerequisites.isNotEmpty) ...[
                    const SizedBox(height: 4),
                    Text('Prereq · ${course.prerequisites.join(', ')}',
                      style: const TextStyle(
                        fontSize: 11, color: AppColors.textSecondary,
                      ),
                    ),
                  ],
                ],
              ),
            ),
            const SizedBox(width: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                DifficultyTag(difficulty: course.difficulty),
                const SizedBox(height: 4),
                const Icon(Icons.chevron_right,
                  size: 14, color: AppColors.textSecondary),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
