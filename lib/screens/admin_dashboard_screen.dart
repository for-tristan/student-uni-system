// lib/screens/admin_dashboard_screen.dart
import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../theme/app_theme.dart';

class AdminDashboardScreen extends StatefulWidget {
  const AdminDashboardScreen({super.key});

  @override
  State<AdminDashboardScreen> createState() => _AdminDashboardScreenState();
}

class _AdminDashboardScreenState extends State<AdminDashboardScreen> {
  final _supabase = Supabase.instance.client;
  List<Map<String, dynamic>> _courses = [];
  bool _loading = true;
  int _totalStudents = 0;
  List<Map<String, dynamic>> _allStudents = [];

  @override
  void initState() {
    super.initState();
    _fetchDashboardData();
  }

  Future<void> _fetchDashboardData() async {
    setState(() => _loading = true);
    try {
      // جلب الطلاب الذين دورهم student
      final usersRes = await _supabase.from('users').select().eq('role', 'student');
      _allStudents = List<Map<String, dynamic>>.from(usersRes);
      _totalStudents = _allStudents.length;

      // جلب الكورسات
      final coursesRes = await _supabase.from('courses').select();
      List<Map<String, dynamic>> tempCourses = List<Map<String, dynamic>>.from(coursesRes);

      // جلب عدد المشتركين الفعلي لكل كورس من جدول enrollments لضمان الدقة
      for (var course in tempCourses) {
        final courseId = course['course_id'];
        final enrollRes = await _supabase
            .from('enrollments')
            .select()
            .eq('course_id', courseId);
        course['enrolled_students_count'] = (enrollRes as List).length;
      }

      if (!mounted) return;
      setState(() {
        _courses = tempCourses;
        _loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() => _loading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error loading data: $e'), backgroundColor: Colors.red),
      );
    }
  }

  // 1. نافذة عرض كل الطلاب المسجلين في النظام عند الضغط على Total Students
  void _showAllStudentsDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1E1B2E),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: BorderSide(color: Colors.white.withValues(alpha: 0.1)),
        ),
        title: const Text(
          'All Registered Students',
          style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
        ),
        content: SizedBox(
          width: 450,
          height: 350,
          child: _allStudents.isEmpty
              ? const Center(child: Text('No students found', style: TextStyle(color: Colors.white54)))
              : ListView.builder(
            itemCount: _allStudents.length,
            itemBuilder: (context, index) {
              final student = _allStudents[index];
              return Container(
                margin: const EdgeInsets.only(bottom: 8),
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: const Color(0xFF13111C),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.white10),
                ),
                child: Row(
                  children: [
                    const CircleAvatar(
                      backgroundColor: Colors.purpleAccent,
                      child: Icon(Icons.person, color: Colors.white, size: 18),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            student['name'] ?? student['full_name'] ?? 'Unknown Student',
                            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            student['email'] ?? 'No email',
                            style: const TextStyle(color: Colors.white60, fontSize: 12),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Close', style: TextStyle(color: Colors.blueAccent)),
          ),
        ],
      ),
    );
  }

  // 2. نافذة عرض الطلاب المشتركين في كورس معين مع إمكانية إلغاء الاشتراك
  void _showCourseEnrolledStudents(Map<String, dynamic> course) async {
    final courseId = course['course_id'];

    showDialog(
      context: context,
      builder: (dialogContext) => StatefulBuilder(
        builder: (context, setStateDialog) {
          return AlertDialog(
            backgroundColor: const Color(0xFF1E1B2E),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
              side: BorderSide(color: Colors.white.withValues(alpha: 0.1)),
            ),
            title: Text(
              'Enrolled in: ${course['course_name']}',
              style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
            ),
            content: SizedBox(
              width: 450,
              height: 350,
              child: FutureBuilder<List<Map<String, dynamic>>>(
                future: _fetchEnrolledStudentsForCourse(courseId),
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const Center(child: CircularProgressIndicator());
                  }
                  if (snapshot.hasError) {
                    return Center(child: Text('Error: ${snapshot.error}', style: const TextStyle(color: Colors.red)));
                  }
                  final enrolledList = snapshot.data ?? [];
                  if (enrolledList.isEmpty) {
                    return const Center(child: Text('No students enrolled in this course yet.', style: TextStyle(color: Colors.white54)));
                  }

                  return ListView.builder(
                    itemCount: enrolledList.length,
                    itemBuilder: (context, index) {
                      final item = enrolledList[index];
                      // افتراض أن جدول enrollments يربط بجدول users أو يحتوي على بيانات الطالب
                      final studentInfo = item['users'] ?? item;

                      return Container(
                        margin: const EdgeInsets.only(bottom: 8),
                        padding: const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: const Color(0xFF13111C),
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: Colors.white10),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    studentInfo['name'] ?? studentInfo['full_name'] ?? 'Student',
                                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13),
                                  ),
                                  Text(
                                    studentInfo['email'] ?? '',
                                    style: const TextStyle(color: Colors.white60, fontSize: 11),
                                  ),
                                ],
                              ),
                            ),
                            // زر إلغاء الاشتراك (Unenroll / Drop)
                            IconButton(
                              icon: const Icon(Icons.remove_circle_outline, color: Colors.redAccent, size: 20),
                              tooltip: 'Remove Student',
                              onPressed: () async {
                                try {
                                  // حذف السجل من جدول enrollments
                                  await _supabase
                                      .from('enrollments')
                                      .delete()
                                      .eq('enrollment_id', item['enrollment_id'] ?? item['id']);

                                  setStateDialog(() {
                                    enrolledList.removeAt(index);
                                  });

                                  // تحديث البيانات الرئيسية في الخلفية ليقل العداد فوراً
                                  _fetchDashboardData();

                                  ScaffoldMessenger.of(context).showSnackBar(
                                    const SnackBar(content: Text('Student unenrolled successfully'), backgroundColor: Colors.green),
                                  );
                                } catch (e) {
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    SnackBar(content: Text('Failed to unenroll: $e'), backgroundColor: Colors.red),
                                  );
                                }
                              },
                            ),
                          ],
                        ),
                      );
                    },
                  );
                },
              ),
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(dialogContext),
                child: const Text('Close', style: TextStyle(color: Colors.blueAccent)),
              ),
            ],
          );
        },
      ),
    );
  }

  // دالة لجلب الطلاب المشتركين في كورس محدد من Supabase
  Future<List<Map<String, dynamic>>> _fetchEnrolledStudentsForCourse(dynamic courseId) async {
    try {
      final res = await _supabase
          .from('enrollments')
          .select('*, users(*)') // جلب بيانات جدول المستخدمين المرتبط بالاشتراك
          .eq('course_id', courseId);
      return List<Map<String, dynamic>>.from(res);
    } catch (e) {
      // لو العلاقة (Foreign Key) اسمها مختلف، نجرب جلب الـ enrollments وحدها
      try {
        final res = await _supabase.from('enrollments').select().eq('course_id', courseId);
        return List<Map<String, dynamic>>.from(res);
      } catch (_) {
        return [];
      }
    }
  }

  void _showCourseDialog({Map<String, dynamic>? course}) {
    final nameController = TextEditingController(text: course?['course_name'] ?? '');
    final instructorNameController = TextEditingController(text: course?['instructor_name'] ?? '');
    final hoursController = TextEditingController(text: course?['course_hours']?.toString() ?? '');
    final priceController = TextEditingController(text: course?['price']?.toString() ?? '');

    showDialog(
      context: context,
      builder: (dialogContext) => AlertDialog(
        backgroundColor: const Color(0xFF1E1B2E),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: BorderSide(color: Colors.white.withValues(alpha: 0.1)),
        ),
        title: Text(
          course == null ? 'Add New Course' : 'Edit Course',
          style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
        ),
        content: SingleChildScrollView(
          child: SizedBox(
            width: 400,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                _buildTextField(controller: nameController, label: 'Course Name', icon: Icons.book),
                const SizedBox(height: 14),
                _buildTextField(controller: instructorNameController, label: 'Instructor Name', icon: Icons.person),
                const SizedBox(height: 14),
                _buildTextField(controller: hoursController, label: 'Course Hours', icon: Icons.timer, keyboardType: TextInputType.number),
                const SizedBox(height: 14),
                _buildTextField(controller: priceController, label: 'Price', icon: Icons.attach_money, keyboardType: TextInputType.number),
              ],
            ),
          ),
        ),
        actionsPadding: const EdgeInsets.fromLTRB(24, 0, 24, 20),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogContext),
            child: const Text('Cancel', style: TextStyle(color: Colors.white70)),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.blueAccent,
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
            ),
            onPressed: () async {
              final name = nameController.text.trim();
              final instructorName = instructorNameController.text.trim();
              final hours = int.tryParse(hoursController.text.trim()) ?? 0;
              final price = double.tryParse(priceController.text.trim()) ?? 0.0;

              if (name.isEmpty) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Please enter course name'), backgroundColor: Colors.red),
                );
                return;
              }

              try {
                if (course == null) {
                  await _supabase.from('courses').insert({
                    'course_name': name,
                    'instructor_name': instructorName,
                    'course_hours': hours,
                    'price': price,
                    'enrolled_students_count': 0,
                  });
                } else {
                  await _supabase.from('courses').update({
                    'course_name': name,
                    'instructor_name': instructorName,
                    'course_hours': hours,
                    'price': price,
                  }).eq('course_id', course['course_id']);
                }

                if (!dialogContext.mounted) return;
                Navigator.pop(dialogContext);
                _fetchDashboardData();

                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Course saved successfully!'), backgroundColor: Colors.green),
                );
              } catch (e) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Failed to save: $e'), backgroundColor: Colors.red),
                );
              }
            },
            child: Text(course == null ? 'Add' : 'Save'),
          ),
        ],
      ),
    );
  }

  Widget _buildTextField({
    required TextEditingController controller,
    required String label,
    required IconData icon,
    TextInputType keyboardType = TextInputType.text,
  }) {
    return TextField(
      controller: controller,
      keyboardType: keyboardType,
      style: const TextStyle(color: Colors.white, fontSize: 14),
      decoration: InputDecoration(
        labelText: label,
        labelStyle: const TextStyle(color: Colors.white60, fontSize: 13),
        prefixIcon: Icon(icon, color: Colors.blueAccent, size: 18),
        filled: true,
        fillColor: const Color(0xFF13111C),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: BorderSide(color: Colors.white.withValues(alpha: 0.1)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: BorderSide(color: Colors.white.withValues(alpha: 0.1)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: Colors.blueAccent, width: 1.5),
        ),
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      ),
    );
  }

  void _deleteCourseWithUndo(Map<String, dynamic> course) {
    final courseId = course['course_id'];

    setState(() {
      _courses.removeWhere((c) => c['course_id'] == courseId);
    });

    ScaffoldMessenger.of(context).clearSnackBars();
    bool isUndone = false;

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        duration: const Duration(seconds: 5),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(child: Text('Deleted "${course['course_name']}"')),
                TextButton(
                  onPressed: () {
                    isUndone = true;
                    ScaffoldMessenger.of(context).hideCurrentSnackBar();
                    setState(() {
                      _courses.add(course);
                    });
                  },
                  child: const Text('UNDO', style: TextStyle(color: Colors.amber, fontWeight: FontWeight.bold)),
                ),
              ],
            ),
            const SizedBox(height: 4),
            TweenAnimationBuilder<double>(
              tween: Tween<double>(begin: 1.0, end: 0.0),
              duration: const Duration(seconds: 5),
              builder: (context, value, child) {
                return LinearProgressIndicator(
                  value: value,
                  backgroundColor: Colors.white24,
                  valueColor: const AlwaysStoppedAnimation<Color>(Colors.amber),
                );
              },
            ),
          ],
        ),
      ),
    ).closed.then((reason) async {
      if (!isUndone && reason != SnackBarClosedReason.hide) {
        try {
          await _supabase.from('courses').delete().eq('course_id', courseId);
        } catch (e) {
          if (!mounted) return;
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Error deleting from database: $e'), backgroundColor: Colors.red),
          );
          _fetchDashboardData();
        }
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF13111C),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E1B2E),
        title: const Text('Smart University Dashboard', style: TextStyle(color: Colors.white, fontSize: 16)),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout, color: Colors.white),
            onPressed: () => Navigator.pushReplacementNamed(context, '/login'),
          ),
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFF231F3D),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.deepPurple.withValues(alpha: 0.3)),
              ),
              child: const Text(
                'SMART UNIVERSITY ADMIN CONTROL PANEL',
                style: TextStyle(color: Colors.blueAccent, fontWeight: FontWeight.bold, letterSpacing: 1),
                textAlign: TextAlign.center,
              ),
            ),
            const SizedBox(height: 20),
            Row(
              children: [
                _buildStatCard('Total Courses', '${_courses.length}', Colors.blue, null),
                const SizedBox(width: 12),
                // ربط بطاقة Total Students بفتح نافذة قائمة الطلاب عند الضغط عليها
                _buildStatCard('Total Students', '$_totalStudents', Colors.purple, _showAllStudentsDialog),
              ],
            ),
            const SizedBox(height: 24),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('Courses Management', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                ElevatedButton.icon(
                  onPressed: () => _showCourseDialog(),
                  icon: const Icon(Icons.add, size: 16),
                  label: const Text('Add Course'),
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.blueAccent),
                ),
              ],
            ),
            const SizedBox(height: 12),
            _courses.isEmpty
                ? const Center(child: Padding(padding: EdgeInsets.all(40), child: Text('No courses found', style: TextStyle(color: Colors.white54))))
                : ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _courses.length,
              itemBuilder: (context, index) {
                final course = _courses[index];
                return Container(
                  margin: const EdgeInsets.only(bottom: 12),
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: const Color(0xFF1E1B2E),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.white10),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(course['course_name'] ?? '', style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                            const SizedBox(height: 4),
                            Text('Instructor: ${course['instructor_name'] ?? 'Not specified'}', style: const TextStyle(color: Colors.blueAccent, fontSize: 13)),
                            const SizedBox(height: 2),
                            // جعل عدد المشتركين قابل للضغط لمعرفة الطلاب المشتركين في هذا الكورس
                            InkWell(
                              onTap: () => _showCourseEnrolledStudents(course),
                              child: Padding(
                                padding: const EdgeInsets.symmetric(vertical: 2),
                                child: Text(
                                  'Hours: ${course['course_hours']}  |  Price: \$${course['price']}  |  Enrolled: ${course['enrolled_students_count'] ?? 0} (View Students)',
                                  style: const TextStyle(color: Colors.amberAccent, fontSize: 12, decoration: TextDecoration.underline),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      Row(
                        children: [
                          IconButton(
                            icon: const Icon(Icons.edit_outlined, color: Colors.blueAccent),
                            onPressed: () => _showCourseDialog(course: course),
                          ),
                          IconButton(
                            icon: const Icon(Icons.delete_outline, color: Colors.redAccent),
                            onPressed: () => _deleteCourseWithUndo(course),
                          ),
                        ],
                      ),
                    ],
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard(String title, String value, Color color, VoidCallback? onTap) {
    return Expanded(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: const Color(0xFF1E1B2E),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: color.withValues(alpha: 0.3)),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(value, style: TextStyle(color: color, fontSize: 24, fontWeight: FontWeight.bold)),
                  if (onTap != null) Icon(Icons.arrow_forward_ios, size: 14, color: color.withValues(alpha: 0.7)),
                ],
              ),
              const SizedBox(height: 4),
              Text(title, style: const TextStyle(color: Colors.white60, fontSize: 12)),
            ],
          ),
        ),
      ),
    );
  }
}