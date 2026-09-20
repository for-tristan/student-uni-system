// lib/screens/profile_screen.dart
// Smart University Assistant — Profile.

import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../data/models.dart';
import '../widgets/primitives.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return MobileScaffold(
      activeTab: 'profile',
      child: Column(
        children: [
          ScreenHeader(
            title: 'Profile',
            right: IconButton(
              icon: const Icon(Icons.settings_outlined, size: 16),
              onPressed: () {},
            ),
          ),
          Expanded(
            child: ListView(
              padding: EdgeInsets.zero,
              children: [
                Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('STUDENT',
                        style: TextStyle(
                          fontSize: 11, fontWeight: FontWeight.w500,
                          letterSpacing: 0.66,
                          color: AppColors.textSecondary,
                        ),
                      ),
                      const SizedBox(height: 2),
                      Text(student.name,
                        style: const TextStyle(
                          fontSize: 22, fontWeight: FontWeight.w600,
                          letterSpacing: -0.22,
                        ),
                      ),
                      const SizedBox(height: 2),
                      Text(student.email,
                        style: const TextStyle(
                          fontSize: 12, color: AppColors.textSecondary,
                        ),
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
                      const SectionHeader(label: 'Student information'),
                      _InfoRow('Student ID', student.id),
                      _InfoRow('Major', student.major),
                      _InfoRow('Year', student.year),
                      _InfoRow('GPA', student.gpa.toStringAsFixed(2)),
                      _InfoRow('Graduation', student.graduation),
                    ],
                  ),
                ),
                const HairlineDivider(),

                Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const SectionHeader(label: 'Interests'),
                      Wrap(
                        spacing: 6, runSpacing: 6,
                        children: student.interests.map((i) => Container(
                          height: 24,
                          padding: const EdgeInsets.symmetric(horizontal: 8),
                          decoration: BoxDecoration(
                            color: AppColors.accentSurface,
                            borderRadius: BorderRadius.circular(AppRadii.md),
                          ),
                          alignment: Alignment.center,
                          child: Text(i,
                            style: const TextStyle(
                              fontSize: 12,
                              color: AppColors.accentSurfaceForeground,
                            ),
                          ),
                        )).toList(),
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
                      const SectionHeader(label: 'Skills'),
                      Wrap(
                        spacing: 6, runSpacing: 6,
                        children: student.skills.map((s) => Container(
                          height: 24,
                          padding: const EdgeInsets.symmetric(horizontal: 8),
                          decoration: BoxDecoration(
                            color: AppColors.surface,
                            border: Border.all(color: AppColors.border),
                            borderRadius: BorderRadius.circular(AppRadii.md),
                          ),
                          alignment: Alignment.center,
                          child: Text(s, style: const TextStyle(fontSize: 12)),
                        )).toList(),
                      ),
                    ],
                  ),
                ),
                const HairlineDivider(),

                Padding(
                  padding: const EdgeInsets.fromLTRB(20, 16, 20, 8),
                  child: Column(
                    children: [
                      _ActionTile(icon: Icons.edit_outlined, label: 'Edit profile', onTap: () {}),
                      const SizedBox(height: 4),
                      _ActionTile(icon: Icons.settings_outlined, label: 'Settings', onTap: () {}),
                      const SizedBox(height: 4),
                      _ActionTile(icon: Icons.logout, label: 'Log out', danger: true, onTap: () {}),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _InfoRow extends StatelessWidget {
  final String label;
  final String value;
  const _InfoRow(this.label, this.value);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 10),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label,
            style: const TextStyle(
              fontSize: 12, color: AppColors.textSecondary,
            ),
          ),
          Text(value,
            style: const TextStyle(
              fontSize: 13, fontWeight: FontWeight.w500,
              fontFeatures: [FontFeature.tabularFigures()],
            ),
          ),
        ],
      ),
    );
  }
}

class _ActionTile extends StatelessWidget {
  final IconData icon;
  final String label;
  final bool danger;
  final VoidCallback onTap;
  const _ActionTile({
    required this.icon,
    required this.label,
    this.danger = false,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: AppColors.surface,
      borderRadius: BorderRadius.circular(AppRadii.md),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppRadii.md),
        child: Container(
          height: 44,
          padding: const EdgeInsets.symmetric(horizontal: 12),
          decoration: BoxDecoration(
            border: Border.all(color: AppColors.border),
            borderRadius: BorderRadius.circular(AppRadii.md),
          ),
          child: Row(
            children: [
              Icon(icon, size: 16,
                color: danger
                    ? AppColors.error
                    : AppColors.textSecondary,
              ),
              const SizedBox(width: 12),
              Text(label,
                style: TextStyle(
                  fontSize: 14,
                  color: danger ? AppColors.error : AppColors.textPrimary,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
