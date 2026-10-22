"""Builds ar/index.html from index.html by exact string replacement.

Run after every change to index.html:  python3 tools/make-ar.py

Every pair must match exactly once (or the stated count), so a change to the
English page that is not mirrored here fails loudly instead of leaving
English text in the Arabic page. Change Arabic copy here, not in
ar/index.html, which this script overwrites.
"""
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src, dst = os.path.join(root, "index.html"), os.path.join(root, "ar", "index.html")
s = open(src, encoding="utf-8").read()

PAIRS = [
    # --- head ---
    ('<html lang="en">', '<html lang="ar" dir="rtl">'),
    ("<title>Tafsell — Tailoring Shop Software &amp; POS for the Gulf</title>",
     "<title>تفصيل | برنامج إدارة محلات الخياطة ونقطة البيع في الخليج</title>"),
    ('<meta name="description" content="Tafsell is the all-in-one system for tailoring shops in the Gulf: point of sale, tailoring orders and measurements, fabric stock, VAT invoices and payroll, in Arabic and English. Book a demo." />',
     '<meta name="description" content="تفصيل (Tafsell) نظام متكامل لمحلات الخياطة في الخليج: نقطة بيع، وطلبات التفصيل والمقاسات، ومخزون الأقمشة، وفواتير ضريبة القيمة المضافة، والرواتب، بالعربية والإنجليزية. احجز عرضًا توضيحيًا." />'),
    ('<link rel="canonical" href="https://tafsell.com/" />', '<link rel="canonical" href="https://tafsell.com/ar/" />'),
    ('<meta property="og:url" content="https://tafsell.com/" />', '<meta property="og:url" content="https://tafsell.com/ar/" />'),
    ('<meta property="og:title" content="Tafsell — Tailoring Shop Software &amp; POS for the Gulf" />',
     '<meta property="og:title" content="تفصيل | برنامج إدارة محلات الخياطة ونقطة البيع" />'),
    ('<meta property="og:description" content="Sales, tailoring orders, measurements, fabric stock, VAT invoices and payroll in one workspace, in Arabic and English." />',
     '<meta property="og:description" content="المبيعات وطلبات التفصيل والمقاسات ومخزون الأقمشة وفواتير ضريبة القيمة المضافة والرواتب في مساحة عمل واحدة، بالعربية والإنجليزية." />'),
    ('<meta property="og:image:alt" content="Tafsell — tailoring shop software, powered by NewMux" />',
     '<meta property="og:image:alt" content="تفصيل — برنامج محلات الخياطة، بدعم من NewMux" />'),
    ('<meta property="og:locale" content="en_US" />\n  <meta property="og:locale:alternate" content="ar_AR" />',
     '<meta property="og:locale" content="ar_AR" />\n  <meta property="og:locale:alternate" content="en_US" />'),
    ("family=Sora:wght@400;500;600;700&display=swap",
     "family=Sora:wght@400;500;600;700&family=Readex+Pro:wght@300;400;500;600;700&display=swap"),
    ('"description": "Business software for tailoring shops: point of sale, tailoring orders and measurements, fabric and stock, VAT invoices, staff and payroll.",',
     '"description": "برنامج أعمال لمحلات الخياطة: نقطة بيع، وطلبات التفصيل والمقاسات، والأقمشة والمخزون، وفواتير ضريبة القيمة المضافة، والموظفون والرواتب.",'),
    ('"url": "https://tafsell.com/",\n        "applicationCategory"', '"url": "https://tafsell.com/ar/",\n        "applicationCategory"'),

    # --- header ---
    ('<a href="#workspace">Product</a>', '<a href="#workspace">المنتج</a>'),
    ('<a href="#getting-started">How it works</a>', '<a href="#getting-started">كيف نبدأ</a>'),
    ('<a href="/ar/" class="header-lang" lang="ar" hreflang="ar">عربي</a>', '<a href="/" class="header-lang" lang="en" hreflang="en">English</a>'),
    ('class="header-signin">Sign in</a>', 'class="header-signin">تسجيل الدخول</a>'),
    ('class="btn btn-primary btn-sm">Book a demo <svg', 'class="btn btn-primary btn-sm">احجز عرضًا <svg'),
    ('nav class="main-nav" aria-label="Primary"', 'nav class="main-nav" aria-label="التنقل الرئيسي"'),

    # --- hero ---
    ('<span class="eyebrow">Built for tailoring businesses</span>', '<span class="eyebrow">مصمَّم لمحلات الخياطة والتفصيل</span>'),
    ('<h1 class="display">Run the counter.<br /><em>See the whole workroom.</em></h1>',
     '<h1 class="display">أدِر الكاونتر.<br /><em>وتابع الورشة بالكامل.</em></h1>'),
    ('<p class="lead">Tafsell brings sales, stock, customers, tailoring orders, and payroll into one clear workspace for shops that make things to measure.</p>',
     '<p class="lead">يجمع «تفصيل» المبيعات والمخزون والعملاء وطلبات التفصيل والرواتب في مساحة عمل واحدة واضحة، لمحلات الخياطة التي تعمل حسب المقاس.</p>'),
    ('class="btn btn-primary btn-lg">Book a demo <svg', 'class="btn btn-primary btn-lg">احجز عرضًا توضيحيًا <svg'),
    ('class="btn-link">See how it works <svg', 'class="btn-link">تعرّف على طريقة العمل <svg'),
    ('<p class="hero-caption">The screen on the right is built from the real operational workspace.</p>',
     '<p class="hero-caption">الشاشة المعروضة مأخوذة من مساحة العمل الفعلية للنظام.</p>'),

    # --- mock app (twice: hero and workspace) ---
    ('<span class="live-tag">Demo workspace</span>', '<span class="live-tag">مساحة عمل تجريبية</span>', 2),
    ('<p>Demo Workshop</p><span>Tailor ERP</span>', '<p>ورشة تجريبية</p><span>نظام الخياطة</span>', 2),
    ('<span class="mock-nav-item is-active">Overview</span>', '<span class="mock-nav-item is-active">نظرة عامة</span>', 2),
    ('<span class="mock-nav-item">Customers</span>', '<span class="mock-nav-item">العملاء</span>', 2),
    ('<span class="mock-nav-item">Inventory</span>', '<span class="mock-nav-item">المخزون</span>', 2),
    ('<span class="mock-nav-item">Point of Sale</span>', '<span class="mock-nav-item">نقطة البيع</span>', 2),
    ('<span class="mock-nav-item">Staff &amp; Payroll</span>', '<span class="mock-nav-item">الموظفون والرواتب</span>', 2),
    ('<span class="mock-nav-item">Tailoring orders</span>', '<span class="mock-nav-item">طلبات التفصيل</span>'),
    ('<span class="mock-nav-item">Sales history</span>', '<span class="mock-nav-item">سجل المبيعات</span>'),
    ('<span class="mock-nav-item">Invoices</span>', '<span class="mock-nav-item">الفواتير</span>'),
    ('<span class="mock-nav-item">Shop Settings</span>', '<span class="mock-nav-item">إعدادات المتجر</span>'),
    ('<p class="mock-eyebrow">Owner overview</p>', '<p class="mock-eyebrow">نظرة المالك</p>', 2),
    ('<h3 class="mock-title">Tailoring desk</h3>', '<h3 class="mock-title">مكتب التفصيل</h3>', 2),
    ('<span class="mock-metric-label">Revenue</span><span class="mock-metric-value">BHD 5,240</span>',
     '<span class="mock-metric-label">الإيرادات</span><span class="mock-metric-value">5,240 د.ب</span>'),
    ('<span class="mock-metric-label">Completed sales</span>', '<span class="mock-metric-label">المبيعات المكتملة</span>', 2),
    ('<span class="mock-metric-label">Registered clients</span>', '<span class="mock-metric-label">العملاء المسجلون</span>', 2),
    ('<p class="mock-sub">A filterable operating view of revenue, stock, client activity, sales performance, and workforce status.</p>',
     '<p class="mock-sub">عرض تشغيلي قابل للتصفية للإيرادات والمخزون ونشاط العملاء وأداء المبيعات وحالة الموظفين.</p>'),
    ('<span class="mock-metric-label">Revenue</span><span class="mock-metric-value">BHD 5,240.000</span><span class="mock-metric-note">Across the last 30 days</span>',
     '<span class="mock-metric-label">الإيرادات</span><span class="mock-metric-value">5,240.000 د.ب</span><span class="mock-metric-note">خلال آخر 30 يومًا</span>'),
    ('<span class="mock-metric-note">Orders created this period</span>', '<span class="mock-metric-note">الطلبات المنشأة في هذه الفترة</span>'),
    ('<span class="mock-metric-label">Average order</span><span class="mock-metric-value">BHD 91.930</span><span class="mock-metric-note">Average transaction value</span>',
     '<span class="mock-metric-label">متوسط الطلب</span><span class="mock-metric-value">91.930 د.ب</span><span class="mock-metric-note">متوسط قيمة المعاملة</span>'),
    ('<span class="mock-metric-note">Customer relationships on record</span>', '<span class="mock-metric-note">علاقات العملاء المسجلة</span>'),
    ('<p class="mock-panel-title">Revenue movement</p>', '<p class="mock-panel-title">حركة الإيرادات</p>'),
    ('<p class="mock-panel-title">Recent sales</p>', '<p class="mock-panel-title">أحدث المبيعات</p>'),
    ('<span>Ahmed Al-Rashid</span><span>BHD 186.000</span>', '<span>أحمد الراشد</span><span>186.000 د.ب</span>'),
    ('<span>Fatima Yusuf</span><span>BHD 95.000</span>', '<span>فاطمة يوسف</span><span>95.000 د.ب</span>'),

    # --- 01 promise ---
    ('<span class="eyebrow eyebrow-on-indigo">01 — The promise</span>', '<span class="eyebrow eyebrow-on-indigo">01 — وعدنا</span>'),
    ('<h2 class="display block-heading">Not another tool.<br /><em>The place the shop runs.</em></h2>',
     '<h2 class="display block-heading">ليس مجرد أداة أخرى.<br /><em>بل المكان الذي يُدار منه المحل.</em></h2>'),
    ('<p class="block-lead">Tafsell keeps the day connected — from the first customer conversation to the final fitting and invoice.</p>',
     '<p class="block-lead">يبقي «تفصيل» يوم العمل مترابطًا — من أول حديث مع العميل حتى البروفة الأخيرة والفاتورة.</p>'),

    # --- 02 workspace ---
    ('<span class="eyebrow eyebrow-on-night">02 — The workspace</span>', '<span class="eyebrow eyebrow-on-night">02 — مساحة العمل</span>'),
    ('<h2 class="display block-heading light"><em>Everything you need.</em><br />Nothing to hunt for.</h2>',
     '<h2 class="display block-heading light"><em>كل ما تحتاجه.</em><br />دون عناء البحث.</h2>'),
    ("<p class=\"block-lead light\">The same ERP your team uses every day — set up as your shop's own dedicated workspace, not a shared account.</p>",
     '<p class="block-lead light">النظام نفسه الذي يستخدمه فريقك يوميًا — مُعدّ كمساحة عمل خاصة بمحلك، وليس حسابًا مشتركًا.</p>'),
    ('<p class="frame-caption">This is the actual operating screen your staff will use — not a rendering.</p>',
     '<p class="frame-caption">هذه هي الشاشة الفعلية التي سيستخدمها موظفوك — وليست تصميمًا تخيليًا.</p>'),

    # --- 03 day-to-day ---
    ('<span class="eyebrow">03 — The day-to-day</span>', '<span class="eyebrow">03 — العمل اليومي</span>'),
    ('<h2 class="display block-heading">Built around<br /><em>how work actually moves.</em></h2>',
     '<h2 class="display block-heading">مبنيّ حول<br /><em>طريقة سير العمل الفعلية.</em></h2>'),
    ('<h3>Run the workroom</h3><p>Move tailoring orders from confirmation through fitting and handover without losing the thread.</p>',
     '<h3>أدِر الورشة</h3><p>تابع طلبات التفصيل من التأكيد إلى البروفة والتسليم دون أن يضيع أي تفصيل.</p>'),
    ('<h3>Keep the counter moving</h3><p>Take payments, issue invoices, and review sales from the same operational workspace, online or off.</p>',
     '<h3>كاونتر لا يتوقف</h3><p>استلم المدفوعات وأصدر الفواتير وراجع المبيعات من مساحة العمل نفسها، متصلًا بالإنترنت أو دونه.</p>'),
    ("<h3>Know what's on hand</h3><p>Track fabric, stock levels, sellable items, and materials that need reordering.</p>",
     '<h3>اعرف ما لديك</h3><p>تتبّع الأقمشة ومستويات المخزون والأصناف المعروضة للبيع والمواد التي تحتاج إلى إعادة طلب.</p>'),
    ('<h3>Bring the team together</h3><p>Give staff the access they need, then keep payroll and attendance in view.</p>',
     '<h3>فريق واحد</h3><p>امنح كل موظف الصلاحيات التي يحتاجها، وتابع الرواتب والحضور.</p>'),
    ('<h3>Keep a clean record</h3><p>Every important action is logged, so you always know who did what and when.</p>',
     '<h3>سجلّ واضح</h3><p>كل إجراء مهم مسجَّل، فتعرف دائمًا من فعل ماذا ومتى.</p>'),
    ('<h3>Never miss a fitting</h3><p>Invoices, deliveries, and balances stay tracked from quote to handover.</p>',
     '<h3>لا تفوّت أي بروفة</h3><p>الفواتير والتسليمات والأرصدة متابَعة من عرض السعر حتى التسليم.</p>'),

    # --- 04 getting started ---
    ('<span class="eyebrow eyebrow-on-indigo">04 — Getting started</span>', '<span class="eyebrow eyebrow-on-indigo">04 — كيف نبدأ</span>'),
    ('<h2 class="display block-heading">From a call<br /><em>to a live counter.</em></h2>',
     '<h2 class="display block-heading">من مكالمة<br /><em>إلى كاونتر يعمل.</em></h2>'),
    ("<h3>Book a demo</h3>\n            <p>Tell us about your shop and we'll walk you through the real workspace, live, on a call.</p>",
     '<h3>احجز عرضًا توضيحيًا</h3>\n            <p>أخبرنا عن محلك، وسنعرض لك مساحة العمل الحقيقية مباشرةً في مكالمة.</p>'),
    ('<h3>Sign &amp; set up</h3>\n            <p>A one-time setup fee and a simple contract get your shop fully configured, with its own private workspace on app.tafsell.com.</p>',
     '<h3>التعاقد والإعداد</h3>\n            <p>رسوم إعداد لمرة واحدة وعقد بسيط، ونجهّز محلك بالكامل بمساحة عمل خاصة به على <bdi>app.tafsell.com</bdi>.</p>'),
    ('<h3>Go live</h3>\n            <p>Your team starts using it day to day, backed by a straightforward monthly subscription.</p>',
     '<h3>ابدأ العمل</h3>\n            <p>يبدأ فريقك باستخدامه يوميًا، باشتراك شهري واضح.</p>'),
    ('<p class="steps-note">No hidden costs. No shared accounts. Your shop\'s own private workspace on app.tafsell.com.</p>',
     '<p class="steps-note">لا تكاليف خفية. لا حسابات مشتركة. مساحة عمل خاصة بمحلك على <bdi>app.tafsell.com</bdi>.</p>'),

    # --- CTA ---
    ('<span class="eyebrow eyebrow-on-night">A clearer way to run the shop</span>', '<span class="eyebrow eyebrow-on-night">طريقة أوضح لإدارة المحل</span>'),
    ('<h2 class="display block-heading light">Make the work<br /><em>easier to see.</em></h2>',
     '<h2 class="display block-heading light">اجعل العمل<br /><em>أوضح أمامك.</em></h2>'),
    ("<p class=\"block-lead light\">Book a demo and we'll show you the exact workspace your shop would run.</p>",
     '<p class="block-lead light">احجز عرضًا توضيحيًا وسنريك مساحة العمل التي سيعمل بها محلك بالضبط.</p>'),
    ('class="btn btn-cream btn-lg">Book a demo <svg', 'class="btn btn-cream btn-lg">احجز عرضًا توضيحيًا <svg'),

    # --- demo form ---
    ('<h2 class="display">Book a demo</h2>', '<h2 class="display">احجز عرضًا توضيحيًا</h2>'),
    ("<p>Tell us a bit about your shop and we'll set up a call to show you the system live.</p>",
     '<p>أخبرنا قليلًا عن محلك، وسنحدد موعد مكالمة لنعرض لك النظام مباشرةً.</p>'),
    ('<label for="demo-name">Your name</label>', '<label for="demo-name">الاسم</label>'),
    ('<label for="demo-shop">Shop or business name</label>', '<label for="demo-shop">اسم المحل أو النشاط التجاري</label>'),
    ('<label for="demo-email">Email</label>', '<label for="demo-email">البريد الإلكتروني</label>'),
    ('<label for="demo-phone">Phone or WhatsApp (optional)</label>', '<label for="demo-phone">الهاتف أو واتساب (اختياري)</label>'),
    ('<label for="demo-message">What would you like to see? (optional)</label>', '<label for="demo-message">ما الذي تودّ أن تراه؟ (اختياري)</label>'),
    ('class="btn btn-primary btn-block">Request a demo <svg', 'class="btn btn-primary btn-block">أرسل الطلب <svg'),
    ("<p class=\"form-note\">We'll get back to you to schedule a time. See our <a href=\"https://app.tafsell.com/privacy\">privacy policy</a>.</p>",
     '<p class="form-note">سنتواصل معك لتحديد موعد. اطّلع على <a href="https://app.tafsell.com/privacy">سياسة الخصوصية</a>.</p>'),
    ("<h3>Thank you — we've got it.</h3>", '<h3>شكرًا لك — وصلنا طلبك.</h3>'),
    ("<p>We'll be in touch soon to schedule your demo. Questions in the meantime: <span data-sales-email>info@newmux.com</span>.</p>",
     '<p>سنتواصل معك قريبًا لتحديد موعد العرض. لأي استفسار حتى ذلك الحين: <span data-sales-email dir="ltr">info@newmux.com</span>.</p>'),

    # --- NewMux ---
    ('<span class="eyebrow eyebrow-newmux">Built by NewMux</span>', '<span class="eyebrow eyebrow-newmux">من تطوير NewMux</span>'),
    ('<h2 class="display block-heading light">Real software company.<br /><em>Not a template.</em></h2>',
     '<h2 class="display block-heading light">شركة برمجيات حقيقية.<br /><em>وليس قالبًا جاهزًا.</em></h2>'),
    ('<p class="block-lead light">Tafsell is built and supported by <strong>NewMux</strong>, a software development studio behind custom platforms, AI-powered applications, and cloud solutions for growing businesses.</p>',
     '<p class="block-lead light">تطوّر <strong>NewMux</strong> منصة «تفصيل» وتدعمها، وهي استوديو لتطوير البرمجيات يقف وراء منصات مخصصة وتطبيقات مدعومة بالذكاء الاصطناعي وحلول سحابية للأعمال النامية.</p>'),
    ('class="btn btn-newmux btn-lg">Visit newmux.com <svg', 'class="btn btn-newmux btn-lg">زيارة newmux.com <svg'),

    # --- footer ---
    ('<p class="footer-tagline">Operational software for tailor shops. &copy; <span id="year">2026</span> Tafsell, powered by <a href="https://www.newmux.com/" target="_blank" rel="noopener">NewMux</a>.</p>',
     '<p class="footer-tagline">برنامج تشغيل لمحلات الخياطة. &copy; <span id="year">2026</span> تفصيل، بدعم من <a href="https://www.newmux.com/" target="_blank" rel="noopener">NewMux</a>.</p>'),
    ('nav class="footer-links" aria-label="Footer"', 'nav class="footer-links" aria-label="روابط التذييل"'),
    ('class="footer-link">Customer sign in</a>', 'class="footer-link">دخول العملاء</a>'),
    ('<a href="#book-a-demo" class="footer-link">Book a demo</a>', '<a href="#book-a-demo" class="footer-link">احجز عرضًا توضيحيًا</a>'),
    ('class="footer-link">Terms</a>', 'class="footer-link">الشروط</a>'),
    ('class="footer-link">Privacy</a>', 'class="footer-link">الخصوصية</a>'),
    ('<a href="/ar/" class="footer-link" lang="ar" hreflang="ar">العربية</a>', '<a href="/" class="footer-link" lang="en" hreflang="en">English</a>'),
]

for pair in PAIRS:
    old, new = pair[0], pair[1]
    count = pair[2] if len(pair) > 2 else 1
    found = s.count(old)
    if found != count:
        sys.exit(f"expected {count} of {old[:80]!r}, found {found}")
    s = s.replace(old, new)

open(dst, "w", encoding="utf-8").write(s)
print("ok")
