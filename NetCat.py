import sys
import socket
import getopt
import threading
import subprocess

#Global Değişkenlerin Tanımlanması.

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


# Ana fonksiyonu oluşturuyoruz diğer tüm fonksiyonlardanda sorumlu.

def Kitapcik():

    print("BHP Net Tool")
    print("")
    print("Usage: NetCat.py -t target_host -p port")
    print("-l --listen - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run - execute the given file upon ¬ reciving a connection")
    print("-c --command - initialize a command shell")
    print("-u --upload=destination - upon receiving connection upload a file and write to [destination]")
    print("")
    print("")
    print("Examples: ")
    #Uygulamanın Target ve portu belirlenir dinleme açılır ve Sonuçlar komut satırına yazdırılır
    print("NetCat.py -t 192.168.0.1 -p 5555 -l -c")
    #Target.exe ye Alınan satırlar yüklenir.
    print("NetCat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    #Dinledikten sonra passwd Çalıştılır 
    print("NetCat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    #İlk önceterminale yazdırır ardından Uygulamayı çalıştırır.
    print("echo 'ABCDEFGHI' | ./NetCat.py -t 192.168.11.12 -p 135")
    sys.exit(0)



def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        Kitapcik()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help","listen","execute=","target=","port=","command","upload="])
    except getopt.GetoptError as err:
        print(str(err))
        Kitapcik()

    
    for o,a in opts:
        if o in ("-h","--help"):
            Kitapcik()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e","--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o  in ("-p", "--port"):
            port = int(a)
        else: # Hata durumunda programdan çıkış yapılması daha iyi olur.
            assert False,"Unhandled Option "
    if not listen and len(target) and port > 0:

     buffer = sys.stdin.read().encode()

     client_sender(buffer)
    
    if listen:
      server_loop()

def client_sender(buffer):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        client.connect((target,port))

        if len(buffer):
            client.send(buffer)

        while True:

            recv_len = 1
            response = b""

            while recv_len:

                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print(response.decode('utf-8', errors='ignore'), end="") # Sunucunun cevabını ekrana bas.

            buffer = input("") # Kullanıcıdan klavye girişi bekle.
            buffer += "\n" # Enter tuşuna basıldığını belirtmek için satır sonu ekle.


            client.send(buffer.encode()) # Yazdığın komutu sunucuya gönder.
    
    except:

        print("[*] Exception! Exiting.")

        client.close() #Bağlantı koparsa veya sunucu kapanırsa programın çökmemesi için try-except bloğu ile hatayı yakalayıp programı kibarca kapatıyorsun


def server_loop():
    global target 

    # Eğer hedef belirtilmemişse tüm arayüzlerde dinle

    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target,port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # Yeni bir iş parçacığı başlat ve client_handler fonksiyonunu çağır
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def run_command(command):
    # Komutun sonundaki yeni satır karakterini kaldır

    command = command.rstrip()

    #Komutu okur ve çıktıyı alır
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    
    except:
        output = b"Komutu calistirma Basarisiz oldu.\r\n"
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command 

    if len(upload_destination):
        client_socket.send(b"Dosya modu hazir. Metni yaz ve Enter'a bas.\n")
        file_buffer = b""

        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            
            file_buffer += data
        
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            client_socket.send(f"Dosya Başarıyla Kaydedildi: {upload_destination}\r\n".encode())

        except:
            client_socket.send(f"Dosya Kaydetme işlemi başarısız oldu: {upload_destination}\r\n".encode())


    

    if len(execute):
        output = run_command(execute)

        client_socket.send(output)

    if command:
        
        while True:
            
            client_socket.send(b"<BHP:#> ")
            
            cmd_buffer = b""

            while b"\n" not in cmd_buffer:
                
                cmd_buffer += client_socket.recv(1024)
            
            response = run_command(cmd_buffer.decode('utf-8', errors='ignore'))

            client_socket.send(response)

if __name__ == '__main__':
    main()
