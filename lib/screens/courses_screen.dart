// lib/screens/courses_screen.dart
// Smart University Assistant — Course browsing.

import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../theme/app_theme.dart';
import '../widgets/primitives.dart';
import 'login_screen.dart'; // للوصول لـ currentLoggedInEmail

class CoursesScreen extends StatefulWidget {
  const CoursesScreen({super.key});

  @override
  State<CoursesScreen> createState() => _CoursesScreenState();
}

class _CoursesScreenState extends State<CoursesScreen> {
  final _supabase = Supabase.instance.client;
  List<Map<String, dynamic>> _courses = [];
  bool _loading = true;
  String _filter = 'All';
  final _filters = ['All', 'AI', 'Systems', 'Data', 'Mathematics'];

  @override
  void initState() {
    super.initState();
    _fetchCourses();
  }

  // جلب الكورسات الحقيقية من Supabase
  Future<void> _fetchCourses() async {
    setState(() => _loading = true);
    try {
      final response = await _supabase.from('courses').select();
      if (!mounted) return;
      setState(() {
        _courses = List<Map<String, dynamic>>.from(response);
        _loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() => _loading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error loading courses: $e'), backgroundColor: Colors.red),
      );
    }
  }

  // دالة لتسجيل الطالب في جدول enrollments وربطه بالكورس بـ Supabase
  Future<void> _enrollInCourse(BuildContext context, dynamic courseId) async {
    try {
      final email = currentLoggedInEmail;
      if (email == null) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Please sign in first!'), backgroundColor: Colors.red),
        );
        return;
      }

      // 1. جلب الـ user_id أو id الخاص بالطالب الحالي من جدول users
      final userRes = await _supabase
          .from('users')
          .select('id')
          .eq('email', email)
          .maybeSingle();

      if (userRes == null) {
        throw Exception('User record not found in database.');
      }

      final studentId = userRes['id'];

      // 2. التحقق مما إذا كان الطالب مسجلاً مسبقاً في هذا الكورس
      final existingEnrollment = await _supabase
          .from('enrollments')
          .select()
          .eq('course_id', courseId)
          .eq('student_id', studentId)
          .maybeSingle();

      if (existingEnrollment != null) {
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('You are already enrolled in this course!'), backgroundColor: Colors.orange),
        );
        return;
      }

      // 3. إضافة سجل جديد في جدول enrollments
      await _supabase.from('enrollments').insert({
        'course_id': courseId,
        'student_id': studentId,
      });

      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Enrolled successfully! Admin can now see your enrollment.'),
          backgroundColor: Colors.green,
        ),
      );

      _fetchCourses(); // تحديث القائمة
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e'), backgroundColor: Colors.red),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final filteredList = _filter == 'All'
        ? _courses
        : _courses.where((c) => c['category'] == _filter).toList();

    return MobileScaffold(
      activeTab: 'courses',
      child: Column(
        children: [
          const ScreenHeader(title: 'Courses'),
          Expanded(
            child: _loading
                ? const Center(child: CircularProgressIndicator())
                : ListView(
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
                  child: Text('${filteredList.length} COURSES',
                    style: const TextStyle(
                      fontSize: 11, fontWeight: FontWeight.w500,
                      letterSpacing: 0.66,
                      color: AppColors.textSecondary,
                    ),
                  ),
                ),
                if (filteredList.isEmpty)
                  const Center(
                    child: Padding(
                      padding: EdgeInsets.all(40),
                      child: Text('No courses found', style: TextStyle(color: Colors.black54)),
                    ),
                  )
                else
                  ...filteredList.map((course) => _CourseRow(
                    course: course,
                    onEnroll: () {
                      final courseId = course['course_id'];
                      _enrollInCourse(context, courseId);
                    },
                  )),
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
  final Map<String, dynamic> course;
  final VoidCallback onEnroll;
  const _CourseRow({required this.course, required this.onEnroll});

  @override
  Widget build(BuildContext context) {
    final courseName = course['course_name'] ?? 'Unnamed Course';
    final instructor = course['instructor_name'] ?? 'Not specified';
    final hours = course['course_hours']?.toString() ?? '0';
    final price = course['price']?.toString() ?? '0';
    final enrolledCount = course['enrolled_students_count'] ?? 0;

    return InkWell(
      onTap: () {},
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
                        child: Text(courseName,
                          style: const TextStyle(
                            fontSize: 15,
                            fontWeight: FontWeight.bold,
                            color: Colors.black87,
                          ),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 4),
                  Text('Instructor: $instructor',
                    style: const TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w500,
                      color: Colors.blue,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text('Hours: $hours  |  Price: \$$price  |  Enrolled: $enrolledCount',
                    style: const TextStyle(
                      fontSize: 11,
                      color: Colors.black54,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                const SizedBox(height: 4),
                IconButton(
                  icon: const Icon(Icons.add_circle_outline, size: 22, color: Colors.blue),
                  onPressed: onEnroll,
                  tooltip: 'Enroll',
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}