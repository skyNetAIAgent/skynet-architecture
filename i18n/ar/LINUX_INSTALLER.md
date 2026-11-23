<!-- translation of installer/linux/README.md, source sha256: abf22229c4680552dec4357a2de39a59a6c18c9238e2ff76b46a2952e7d8f0b0 -->

# مثبّت Linux

[English](../../installer/linux/README.md) · [中文](../zh/LINUX_INSTALLER.md) · [Español](../es/LINUX_INSTALLER.md) · [Français](../fr/LINUX_INSTALLER.md) · [Deutsch](../de/LINUX_INSTALLER.md) · [Italiano](../it/LINUX_INSTALLER.md) · [Русский](../ru/LINUX_INSTALLER.md) · [Português](../pt/LINUX_INSTALLER.md) · **العربية**

شغّل الملف الواحد من صفحة Releases الخاصة بالمشروع بحسابك أنت.

```sh
sh skynet-agent-install.sh
```

يحمل الملف إصدار الوكيل الموقَّع. ويتحقق التثبيت من توقيعه Ed25519 وبصمات ملفاته دون اتصال. وإذا كان Python 3.9 أو أحدث موجودًا على PATH، فسيستخدم الإعداد ذلك المفسِّر. وإلا فإنه يحتاج نسخة CPython مبنية على glibc ومثبَّتة على إصدار محدَّد لمنصّتي x86_64 أو aarch64. **البصمتان معلَّقتان في الوقت الحالي. وتحتاج هذه النسخة إلى Python النظام.**

ويستخدم المثبّت المتصل بالإنترنت إجراء الإعداد نفسه. وعند وجود بصمة موثَّقة، يستطيع جلب بيئة التشغيل المطابقة من python-build-standalone والتحقق من SHA-256 قبل فك الضغط. وتقع المفسِّرات المحمولة تحت `$XDG_DATA_HOME/skynet-agent/python/<sha256>`، وعادةً `~/.local/share/skynet-agent/python/<sha256>`. ويستخدم الأمر في `~/.local/bin` وخدمة systemd للمستخدم الملفَّ التنفيذي المختار.

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

## البدء والإزالة

في الطرفية، ضغط Enter عند المطالبة الأولى يبدأ الخدمة الآن وعند تسجيل الدخول. وضغط Enter عند المطالبة الثانية يبقيها مرتبطة بجلسات تسجيل الدخول. وبدون طرفية، يتخطى الإعداد المطالبتين. وهذه الأوامر تحدد الخيارات صراحةً.

```sh
sh skynet-agent-install.sh --autostart           # Run now and at sign-in
sh skynet-agent-install.sh --autostart --linger  # Also run before login and after logout
sh skynet-agent-install.sh --no-autostart        # Install for manual use
```

تحتاج الخدمة إلى مدير systemd للمستخدم قيد التشغيل. ويدعم كاتب الخدمة الموقَّع في الإصدار 0.2.2 المسارات التي تحتوي على مسافات. ويطلب الإعداد البدء اليدوي إذا احتوى مسار المفسِّر أو مسار الوكيل على علامة اقتباس مزدوجة أو شرطة مائلة عكسية أو علامة دولار أو علامة نسبة مئوية أو فاصل سطر. وإذا رفضت السياسة المحلية البقاء (lingering)، يبلّغ الإعداد بذلك، وتظل الخدمة تعمل خلال جلسات تسجيل الدخول. ويمكن تغيير البقاء على مستوى الحساب كله على حدة باستخدام `loginctl disable-linger "$(id -un)"`. وللتثبيت اليدوي، ابدأ العمل باستخدام `~/.local/bin/skynet-agent run`.

```sh
~/.local/bin/skynet-agent selftest
~/.local/bin/skynet-agent version
~/.local/bin/skynet-agent uninstall --yes
```

تُعطّل الإزالة الخدمة، وتطلب إيقافها، وتنتظر قفل الوكيل. ويبقى مفتاح هويتك وصندوق الصادر وسجلات المرحّلات المعلَّقة والإعدادات في مجلد الوكيل لإعادة التثبيت. ولمحو بيانات الوكيل المحفوظة أيضًا، استخدم `uninstall --yes --purge`. والبقاء (lingering) إعداد للحساب كله ويستمر بعد الإزالة.

## البناء والتحقق

من جذر المستودع، استخدم Python 3.9 أو أحدث على جهاز البناء.

```sh
sh installer/linux/build.sh
shellcheck -s sh agent/install.sh installer/linux/build.sh installer/linux/smoke.sh
dash -n installer/linux/skynet-agent-install.sh
python3 -I -m unittest discover -s agent/tests -t agent/tests
```

ويتحقق الباني من صحة الإصدار بالمفتاح العام الموجود في `agent/install.py`، وينتج `installer/linux/skynet-agent-install.sh`. ولتفعيل Python المحمول، تحقق من كل أرشيف من المنبع على حدة، وسجّل بصمة SHA-256 الخاصة به في `python.lock` (حقل واحد في كل سطر). وللمدخل الفارغ فقط، يمكن لـ CI تزويد بصمة موثَّقة عبر `SKYNET_PYTHON_SHA256_X86_64` أو `SKYNET_PYTHON_SHA256_AARCH64`. وهذه إعدادات وقت البناء. ويتحقق الباني من كل أرشيف مثبَّت ويضمّنه. وللبناء دون اتصال باستخدام الأرشيفات المثبَّتة، استخدم `sh installer/linux/build.sh --runtime-dir /path/to/archives`.

يشغّل سير عمل مثبّت Linux الحزمة بمستخدم عادي لا يملك صلاحيات، مع تعطيل الشبكة. ويجرّب Ubuntu 24.04 استخدام Python النظام. وتجرّب Debian 12 slim المفسِّر المحمول عندما تتوفر بصمة x86_64، وتتحقق من رفض التثبيت عندما تكون البصمة معلَّقة. والتثبيتات الناجحة تشغّل الاختبار الذاتي، وتبلّغ عن الإصدار، وتجرّب طريقتي الإزالة. ويرفع سير العمل السكربت كمنتج بناء للتوزيع اليدوي.
