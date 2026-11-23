<!-- translation of installer/linux/README.md, source sha256: 7ece3bc522f30a5f0b62b4a6580a177b3d4725e5b1eaa5513e255f0772f27156 -->

# مثبّت Linux

[English](../../installer/linux/README.md) · [中文](../zh/LINUX_INSTALLER.md) · [Español](../es/LINUX_INSTALLER.md) · [Français](../fr/LINUX_INSTALLER.md) · [Deutsch](../de/LINUX_INSTALLER.md) · [Italiano](../it/LINUX_INSTALLER.md) · [Русский](../ru/LINUX_INSTALLER.md) · [Português](../pt/LINUX_INSTALLER.md) · **العربية**

يحتوي المثبّت دون اتصال على ملفات تنفيذية موقَّعة مكتوبة بـ Go لمعماريات amd64 وarm64 وARMv7. شغّله بحساب مستخدم سطح المكتب. ويستخدم التثبيت الجديد مجلد البيانات الخاص بكل مستخدم ويضع الأمر في `~/.local/bin`.

~~~sh
sh skynet-agent-install.sh --no-autostart
~/.local/bin/skynet-agent verify-install
~~~

استخدم `--home DIR` لملف تعريف مخصّص. ويحافظ الإعداد افتراضيًا على البدء عند تسجيل الدخول. استخدم `--autostart` لبدء خدمة systemd للمستخدم الآن وعند تسجيل الدخول، أو أضف `--linger` لإبقائها تعمل خارج جلسات تسجيل الدخول. وتحافظ إزالة الوكيل على الهوية وقوائم الانتظار. وإضافة `--purge` تحذف بياناته المحفوظة صراحةً.

~~~sh
~/.local/bin/skynet-agent uninstall --yes
~~~

يستخدم سكربت الإقلاع المتصل بالإنترنت الموجود في `agent/install.sh` الأدوات curl وjq وxxd وsha256sum وOpenSSL مع دعم Ed25519. احصل على السكربت من إصدار موثوق. ويتحقق من صحة البيان قبل تنفيذ الملف التنفيذي الخاص بالمعمارية.

لبناء المثبّت دون اتصال من الأصول الموقَّعة، شغّل ما يلي من جذر المستودع. يقع البيان والتوقيع في `agent/v2`. ويتحقق الباني من كل أصل قبل تعبئته.

~~~sh
sh installer/linux/build.sh --dir dist
~~~
