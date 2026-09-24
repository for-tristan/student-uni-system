// lib/screens/login_screen.dart
// Smart University Assistant — Login screen.

import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../theme/app_theme.dart';

// متغير عام وبسيط لحفظ إيميل المستخدم الحالي في الذاكرة لتسهيل عرضه في التطبيق
String? currentLoggedInEmail;

// شاشة تسجيل الحساب الجديد (Sign up)
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

              _Label('Name'),
              const SizedBox(height: 4),
              TextField(
                controller: _nameController,
                decoration: const InputDecoration(hintText: 'Your Name'),
              ),
              const SizedBox(height: 16),

              _Label('Email'),
              const SizedBox(height: 4),
              TextField(
                controller: _emailController,
                decoration: const InputDecoration(hintText: 'student@university.com'),
              ),
              const SizedBox(height: 16),

              _Label('Password'),
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

      await _supabase.from('users').insert({
        'name': name,
        'email': email,
        'role': 'student',
      });

      if (!mounted) return;

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

// شاشة تسجيل الدخول الرئيسية
class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  bool _showPassword = false;
  bool _loading = false;
  String? _error;

  final TextEditingController _identifierController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  String _selectedRole = 'student';
  final _supabase = Supabase.instance.client;

  @override
  void dispose() {
    _identifierController.dispose();
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
              const Text('Sign in',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.w600),
              ),
              const SizedBox(height: 4),
              const Text('Use your university email.',
                style: TextStyle(fontSize: 13, color: AppColors.textSecondary),
              ),
              const SizedBox(height: 32),

              _Label('Email'),
              const SizedBox(height: 4),
              TextField(
                controller: _identifierController,
                decoration: const InputDecoration(hintText: 'example@university.com'),
              ),
              const SizedBox(height: 16),

              _Label('Password'),
              const SizedBox(height: 4),
              TextField(
                controller: _passwordController,
                obscureText: !_showPassword,
                decoration: InputDecoration(
                  hintText: '••••••••',
                  suffixIcon: IconButton(
                    icon: Icon(
                      _showPassword ? Icons.visibility_off_outlined : Icons.visibility_outlined,
                      size: 16, color: AppColors.textSecondary,
                    ),
                    onPressed: () => setState(() => _showPassword = !_showPassword),
                  ),
                ),
              ),
              const SizedBox(height: 16),

              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Row(
                    children: [
                      Radio<String>(
                        value: 'admin',
                        groupValue: _selectedRole,
                        onChanged: (val) => setState(() => _selectedRole = val!),
                      ),
                      const Text('Admin', style: TextStyle(fontSize: 12, color: AppColors.textSecondary)),
                    ],
                  ),
                  const SizedBox(width: 16),
                  Row(
                    children: [
                      Radio<String>(
                        value: 'student',
                        groupValue: _selectedRole,
                        onChanged: (val) => setState(() => _selectedRole = val!),
                      ),
                      const Text('Student', style: TextStyle(fontSize: 12, color: AppColors.textSecondary)),
                    ],
                  ),
                ],
              ),

              if (_error != null) ...[
                const SizedBox(height: 8),
                Text(_error!, style: const TextStyle(fontSize: 12, color: AppColors.error)),
              ],

              const SizedBox(height: 24),

              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _loading ? null : _onSubmit,
                  child: _loading
                      ? const SizedBox(height: 14, width: 14, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                      : const Text('Sign in'),
                ),
              ),
              const SizedBox(height: 12),
              Center(
                child: TextButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => const SignupScreen()),
                    );
                  },
                  child: const Text("Don't have an account? Sign up"),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _onSubmit() async {
    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      final email = _identifierController.text.trim();

      if (email.isEmpty) {
        setState(() {
          _error = 'Please enter your email';
          _loading = false;
        });
        return;
      }

      final response = await _supabase
          .from('users')
          .select()
          .eq('email', email)
          .maybeSingle();

      if (!mounted) return;

      if (response == null) {
        setState(() {
          _error = 'User not found. Please sign up first.';
          _loading = false;
        });
        return;
      }

      final userRole = response['role'].toString().trim().toLowerCase();

      // حفظ الإيميل المسجل حالياً لكي تظهر بياناته في الـ Home و Profile
      currentLoggedInEmail = email;

      setState(() => _loading = false);

      if (_selectedRole == 'admin' && userRole == 'admin') {
        Navigator.pushReplacementNamed(context, '/admin_dashboard');
      } else if (_selectedRole == 'student' && (userRole == 'student' || userRole == 'user')) {
        Navigator.pushReplacementNamed(context, '/home');
      } else {
        setState(() {
          _error = 'Role mismatch! Please check your account type.';
        });
      }
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _error = 'An error occurred: $e';
        _loading = false;
      });
    }
  }
}

class _Label extends StatelessWidget {
  final String text;
  const _Label(this.text);

  @override
  Widget build(BuildContext context) {
    return Text(text.toUpperCase(),
      style: const TextStyle(
        fontSize: 11, fontWeight: FontWeight.w500,
        letterSpacing: 0.66, color: AppColors.textSecondary,
      ),
    );
  }
}