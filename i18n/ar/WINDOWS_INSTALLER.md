<!-- translation of installer/windows/README.md, source sha256: 95e38378255edcbcadd409d118146850d8282a8a66501bbe40381b095e4893d7 -->

# مثبّت Windows x64

[English](../../installer/windows/README.md) · [中文](../zh/WINDOWS_INSTALLER.md) · [Español](../es/WINDOWS_INSTALLER.md) · [Français](../fr/WINDOWS_INSTALLER.md) · [Deutsch](../de/WINDOWS_INSTALLER.md) · [Italiano](../it/WINDOWS_INSTALLER.md) · [Русский](../ru/WINDOWS_INSTALLER.md) · [Português](../pt/WINDOWS_INSTALLER.md) · **العربية**

نزّل ملف EXE وملف `.exe.sha256` المطابق له من إصدار المشروع نفسه. في
PowerShell، افتح مجلد التنزيل وقارن بصمة التحقق. [إصدارات GitHub](https://github.com/skyNetAIAgent/skynet-architecture/releases)

```powershell
$file = 'SkyNetAgentSetup-0.2.2.exe'
$expected = ((Get-Content -Raw "$file.sha256") -split '\s+')[0]
if ((Get-FileHash $file -Algorithm SHA256).Hash -ne $expected) { throw 'Checksum mismatch.' }
```

افتح ملف EXE الذي تحققت منه. قد يعرض SmartScreen رسالة **تم حماية جهاز
الكمبيوتر الخاص بك** (Windows protected your PC) لأن المثبّت لا يحمل توقيعًا برمجيًا.
اختر **مزيد من المعلومات** (More info)، وتأكد من اسم الملف، ثم اختر **التشغيل على
أي حال** (Run anyway). يثبّت البرنامج للمستخدم الحالي فقط. أزل علامة أيٍّ من مربّعَي
الاختيار الخاصين ببدء التشغيل لتغيير وقت تشغيل الوكيل.

يقبل الوكيل تحديثات موقَّعة لملفاته. ويحدّث المثبّت الأحدث نسخة Python المضمَّنة.
ثبّت فوق النسخة الموجودة للحفاظ على هوية الجهاز والنتائج المنتظرة. وتحتفظ أداة الإزالة
في قائمة ابدأ بها أيضًا افتراضيًا. ويشمل مربّع اختيار حذف البيانات الاختياري التابع
لها صندوق الصادر والسجلات الموقَّعة المعلّقة.

## البناء والاختبار

استخدم نسخة سحب نظيفة من المستودع بنهايات أسطر LF للملفات الموقَّعة. من جذر المستودع على
Windows x64، شغّل PowerShell 7 مع مجلد بناء جديد. يتحقق البناء من وجود Inno
Setup 6.3.3 أو أحدث في PATH أو في موقعه المعتاد. ويستخدم Chocolatey لتثبيت
6.3.3 إذا كان المترجم غير موجود.

```powershell
./installer/windows/build.ps1 -BuildDir build
```

يجب أن يحتوي `python.lock` على رقم إصدار التصحيح 3.12 الدقيق وبصمة SHA-256
المكوَّنة من 64 رقمًا للملف الرسمي `python-<version>-embed-amd64.zip`. لتثبيت رقم
إصدار جديد، تحقّق من صحة الأرشيف باستخدام التعليمات وحزمة Sigstore المرتبطتين
بصفحة إصدار Python، ثم سجّل بصمة SHA-256 الخاصة به. يوقف رقم الإصدار الفارغ أو
غير الصالح البناء قبل التنزيل. [إصدار Python 3.12.10](https://www.python.org/downloads/release/python-31210/)

يتحقق البناء من الأرشيف قبل فكّ ضغطه. ولا يُجهّز المفسّر المضمَّن إلا الملفات
الواردة في بيان الإصدار الموثَّق. وعند التثبيت يتحقق من الحزمة مرة أخرى، بما في ذلك
قائمة ملفاتها، قبل تشغيل المرشّح. ويوفّر ملف `python312._pth` الأصلي المكتبة
القياسية. ويضيف المشغّل وفحص المرشّح مجلد الإصدار المحدد إلى `sys.path` عند
العمل بخيار `-I`.

على ملف تعريف Windows مؤقّت لا يحتوي على تثبيت SkyNet موجود، شغّل الاختبار
السريع. يثبّت بصمت، ويتحقق من تسجيل التشغيل عند الدخول ومن واجهة سطر الأوامر (CLI) دون وجود
Python النظام في PATH، ثم يزيل التثبيت ويتحقق من البيانات المحتفظ بها.

```powershell
./installer/windows/smoke.ps1 -BuildDir build
```

بدلًا من ذلك، شغّل **الإجراءات (Actions) → مثبّت Windows (Windows installer) → تشغيل
سير العمل (Run workflow)**. بعد نجاح الاختبار السريع، نزّل الملف الناتج
`SkyNetAgentSetup-x64`. وملفّا `SkyNetAgentSetup-<version>.exe`
و`.exe.sha256` هما الملفان اللذان يجب إرفاقهما يدويًا بإصدار GitHub المطابق.
