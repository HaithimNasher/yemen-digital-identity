# Architecture

## v1
المشروع في الإصدار الأول عبارة عن:
- Static portal عبر GitHub Pages.
- ملفات بيانات JSON موثقة.
- أدوات Python للتحقق من البيانات.
- GitHub Actions للاختبار والنشر.

## v2 المقترح
```text
Public Portal
     |
API Gateway
     |
+----+---------+----------+
|              |          |
RDAP client   DNS probe   Metrics
|              |          |
PostgreSQL / Time-series store
     |
Observatory Dashboard
```

## ضوابط
- عدم تخزين بيانات شخصية غير لازمة.
- Rate limiting.
- Cache لطلبات RDAP/DNS.
- فصل البيانات الخام عن البيانات المعروضة.
