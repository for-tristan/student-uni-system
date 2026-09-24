// lib/screens/signup_screen.dart
import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../theme/app_theme.dart';

class SignupScreen extends StatefulWidget {
  const SignupScreen({super.key});

  @override
  State<SignupScreen> createState() => _SignupScreenState();
}

class _SignupScreenState extends State<SignupScreen> {
  bool _loading = false;
  String? _error;

  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  final _supabase = Supabase.instance.client;

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(24, 64, 24, 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    width: 32, height: 32,
                    decoration: BoxDecoration(
                      color: AppColors.textPrimary,
                      borderRadius: BorderRadius.circular(AppRadii.md),
                    ),
                    child: const Icon(Icons.school, size: 16, color: AppColors.background),
                  ),
                  const SizedBox(width: 8),
                  const Text('Smart University Assistant',
                    style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
                  ),
                ],
              ),
              const SizedBox(height: 48),
              const Text('Create Account',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.w600),
              ),
              const SizedBox(height: 4),
              const Text('Sign up as a new student.',
                style: TextStyle(fontSize: 13, color: AppColors.textSecondary),
              ),
              const SizedBox(height: 32),

              // Name
              const Text('NAME', style: TextStyle(fontSize: 11, fontWeight: FontWeight.w500, color: AppColors.textSecondary)),
              const SizedBox(height: 4),
              TextField(
                controller: _nameController,
                decoration: const InputDecoration(hintText: 'Your Name'),
              ),
              const SizedBox(height: 16),

              // Email
              const Text('EMAIL', style: TextStyle(fontSize: 11, fontWeight: FontWeight.w500, color: AppColors.textSecondary)),
              const SizedBox(height: 4),
              TextField(
                controller: _emailController,
                decoration: const InputDecoration(hintText: 'student@university.com'),
              ),
              const SizedBox(height: 16),

              // Password
              const Text('PASSWORD', style: TextStyle(fontSize: 11, fontWeight: FontWeight.w500, color: AppColors.textSecondary)),
              const SizedBox(height: 4),
              TextField(
                controller: _passwordController,
                obscureText: true,
                decoration: const InputDecoration(hintText: '••••••••'),
              ),

              if (_error != null) ...[
                const SizedBox(height: 8),
                Text(_error!, style: const TextStyle(fontSize: 12, color: AppColors.error)),
              ],

              const SizedBox(height: 24),

              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _loading ? null : _onSignup,
                  child: _loading
                      ? const SizedBox(height: 14, width: 14, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                      : const Text('Sign up'),
                ),
              ),
              const SizedBox(height: 12),
              Center(
                child: TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('Already have an account? Sign in'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _onSignup() async {
    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      final name = _nameController.text.trim();
      final email = _emailController.text.trim();

      if (name.isEmpty || email.isEmpty) {
        setState(() {
          _error = 'Please fill in all fields';
          _loading = false;
        });
        return;
      }

      // إضافة الطالب الجديد مباشرة لجدول users بدور student
      await _supabase.from('users').insert({
        'name': name,
        'email': email,
        'role': 'student',
      });

      if (!mounted) return;

      // رجوعه لشاشة اللوج إن أو دخوله الهوم مباشرة
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Account created successfully! Please sign in.')),
      );
      Navigator.pop(context);
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _error = 'Error: $e';
        _loading = false;
      });
    }
  }
}