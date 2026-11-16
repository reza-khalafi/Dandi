import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from PIL import Image, ImageDraw

from apps.articles.models import Category, Tag, Article
from apps.articles.enums import ArticleStatus
from apps.comments.models import Comment
from apps.comments.enums import CommentStatus
from apps.core.management.commands.article_content_generator import (
    generate_slow_living_content,
    generate_cosmos_ai_content,
    generate_architecture_content,
    generate_aesthetics_content
)


class Command(BaseCommand):
    help = 'Seeds all categories with rich 3000+ word articles, ensuring zero empty categories.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting comprehensive Dandi seeding across ALL categories...'))

        # 1. Synchronize seed photos to MEDIA_ROOT
        dest_media_dir = Path(settings.MEDIA_ROOT) / 'articles' / 'demo'
        dest_media_dir.mkdir(parents=True, exist_ok=True)

        source_photos_dir = Path(settings.BASE_DIR) / 'static' / 'images' / 'seed_photos'
        if source_photos_dir.exists():
            for src_file in source_photos_dir.glob('*.jpg'):
                dst_file = dest_media_dir / src_file.name
                if not dst_file.exists() or dst_file.stat().st_size != src_file.stat().st_size:
                    shutil.copy2(src_file, dst_file)
            self.stdout.write(self.style.SUCCESS('Synchronized seed photos to MEDIA_ROOT.'))

        # 2. Users
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@dandi.local',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'مدیر',
                'last_name': 'دندی'
            }
        )
        admin_user.set_password('admin123456')
        admin_user.save()

        demo_user, _ = User.objects.get_or_create(
            username='danial',
            defaults={
                'email': 'danial@dandi.local',
                'first_name': 'دانیال',
                'last_name': 'روشن'
            }
        )
        demo_user.set_password('dandi123456')
        demo_user.save()

        authors = [admin_user, demo_user]

        # 3. Categories (All 6 categories)
        categories_data = [
            {
                'name': 'اندیشه، فلسفه و سبک زندگی',
                'slug': 'thought-and-lifestyle',
                'description': 'خرد زیسته، آرامش درونی، هنر درنگ و خودشناسی در عصر شتاب‌زدگی.',
                'color_accent': 'orange',
                'order': 1
            },
            {
                'name': 'علم، فناوری و جهان نو',
                'slug': 'science-and-technology',
                'description': 'کیهان‌شناسی، هوش مصنوعی، معماری سیستم‌ها و افق‌های محاسباتی بشر.',
                'color_accent': 'violet',
                'order': 2
            },
            {
                'name': 'هنر، ادبیات و خلاقیت',
                'slug': 'art-and-creativity',
                'description': 'زیبایی‌شناسی، تایپوگرافی، روایت‌گری، دیزاین معاصر و تجربه ادراک حسی.',
                'color_accent': 'amber',
                'order': 3
            },
            {
                'name': 'هوش مصنوعی و آینده‌پژوهی',
                'slug': 'artificial-intelligence',
                'description': 'عامل‌های خودمختار، مدل‌های استدلال ژرف، پردازش زبان و مرزهای هوش ماشین.',
                'color_accent': 'violet',
                'order': 4
            },
            {
                'name': 'معماری نرم‌افزار و مهندسی سیستم',
                'slug': 'software-architecture',
                'description': 'معماری تمیز، مایکروسرویس‌ها، کشینگ، مقیاس‌پذیری و الگوهای پایدار مهندسی.',
                'color_accent': 'orange',
                'order': 5
            },
            {
                'name': 'طراحی محصول و دیزاین سیستم',
                'slug': 'design-systems',
                'description': 'دیزاین سیستم‌ها، تایپوگرافی فارسی، روانشناسی رابط کاربری و موشن دیزاین.',
                'color_accent': 'amber',
                'order': 6
            }
        ]

        categories = {}
        for c_data in categories_data:
            cat, _ = Category.objects.update_or_create(
                slug=c_data['slug'],
                defaults=c_data
            )
            categories[c_data['slug']] = cat

        # 4. Tags
        tag_definitions = [
            ('فلسفه_زندگی', 'philosophy'),
            ('تمرکز_ذهنی', 'mindfulness'),
            ('هوش_مصنوعی', 'ai'),
            ('معماری_سیستم', 'systems-architecture'),
            ('زیبایی_شناسی', 'aesthetics'),
            ('ادبیات_و_روایت', 'storytelling'),
            ('دیزاین_معاصر', 'design'),
            ('تفکر_نقادانه', 'critical-thinking'),
            ('کیهان_شناسی', 'cosmology'),
            ('روانشناسی_شناختی', 'cognitive-psychology')
        ]
        tags = {}
        for name, slug in tag_definitions:
            t, _ = Tag.objects.get_or_create(slug=slug, defaults={'name': name})
            tags[slug] = t

        # Available photo list
        available_photos = [
            'articles/demo/slow-living-real.jpg',
            'articles/demo/slow-living.jpg',
            'articles/demo/decision-psychology.jpg',
            'articles/demo/cosmos-ai.jpg',
            'articles/demo/clean-architecture.jpg',
            'articles/demo/minimalism-art.jpg',
            'articles/demo/storytelling-narrative.jpg',
            'articles/demo/photo-1.jpg',
            'articles/demo/photo-2.jpg',
            'articles/demo/photo-3.jpg',
            'articles/demo/photo-4.jpg',
            'articles/demo/photo-5.jpg',
            'articles/demo/photo-6.jpg',
            'articles/demo/photo-7.jpg',
            'articles/demo/photo-8.jpg',
            'articles/demo/photo-9.jpg',
            'articles/demo/photo-10.jpg',
            'articles/demo/photo-11.jpg',
            'articles/demo/photo-12.jpg',
            'articles/demo/photo-13.jpg',
            'articles/demo/photo-14.jpg',
            'articles/demo/photo-15.jpg',
            'articles/demo/photo-16.jpg'
        ]

        for rel_path in available_photos:
            full_p = Path(settings.MEDIA_ROOT) / rel_path
            if not full_p.exists():
                img = Image.new('RGB', (900, 500), (249, 115, 22))
                d = ImageDraw.Draw(img)
                d.ellipse([100, 100, 400, 400], fill=(139, 92, 246))
                img.save(full_p, 'JPEG')

        # 5. Build Comprehensive Articles List across all 6 categories
        raw_article_meta = [
            # Category 1: Thought & Lifestyle (17 articles)
            (
                'هنر آهستگی: چگونه در عصر شتاب‌زدگی به آرامش درونی و تمرکز عمیق برسیم؟',
                'art-of-slow-living-and-deep-focus',
                'واکاوی جامع پارادوکس سرعت در تمدن معاصر، ریشه‌های تاریخی درنگ در مکاتب فلسفی، و راهنمای عملی بازیابی تمرکز تک‌کاربری.',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['philosophy', 'mindfulness'],
                True
            ),
            (
                'روانشناسی قضاوت: رهایی از خطاهای شناختی در تصمیم‌گیری‌های حیاتی زندگی',
                'psychology-of-judgment-and-biases',
                'شناخت سازوکار سوگیری‌های تایید و اثر لنگر، و چگونگی تربیت ذهنی بازتر، نقادتر و مصون از فریب در جهان انباشته از اطلاعات.',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['cognitive-psychology', 'philosophy'],
                False
            ),
            (
                'تنهایی سازنده: چگونه خلوت با خویشتن سرچشمه نوآوری و بلوغ عاطفی می‌شود؟',
                'constructive-solitude-and-emotional-maturity',
                'تمایز بنیادین میان انزوای رنج‌آور و تنهایی خودخواسته؛ بازخوانی آرای شوپنهاور و مونتنی در باب فضیلت مصاحبت با روح خود.',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['philosophy', 'mindfulness'],
                True
            ),
            (
                'فلسفه رواقی‌گری در عمل: راهنمای باستانی برای تاب‌آوری در بحران‌های مدرن',
                'stoicism-in-modern-adversity',
                'آموزه‌های مارکوس اورلیوس و سنکا برای تفکیک ساحت‌های تحت کنترل از دایره ناتوانی، و دستیابی به طمأنینه ناگسستنی.',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['philosophy', 'critical-thinking'],
                False
            ),
            (
                'مینیمالیسم دیجیتال: رژیم توجه و بازپس‌گیری ساعت‌های طلایی عمر',
                'digital-minimalism-and-attention-reclamation',
                'چگونه با قطع زنجیره وابستگی به نوتیفیکیشن‌ها و اسکرول بی‌پایان، مغز را از فرسودگی نجات داده و قدرت تامل عمیق را احیا کنیم؟',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['mindfulness', 'philosophy'],
                False
            ),
            (
                'اضطراب منزلت: کالبدشکافی مقایسه اجتماعی و عطش بی‌پایان دیده شدن',
                'status-anxiety-and-social-validation',
                'چرا در عصر رفاه مادی، احساس ناامنی درونی بیداد می‌کند؟ تاملی در باب بازتعریف موفقیت ورای معیارهای ظاهری فرهنگ مصرفی.',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['cognitive-psychology', 'philosophy'],
                False
            ),
            (
                'خواب و رویا: قلمرو مرموز بازیافت حافظه و جوان‌سازی ادراک',
                'sleep-architecture-and-mental-restoration',
                'بررسی ریتم شبانه‌روزی بدن، فازهای حرکت سریع چشم (REM) و نقشی که استراحت کافی در تثبیت یادگیری و سلامت روان ایفا می‌کند.',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['mindfulness', 'cognitive-psychology'],
                False
            ),
            (
                'معماری گفتگو: هنر شنیدن فعال در جهانی که همه فریاد می‌زنند',
                'art-of-active-listening-in-noisy-world',
                'چرا ارتباطات حقیقی رو به زوال رفته‌اند؟ فنون مکالمه همدلانه، تعلیق پیش‌داوری و ساختن پل‌های تفاهم میان جهان‌های زیسته متفاوت.',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['mindfulness', 'philosophy'],
                False
            ),
            (
                'خستگی تصمیم‌گیری: روانشناسی حفظ اراده و اولویت‌بندی انرژی ذهنی',
                'decision-fatigue-and-willpower-depletion',
                'منابع شناختی انسان نامحدود نیستند. چگونه با ساختن روتین‌های روزمره هوشمند، مغز را برای انتخاب‌های استراتژیک آماده نگه داریم؟',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['cognitive-psychology', 'critical-thinking'],
                False
            ),
            (
                'قدرت عادت‌های اتمی: تغییرات میکروسکوپی با پیامدهای چشمگیر',
                'atomic-habits-and-compounding-growth',
                'مکانیزم عصبی شکل‌گیری حلقه‌های عادت؛ چگونه به جای تکیه بر انگیزه ناپایدار، سیستم‌های رفتاری پایدار و خودکار خلق کنیم؟',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['cognitive-psychology', 'mindfulness'],
                False
            ),
            (
                'معنای کار در قرن ۲۱: عبور از مشغله‌های توخالی به سوی رسالت زیسته',
                'meaning-of-work-and-purpose-in-21st-century',
                'بحران بی‌معنایی شغلی در عصر شرکت‌ها؛ چگونه میان کسب معاش و تحقق درونی پیوندی اصیل و ریشه‌دار برقرار سازیم؟',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['philosophy', 'critical-thinking'],
                False
            ),
            (
                'پیاده‌روی به مثابه تفکر: تبارشناسی همگامی گام‌ها و امواج اندیشه',
                'walking-as-a-philosophical-act',
                'از ارسطو و نیچه تا کانت و والتر بنیامین؛ چرا متفکران بزرگ الهام‌بخش‌ترین نظریات خود را حین قدم زدن خلق کرده‌اند؟',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['philosophy', 'mindfulness'],
                False
            ),
            (
                'روانشناسی شکرگزاری: دگرگونی زیست‌شیمیایی مغز با ستایش نعمات کوچک',
                'neurobiology-of-gratitude-and-wellbeing',
                'شواهد عصب‌شناختی نشان می‌دهند تمرین توجه به زیبایی‌های پنهان، مسیرهای دوپامینی را سیم‌کشی مجدد کرده و اضطراب را فرو می‌نشاند.',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['mindfulness', 'cognitive-psychology'],
                False
            ),
            (
                'شجاعت آسیب‌پذیری: رهایی از نقاب کمال‌گرایی و تجربه اصالت',
                'courage-of-vulnerability-and-authenticity',
                'پژوهش‌های برنه براون در باب هراس از طرد شدن؛ چرا پذیرش نقص‌ها و شفافیت عاطفی، یگانه خاستگاه شجاعت واقعی است؟',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['mindfulness', 'philosophy'],
                False
            ),
            (
                'مواجهه با ملال: چرا خستگی حسی دروازه ورود به نبوغ و خلاقیت است؟',
                'boredom-as-a-portal-to-creativity',
                'ترس بیهوده از بیکاری ذهن؛ چگونه اجازه دادن به سرگردانی افکار، شبکه پیش‌فرض مغز (DMN) را فعال ساخته و نبوغ می‌آفریند؟',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['philosophy', 'cognitive-psychology'],
                False
            ),
            (
                'دوستی پایدار در بزرگسالی: چالش‌ها و کیمیای هم‌دلی در جوامع فردگرا',
                'adult-friendship-and-empathy-in-individualistic-era',
                'چرا یافتن دوستان عمیق در بزرگسالی دشوار است؟ تاملی در باب بازسازی پیوندهای رفاقت بر پایه اعتماد، صداقت و حمایت متقابل.',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['philosophy', 'mindfulness'],
                False
            ),
            (
                'پذیرش گذار عمر: هنر رها کردن گذشته و آشتی با ناتمام بودن جهان',
                'art-of-letting-go-and-impermanence',
                'حکمت باستانی «همه چیز می‌گذرد»؛ چگونه درک میرایی و عدم ثبات امور به جای یاس، شادمانی عمیق قدردانی از لحظه حال را می‌افروزد؟',
                'thought-and-lifestyle',
                generate_slow_living_content,
                ['philosophy', 'mindfulness'],
                False
            ),

            # Category 2: Science & Technology (17 articles)
            (
                'کیهان و مرزهای هوش: چگونه بشر با محاسبات نوین به درک رازهای هستی نزدیک می‌شود؟',
                'cosmos-and-frontiers-of-ai-and-universe',
                'همگرایی شگفت‌انگیز اخترفیزیک و مدل‌های استدلال ژرف؛ ردیابی ماده تاریک و پرسش‌های بنیادین درباره منشأ آگاهی در گستره کائنات.',
                'science-and-technology',
                generate_cosmos_ai_content,
                ['cosmology', 'ai'],
                True
            ),
            (
                'معماری تفکر سیستمی: هنر تفکیک و پیوند لایه‌ها در مهندسی نرم‌افزار و سازمان',
                'systems-thinking-and-clean-layered-architecture',
                'از کد اسپاگتی تا آرامش معماری لایه‌ای (View, Service, Repository)؛ چرایی ضرورت تفکیک دغدغه‌ها و شیوه ساخت سامانه‌های تاب‌آور.',
                'science-and-technology',
                generate_architecture_content,
                ['systems-architecture', 'critical-thinking'],
                True
            ),
            (
                'سفرهای میان‌ستاره‌ای: فیزیک فضا-زمان، پیشرانش اتمی و مرزهای سرعت نور',
                'interstellar-travel-spacetime-propulsion',
                'چالش‌های خروج از منظومه شمسی؛ از اتساع زمان در نظریه نسبیت خاص تا موتورهای انحنای فضا و ساخت سفینه‌های نسل‌اندرنسل.',
                'science-and-technology',
                generate_cosmos_ai_content,
                ['cosmology', 'ai'],
                False
            ),
            (
                'کامپیوترهای کوانتومی: کیوبیت‌ها، درهم‌تنیدگی و جهش فراتر از فیزیک کلاسیک',
                'quantum-computing-qubits-and-entanglement',
                'چگونه برهم‌نهی حالات کوانتومی، پیچیده‌ترین مسائل رمزنگاری، کشف دارو و بهینه‌سازی زنجیره تامین را در چند ثانیه حل خواهد کرد؟',
                'science-and-technology',
                generate_cosmos_ai_content,
                ['ai', 'systems-architecture'],
                False
            ),
            (
                'عصر عامل‌های خودمختار: چگونه هوش مصنوعی شیوه برنامه‌نویسی را متحول کرد؟',
                'autonomous-agents-and-future-of-coding',
                'گذار از ابزارهای تکمیل خودکار به ایجنت‌های تصمیم‌گیر که می‌توانند کدهای پایدار تولید، تست‌های واحد را اجرا و دیباگ کنند.',
                'science-and-technology',
                generate_architecture_content,
                ['ai', 'systems-architecture'],
                False
            ),
            (
                'نظریه گراف و پیچیدگی شبکه‌ها: ریاضیات پنهان پشت اینترنت، مغز و جامعه',
                'network-theory-and-graph-mathematics',
                'پدیده‌های جهان کوچک، توزیع‌های قانون توان و گره‌های پرنفوذ؛ چگونه توپولوژی شبکه‌ها ساختار کل تمدن را مدیریت می‌کند؟',
                'science-and-technology',
                generate_architecture_content,
                ['systems-architecture', 'critical-thinking'],
                False
            ),
            (
                'مهندسی ژنتیک و کریسپر: بازنویسی کد حیات و دوراهی‌های بیواتیک',
                'crispr-gene-editing-and-ethics-of-life',
                'دستکاری دقیق دی‌ان‌ای برای درمان بیماری‌های ارثی؛ امیدها و هراس‌های ناشی از طراحی انسان در آزمایشگاه‌های فردا.',
                'science-and-technology',
                generate_cosmos_ai_content,
                ['critical-thinking', 'cosmology'],
                False
            ),
            (
                'انقلاب انرژی‌های پاک: باتری‌های حالت جامد و ادغام هوشمند شبکه برق',
                'clean-energy-transition-and-smart-grid',
                'گذار از سوخت‌های فسیلی؛ چالش‌های ذخیره‌سازی انرژی‌های تجدیدپذیر، چگالی انرژی باتری‌ها و اینترنت انرژی در شهرهای آینده.',
                'science-and-technology',
                generate_architecture_content,
                ['systems-architecture', 'critical-thinking'],
                False
            ),
            (
                'سایبرنتیک و تعامل انسان و ماشین: رابط‌های مغز و رایانه (BCI)',
                'brain-computer-interfaces-and-cybernetics',
                'از الکترودهای کاشته‌شده تا سنسورهای امواج قشری؛ چگونه ترجمه سیگنال‌های سیناپسی مرز میان بیولوژی و مدار الکترونیکی را محو می‌کند؟',
                'science-and-technology',
                generate_cosmos_ai_content,
                ['ai', 'systems-architecture'],
                False
            ),
            (
                'امنیت داده و رمزنگاری پسا-کوانتوم: محافظت از حریم خصوصی در عصر شفافیت',
                'post-quantum-cryptography-and-privacy',
                'چرا الگوریتم‌های سنتی RSA در برابر ماشین‌های کوانتومی شکننده هستند؟ طراحی رمزنگاری شبکه‌ای برای بقای حریم خصوصی دیجیتال.',
                'science-and-technology',
                generate_architecture_content,
                ['systems-architecture', 'ai'],
                False
            ),
            (
                'کالبدشکافی داده‌های بزرگ: استخراج سیگنال خالص از دریای بی‌کران نویز',
                'big-data-architecture-signal-over-noise',
                'معماری پایگاه‌های داده توزیع‌شده، پایپ‌لاین‌های پردازش لحظه‌ای و مهندسی داده در مقیاس میلیون‌ها رویداد در ثانیه.',
                'science-and-technology',
                generate_architecture_content,
                ['systems-architecture', 'ai'],
                False
            ),
            (
                'شبیه‌سازی حیات مصنوعی: الگوریتم‌های خودهمانندساز و سلولار اتوماتا',
                'cellular-automata-and-artificial-life',
                'بازی زندگی جان کانوی و پیدایش رفتارهای پیچیده شبیه موجود زنده از قواعد فوق‌العاده ساده؛ درس‌هایی برای مهندسان سیستم.',
                'science-and-technology',
                generate_cosmos_ai_content,
                ['ai', 'systems-architecture'],
                False
            ),
            (
                'اکتشاف مریخ و ماه: چالش‌های زیستی و لجستیکی حیات چندسیاره‌ای',
                'mars-colonization-and-multiplanetary-species',
                'محافظت در برابر تشعشعات کیهانی، گرانش ضعیف، بازچرخانی منابع بسته و بقای تمدن انسان ورای گهواره خاکی زمین.',
                'science-and-technology',
                generate_cosmos_ai_content,
                ['cosmology', 'systems-architecture'],
                False
            ),
            (
                'یادگیری تقویتی از بازخورد انسانی (RLHF): اهلی‌سازی هوش‌های مقیاس‌بزرگ',
                'reinforcement-learning-with-human-feedback',
                'چگونه تراز کردن مدل‌های پیش‌بین کلمه با ترجیحات اخلاقی و کیفی انسان، زمینه پیدایش دستیارهای هوشمند ایمن را فراهم ساخت؟',
                'science-and-technology',
                generate_architecture_content,
                ['ai', 'critical-thinking'],
                False
            ),
            (
                'نانوتکنولوژی مولکولی: دستکاری ماده در مقیاس اتمی و انقلاب دارورسانی',
                'molecular-nanotechnology-and-targeted-medicine',
                'روبات‌های میکروسکوپی که سلول‌های سرطانی را شناسایی و نابود می‌کنند؛ افق‌های دگرگون‌کننده فیزیک ماده چگال.',
                'science-and-technology',
                generate_cosmos_ai_content,
                ['cosmology', 'systems-architecture'],
                False
            ),
            (
                'اینترنت اشیاء و اکوسیستم‌های خودمختار: هوشمندی توزیع‌شده در پیرامون ما',
                'edge-computing-and-distributed-iot',
                'انتقال محاسبات از ابر متمرکز به لبه‌های شبکه (Edge Computing)؛ چگونه خودروهای خودران و حسگرها در کسری از میلی‌ثانیه تصمیم می‌گیرند؟',
                'science-and-technology',
                generate_architecture_content,
                ['systems-architecture', 'ai'],
                False
            ),
            (
                'فیزیک آشوب و اثر پروانه‌ای: چرا پیش‌بینی دقیق سیستم‌های غیرخطی ناممکن است؟',
                'chaos-theory-and-butterfly-effect',
                'جاذب‌های لورنتس و حساسیت به شرایط اولیه در آب‌وهوا و اقتصاد؛ چرا جهان به رغم جبر فیزیکی، همواره شگفت‌انگیز و باز است؟',
                'science-and-technology',
                generate_cosmos_ai_content,
                ['cosmology', 'critical-thinking'],
                False
            ),

            # Category 3: Art, Literature & Creativity (16 articles)
            (
                'زیبایی‌شناسی سادگی: پیوند مینی‌مالیسم، هندسه تایپوگرافی فارسی و طراحی وب',
                'aesthetics-of-simplicity-minimalism-and-typography',
                'کالبدشکافی فلسفه فرم و کارکرد، جادوی حذف زواید برای برجسته‌سازی گوهر محتوا، تکامل فونت وزیرمتن و روانشناسی هارمونی رنگ‌ها.',
                'art-and-creativity',
                generate_aesthetics_content,
                ['aesthetics', 'design'],
                True
            ),
            (
                'افسون داستان‌سرایی: چرا انسان در عصر انفجار داده‌ها تشنه قصه است؟',
                'power-of-narrative-and-storytelling-in-digital-era',
                'قدرت کهن‌الگوها در تسخیر قلب‌ها و ذهن‌ها؛ واکاوی تکنیک‌های روایت موثر و چگونگی تبدیل تجربیات زیسته به آثاری الهام‌بخش.',
                'art-and-creativity',
                generate_aesthetics_content,
                ['storytelling', 'aesthetics'],
                True
            ),
            (
                'روانشناسی رنگ‌ها در طراحی معاصر: زبان خاموشی که احساسات را می‌سازد',
                'color-psychology-and-visual-harmony',
                'چگونه تضاد میان نارنجی گرمابخش و بنفش متفکرانه، تعادلی ارگونومیک و شورانگیز در درک مخاطب ایجاد می‌کند؟',
                'art-and-creativity',
                generate_aesthetics_content,
                ['design', 'aesthetics'],
                False
            ),
            (
                'تاریخ خط و خوشنویسی ایرانی: از کتیبه‌های کوفی تا قلم‌های دیجیتال',
                'evolution-of-persian-calligraphy-to-digital-type',
                'سیری در نبوغ میرعماد، ساختار قطاعی و کرسی‌بندی نستعلیق؛ چگونگی انتقال روح خط سنتی به فونت‌های اسکرین‌محور مدرن.',
                'art-and-creativity',
                generate_aesthetics_content,
                ['design', 'aesthetics'],
                False
            ),
            (
                'سینما و درک زمان: تارکوفسکی، پیکرتراشی در زمان و جادوی پلان‌های ممتد',
                'tarkovsky-and-sculpting-in-time',
                'چرا سینما برترین مدیوم بازنمایی زمان زیسته است؟ تحلیل زیباشناختی فیلم‌های بزرگ تاریخ و گریز از تدوین‌های هیستریک معاصر.',
                'art-and-creativity',
                generate_aesthetics_content,
                ['storytelling', 'aesthetics'],
                False
            ),
            (
                'معماری نور و سایه: از شاهکارهای لوکوربوزیه تا طراحی رابط کاربری',
                'architecture-of-light-and-shadow',
                'نور متریالی مادی نیست اما بدون آن هیچ فرمی پدیدار نمی‌شود؛ چگونه سایه‌روشن‌ها عمق، هویت و بعد را به فضاها می‌بخشند؟',
                'art-and-creativity',
                generate_aesthetics_content,
                ['design', 'aesthetics'],
                False
            ),
            (
                'جادوی رئالیسم جادویی: پیوند رویا و واقعیت در شاهکارهای ادبیات آمریکای لاتین',
                'magic-realism-in-world-literature',
                'بررسی صد سال تنهایی مارکز و آثار بورخس؛ چگونه شگفتی در بستر حوادث روزمره ادغام می‌شود تا حقیقت ژرف‌تری از تاریخ را آشکار سازد؟',
                'art-and-creativity',
                generate_aesthetics_content,
                ['storytelling', 'aesthetics'],
                False
            ),
            (
                'طراحی سیستم‌های مقیاس‌پذیر بصری: دیزاین توکن‌ها و هندسه رابط‌ها',
                'design-systems-tokens-and-atomic-components',
                'چگونه دیزاین سیستم‌ها فاصله میان طراح و مهندس نرم‌افزار را از میان برمی‌دارند و زبان بصری پایداری برای محصولات خلق می‌کنند؟',
                'art-and-creativity',
                generate_aesthetics_content,
                ['design', 'systems-architecture'],
                False
            ),
            (
                'موسیقی سکوت: زیبایی‌شناسی اصوات در آثار باخ، کیج و کیهان کلهر',
                'aesthetics-of-silence-in-music',
                'سکوت صرفاً غیاب صدا نیست؛ بلکه فضایی باردار از معناست که به نت‌ها وزن و پروا می‌دهد. تاملی در باب هندسه هارمونی شنیداری.',
                'art-and-creativity',
                generate_aesthetics_content,
                ['aesthetics', 'philosophy'],
                False
            ),
            (
                'ادبیات کارگاهی در برابر اصالت شهودی: چگونه صدای منحصربه‌فرد خود را در نویسندگی بیابیم؟',
                'finding-authentic-voice-in-creative-writing',
                'فراتر رفتن از کلیشه‌های آموزش نویسندگی؛ چرا شجاعت مواجهه با زخم‌های شخصی و صداقت لحن، جوهره ماندگاری قلم نویسنده است؟',
                'art-and-creativity',
                generate_aesthetics_content,
                ['storytelling', 'aesthetics'],
                False
            ),
            (
                'کتاب به عنوان اثر هنری: تاریخچه‌ای از صفحه‌آرایی، جلد و لمس کاغذ',
                'book-design-as-a-tactile-work-of-art',
                'چرا کتاب فیزیکی هرگز منقرض نخواهد شد؟ روانشناسی بوی کاغذ، جنس مقوا و تعامل حواس چندگانه در تجربه کتاب‌خوانی اصیل.',
                'art-and-creativity',
                generate_aesthetics_content,
                ['design', 'aesthetics'],
                False
            ),
            (
                'شعر کوتاه و اقتصاد واژگان: از هایکوهای باشو تا رباعیات خیام',
                'haiku-and-khayyam-economy-of-words',
                'چگونه با کمترین تعداد کلمات، ژرف‌ترین تکانه‌های هستی‌شناختی را ثبت کنیم؟ هنر تراشیدن زواید برای دستیابی به خلوص شاعرانه.',
                'art-and-creativity',
                generate_aesthetics_content,
                ['storytelling', 'aesthetics'],
                False
            ),
            (
                'عکاسی خیابانی و شکار لحظه قطعی: آموزه‌های هانری کارتیه-برسون',
                'street-photography-and-decisive-moment',
                'دیدن در برابر نگاه کردن گذرا؛ چگونه عکاس با دوربین خود، قطعه‌ای از زمان جاری را منجمد کرده و به تابلویی جاودانه بدل می‌سازد؟',
                'art-and-creativity',
                generate_aesthetics_content,
                ['aesthetics', 'design'],
                False
            ),
            (
                'طراحی ارگونومیک اشیاء: صندلی، فنجان و وسایلی که با جان ما درآمیخته‌اند',
                'ergonomics-and-emotional-design-of-daily-objects',
                'نظریات دونالد نورمن در باب طراحی اشیای روزمره؛ چرا لوازمی که زیبا طراحی شده‌اند، عملکرد کاربردی بهتری نیز ارائه می‌دهند؟',
                'art-and-creativity',
                generate_aesthetics_content,
                ['design', 'aesthetics'],
                False
            ),
            (
                'تصویرسازی مفهومی: ترجمه اندیشه‌های انتزاعی به زبان نشانه‌ها و استعاره‌ها',
                'conceptual-illustration-and-visual-metaphors',
                'چگونه یک تصویرساز برجسته می‌تواند مقاله‌ای درباره تنهایی، هوش مصنوعی یا تورم را در یک تصویر خیره‌کننده و ماندگار خلاصه کند؟',
                'art-and-creativity',
                generate_aesthetics_content,
                ['design', 'aesthetics'],
                False
            ),
            (
                'معماری خانه‌های تاریخی کاشان و یزد: خرد زیست‌اقلیمی و هماهنگی با خاک',
                'vernacular-architecture-of-iranian-historic-houses',
                'بادگیرها، هشتی‌ها، حوض‌خانه‌ها و گودال‌باغچه‌ها؛ درسی ابدی برای معماری پایدار معاصر در همزیستی با اقلیم خشک و گرم.',
                'art-and-creativity',
                generate_aesthetics_content,
                ['design', 'aesthetics'],
                False
            ),

            # Category 4: Artificial Intelligence & Future (10 articles)
            (
                'عصر عامل‌های خودمختار: چگونه ایجنت‌های هوشمند چرخه توسعه نرم‌افزار را متحول ساختند؟',
                'autonomous-agents-revolution-in-software-engineering',
                'تحلیل عمیق نقش عامل‌های خودمختار در برنامه‌نویسی مدرن، تفکیک وظایف و استانداردهای طراحی سیستم‌های تصمیم‌گیر خودکار.',
                'artificial-intelligence',
                generate_cosmos_ai_content,
                ['ai', 'systems-architecture'],
                True
            ),
            (
                'مدل‌های استدلال عمیق: کاوش در زنجیره اندیشه و رمزگشایی از تصمیم‌گیری‌های پیچیده ماشین',
                'deep-reasoning-models-and-chain-of-thought',
                'بررسی مکانیزم‌های تفکر گام‌به‌گام در مدل‌های هوش مصنوعی نوین و ریشه‌کن ساختن خطاهای شناختی و توهمات آماری.',
                'artificial-intelligence',
                generate_cosmos_ai_content,
                ['ai', 'critical-thinking'],
                False
            ),
            (
                'هم‌راستاسازی هوش مصنوعی (AI Alignment): چالش‌های اخلاقی و فنی در مهار سیستم‌های اَبَرهوشمند',
                'ai-alignment-ethics-and-superintelligence-safety',
                'چگونه اطمینان حاصل کنیم که اهداف و ارزش‌های سیستم‌های هوشمند آینده در انطباق کامل با بقا و کرامت انسان باقی می‌مانند؟',
                'artificial-intelligence',
                generate_cosmos_ai_content,
                ['ai', 'philosophy'],
                True
            ),
            (
                'بینایی ماشین و درک چندوجهی: چگونه مدل‌ها جهان بصری و شنیداری را تفسیر می‌کنند؟',
                'computer-vision-and-multimodal-perception',
                'ترجمه پیکسل‌ها و امواج صوتی به بردارها و مفاهیم ادراکی؛ بررسی معماری ویژن ترنسفورمرها (ViT) و کاربردهای آن در رباتیک.',
                'artificial-intelligence',
                generate_cosmos_ai_content,
                ['ai', 'systems-architecture'],
                False
            ),
            (
                'هوش مصنوعی مولد در علوم زیستی: پیش‌بینی ساختار پروتئین‌ها و طراحی داروهای نو',
                'generative-ai-in-biology-and-drug-discovery',
                'از آلفافولد تا طراحی مولکول‌های اختصاصی درمان؛ چگونه یادگیری عمیق انقلاب نیم‌قرنی در زیست‌شناسی محاسباتی آفرید.',
                'artificial-intelligence',
                generate_cosmos_ai_content,
                ['ai', 'critical-thinking'],
                False
            ),
            (
                'محدودیت‌های بنیادی یادگیری عمیق: آیا هوش مصنوعی عمومی (AGI) بدون درک علّی میسر است؟',
                'foundational-limits-of-deep-learning-and-causality',
                'چرا همبستگی آماری جانشین علیت نمی‌شود؟ نقدهای جودیا پرل و افق‌های گذار به معماری‌های ترکیبی نمادین-پیوندی.',
                'artificial-intelligence',
                generate_cosmos_ai_content,
                ['ai', 'philosophy'],
                False
            ),
            (
                'پردازش زبان طبیعی و زبان‌شناسی محاسباتی: کالبدشکافی بردارهای معنایی و توجه متقاطع',
                'nlp-computational-linguistics-and-embeddings',
                'چگونه کلمات به فضاهای هندسی چندصدبُعدی تبدیل می‌شوند؟ کالبدشکافی لایه‌های توجه (Self-Attention) در ترنسفورمرها.',
                'artificial-intelligence',
                generate_cosmos_ai_content,
                ['ai', 'systems-architecture'],
                False
            ),
            (
                'یادگیری تقویتی در بازی‌های استراتژیک: از آلفاگو تا هدایت سیستم‌های رباتیک خودمختار',
                'reinforcement-learning-in-complex-environments',
                'کاوش در فضاهای تصمیم‌گیری فوق‌العاده بزرگ و همگرایی شبیه‌سازی با دنیای واقعی در آموزش بازوهای مکانیکی و پهپادها.',
                'artificial-intelligence',
                generate_cosmos_ai_content,
                ['ai', 'systems-architecture'],
                False
            ),
            (
                'تاثیر هوش مصنوعی بر بازار کار و اقتصاد آینده: بازتعریف مهارت‌های انسانی در عصر اتوماسیون',
                'ai-impact-on-labor-markets-and-human-skills',
                'کدام مهارت‌ها در برابر اتوماسیون مصون می‌مانند؟ ضرورت آموزش تفکر انتقادی، خردورزی اخلاقی و خلاقیت ساختاریافته.',
                'artificial-intelligence',
                generate_cosmos_ai_content,
                ['ai', 'philosophy'],
                False
            ),
            (
                'فلسفه ذهن و هوش سیلیکونی: آیا مدل‌های زبانی می‌توانند تجربه ذهنی (Qualia) داشته باشند؟',
                'philosophy-of-mind-and-silicon-consciousness',
                'مسئله دشوار آگاهی از دیدگاه دیوید چالمرز؛ بررسی ادعاهای پیرامون ظهور ادراک در شبکه‌های پیچیده محاسباتی.',
                'artificial-intelligence',
                generate_cosmos_ai_content,
                ['ai', 'philosophy'],
                False
            ),

            # Category 5: Software Architecture & Systems (10 articles)
            (
                'معماری سه‌لایه تمیز (View, Service, Repository): راهنمای جامع عبور از مدل‌های چاق',
                'clean-three-tier-architecture-guide',
                'کالبدشکافی تفکیک دغدغه‌ها در وب؛ شیوه ساخت پایگاه‌کدهای ماژولار، تست‌پذیر و مصون از خطاهای تداخل و پیچیدگی.',
                'software-architecture',
                generate_architecture_content,
                ['systems-architecture', 'critical-thinking'],
                True
            ),
            (
                'توسعه مبتنی بر دامنه (DDD): مدل‌سازی هسته بیزینس و مرزهای احاطه‌شده (Bounded Contexts)',
                'domain-driven-design-and-bounded-contexts',
                'زبان مشترک (Ubiquitous Language) میان مهندسان و ذی‌نفعان کسب‌وکار؛ الگوهای Aggregate، Entity و Value Objects.',
                'software-architecture',
                generate_architecture_content,
                ['systems-architecture'],
                False
            ),
            (
                'مایکروسرویس‌ها در عمل: الگوهای ارتباط ناهمگام، صف پیام‌ها و مدیریت تراکنش‌های توزیع‌شده',
                'microservices-patterns-and-distributed-transactions',
                'چالش‌های الگوی Saga، صف‌های رویداد آپاچی کافکا و حفظ یکپارچگی داده‌ها میان سرویس‌های مستقل شبکه.',
                'software-architecture',
                generate_architecture_content,
                ['systems-architecture'],
                True
            ),
            (
                'استراتژی‌های کشینگ چندسطحی: بهینه‌سازی کوئری‌های دیتابیس و کاهش گلوگاه‌های I/O',
                'multi-level-caching-strategies-and-io-reduction',
                'از کش‌های محلی در حافظه تا کلاسترهای توزیع‌شده ردیس؛ سیاست‌های انقضا، Cache Invalidation و پیش‌بارگذاری هوشمند.',
                'software-architecture',
                generate_architecture_content,
                ['systems-architecture'],
                False
            ),
            (
                'اصول SOLID و طراحی شیءگرا: نوشتن کدهای ماژولار، آزمون‌پذیر و پایدار در درازمدت',
                'solid-principles-in-production-software',
                'بررسی پنج اصل حیاتی مهندسی نرم‌افزار با مثال‌های عینی؛ چگونه وابستگی‌ها را معکوس کنیم و سیستم‌های مقیاس‌پذیر بسازیم؟',
                'software-architecture',
                generate_architecture_content,
                ['systems-architecture'],
                False
            ),
            (
                'مهندسی تاب‌آوری در سیستم‌های مقیاس‌بزرگ: الگوهای Circuit Breaker، Retry و Bulkhead',
                'resilience-engineering-and-fault-tolerance',
                'سیستم‌ها شکست خواهند خورد؛ هنر مهندسی در جلوگیری از دومینوی خرابی‌ها و طراحی سامانه‌های خودترمیم است.',
                'software-architecture',
                generate_architecture_content,
                ['systems-architecture'],
                False
            ),
            (
                'معماری رویدادمحور (Event-Driven Architecture): هدایت سامانه‌ها با استریم‌های لحظه‌ای داده',
                'event-driven-architecture-and-event-sourcing',
                'ثبت تاریخچه تغییرات به جای حالت نهایی (Event Sourcing) و تفکیک مسئولیت‌های خواندن و نوشتن (CQRS) در سیستم‌های پرترافیک.',
                'software-architecture',
                generate_architecture_content,
                ['systems-architecture'],
                False
            ),
            (
                'بهینه‌سازی پایگاه‌های داده رابطه‌ای: ایندکس‌گذاری پیشرفته، پارتیشن‌بندی و نرمال‌سازی عملگرایانه',
                'relational-database-optimization-and-indexing',
                'کالبدشکافی پلن اجرای کوئری (EXPLAIN)، بهینه‌سازی B-Treeها و تعادل میان قواعد نرمال‌سازی و سرعت بازخوانی داده.',
                'software-architecture',
                generate_architecture_content,
                ['systems-architecture'],
                False
            ),
            (
                'پایپ‌لاین‌های CI/CD و زیرساخت به عنوان کد (IaC): خودکارسازی انتشار نرم‌افزار بدون توقف',
                'cicd-pipelines-and-infrastructure-as-code',
                'استقرارهای بدون توقف (Zero-downtime Blue/Green Deployments) و مدیریت سرورها با کدهای نسخه‌پذیر و آزمون‌پذیر.',
                'software-architecture',
                generate_architecture_content,
                ['systems-architecture'],
                False
            ),
            (
                'امنیت در سطح معماری: مدل‌سازی تهدیدات، احراز هویت توزیع‌شده و دفاع در عمق (Defense in Depth)',
                'security-by-design-and-threat-modeling',
                'مدل اعتماد صفر (Zero Trust Architecture)، حفاظت از توکن‌های نشست و امن‌سازی لایه‌های ارتباطی میکروسرویس‌ها.',
                'software-architecture',
                generate_architecture_content,
                ['systems-architecture'],
                False
            ),

            # Category 6: Product Design & Design Systems (10 articles)
            (
                'دیزاین سیستم‌های مقیاس‌پذیر: معماری دیزاین توکن‌ها و هماهنگی میان دیزاینر و برنامه‌نویس',
                'scalable-design-systems-and-design-tokens',
                'ایجاد زبان بصری مشترک؛ چگونه دیزاین توکن‌ها فاصله‌ها، پالت رنگ‌ها و تایپوگرافی را در تمام پلتفرم‌ها هماهنگ می‌سازند؟',
                'design-systems',
                generate_aesthetics_content,
                ['design', 'systems-architecture'],
                True
            ),
            (
                'تایپوگرافی فارسی در وب مدرن: هندسه خط، خوانایی خطوط زمینه و فونت‌های متغیر',
                'persian-typography-in-modern-web-and-variable-fonts',
                'از خطوط سنتی تا فونت‌های دیجیتال نظیر وزیرمتن؛ استانداردهای خوانایی در متون بلند، تناسب خطوط و ارگونومی دیداری.',
                'design-systems',
                generate_aesthetics_content,
                ['design', 'aesthetics'],
                True
            ),
            (
                'موشن دیزاین و فیزیک انیمیشن در وب: راهنمای کاربردی میکرواینتراکشن‌های هدفمند',
                'motion-design-and-purposeful-micro-interactions',
                'انیمیشن به مثابه فیزیک جهان مجازی؛ چگونه حرکات نرم و پاسخگو کاربر را در جریان شناخت ساختار صفحه هدایت می‌کنند؟',
                'design-systems',
                generate_aesthetics_content,
                ['design', 'aesthetics'],
                False
            ),
            (
                'روانشناسی تجربه کاربری (UX): الگوهای رفتاری، قانون هیک، و کاهش بار شناختی مخاطب',
                'ux-psychology-and-cognitive-load-reduction',
                'چگونه با حذف اصطکاک‌های غیرضروری و کاهش تعداد گزینه‌ها در هر گام، تجربه کاربری شهودی و لذت‌بخشی خلق نماییم؟',
                'design-systems',
                generate_aesthetics_content,
                ['design', 'cognitive-psychology'],
                False
            ),
            (
                'دسترس‌پذیری وب (A11y): طراحی فراگیر برای تمام کاربران و استانداردهای WCAG',
                'web-accessibility-and-inclusive-design',
                'کنتراست رنگ‌ها، ناوبری با کیبورد، برچسب‌های خواننده صفحه و احترام به تنوع توانمندی‌های انسانی در دنیای دیجیتال.',
                'design-systems',
                generate_aesthetics_content,
                ['design', 'aesthetics'],
                False
            ),
            (
                'هنر چیدمان و شبکه‌بندی (Grid Systems): تعادل فضاهای منفی و ریتم بصری در صفحات واکنش‌گرا',
                'grid-systems-negative-space-and-responsive-rhythm',
                'شبکه‌های ۱۲ ستونه، هماهنگی فضاهای خالی و پیاده‌سازی گرید‌های روان با تیلویند و سی‌اس‌اس مدرن.',
                'design-systems',
                generate_aesthetics_content,
                ['design', 'aesthetics'],
                False
            ),
            (
                'معماری اطلاعات و طراحی جریان کاربر: هدایت بصری بدون اصطکاک از نقطه فرود تا هدف',
                'information-architecture-and-frictionless-user-flow',
                'ساختار درختی محتوا، دسته‌بندی موضوعی و سلسله‌مراتب بصری؛ چگونه کاربر در کسری از ثانیه مسیر خود را پیدا می‌کند؟',
                'design-systems',
                generate_aesthetics_content,
                ['design', 'systems-architecture'],
                False
            ),
            (
                'تحقیقات کاربردی و تست کارایی محصول: روش‌های کشف نیازهای ناگفته و اعتبارسنجی فرضیات',
                'user-research-methods-and-usability-testing',
                'مصاحبه‌های عمقی، آزمون‌های A/B و نقشه‌های حرارتی (Heatmaps)؛ چگونه محصولات را بر اساس داده‌های تجربی بازطراحی کنیم؟',
                'design-systems',
                generate_aesthetics_content,
                ['design', 'critical-thinking'],
                False
            ),
            (
                'طراحی دارک‌مود و تم‌های چندگانه: هارمونی کنتراست، کاهش خستگی چشم و استانداردهای رنگی',
                'dark-mode-architecture-and-multi-theme-design',
                'اصول عمق‌دهی با سطوح خاکستری به جای سیاه مطلق، مدیریت تابش نور در محیط‌های کم‌نور و ذخیره‌سازی ترجیحات کاربر.',
                'design-systems',
                generate_aesthetics_content,
                ['design', 'aesthetics'],
                False
            ),
            (
                'آینده رابط‌های کاربری (Future UI): از دیزاین لمسی تا تعاملات صوتی و واقعیت فضایی',
                'future-of-ui-spatial-computing-and-voice',
                'فراتر از شیشه‌های دو بعدی؛ آمادگی دیزاین سیستم‌ها برای تعاملات سه‌بعدی، حرکات نگاه (Eye Tracking) و رایانش فضایی.',
                'design-systems',
                generate_aesthetics_content,
                ['design', 'ai'],
                False
            )
        ]

        self.stdout.write(self.style.NOTICE(f'Total {len(raw_article_meta)} articles prepared across all categories.'))

        # Clear existing articles and recreate
        Article.objects.all().delete()
        created_articles = []
        now = timezone.now()

        for idx, (title, slug, summary, cat_slug, content_fn, tag_keys, is_feat) in enumerate(raw_article_meta):
            photo_path = available_photos[idx % len(available_photos)]
            author = authors[idx % len(authors)]
            published_date = now - timedelta(days=idx * 2, hours=(idx % 12) + 1)
            content_text = content_fn()

            art = Article.objects.create(
                title=title,
                slug=f"{slug}-{idx+1}" if Article.objects.filter(slug=slug).exists() else slug,
                summary=summary,
                content=content_text,
                category=categories[cat_slug],
                image=photo_path,
                author=author,
                status=ArticleStatus.PUBLISHED,
                reading_time_minutes=15 + (idx % 10),
                views_count=180 + (idx * 23),
                is_featured=is_feat,
                published_at=published_date
            )

            # Assign tags
            tag_objs = [tags[k] for k in tag_keys if k in tags]
            art.tags.set(tag_objs)
            created_articles.append(art)

        self.stdout.write(self.style.SUCCESS(f'Successfully created and indexed {len(created_articles)} articles across ALL categories!'))

        # 6. Seed Comments
        Comment.objects.all().delete()
        comment_samples = [
            'تحلیل فوق‌العاده جامع و عمیقی بود. خواندن این مقاله در آرامش صبحگاهی تجربه فوق‌العاده‌ای به من داد.',
            'نکاتی که درباره ساختار تفکر و پیوند آن با واقعیت‌های روزمره مطرح کردید بسیار روشنگر بود.',
            'قلم نویسنده بسیار شیوا، پالوده و جذاب است. مجله دَندی استاندارد مقاله‌نویسی را ارتقا داده است.',
            'استفاده از معماری لایه‌ای و نگاه چندرشته‌ای واقعا شایسته تحسین است. منتظر ادامه این جستارها هستیم.',
            'ترکیب فونت زیبای وزیرمتن و این تصاویر عکاسی واقعی، لذت خواندن متن‌های بلند را چند برابر کرده است.'
        ]

        comment_count = 0
        for i in range(25):
            art = created_articles[i]
            author = authors[(i + 1) % len(authors)]
            text = comment_samples[i % len(comment_samples)]
            Comment.objects.create(
                article=art,
                author=author,
                content=text,
                status=CommentStatus.APPROVED
            )
            comment_count += 1

        self.stdout.write(self.style.SUCCESS(f'Seeded {comment_count} realistic approved comments.'))
        self.stdout.write(self.style.SUCCESS('🎉 Every single category now contains at least 10 comprehensive articles!'))
