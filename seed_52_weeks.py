import os
import django
import random
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alkinvaran_proj.settings")
django.setup()

from website.models import BlogPost
from django.utils import timezone

s1 = ["Vücut ağırlığı antrenmanları, insanın kendi kinetik zincirini anlaması için en mükemmel yoldur.",
      "Cimnastik, salt esneklik değil, bu esneklik açılarında kuvvet üretebilme becerisidir.",
      "Atletik performansın temel sırrı, iyi programlanmış bir toparlanma sürecinden geçer.",
      "İnsan bedeni, karşılaştığı strese adaptasyon göstererek hayatta kalacak şekilde kusursuzca dizayn edilmiştir.",
      "Mobilite eksiklikleri, zamanla tüm fonksiyonel hareket paternlerini bozarak sakatlıklara yol açar.",
      "Kuvvet antrenmanlarında her tekrar bir ustalığa, her set sarsılmaz bir kararlılığa işaret eder.",
      "Modern çağın hareketsizliği, fasyal dokularımızın giderek daha da sertleşmesine sebep olmaktadır.",
      "Spora kalıcı bir disiplinle yaklaşmak, anlık motivasyon patlamalarından çok daha garantili bir yöntemdir."]

s2 = ["Her antrenman seansında, merkez bölgemizin (core) gücünü diğer uzuvlara nasıl başarıyla aktardığını hissederiz.",
      "Özellikle omuz mobilitesi, üst beden mekaniği için kilit bir performans eşik görevi görmektedir.",
      "Dinamik gerdirme protokolleri, merkezi sinir sistemini yaklaşan zorlu görevlere bütünüyle hazırlar.",
      "Antrenman hacmi ile toparlanma kapasitesi arasındaki o çok hassas dengeyi mutlak suretle kurmak şarttır.",
      "Zihinsel odaklanma olmadan yapılan rastgele hareketler, istenmeyen eklem streslerine zemin hazırlar.",
      "Elestik enerjiyi depolayıp boşaltma yeteneği (plyometrics), sporcudaki gerçek patlayıcı gücü oluşturur.",
      "Barfiks ve şınav gibi kapalı kinetik zincir hareketleri, kıkırdak ve eklem sağlığı açısından tartışmasız kusursuzdur.",
      "Hareket aralığının tamamını yüksek kontrolle kullanmak, kas dokusunda olağanüstü maksimum adaptasyon yaratır."]

s3 = ["Plato evrelerine ulaştığınızda, antrenman frekansını hızla artırmak yerine uygulanan mekanik stresi değiştirmelisiniz.",
      "Kaliteli gece uykusu, kaslardaki protein sentezinin maksimize olduğu ve birikmiş doku hasarlarının onarıldığı evredir.",
      "Statik esnemelerin aksine, dinamik sistemli tekrarlar kasa giden kan akışını hızlandırarak gergin fasyayı anında yumuşatır.",
      "Amut (handstand) pratiği, bacakların havalanmasının ötesinde devasa bir vücut uzaysal farkındalığı (propriosepsiyon) geliştirir.",
      "İleri seviye statik hareketler, bedenin çok boyutlu temel güç standartları yerine tam olarak oturmadan asla denenmemelidir.",
      "Kaslardaki nöromusküler adaptasyon, görsel kas hipertrofisinden (büyümesinden) çok daha önce, henüz ilk haftalarda başlar.",
      "İdman sonrasındaki karbonhidrat zamanlaması, tükenen kaslardaki yoğun glikojen depolarını hızla yerine koyar.",
      "Eklemlerin sahip oldukları tüm rotasyonel açılarda çok güçlü durabilmesi, uzun süreli ve hedeflenen mobilite pratiğinin sonucudur."]

s4 = ["Yaşamsal sakatlıklardan korunmanın belki de en birincil yolu, salondaki anlamsız ağırlık kaldırma egosunu geride bırakmaktır.",
      "Egzersizi yapış hızınız (tempo), kastaki fizyolojik gerilim altındaki süreyi bütünüyle belirleyen ana biyomekanik unsurdur.",
      "Core sadece dıştan görünen atletik karın kası değil, aynı zamanda omurgayı bir zırh gibi saran çok katmanlı, dayanıklı bir yapıdır.",
      "Sürekli aynı tekrarlarla ve formlarla çalışmak, bedenin doğal direnç uyum sağlama potansiyelini bir süre sonra tamamen köreltir.",
      "Diz eklemi etrafındaki o destekleyici bağ dokuları kuvvetlendirirseniz, olası ani burkulma vakalarının direkt önüne geçersiniz.",
      "Ulaşılan metabolik stres ve ortaya çıkarılan mekanik gerilim, aynı program içerisinde mutlaka dengeli bir şekilde uygulanmalıdır.",
      "İhtiyacınız olan şey kalitesizce daha fazla set yapmak değil, her sette hedeflenen kastaki içsel hissiyat ve odaklanmayı artırmaktır.",
      "Tüm kinetik zinciri sistematik bir bütün olarak ele aldığınızda, uygulanacak o bileşik (compound) egzersizler daha da değerlenir."]

