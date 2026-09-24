// lib/screens/courses_screen.dart
// Smart University Assistant — Course browsing.

import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../theme/app_theme.dart';
import '../widgets/primitives.dart';

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

  // دالة لتسجيل الطالب في الكورس وزيادة العداد في Supabase
  Future<void> _enrollInCourse(BuildContext context, dynamic courseId, int currentCount) async {
    try {
      await _supabase
          .from('courses')
          .update({'enrolled_students_count': currentCount + 1})
          .eq('course_id', courseId);

      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Enrolled successfully! Student count updated.'),
          backgroundColor: Colors.green,
        ),
      );

      _fetchCourses(); // تحديث القائمة لإظهار العداد الجديد
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
                      final currentCount = course['enrolled_students_count'] ?? 0;
                      _enrollInCourse(context, courseId, currentCount);
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
                            color: Colors.black87, // لون غامق وواضح على الخلفية الفاتحة
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
                      color: Colors.blue, // لون أزرق واضح للمحاضر
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text('Hours: $hours  |  Price: \$$price  |  Enrolled: $enrolledCount',
                    style: const TextStyle(
                      fontSize: 11,
                      color: Colors.black54, // لون رمادي غامق وواضح للتفاصيل
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