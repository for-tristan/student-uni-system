// lib/screens/home_screen.dart
// Smart University Assistant — Home screen.

import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../theme/app_theme.dart';
import '../data/models.dart';
import '../widgets/primitives.dart';
import 'login_screen.dart'; // لاستخدام currentLoggedInEmail

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _supabase = Supabase.instance.client;
  Map<String, dynamic>? _userData;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _fetchUserData();
  }

  Future<void> _fetchUserData() async {
    try {
      final emailToSearch = currentLoggedInEmail ?? student.email;
      final response = await _supabase
          .from('users')
          .select()
          .eq('email', emailToSearch)
          .maybeSingle();

      if (response != null) {
        setState(() {
          _userData = response;
          _loading = false;
        });
      } else {
        setState(() => _loading = false);
      }
    } catch (e) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const MobileScaffold(
        activeTab: 'home',
        child: Center(child: CircularProgressIndicator()),
      );
    }

    final studentName = _userData?['name'] ?? student.name;
    final double studentGpa = student.gpa;
    final int creditsCompleted = student.creditsCompleted;
    final int creditsRequired = student.creditsRequired;
    final int creditsInProgress = student.creditsInProgress;
    final graduation = student.graduation;

    final pct = (creditsCompleted / creditsRequired * 100).round();

    return MobileScaffold(
      activeTab: 'home',
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(20, 20, 20, 12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('GOOD MORNING',
                  style: TextStyle(
                    fontSize: 11, fontWeight: FontWeight.w500,
                    letterSpacing: 0.66, color: AppColors.textSecondary,
                  ),
                ),
                const SizedBox(height: 2),
                Text(studentName,
                  style: const TextStyle(
                    fontSize: 22, fontWeight: FontWeight.w600,
                    letterSpacing: -0.22,
                  ),
                ),
                const SizedBox(height: 2),
                Text('${student.major} · ${student.year}',
                  style: const TextStyle(fontSize: 12, color: AppColors.textSecondary),
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
                const SectionHeader(label: 'Academic progress'),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text('Credits', style: TextStyle(fontSize: 12, color: AppColors.textSecondary)),
                    Text('$creditsCompleted / $creditsRequired', style: const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
                  ],
                ),
                const SizedBox(height: 8),
                ClipRRect(
                  borderRadius: BorderRadius.circular(AppRadii.sm),
                  child: LinearProgressIndicator(
                    value: pct / 100,
                    minHeight: 6,
                    backgroundColor: AppColors.surfaceRaised,
                    valueColor: const AlwaysStoppedAnimation(AppColors.accent),
                  ),
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    _Stat('GPA', studentGpa.toStringAsFixed(2)),
                    const SizedBox(width: 12),
                    _Stat('In progress', '$creditsInProgress cr'),
                    const SizedBox(width: 12),
                    _Stat('Graduation', graduation),
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
                SectionHeader(
                  label: 'Current courses',
                  right: TextButton(onPressed: () {}, child: const Text('View all')),
                ),
                ...inProgressCourses.map((c) => _CourseTile(course: c)),
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
            Text(label.toUpperCase(), style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w500, color: AppColors.textSecondary)),
            const SizedBox(height: 2),
            Text(value, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500)),
          ],
        ),
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
        border: Border(bottom: BorderSide(color: AppColors.border, width: 0.5)),
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(course.name, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500)),
                const SizedBox(height: 2),
                Text('${course.category} · ${course.credits} credits', style: const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
              ],
            ),
          ),
          DifficultyTag(difficulty: course.difficulty),
        ],
      ),
    );
  }
}