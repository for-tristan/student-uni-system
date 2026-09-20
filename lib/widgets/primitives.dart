// lib/widgets/primitives.dart
// Smart University Assistant — shared Flutter widgets.
// Restrained academic style. Flat, thin borders. No glow, no gradients.

import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class AppSectionTitle extends StatelessWidget {
  final String title;
  final String? subtitle;
  final Widget? right;
  const AppSectionTitle({
    super.key,
    required this.title,
    this.subtitle,
    this.right,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title,
                  style: const TextStyle(
                    fontSize: 15, fontWeight: FontWeight.w600,
                    letterSpacing: -0.15,
                    color: AppColors.textPrimary,
                  ),
                ),
                if (subtitle != null)
                  Padding(
                    padding: const EdgeInsets.only(top: 2),
                    child: Text(subtitle!,
                      style: const TextStyle(
                        fontSize: 13, color: AppColors.textSecondary,
                      ),
                    ),
                  ),
              ],
            ),
          ),
          if (right != null) right!,
        ],
      ),
    );
  }
}

class DifficultyTag extends StatelessWidget {
  final Difficulty difficulty;
  const DifficultyTag({super.key, required this.difficulty});

  String get _label {
    switch (difficulty) {
      case Difficulty.introductory: return 'Introductory';
      case Difficulty.intermediate: return 'Intermediate';
      case Difficulty.advanced: return 'Advanced';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Text(_label.toUpperCase(),
      style: const TextStyle(
        fontSize: 11, fontWeight: FontWeight.w500,
        letterSpacing: 0.66,
        color: AppColors.textSecondary,
      ),
    );
  }
}

class StatusPill extends StatelessWidget {
  final StatusKind kind;
  final String label;
  const StatusPill({super.key, required this.kind, required this.label});

  static const _styles = <StatusKind, ({Color bg, Color fg})>{
    StatusKind.neutral:  (bg: Color(0xFFF1F1EE), fg: Color(0xFF666666)),
    StatusKind.success:  (bg: Color(0xFFECF5EF), fg: Color(0xFF2F7D4A)),
    StatusKind.warning:  (bg: Color(0xFFFBF2E3), fg: Color(0xFFA66A00)),
    StatusKind.error:    (bg: Color(0xFFFBEAE8), fg: Color(0xFFB42318)),
    StatusKind.accent:   (bg: Color(0xFFEEF1FF), fg: Color(0xFF1D3A8A)),
  };

  @override
  Widget build(BuildContext context) {
    final s = _styles[kind]!;
    return Container(
      height: 20,
      padding: const EdgeInsets.symmetric(horizontal: 6),
      decoration: BoxDecoration(
        color: s.bg,
        borderRadius: BorderRadius.circular(AppRadii.sm),
      ),
      alignment: Alignment.center,
      child: Text(label,
        style: TextStyle(
          fontSize: 11, fontWeight: FontWeight.w500,
          color: s.fg, height: 1,
        ),
      ),
    );
  }
}

enum StatusKind { neutral, success, warning, error, accent }

class MatchMeter extends StatelessWidget {
  final int value;
  const MatchMeter({super.key, required this.value});