s5 = ["Zayıf fiziksel noktaları net tespit etmek ve asıl antrenmanı güvenle oraya yönlendirmek deneyimli sporcunun en büyük sınavıdır.",
      "Bel kemeri ve omuz kuşağı arasındaki var olan kasılma kuvveti dengesizliği ilerleyen dönemde ağır postür bozukluğu yaratır.",
      "Bilimsel ve iyi bir kişisel antrenör, hazır fotokopi programlar yerine sizi sadece o güne özel performans analicinizi okuyarak yönlendirir.",
      "Bilinen yüksek şiddetli interval antrenmanlar (HIIT), kardiyovasküler (kalp-damar) limitlerin kapasitesini en hızlı ve etkin biçimde artırır.",
      "Temelde fonksiyonel kuvvet demek, salonda basabildiğiniz gücünüzü günlük hayattaki sıradan bedensel görevlerinize dökebilmektir.",
      "Vücuda giren mikro besin grupları ve mineraller, zorlu kas kasılmaları mekanizmasında trilyonlarca biyokimyasal reaksiyonu yürütür.",
      "Kritik güç antrenman öncesinde kararında alınan kafein tüketimi, laktik asit eşiğini sinirsel boyutta geciktirerek performansı destekler.",
      "Öfkeli bedeni esnetmek için öncelikle beyni de o kası cidden gevşetmeye telkinle ikna etmeniz, nefesle beraber en iyi mümkündür."]

s6 = ["Özenle tutulan bir antrenman günlüğü, ağırlık gelişim eğrisini (progresif overload takibi) objektif bir şekilde izlemenizi şüphesiz sağlar.",
      "Sinemalarda hep aks ettirilenin tersine, esneklik tek bir günde hevesle kazanılmaz; hücresel bir anatomik uyum sürecine ihtiyaç vardır.",
      "Herhangi bir idman hareketinde takıldığınızda, asistan yarım egzersizlerle en geriye dönük inşa yapmak çok en sağlıklı gelişim metodudur.",
      "Salon idman kalitesi nedensiz düştüğünde, plandaki dinlenme gününü tereddütsüz öne çekmek bir tembellik zaafiyeti değil, profesyonelliktir.",
      "Kollagen yapısının inanılmaz esneme payına uyum göstermesi, kemiğe tutunduğu o sağlam tendonların derinlemesine güçlenmesiyle el ele ilerler.",
      "İtiş eksentrik (negatif) kasılma anlarında zorla oluşan ufak mikro kas yırtıkları, o bölgedeki net hacimsel hipertrofinin en büyük nedenlerindendir.",
      "Sabahın erken ve taze zamanlarında günün ilk ışıklarıyla yapılan hafif, temposuz kardiyo, sirkadiyen (biyolojik saat) ritmimizi harika düzene koyar.",
      "Kalça kası (Glute) kompleksinin tam kuvvetle ve hissederek aktif edilebilmesi, diz ekleminize senelerce binen tüm aşınma yükünü anında yok edecektir."]

s7 = ["Beslenmenin pratik anlamda sadece o devasa niceliğine değil mutlak niteliğine, yani temiz, katkısız kaliteli gıda profillerine yoğunlukla odaklanılmalıdır.",
      "Planlanan düzenli köpük rulo (foam roller) baskı uygulamaları ve masaj tabancaları laktik asitin dokudaki hızlı yıkımında ciddi devasa rol oynar.",
      "Adeta saplantı gibi her gün son limite kadar yorgunca antrenman yapmak (overtraining), genelde sürdürülebilir genel başarıya maalesef her zaman terstir.",
      "Kafamızdaki zihinsel ve hayali o dev bariyerler, kaslardaki o kramp giren fiziksel yorgunluktan çok daha önce devreye girip seti acımasızca bırakmamızı söyler.",
      "Paha biçilmez değerdeki eklem sıvısının (sinovyal sıvı) hiç durmadan üretimi için düzenli zorlanmasız hareket etmek ve kan hidrasyon (su tüketimi) yaşamsaldır.",
      "Ellerdeki karpal tünel dengesine ve zayıf el bileklerine gereken esnekliği kazandırmadan rastgele amuta (handstand) kalkmak, zamanla ciddi sinirsel sıkışmalara yol açar.",
      "Evdeki direnç bandı egzersizleri hem acemi sıfır başlangıç hem de iddialı ileri seviye atletler için en sadık hasarsız bir asistan ve kas düzelticidir.",
      "Kemik mekanik sınır kapasitenize derinden saygı duyup plansızca acele etmeden sağlam bir gövde temeli inşa ettiğinizde sporla ilgili hemen hemen her şey sihirli şekilde değişir."]

