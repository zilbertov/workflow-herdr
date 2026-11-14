# Workflow Herdr

Контракт → пропорциональный план → исполнение → проверенные receipts. Herdr остаётся runtime; без него можно применить контракт в текущем чате без имитации агентов.

Full trust поддерживается: по умолчанию наследуется политика CLI, явный профиль задаётся для точного корня проекта через `scripts/trust_policy.py --project <root> --full-trust`. Автопрохождение trust — отдельный флаг `--auto-confirm-workspace`, оно возможно только при видимом выбранном Yes. Подробности: [SKILL](SKILL.md), [trust policy](references/trust-policy.md), [изменения](../../CHANGES.md).
