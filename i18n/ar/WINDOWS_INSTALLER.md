<!-- translation of installer/windows/README.md, source sha256: ea7cbbbfeb25d77b3a5b0c8e09d4f0869dfa666efd0d84e0755573b22c5206ae -->

# مثبّت Windows لسطح المكتب

[English](../../installer/windows/README.md) · [中文](../zh/WINDOWS_INSTALLER.md) · [Español](../es/WINDOWS_INSTALLER.md) · [Français](../fr/WINDOWS_INSTALLER.md) · [Deutsch](../de/WINDOWS_INSTALLER.md) · [Italiano](../it/WINDOWS_INSTALLER.md) · [Русский](../ru/WINDOWS_INSTALLER.md) · [Português](../pt/WINDOWS_INSTALLER.md) · **العربية**

اختر مثبّت amd64 أو arm64 لجهاز الكمبيوتر الخاص بك. تحقّق من بصمة SHA-256 الخاصة به
باستخدام بصمة تحقق تم الحصول عليها عبر قناة موثوقة. يثبّت برنامج الإعداد الإصدار
الأصلي الموقَّع في ملف تعريف المستخدم الحالي. يبدأ برنامج الإعداد الوكيل فورًا وعند كل
تسجيل دخول إلى Windows؛ يمكن إلغاء تحديد كليهما في صفحة المهام. تستدعي اختصارات
قائمة ابدأ المشغّل الدائم.

تحتفظ أداة الإزالة بالهوية وقوائم الانتظار وسجل الإصدارات افتراضيًا. اختر خيار حذف
البيانات لإزالتها. أثناء الترحيل، يُحتفظ بجسر Python الموقَّع السابق ومفسّره للاسترجاع.

## البناء والاختبار

استخدم Python 3.9+ وInno Setup 6 على جهاز البناء. ضع بيان الإصدار والتوقيع المنفصل
تحت `agent/v2` وملفات الإصدار الثنائية المطابقة له تحت `dist`. استخدم مجلد بناء
جديدًا. يحتاج الاختبار السريع إلى حساب Windows مؤقّت.

~~~powershell
./installer/windows/build.ps1 -BuildDir build -AssetDir dist -Arch amd64
./installer/windows/smoke.ps1 -BuildDir build
~~~