s8 = ["Bedenin o inanılmaz sistemli muazzam tamir fabrikası gece tamamen karanlıkta çalışır, bu yüzden deliksiz uyku düzeniniz ileriki spor performansınızın tek güvencesidir.",
      "Bozuk hissettiğiniz yorgun günlerde düşük ritimli aktif toparlanma seansları, kan akışını istikrarlı artırarak yıpranmış kaslardaki laktik atıkları adeta adeta yıkar temizler.",
      "Özgür omurganın genetiğinde sahip olduğu doğal ve darbe emici 'S' kavisini tüm ağırlık kaldırma idman anlarında dik tutarak korumak asil yük paylaşımını acısız tüm disklere sağlar.",
      "Katı olan o anatomik hareket sınırını yavaş ve güvenli adımlarla milimetrik genişleterek esneklik çalışmalarını uzun soluklu bir hayat pratik displini haline sonuna kadar getirin.",
      "İdmanın kan ter içinde biten saniyesi antrenman sonrası alınan temiz karbonhidrat ve lösin bakımından zengin proteinin o harika onarıcı sinerjik etkisiyle, kas yakımı kesin olarak sertçe durdurulur.",
      "Mekanik sistemli ve kısıtlayıcı dışarıdan müdahalede bulunan makineler yerine, merkezinizi tamamen açık alanda rüzgarda dik dururcasına korumayı iliklerinize kadar öğreten serbest halter ve bar çalışmalarını cesurca seçin.",
      "Aletli veya düz zemin modern Jimnastik, basit kaba kas şişikliği ve suni kas büyümesinden ziyade kaslar arası sinirsel akış ve senkronize iletişimi olağanca artırmaya odaklanan harikalar yepyeni bir boyuttur.",
      "İçlerindeki temel fonksiyonelliğin tamamıyla yitirildiği ve yozlaştığı, dışı devasa şişme o salt estetik bedenler, en ufak bir günlük aksiyonda, ağır bir poşet taşırken veya dengesiz hareketlerde zor anlarda kasık çeken zayıf süslü birer bibloyu andırırlar."]

s9 = ["Ağır squat veya bench antrenmanları öncesinde yapılan bir dakikalık o derin mental simülasyon (tam hareketin zihinde canlandırılması ve hayal etme), adeta merkezi sistemden yollanan güçlü sinyallerle kas inervasyonunu doğrudan derinden destekler.",
      "Dopamin deposu sabah enerjik idmanları, kortizol gibi stres salgılayan hormon profilinizi bütünüyle günün zirve mesai anlarında bile en yapıcı ideal şekilde dengede tutarak yoğun stresi yönetir.",
      "Kalın tendon ve bağ dokusunun değişime adaptasyonu normal esnek kas dokusundan çok ama çok daha yavaş bir zaman zarfında gerçekleştiği için, program gelişimini tendon yeteneğine uygun kısıtlara göre sabırla ayarlamalısınız.",
      "Ölene dek hiçbir egzersiz rutini yeryüzünde yüzde yüz vazgeçilmez değildir; asıl dikkate değer ve yegane önemli olan sizin hedefinize ve kendi eşsiz kas biyomekaniği prensibinize en dürüst sadık o özel varyasyonu deneyerek bulmaktır.",
      "Tartıdaki yanıltıcı vücut kütle ya da kilo yağ oranından ziyade, doğrudan aynadaki fonksiyonel kas hacmine ve kalite dokusuna (kas içi sinsi bölgesel yağlanmanın gözle bariz azalması) sürekli motive ve odaklanmak, hedefe varış hızınızı inanılmaz kolaylaştırır.",
      "Doğuştan gelen genetik, zorlayıcı bireysel kıkırdak ve eklem sınırlarınızı gerçekçi adımlarla ve kabullenmeyle bilmek, ve onlara acı dolu bir dikkafalılıkla kaba bir savaş açmak yerine isyankar olmadan o sınır uçlarını sıcak ısıtılarak nazikçe ince milimlere doğru esnetmeyi akıllıca öğrenmelisiniz.",
      "Gelip geçici sığ ve popüler fitness akımlı günübirlik yaz başarıları yerine ömür denilen bu uzun solukta yaşam boyu yaşlandıkça uygulanabilir gerçekçi dinamik rutinler oturttuğunuzda bedeninizdeki kalıcı eşsiz iskeletsel değişimi işte tam o an sağlarsınız.",
      "Hedefler ve hayaller uğruna yıllar boyu yutkunularak verilen geri tavizsiz o sağlam disiplinli terli çalışma süreci, sizi dış dünyadan tamamen izole ederek sporcu kimliğinizin en erişilmez üst mertebesine adeta yüksek güçlü bir füzeyle sarsmasızca hızla ulaştırır."]

