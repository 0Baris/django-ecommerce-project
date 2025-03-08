# 🛒 Django E-commerce Project

![localhost_8000_ (1)](https://github.com/user-attachments/assets/38e73756-973a-479d-9b6a-965686a4b1c9)


## 📦 İçindekiler

- [📖 Proje Hakkında](#-proje-hakkında)
- [✨ Özellikler](#-özellikler)
- [🛠️ Teknolojiler](#-teknolojiler)
- [⚙️ Kurulum ve Başlangıç](#-adım-adım-kurulum-docker-ile)
- [📚 Kullanım](#-kullanım)
- [📂 Proje Yapısı](#-proje-yapısı)
- [🤝 Katkıda Bulunma](#-katkıda-bulunma)
- [📜 Lisans](#-lisans)
- [📞 İletişim](#-iletişim)

## 📖 Proje Hakkında

Django E-commerce Projesi, kullanıcıların ürünleri görüntüleyip sepetlerine ekleyebilecekleri, adres yönetimi yapabilecekleri ve güvenli bir şekilde ödeme gerçekleştirebilecekleri tam teşekküllü bir çevrimiçi alışveriş platformudur. Proje, modern web geliştirme en iyi uygulamalarını takip ederek kullanıcı dostu bir arayüz ve sağlam bir yapı sunmayı hedeflemektedir.

## ✨ Özellikler

- **Kullanıcı Kimlik Doğrulama:** Kayıt olma, giriş yapma ve profil yönetimi.
- **Adres Yönetimi:** Kullanıcıların birden fazla adres ekleyip yönetebilmesi.
- **Ürün Kataloğu:** Kategorilere göre düzenlenmiş ürün listesi ve detay sayfaları.
- **Sepet İşlevselliği:** Ürünleri sepete ekleme, miktarını değiştirme ve indirim kodu özelliklerini içerir.
- **Satın Alma ve Ödeme:** Güvenli ödeme süreci ve sipariş onayı.
- **Stok Yönetimi:** Ürün stok seviyelerinin kontrolü ve güncellenmesi.
- **Responsive Tasarım:** Mobil ve masaüstü cihazlarda uyumlu kullanıcı arayüzü.
- **ADMIN Panel:** Ürün, kategori ve sipariş yönetimi için Django admin paneli entegrasyonu. İndirim kodu yönetimi ve kod komisyon görüntülenmesi.

## 🛠️ Teknolojiler

- **Backend:**
  - Python 3.x
  - Django 4.x
- **Frontend:**
  - HTML5
  - CSS3
  - Bootstrap 5
  - JavaScript (ES6+)
- **Veritabanı:**
  - PostgreSQL / SQLite (geliştirme ve prodüksiyon için)
- **Diğer:**
  - Git
  - GitHub
  - Pillow (Görüntü İşleme için)
  - Whitenoise 

## ⚙️ Kurulum ve Başlangıç

### 🚀 Adım Adım Kurulum (Docker ile)

1. **Proje Deposu Klonlama:**

    ```bash
    git clone https://github.com/0Baris/django-ecommerce-project.git
    cd django-ecommerce
    ```

2. **Docker ve Docker Compose Kurulumu:**

    Docker ve Docker Compose'un sisteminizde kurulu olduğundan emin olun. Kurulum için aşağıdaki bağlantıları kullanabilirsiniz:
    - [Docker Kurulumu](https://docs.docker.com/get-docker/)
    - [Docker Compose Kurulumu](https://docs.docker.com/compose/install/)

3. **.env Dosyasını Oluşturma ve Yapılandırma:**

    Projenin kök dizininde `.env` dosyası oluşturun ve aşağıdaki ortam değişkenlerini ekleyin:

    ```env
    SECRET_KEY=<your_secret_key>
    DEBUG=False
    ALLOWED_HOSTS=localhost,127.0.0.1

    # Veritabanı Ayarları
    DATABASE_URL=postgres://<db_user>:<db_password>@localhost:5432/<db_name>

    # E-posta Ayarları
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=<your_email>
    EMAIL_HOST_PASSWORD=<your_email_password>
    ```

    `<your_secret_key>`, `<db_user>`, `<db_password>`, `<db_name>`, `<your_email>`, ve `<your_email_password>` değerlerini kendi bilgilerinize göre doldurun.

4. **Docker Konteynerlerini Başlatma:**

    ```bash
    docker-compose up --build
    ```

    Bu komut, gerekli Docker konteynerlerini oluşturacak ve başlatacaktır.

5. **Veritabanı Migrasyonlarını Uygulama:**

    Ayrı bir terminal penceresi açarak aşağıdaki komutu çalıştırın:

    ```bash
    docker-compose exec web python manage.py migrate
    ```

    Bu komut, veritabanı tablolarını oluşturacaktır.

6. **Süper Kullanıcı Oluşturma:**

    Ayrı bir terminal penceresi açarak aşağıdaki komutu çalıştırın:

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

    Takip eden adımları doldurarak yönetici hesabınızı oluşturun.

7. **Geliştirme Sunucusunu Başlatma:**

    Docker Compose ile başlatılan sunucu zaten çalışıyor olacaktır. Tarayıcıda `http://127.0.0.1:8000/` adresine giderek projeyi görüntüleyebilirsiniz.

Docker ile kurulum tamamlandı! Artık projeyi Docker konteynerleri içinde çalıştırabilirsiniz.

## 📚 Kullanım

Proje başlatıldıktan sonra aşağıdaki özellikleri kullanabilirsiniz:

1. **Kayıt Olma ve Giriş Yapma:**
   - Sağ üst köşede bulunan "Kayıt Ol" veya "Giriş Yap" butonları aracılığıyla kullanıcı hesabı oluşturabilir ve giriş yapabilirsiniz.

2. **Adres Yönetimi:**
   - Profil sayfanızda mevcut adreslerinizi görüntüleyebilir, yeni adres ekleyebilir veya mevcut adresleri düzenleyebilirsiniz.

3. **Ürünleri Görüntüleme:**
   - Anasayfada listelenen ürünleri inceleyebilir, detay sayfalarına giderek daha fazla bilgi edinebilirsiniz.
    
4. **Sepet Özellikleri:** 
    - Ürünleri sepete ekleyebilir, sepetinizi görüntüleyebilir, miktarını değiştirebilir ve indirim kodu ekleyebilirsiniz.

5. **Satın Alma ve Ödeme:**
   - Sepetinizi onaylayarak ödeme sürecine geçebilir ve siparişinizi tamamlayabilirsiniz.

## 🤝 Katkıda Bulunma

Katkıda bulunmak isteyen herkes hoş geldiniz! Proje adına katılmak için aşağıdaki adımları izleyebilirsiniz:

1. **Fork'layın:** Projenin GitHub sayfasını forkladıktan sonra kendi bilgisayarınıza klonlayın.

2. **Yeni Bir Dal Oluşturun:**

    ```bash
    git checkout -b feature/özellik_adı
    ```

3. **Değişiklikleri Yapın ve Commit Edin:**

    ```bash
    git add .
    git commit -m "Özellik: Yeni özellik eklendi"
    ```

4. **Dalınızı Push Edin:**

    ```bash
    git push origin feature/özellik_adı
    ```

5. **Pull Request Oluşturun:** GitHub üzerinden orijinal depo için pull request açın ve değişikliklerinizi açıklayın.

**Not:** Kod katkılarınızın temiz, iyi yapılandırılmış ve proje stil rehberine uygun olmasına dikkat edin. Testler ekleyerek katkıda bulunmanız büyük takdir toplayacaktır.

## 📜 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - LICENSE dosyasını inceleyebilirsiniz.

## 📞 İletişim

Projeyle ilgili sorularınız, önerileriniz veya geri bildirimleriniz için benimle iletişime geçebilirsiniz:

- **E-posta:** bariscem@proton.me
- **LinkedIn:** [Barış Cem Ant](https://www.linkedin.com/in/baris-cem-ant/)
- **GitHub:** [Barış Cem Ant](https://github.com/0Baris)

---

> **Not:** Bu proje, eğitim amaçlı geliştirilmiş olup gerçek bir ürünün yerini almamaktadır. Güvenlik ve performans iyileştirmeleri için her zaman profesyonel danışmanlık almanız önerilir.
