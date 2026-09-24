// lib/main.dart
// Smart University Assistant — App entry point.

import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart'; // 1. استيراد حزمة سوبابيس
import 'theme/app_theme.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';
import 'screens/courses_screen.dart';
import 'screens/course_details_screen.dart';
import 'screens/recommendations_screen.dart';
import 'screens/progress_screen.dart';
import 'screens/profile_screen.dart';
import 'screens/assistant_screen.dart';
import 'screens/admin_dashboard_screen.dart'; // 2. استيراد شاشة لوحة تحكم الأدمن

void main() async {
  // 3. التأكد من تهيئة ودجتس فلاتر قبل تشغيل أي شيء
  WidgetsFlutterBinding.ensureInitialized();

  // 4. تهيئة Supabase بالمعلومات الخاصة بمشروعك
  // (استبدلي الـ URL والـ AnonKey بالبيانات الخاصة بمشروعك من لوحة تحكم Supabase)
  await Supabase.initialize(
    url: 'https://tziyaoymsbyoeenkxnot.supabase.co',
    anonKey: 'sb_publishable_ldYch8F68SclwKSTCCmwZw_xoSvzVmZ',
  );

  runApp(const SmartUniversityAssistant());
}

class SmartUniversityAssistant extends StatelessWidget {
  const SmartUniversityAssistant({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart University Assistant',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light(),
      initialRoute: '/',
      onGenerateRoute: (settings) {
        switch (settings.name) {
          case '/':
            return MaterialPageRoute(builder: (_) => const LoginScreen());
          case '/admin_dashboard': // 5. إضافة مسار الأدمن الجديد
            return MaterialPageRoute(builder: (_) => const AdminDashboardScreen());
          case '/home':
            return MaterialPageRoute(builder: (_) => const HomeScreen());
          case '/courses':
            return MaterialPageRoute(builder: (_) => const CoursesScreen());
          case '/course':
            final code = settings.arguments as String;
            return MaterialPageRoute(
              builder: (_) => CourseDetailsScreen(courseCode: code),
            );
          case '/recommendations':
            return MaterialPageRoute(builder: (_) => const RecommendationsScreen());
          case '/progress':
            return MaterialPageRoute(builder: (_) => const ProgressScreen());
          case '/profile':
            return MaterialPageRoute(builder: (_) => const ProfileScreen());
          case '/assistant':
            return MaterialPageRoute(builder: (_) => const AssistantScreen());
          default:
            return MaterialPageRoute(builder: (_) => const LoginScreen());
        }
      },
    );
  }
}