s10 = ["Bu yolda sadece güçlenmeyecek, aynı zamanda yılların getirdiği prangaları bedensel bir özgürlükle kıracaksınız.",
      "Gelişimi sadece aynaya bakarak değil, antrenmandaki odaklanmanız ve duruşunuzdaki o sarsılmaz güvenle ölçün.",
      "Nefesinizi egzersizin içine doğru şekilde entegre ettiğiniz an, zorlukların nasıl sihirli bir şekilde hafiflediğine inanamayacaksınız.",
      "Sağlıklı, bol pürüzsüz hareketli ve müzmin sakatlıklardan tamamen arınmış, yepyeni bir elit spor bilinciyle donanmış uzun yıllarınız daima olsun.",
      "Ömür boyu sahip olacağınız eşsiz tek tapu bu paha biçilmez beden, dışarıdan kirletmeden, temiz gıda ve ona son derece zekice tasarlanmış antrenmanlarla derin bir saygı sunun.",
      "Son söz: Sporun ta kendisini felsefi olarak anladığınızda aslında kendinizi özünüzden anlarsınız; işte bu yüzden, profesyonel vizyoner bir baş koçla olan çalışma sürecinizi ertelemeden bir an önce tam motivasyonla başlatın.",
      "Geriye dönüp yıllar sonrasında tüm bu çalışmalara huzurla arkadan baktığınızda, bugün üşenmeden atılan ve önemsiz gibi duran her bu küçük terli adımların okyanus büyüklüğünde ve çok çelik sağlam devasa bir biyolojik altyapı oluşturduğuna kendi gözlerinizle gururla şahit olacaksınız.",
      "Sizlere yeni spor ve aktif kalma hayatınızda, çelik kadar kalıcı bir harika iskelet esnekliği, sınır tanımayan beton gibi aşılmaz bir kardiyovasküler kalp dayanıklılığı ve sayısız bedensel, son derece devasa yüksek elit fonksiyonel ve mutlak başarılar dilerim."]

