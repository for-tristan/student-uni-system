// lib/screens/login_screen.dart
// Smart University Assistant — Login screen.
// Straightforward. Gets the user into the product quickly.

import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  bool _showPassword = false;
  bool _loading = false;
  String? _error;

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
              // Brand
              Row(
                children: [
                  Container(
                    width: 32, height: 32,
                    decoration: BoxDecoration(
                      color: AppColors.textPrimary,
                      borderRadius: BorderRadius.circular(AppRadii.md),
                    ),
                    child: const Icon(Icons.school,
                      size: 16, color: AppColors.background),
                  ),
                  const SizedBox(width: 8),
                  const Text('Smart University Assistant',
                    style: TextStyle(
                      fontSize: 14, fontWeight: FontWeight.w600,
                      letterSpacing: -0.1,
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 48),

              const Text('Sign in',
                style: TextStyle(
                  fontSize: 22, fontWeight: FontWeight.w600,
                  letterSpacing: -0.22,
                ),
              ),
              const SizedBox(height: 4),
              const Text('Use your university student ID.',
                style: TextStyle(
                  fontSize: 13, color: AppColors.textSecondary,
                ),
              ),

              const SizedBox(height: 32),

              // Student ID
              _Label('Student ID or email'),
              const SizedBox(height: 4),
              TextField(
                decoration: InputDecoration(
                  hintText: 'S-2023-1148',
                  errorText: _error != null ? '' : null,
                ),
              ),

              const SizedBox(height: 16),

              // Password
              _Label('Password'),
              const SizedBox(height: 4),
              TextField(
                obscureText: !_showPassword,
                decoration: InputDecoration(
                  hintText: '••••••••',
                  suffixIcon: IconButton(
                    icon: Icon(
                      _showPassword
                          ? Icons.visibility_off_outlined
                          : Icons.visibility_outlined,
                      size: 16,
                      color: AppColors.textSecondary,
                    ),
                    onPressed: () => setState(
                      () => _showPassword = !_showPassword,
                    ),
                  ),
                ),
              ),

              if (_error != null) ...[
                const SizedBox(height: 8),
                Text(_error!,
                  style: const TextStyle(
                    fontSize: 12, color: AppColors.error,
                  ),
                ),
              ],

              const SizedBox(height: 24),

              // Sign in
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _loading ? null : _onSubmit,
                  child: _loading
                      ? const SizedBox(
                          height: 14, width: 14,
                          child: CircularProgressIndicator(
                            strokeWidth: 2, color: Colors.white,
                          ),
                        )
                      : const Text('Sign in'),
                ),
              ),

              const SizedBox(height: 12),
              Center(
                child: TextButton(
                  onPressed: () {},
                  child: const Text('Forgot password?'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _onSubmit() {
    setState(() {
      _loading = true;
      _error = null;
    });
    Future.delayed(const Duration(milliseconds: 1200), () {
      if (!mounted) return;
      setState(() => _loading = false);
      Navigator.pushReplacementNamed(context, '/home');
    });
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
        letterSpacing: 0.66,
        color: AppColors.textSecondary,
      ),
    );
  }
}
