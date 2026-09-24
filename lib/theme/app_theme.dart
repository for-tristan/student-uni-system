// lib/theme/app_theme.dart
// Smart University Assistant — Flutter theme.
// Restrained academic palette. No gradients, no glow.

import 'package:flutter/material.dart';

class AppColors {
  AppColors._();

  // Surfaces
  static const Color background = Color(0xFFF7F7F5);
  static const Color surface = Color(0xFFFFFFFF);
  static const Color surfaceRaised = Color(0xFFFAFAF8);

  // Borders & dividers
  static const Color border = Color(0xFFE4E4E1);
  static const Color hairline = Color(0xFFE4E4E1);

  // Text
  static const Color textPrimary = Color(0xFF171717);
  static const Color textSecondary = Color(0xFF666666);
  static const Color textTertiary = Color(0xFF9A9A96);

  // Accent — used sparingly
  static const Color accent = Color(0xFF315CFF);
  static const Color accentForeground = Color(0xFFFFFFFF);
  static const Color accentSurface = Color(0xFFEEF1FF);
  static const Color accentSurfaceForeground = Color(0xFF1D3A8A);

  // Semantic
  static const Color success = Color(0xFF2F7D4A);
  static const Color successSurface = Color(0xFFECF5EF);
  static const Color warning = Color(0xFFA66A00);
  static const Color warningSurface = Color(0xFFFBF2E3);
  static const Color error = Color(0xFFB42318);
  static const Color errorSurface = Color(0xFFFBEAE8);

  // Difficulty tags — neutral tone
  static const Color difficultyIntro = Color(0xFF666666);
  static const Color difficultyInter = Color(0xFF666666);
  static const Color difficultyAdvanced = Color(0xFF666666);

  static Color? get errorForeground => null;
}

class AppSpacing {
  AppSpacing._();
  static const double s4 = 4;
  static const double s8 = 8;
  static const double s12 = 12;
  static const double s16 = 16;
  static const double s20 = 20;
  static const double s24 = 24;
  static const double s32 = 32;
  static const double s40 = 40;
  static const double s48 = 48;
  static const double s64 = 64;
}

class AppRadii {
  AppRadii._();
  static const double sm = 4;
  static const double md = 6;
  static const double lg = 8;
  static const double xl = 12;
}

class AppTheme {
  AppTheme._();

  static ThemeData light() {
    final base = ThemeData.light(useMaterial3: true);
    return base.copyWith(
      colorScheme: base.colorScheme.copyWith(
        surface: AppColors.surface,
        primary: AppColors.accent,
        onPrimary: AppColors.accentForeground,
        secondary: AppColors.accent,
        onSecondary: AppColors.accentForeground,
        error: AppColors.error,
        onError: AppColors.errorForeground,
        onSurface: AppColors.textPrimary,
        outline: AppColors.border,
      ),
      scaffoldBackgroundColor: AppColors.background,
      dividerColor: AppColors.border,
      dividerTheme: const DividerThemeData(
        color: AppColors.border,
        thickness: 1,
        space: 1,
      ),
      textTheme: const TextTheme(
        displayLarge: TextStyle(
          fontSize: 34, height: 40 / 34, fontWeight: FontWeight.w600,
          letterSpacing: -0.34, color: AppColors.textPrimary,
        ),
        displayMedium: TextStyle(
          fontSize: 26, height: 32 / 26, fontWeight: FontWeight.w600,
          letterSpacing: -0.26, color: AppColors.textPrimary,
        ),
        headlineMedium: TextStyle(
          fontSize: 20, height: 28 / 20, fontWeight: FontWeight.w600,
          color: AppColors.textPrimary,
        ),
        titleMedium: TextStyle(
          fontSize: 16, height: 24 / 16, fontWeight: FontWeight.w600,
          color: AppColors.textPrimary,
        ),
        bodyMedium: TextStyle(
          fontSize: 14, height: 22 / 14, fontWeight: FontWeight.w400,
          color: AppColors.textPrimary,
        ),
        bodySmall: TextStyle(
          fontSize: 13, height: 20 / 13, fontWeight: FontWeight.w400,
          color: AppColors.textPrimary,
        ),
        labelSmall: TextStyle(
          fontSize: 12, height: 16 / 12, fontWeight: FontWeight.w500,
          color: AppColors.textSecondary,
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: AppColors.surface,
        contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadii.md),
          borderSide: const BorderSide(color: AppColors.border, width: 1),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadii.md),
          borderSide: const BorderSide(color: AppColors.border, width: 1),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadii.md),
          borderSide: const BorderSide(color: AppColors.accent, width: 2),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadii.md),
          borderSide: const BorderSide(color: AppColors.error, width: 1),
        ),
        labelStyle: const TextStyle(
          fontSize: 11, fontWeight: FontWeight.w500,
          letterSpacing: 0.66,
          color: AppColors.textSecondary,
        ),
        hintStyle: const TextStyle(color: AppColors.textTertiary),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.accent,
          foregroundColor: AppColors.accentForeground,
          elevation: 0,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppRadii.md),
          ),
          textStyle: const TextStyle(
            fontSize: 14, fontWeight: FontWeight.w500,
          ),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: AppColors.textPrimary,
          side: const BorderSide(color: AppColors.border, width: 1),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppRadii.md),
          ),
          textStyle: const TextStyle(
            fontSize: 14, fontWeight: FontWeight.w500,
          ),
        ),
      ),
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          foregroundColor: AppColors.accent,
          textStyle: const TextStyle(
            fontSize: 13, fontWeight: FontWeight.w500,
          ),
        ),
      ),
    );
  }
}