titles_pool = [
    "Cimnastik ve Atletik Performansın Bilinmeyenleri",
    "Merkez Bölgesi (Core) Kuvvetinin Derin Biyomekaniği",
    "Geleceğe Yatırım: İleri Seviye Vücut Kontrolü",
    "Esneklik ve Mobilite Arasındaki Karışık Çizgi",
    "Gücün Gerçek Kaynağı: İyi Toparlanma Stratejisi",
    "Kendi Vücut Kütlene Mutlak Şekilde Hükmetmek",
    "Vücut Ağırlığı Egzersizlerinden Maksimum Verim Almak",
    "Mental Dayanıklılığı Sporda Kalıcı Hale Getirmek",
    "Fitness Hurdalarını Çöpe Atın ve Fonksiyonelliğe Dönün",
    "Hatalı Hareket Paternlerinizi Yeniden Programlayın",
    "Sakatlıklardan Uzun Yıllar Boyunca Korunmanın Kuralları",
    "Dinamik Isınma İle Sinir Sistemini Anında Uyandırmak",
    "Amut (Handstand) Dengesinin Görünmeyen Dinamikleri",
    "Neden Uzman Bir Kişisel Antrenörle (PT) İlerlemelisiniz?",
    "Aşırı Yüklenme (Progressive Overload) Ne İşe Yarar?",
    "Uygulamalı Egzersiz Beslenmesindeki Sinsi Yanlışlar",
    "Antrenman Hacmi, Yoğunluğu ve Gelişimin Matematiği",
    "Hücresel Toparlanma Süreci: Dinlenmenin Gerçek Sırrı",
    "İrade Sınavı: Can Sıkan Plato Evrelerini Rahatça Atlatmak",
    "Doğal İnsan Hareketlerine Evrimsel ve Pratik Bir Yaklaşım",
    "Yüksek Şiddet (HIIT) Çalışmaları ve Laktat Eşiği Yönetimi",
    "Propriosepsiyon Zekası: Vücudun Mekanı Kusursuz Algılaması",
    "Sıkılaşma ve Kas Gelişiminde Metabolik Stres Faktörü",
    "Egzersiz Fizyolojisine Dair En Popüler Çürük Mitler",
    "Zihinsel Derin Odaklanma Sayesinde Tekrar Kalitesini Artırmak",
    "Tendon ve Bağ Dokularını Beton Gibi Güçlendirmenin Yolları",
    "Hareket Analizi İle Vücudunuzdaki Kör Noktaları Bulmak",
    "Fasyal Ağları Gerdirerek Hayati Kronik Ağrılardan Kurtulmak",
    "Fonksiyonel Kapasitenizi Günlük Başarınıza Doğrudan Aktarmak",
    "Kinetik Zincir Prensibi İle Patlayıcı Gücünüzü Konuşturmak",
    "Sirkadiyen Ritminizi Hormon Profillerinize Göre Eğitmek",
    "Mekanik Gerilimi Zirvede Tutan Üst İleri Seviye Taktikler",
    "Core Bölgenizi Sıradan Karın Egzersizlerinin Çok Ötesine Taşımak",
    "Gerçek Kondisyon Nedir ve Akciğer Kapasitesi Nasıl Büyütülür",
    "Hücrelerin İçinde Adeta Yeni Bir Performans Santrali Kurmak",
    "Esneklik Bariyerlerinizi Acı Çekmeden Adım Adım Nasıl Aşarsınız",
    "Kuvvette Devamlılık Stratejisiyle Spor Sınırlarını Tamamen Zorlayın",
    "Başarının Psikolojisi: Kendimize İnanmanın Somut Antrenmanı",
    "Tükenmişlik (Overtraining) Sendromuna Düşmeden Limitlerinizi Bulun",
    "Direnç Bantları İle Evinizin Tamamını Donanımlı Çelik Salona Çevirin",
    "Omuz Mobilitenizi Genişleterek Boyun Düzleşmesini Ortadan Kaldırın",
    "Denge Mekanizmasını Bozarak Yeni Kas Lifi Katkısı Sağlamak",
    "Ağırlık Merkezinin Sırlarını Açığa Çıkaran Gelişmiş Jimnastik Püfleri",
    "Duruş Bozukluklarını Kalıcı Şekilde Düzeltmenin Postüral Adımları",
    "Nöromusküler Bağlantıları Yalnızca Akıl Odaklanması Çatısıyla Kurmak",
    "Oksijen Tüketim Kapasitenizi Profesyonel Bir Atlet Seviyesine Korumak",
    "Haftada Sadece Üç Günle Nasıl Elit ve Fit Bir Noktaya Ulaşabilirsiniz",
    "Dinlenme Günlerini Temiz ve Katkılı Bir Arınma Kampına Benzetmek",
    "Hücresel Şişkinliğin Gizemleri ve Pump Etkisini Anlamanın Gerçekleri",
    "Eklemleri Etrafında Büyüyen Kusursuz Yastıkçıklara Karşı Direncini Ölç",
    "Sakatlık Sonrası Kesintisiz Antrenman Sürecinin Altın Geri Dönüş Rehberi",
    "Sıfırdan Gerçek Şampiyonluğa Giden Kusursuz Hedef Yönetimi Sırları"
]

def seed():
    print("Deleting all existing posts to remove HTML and setup the yearly pipeline...")
    BlogPost.objects.all().delete()
    
    # Start 10 weeks in the past so the blog instantly has 11 visible posts, 
    # and the remaining 41 posts are queued for the future!
    start_date = timezone.now() - timedelta(days=10*7)
    
    random.shuffle(titles_pool)
    sentence_arrays = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
    
    for i in range(52):
        title = titles_pool[i]
        
        # Pick 1 sentence from each part, generating exactly 10 coherent sentences per post
        content_sentences = []
        for s_arr in sentence_arrays:
            content_sentences.append(random.choice(s_arr))
        
        # Plain text space combining, completely without HTML!
        content = " ".join(content_sentences)
        
        # Each post steps 7 days out
        scheduled_date = start_date + timedelta(days=7*i)
        
        # Create and brutally override created_at
        post = BlogPost.objects.create(title=title, content=content)
        post.created_at = scheduled_date
        post.save()
        
    print(f"BINGO! Seeded 52 automated posts from {start_date.date()} up to {(start_date + timedelta(days=7*51)).date()}.")

if __name__ == "__main__":
    seed()