  @override
  Widget build(BuildContext context) {
    final v = value.clamp(0, 100);
    final tone = v >= 85
        ? AppColors.success
        : v >= 70
            ? AppColors.accent
            : AppColors.warning;
    return Row(
      children: [
        Expanded(
          child: Container(
            height: 6,
            decoration: BoxDecoration(
              color: AppColors.surfaceRaised,
              borderRadius: BorderRadius.circular(AppRadii.sm),
            ),
            child: Align(
              alignment: Alignment.centerLeft,
              child: FractionallySizedBox(
                widthFactor: v / 100,
                child: Container(
                  decoration: BoxDecoration(
                    color: tone,
                    borderRadius: BorderRadius.circular(AppRadii.sm),
                  ),
                ),
              ),
            ),
          ),
        ),
        const SizedBox(width: 8),
        Text('$v%',
          style: const TextStyle(
            fontSize: 12, fontWeight: FontWeight.w500,
            color: AppColors.textPrimary,
            fontFeatures: [FontFeature.tabularFigures()],
          ),
        ),
      ],
    );
  }
}

class BottomNavItem extends StatelessWidget {
  final String label;
  final bool active;
  final IconData icon;
  final VoidCallback? onTap;
  const BottomNavItem({
    super.key,
    required this.label,
    required this.active,
    required this.icon,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.only(top: 8, bottom: 12),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                height: 24,
                width: 48,
                decoration: BoxDecoration(
                  color: active ? AppColors.accentSurface : Colors.transparent,
                  borderRadius: BorderRadius.circular(AppRadii.md),
                ),
                child: Icon(icon,
                  size: 14,
                  color: active
                      ? AppColors.accentSurfaceForeground
                      : AppColors.textSecondary,
                ),
              ),
              const SizedBox(height: 4),
              Text(label,
                style: TextStyle(
                  fontSize: 10, fontWeight: FontWeight.w500,
                  color: active
                      ? AppColors.textPrimary
                      : AppColors.textSecondary,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class MobileScaffold extends StatelessWidget {
  final Widget child;
  final String activeTab;
  const MobileScaffold({
    super.key,
    required this.child,
    required this.activeTab,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(child: child),
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          color: AppColors.surface,
          border: Border(
            top: BorderSide(color: AppColors.border, width: 1),
          ),
        ),
        child: Row(
          children: [
            BottomNavItem(
              label: 'Home',
              active: activeTab == 'home',
              icon: Icons.home_outlined,
              onTap: () => Navigator.pushReplacementNamed(context, '/home'),
            ),
            BottomNavItem(
              label: 'Courses',
              active: activeTab == 'courses',
              icon: Icons.menu_book_outlined,
              onTap: () => Navigator.pushReplacementNamed(context, '/courses'),
            ),
            BottomNavItem(
              label: 'Assistant',
              active: activeTab == 'assistant',
              icon: Icons.chat_bubble_outline,
              onTap: () => Navigator.pushReplacementNamed(context, '/assistant'),
            ),
            BottomNavItem(
              label: 'Progress',
              active: activeTab == 'progress',
              icon: Icons.trending_up,
              onTap: () => Navigator.pushReplacementNamed(context, '/progress'),
            ),
            BottomNavItem(
              label: 'Profile',
              active: activeTab == 'profile',
              icon: Icons.person_outline,
              onTap: () => Navigator.pushReplacementNamed(context, '/profile'),
            ),
          ],
        ),
      ),
    );
  }
}

class ScreenHeader extends StatelessWidget {
  final String title;
  final Widget? right;
  const ScreenHeader({super.key, required this.title, this.right});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 48,
      decoration: const BoxDecoration(
        color: AppColors.background,
        border: Border(
          bottom: BorderSide(color: AppColors.border, width: 1),
        ),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 20),
      child: Row(
        children: [
          Expanded(
            child: Text(title,
              style: const TextStyle(
                fontSize: 15, fontWeight: FontWeight.w600,
                letterSpacing: -0.05,
                color: AppColors.textPrimary,
              ),
            ),
          ),
          if (right != null) right!,
        ],
      ),
    );
  }
}

class SectionHeader extends StatelessWidget {
  final String label;
  final Widget? right;
  const SectionHeader({super.key, required this.label, this.right});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        children: [
          Expanded(
            child: Text(label.toUpperCase(),
              style: const TextStyle(
                fontSize: 11, fontWeight: FontWeight.w500,
                letterSpacing: 0.66,
                color: AppColors.textSecondary,
              ),
            ),
          ),
          if (right != null) right!,
        ],
      ),
    );
  }
}

class HairlineDivider extends StatelessWidget {
  const HairlineDivider({super.key});
  @override
  Widget build(BuildContext context) {
    return Container(height: 1, color: AppColors.border);
  }
}
