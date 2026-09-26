# 🇾🇪 Yemen Digital Identity Initiative (YDII)

**مبادرة الهوية الرقمية اليمنية** — مشروع مفتوح المصدر لدراسة وتطوير الحضور الرقمي اليمني حول النطاق الوطني **`.ye`**، بالاستفادة من الخبرات الخليجية والدولية في إدارة النطاقات الوطنية.

> **تنبيه مهم:** هذا المشروع **ليس السجل الرسمي لنطاق `.ye`** ولا يمثل TeleYemen أو IANA أو ICANN أو أي جهة حكومية. هو مبادرة بحثية/تقنية مستقلة ومفتوحة المصدر.

## الرؤية

بناء مرجع تقني ومؤسسي مفتوح يساعد على:
- توثيق الوضع الحالي للنطاق `.ye`.
- دراسة نماذج دول الخليج في الحوكمة، التسجيل، DNSSEC، IDN، وسياسات النطاقات.
- اقتراح نموذج مستقبلي شفاف وآمن للنطاقات اليمنية.
- إنشاء **Yemen .YE Observatory** لمؤشرات DNS وHTTPS وIPv6 وDNSSEC وRDAP.
- إشراك المطورين والجامعات والقطاع الخاص والمجتمع التقني.
- إعداد مسار بحثي مستقل للهوية العربية الرقمية **`.اليمن`** وفق الإجراءات الرسمية المطلوبة.

## الوضع الرسمي الحالي

بحسب IANA، النطاق **`.ye`** هو ccTLD مفوّض لليمن، ومديره المسجل هو **TeleYemen**، مع خدمة WHOIS وRDAP منشورة رسميًا.

المصدر:
- IANA `.ye` delegation record: https://www.iana.org/domains/root/db/ye.html

## النموذج المقترح للمشروع

```text
YDII
├── Research & Benchmarking
│   └── GCC ccTLD comparison
├── Governance & Policies
├── .YE Observatory
├── DNS / RDAP / DNSSEC Research
├── Arabic IDN Research (.اليمن)
├── Community & Universities
└── Public Web Portal
```

## هيكل المستودع

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
├── data/
├── docs/
│   ├── architecture.md
│   ├── benchmark-gcc.md
│   ├── namespace-proposal.md
│   └── research-idn-ar.md
├── scripts/
├── site/
├── tests/
├── GOVERNANCE.md
├── ROADMAP.md
└── README.md
```

## تشغيل الموقع محليًا

```bash
python -m http.server 8080 -d site
```

ثم افتح:
`http://localhost:8080`

## الاختبارات

```bash
python -m unittest discover -s tests -v
```

## النشر عبر GitHub Pages

المستودع يحتوي على Workflow جاهز لـ GitHub Pages.

بعد رفع المشروع:
1. افتح **Settings**.
2. افتح **Pages**.
3. في **Build and deployment** اختر **GitHub Actions**.
4. ادفع أي تحديث إلى فرع `main`.
5. سيعمل Workflow باسم **Deploy GitHub Pages**.

## المساهمة

راجع:
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [GOVERNANCE.md](GOVERNANCE.md)
- [SECURITY.md](SECURITY.md)
- [ROADMAP.md](ROADMAP.md)

## الرخصة

الكود متاح تحت رخصة MIT. راجع [LICENSE](LICENSE).
