// lib/screens/assistant_screen.dart
// Smart University Assistant — University assistant chat.

import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../data/models.dart';
import '../widgets/primitives.dart';
import 'login_screen.dart'; // لاستخدام currentLoggedInEmail إذا احتجتِ لتحديث البيانات

class AssistantScreen extends StatelessWidget {
  const AssistantScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Column(
          children: [
            // Header مع زر رجوع للهوم
            Container(
              decoration: const BoxDecoration(
                color: AppColors.surface,
                border: Border(
                  bottom: BorderSide(color: AppColors.border, width: 1),
                ),
              ),
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              child: Row(
                children: [
                  // زر الرجوع للصفحة الرئيسية
                  IconButton(
                    icon: const Icon(Icons.arrow_back, size: 20),
                    onPressed: () {
                      Navigator.pushReplacementNamed(context, '/home');
                    },
                  ),
                  const SizedBox(width: 4),
                  Container(
                    width: 28, height: 28,
                    decoration: BoxDecoration(
                      color: AppColors.textPrimary,
                      borderRadius: BorderRadius.circular(AppRadii.md),
                    ),
                    child: const Icon(Icons.chat_bubble_outline,
                        size: 14, color: AppColors.background),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('University Assistant',
                          style: TextStyle(
                            fontSize: 13, fontWeight: FontWeight.w500,
                          ),
                        ),
                        Text('${student.major} · ${student.year}',
                          style: const TextStyle(
                            fontSize: 10, color: AppColors.textSecondary,
                          ),
                        ),
                      ],
                    ),
                  ),
                  TextButton(onPressed: () {}, child: const Text('New')),
                ],
              ),
            ),
            // Conversation
            Expanded(
              child: assistantConversation.isEmpty
                  ? _EmptyAssistant()
                  : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: assistantConversation.length,
                itemBuilder: (context, i) {
                  final m = assistantConversation[i];
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 16),
                    child: _Message(message: m),
                  );
                },
              ),
            ),
            // Composer
            Container(
              decoration: const BoxDecoration(
                color: AppColors.surface,
                border: Border(
                  top: BorderSide(color: AppColors.border, width: 1),
                ),
              ),
              padding: const EdgeInsets.all(12),
              child: Row(
                children: [
                  const Expanded(
                    child: TextField(
                      minLines: 1,
                      maxLines: 4,
                      decoration: InputDecoration(
                        hintText: 'Ask about courses, prerequisites, university rules…',
                        isDense: true,
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Container(
                    width: 40, height: 40,
                    decoration: BoxDecoration(
                      color: AppColors.accent,
                      borderRadius: BorderRadius.circular(AppRadii.md),
                    ),
                    child: const Icon(Icons.send, size: 16, color: Colors.white),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _EmptyAssistant extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 40, height: 40,
            decoration: BoxDecoration(
              color: AppColors.surface,
              border: Border.all(color: AppColors.border),
              borderRadius: BorderRadius.circular(AppRadii.md),
            ),
            child: const Icon(Icons.chat_bubble_outline,
                size: 16, color: AppColors.textSecondary),
          ),
          const SizedBox(height: 12),
          const Text('Ask about your studies.',
            style: TextStyle(fontSize: 15, fontWeight: FontWeight.w500),
          ),
          const SizedBox(height: 4),
          const Text(
            'Course prerequisites, next-semester options, completed courses, university rules.',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 13, color: AppColors.textSecondary),
          ),
        ],
      ),
    );
  }
}

class _Message extends StatelessWidget {
  final AssistantMessage message;
  const _Message({required this.message});

  @override
  Widget build(BuildContext context) {
    final isUser = message.role == 'user';
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: ConstrainedBox(
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.8,
        ),
        child: Column(
          crossAxisAlignment:
          isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              decoration: BoxDecoration(
                color: isUser
                    ? AppColors.surfaceRaised
                    : AppColors.surface,
                border: Border.all(
                  color: isUser ? Colors.transparent : AppColors.border,
                ),
                borderRadius: BorderRadius.only(
                  topLeft: const Radius.circular(8),
                  topRight: const Radius.circular(8),
                  bottomLeft: Radius.circular(isUser ? 8 : 2),
                  bottomRight: Radius.circular(isUser ? 2 : 8),
                ),
              ),
              child: Text(message.content,
                style: const TextStyle(fontSize: 13, height: 1.5),
              ),
            ),
            if (message.sources != null && message.sources!.isNotEmpty) ...[
              const SizedBox(height: 6),
              Wrap(
                spacing: 6, runSpacing: 4,
                children: message.sources!.map((s) => Container(
                  height: 20,
                  padding: const EdgeInsets.symmetric(horizontal: 6),
                  decoration: BoxDecoration(
                    color: AppColors.surface,
                    border: Border.all(color: AppColors.border),
                    borderRadius: BorderRadius.circular(AppRadii.sm),
                  ),
                  alignment: Alignment.center,
                  child: Text('${s.label}${s.code != null ? ' · ${s.code}' : ''}',
                    style: const TextStyle(
                      fontSize: 10, color: AppColors.textSecondary,
                    ),
                  ),
                )).toList(),
              ),
            ],
          ],
        ),
      ),
    );
  }
}