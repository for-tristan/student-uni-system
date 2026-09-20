// lib/main.dart
// Smart University Assistant — App entry point.

import 'package:flutter/material.dart';
import 'theme/app_theme.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';
import 'screens/courses_screen.dart';
import 'screens/course_details_screen.dart';
import 'screens/recommendations_screen.dart';
import 'screens/progress_screen.dart';
import 'screens/profile_screen.dart';
import 'screens/assistant_screen.dart';

void main() {
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
