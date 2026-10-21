# Praktikum Minggu 03 — Sinkronisasi pada Sistem Terdistribusi

**Nama:** Arsenius Kelvin Jemudin  
**NIM:** 255410015  
**Kelas:** IF-1  
**Program Studi:** Informatika  
**Universitas:** Universitas Teknologi Digital Indonesia

## 1. Tujuan Praktikum

Tujuan praktikum ini adalah:

1. Memahami pentingnya sinkronisasi waktu pada sistem terdistribusi.
2. Memahami cara kerja Vector Clock untuk mencatat urutan kejadian antarproses.
3. Mengamati perbedaan urutan eksekusi thread dan memahami masalah yang dapat muncul ketika beberapa thread berjalan bersamaan.
4. Memahami penyebab race condition dan cara mengatasinya menggunakan mekanisme lock.
5. Memahami proses terjadinya deadlock serta cara mengurangi risiko deadlock.
6. Memahami proses pemilihan pemimpin (*leader election*) dalam algoritma Raft.
7. Membuat dan menjalankan modul Python sederhana untuk Vector Clock dan simulasi Raft.

## Struktur Folder

```
03/
├── README.md
├── images/
│   ├── 01-sinkronisasi-waktu.png
│   ├── 02-kode-vector-clock-1.png
│   ├── 02-kode-vector-clock-2.png
│   ├── 02-kode-vector-clock-3.png
│   ├── 03-hasil-vector-clock.png
│   ├── 03b-kode-modul-vector-clock.png
│   ├── contoh_vector_clock.py.png
│   ├── hasil-modul-vector-clock.png
│   ├── 04-kode-multithreaded.png
│   ├── 05-hasil-multithreaded.png
│   ├── 06-kode-race-condition.png
│   ├── 07-hasil-race-condition.png
│   ├── 08-kode-race-condition-02.png
│   ├── 09-hasil-race-condition-02.png
│   ├── 10-kode-deadlock-01.png
│   ├── 11-hasil-deadlock-01.png
│   ├── 12-kode-deadlock-02-1.png
│   ├── 13-kode-deadlock-02-2.png
│   ├── 14-hasil-deadlock-02.png
│   ├── 15-kode-raft-1.png
│   ├── 16-kode-raft-2.png
│   ├── 17-kode-raft-3.png
│   ├── 18-kode-raft-4.png
│   ├── 19-kode-raft-module-1.png
│   ├── 20-kode-raft-module-2.png
│   ├── 21-kode-raft-module-3.png
│   ├── 22-kode-raft-simulation-1.png
│   ├── 23--hasil-raft-module-1.png
│   ├── 24-hasil-raft-module-2.png
│   ├── hasil-raft-1.png
│   ├── hasil-raft-2.png
│   ├── hasil-raft-3.png
│   ├── hasil-raft-4.png
│   ├── hasil-raft-5.png
│   ├── hasil-raft-6.png
│   ├── gambar-race-condition.jpg
│   ├── gambar-deadlock.jpg
│   └── gambar-raft.jpg
└── workspace-01/
    ├── vclocks.py
    ├── vector_clock.py
    ├── contoh_vector_clock.py
    ├── multithreaded-example.py
    ├── race-conditions-01.py
    ├── race-conditions-02.py
    ├── deadlock-01.py
    ├── deadlock-02.py
    ├── raft.py
    ├── raft_module.py
    └── raft_simulation.py
```

## 2. Dasar Teori

### 2.1 Sinkronisasi Waktu

Pada sistem terdistribusi, beberapa komputer atau proses dapat berjalan secara bersamaan dan berkomunikasi melalui jaringan. Setiap komputer memiliki jam masing-masing sehingga waktu yang ditampilkan tidak selalu sama. Sinkronisasi waktu diperlukan agar waktu antarperangkat lebih mendekati satu sama lain. Salah satu cara yang digunakan adalah Network Time Protocol (NTP), yaitu protokol untuk menyinkronkan waktu komputer dengan server waktu.

### 2.2 Vector Clock

Vector Clock merupakan metode untuk mencatat urutan kejadian pada sistem terdistribusi. Setiap proses memiliki vector yang berisi penghitung kejadian dari proses-proses yang terlibat. Nilainya bertambah ketika proses melakukan kejadian lokal dan diperbarui ketika menerima pesan dari proses lain. Vector Clock membantu menentukan apakah suatu kejadian terjadi sebelum kejadian lain (*happens-before*) atau apakah kedua kejadian tidak memiliki hubungan urutan yang dapat ditentukan.

### 2.3 Multithreading

Multithreading adalah teknik menjalankan beberapa thread dalam satu proses program. Thread dapat bekerja secara bersamaan sehingga program dapat menangani beberapa tugas tanpa harus menunggu satu tugas selesai terlebih dahulu. Namun, urutan eksekusi thread dapat berubah pada setiap program dijalankan karena penjadwalan sistem operasi.

### 2.4 Race Condition

Race condition terjadi ketika beberapa thread mengakses atau mengubah data bersama pada waktu yang berdekatan sehingga hasilnya bergantung pada urutan eksekusi. Contohnya adalah dua thread yang memeriksa saldo sebelum mengurangi saldo tersebut. Jika tidak ada pengamanan, keduanya dapat mengambil keputusan berdasarkan nilai saldo yang sama dan menyebabkan hasil yang tidak sesuai. Salah satu cara mengatasinya adalah menggunakan lock agar bagian program yang mengakses data bersama dijalankan secara bergantian.

### 2.5 Deadlock

Deadlock adalah kondisi ketika dua atau lebih thread saling menunggu sumber daya yang sedang dipegang oleh thread lain. Akibatnya, thread tidak dapat melanjutkan pekerjaannya. Deadlock dapat terjadi ketika beberapa lock diambil dalam urutan yang berbeda. Pengaturan urutan pengambilan lock dan pelepasan lock secara tepat dapat membantu menghindari kondisi tersebut.

### 2.6 Algoritma Raft

Raft merupakan algoritma konsensus yang digunakan untuk membantu beberapa node mencapai kesepakatan mengenai keadaan sistem. Dalam Raft, node dapat berstatus *follower*, *candidate*, atau *leader*. Leader bertugas menerima perintah dan mengoordinasikan pekerjaan dengan node lain. Jika follower tidak menerima heartbeat dalam waktu tertentu, node dapat memulai proses pemilihan leader. Praktikum ini menggunakan simulasi sederhana untuk mengamati perubahan status node, term, dan panjang log.

## 3. Implementasi dan Hasil Pengujian

### 3.1 Sinkronisasi Waktu

#### Implementasi

Praktikum sinkronisasi waktu dilakukan menggunakan aplikasi NetTime pada Windows. Aplikasi dihubungkan dengan server NTP untuk menyinkronkan waktu komputer.

#### Hasil Pengujian

Berdasarkan hasil pengujian, aplikasi NetTime menampilkan status *Time is synchronized*. Server yang digunakan adalah `0.nettime.pool.ntp.org`. Nilai offset yang ditampilkan sebesar -7 ms dan lag sebesar 33 ms. Status server menunjukkan *Good* dan tidak terdapat kesalahan pada proses sinkronisasi.

![Hasil Sinkronisasi Waktu](images/01-sinkronisasi-waktu.png)

#### Pembahasan

Hasil tersebut menunjukkan bahwa NetTime berhasil melakukan sinkronisasi dengan server waktu yang digunakan. Sinkronisasi waktu membantu sistem memiliki acuan waktu yang lebih konsisten, terutama ketika beberapa komputer atau proses perlu mencatat kejadian berdasarkan waktu.

Proses sinkronisasi pada NTP berjalan sebagai berikut:

1. Client mengirim permintaan ke server dan mencatat waktu kirim (**T1**).
2. Server mencatat waktu ia menerima permintaan (**T2**), lalu membalas dengan mencatat waktu kirim balasan (**T3**).
3. Client mencatat waktu ia menerima balasan (**T4**).
4. Dari keempat nilai tersebut client menghitung:
   - *offset* = ((T2 − T1) + (T3 − T4)) / 2, yaitu selisih jam client dengan jam server,
   - *delay* = (T4 − T1) − (T3 − T2), yaitu lama perjalanan data di jaringan.
5. Jam client dikoreksi sebesar nilai offset tersebut.

Pada percobaan ini, offset sebesar -7 ms menunjukkan jam laptop hanya selisih sangat kecil dari server, dan lag sebesar 33 ms menunjukkan waktu komunikasi dengan server yang dilaporkan aplikasi.

### 3.2 Vector Clock

#### Implementasi

Program `vclocks.py` dijalankan menggunakan Python. Program melibatkan tiga proses, yaitu P0, P1, dan P2. Setiap proses memiliki Vector Clock yang diperbarui ketika terjadi aktivitas lokal dan pertukaran pesan. Program juga memeriksa hubungan *happens-before* dan konkurensi antara vector yang dihasilkan.

#### Hasil Pengujian

Program berhasil dijalankan dan menghasilkan output berikut untuk pemeriksaan hubungan kejadian:

- `VC0 happens before VC1: True`
- `VC1 happens before VC0: False`
- `VC0 is concurrent with VC2: False`

#### Perhitungan Manual

Aturan Vector Clock yang dipakai:

- **Event lokal:** proses menambah 1 pada slot miliknya sendiri.
- **Kirim pesan:** tambah 1 pada slot sendiri, lalu kirim salinan vektor.
- **Terima pesan:** ambil nilai maksimum tiap slot dari vektor sendiri dan vektor kiriman, lalu tambah 1 pada slot sendiri.

| Langkah | Kejadian | P0 | P1 | P2 |
|---|---|---|---|---|
| 0 | Awal | [0,0,0] | [0,0,0] | [0,0,0] |
| 1 | P0 event lokal | [1,0,0] | [0,0,0] | [0,0,0] |
| 2 | P0 kirim pesan ke P1 | [2,0,0] | [0,0,0] | [0,0,0] |
| 3 | P1 terima: max([0,0,0],[2,0,0]) = [2,0,0], lalu +1 slot P1 | [2,0,0] | [2,1,0] | [0,0,0] |
| 4 | P2 event lokal | [2,0,0] | [2,1,0] | [0,0,1] |
| 5 | P1 kirim pesan ke P2 | [2,0,0] | [2,2,0] | [0,0,1] |
| 6 | P2 terima: max([0,0,1],[2,2,0]) = [2,2,1], lalu +1 slot P2 | [2,0,0] | [2,2,0] | [2,2,2] |

Hasil perhitungan manual sama dengan keluaran program: P0 = [2,0,0], P1 = [2,2,0], P2 = [2,2,2].

#### Pembahasan

Pada awal program, ketiga proses memiliki nilai clock `[0, 0, 0]`. Nilai tersebut berubah ketika proses melakukan aktivitas lokal dan bertukar pesan.

- `VC0 happens before VC1: True`. Vektor [2,0,0] dan [2,2,0]: semua elemen VC0 lebih kecil atau sama, dan ada yang lebih kecil. Artinya kejadian di P0 mendahului kejadian di P1, sesuai dengan pesan yang dikirim P0 dan diterima P1.
- `VC1 happens before VC0: False`. Elemen kedua VC1 (2) lebih besar dari VC0 (0), sehingga hubungan sebaliknya tidak terpenuhi.
- `VC0 is concurrent with VC2: False`. Walaupun P0 tidak mengirim pesan langsung ke P2, informasi dari P0 sampai ke P2 melalui P1. Maka VC0 [2,0,0] tetap mendahului VC2 [2,2,2], sehingga keduanya tidak konkuren. Jika P1 tidak pernah meneruskan pesan ke P2, hasilnya akan `True`.

![Kode Vector Clock Bagian 1](images/02-kode-vector-clock-1.png)

![Kode Vector Clock Bagian 2](images/02-kode-vector-clock-2.png)

![Kode Vector Clock Bagian 3](images/02-kode-vector-clock-3.png)

![Hasil Pengujian Vector Clock](images/03-hasil-vector-clock.png)

#### Pembuatan Modul Python Vector Clock

Class `VectorClock` dipisahkan ke dalam file `vector_clock.py` tanpa kode simulasi. File `contoh_vector_clock.py` dibuat untuk mengimpor modul tersebut dan menunjukkan cara memakainya dengan dua proses (P0 dan P1).

Contoh pemakaian:

```python
from vector_clock import VectorClock

a = VectorClock(num_processes=2, process_id=0)
b = VectorClock(num_processes=2, process_id=1)

a.increment()
b.increment()
print(a.is_concurrent(b))      # True, belum ada pesan antar proses

pesan = a.send_message()
b.receive_message(pesan)
print(a.happens_before(b))     # True, P0 mengirim pesan ke P1
```

Hasil pengujian modul:

```
Sebelum ada pesan:
P0: [1, 0]
P1: [0, 1]
A concurrent dengan B: True

Setelah P0 mengirim pesan ke P1:
P0: [2, 0]
P1: [2, 2]
A happens before B: True
B happens before A: False
A concurrent dengan B: False
```

Sebelum ada pesan, kedua proses concurrent karena vektornya [1,0] dan [0,1] tidak saling mendahului. Setelah P0 mengirim pesan, P1 menggabungkan vektor kiriman ([2,0]) dengan vektornya sendiri lalu menambah slot-nya, sehingga menjadi [2,2]. Sejak itu P0 mendahului P1.

![Kode Modul Vector Clock](images/03b-kode-modul-vector-clock.png)

![Kode Contoh Pemakaian Modul Vector Clock](images/contoh_vector_clock.py.png)

![Hasil Modul Vector Clock](images/hasil-modul-vector-clock.png)

### 3.3 Problem Without Synchronization

#### A. Multithreading

Program `multithreaded-example.py` menggunakan lima thread, yaitu A, B, C, D, dan E. Setiap thread menjalankan tugas dengan waktu tunggu lima detik. Program menggunakan `start()` untuk memulai thread dan `join()` untuk menunggu seluruh thread selesai.

Hasil pengujian menunjukkan bahwa urutan thread mulai dan selesai dapat berbeda pada setiap eksekusi. Hal ini terjadi karena penjadwalan thread dilakukan oleh sistem operasi. Meskipun seluruh thread menjalankan tugas yang sama, urutan tampilnya pesan tidak selalu tetap. Total waktu program sekitar lima detik, bukan dua puluh lima detik, karena kelima thread berjalan bersamaan. Karena urutan selesainya tidak bisa diprediksi, pola pikir sekuensial tidak bisa dipakai pada program konkuren.

![Kode Multithreading](images/04-kode-multithreaded.png)

![Hasil Multithreading Percobaan 1](images/05-hasil-multithreaded.png)

#### B. Race Condition

Program `race-conditions-01.py` menggunakan saldo awal Rp100 dan menjalankan dua thread yang masing-masing mencoba mengambil Rp80. Pada hasil pengujian, kedua thread berhasil melewati pemeriksaan saldo sebelum perubahan saldo dilakukan. Akibatnya, saldo menjadi Rp20 setelah pengambilan pertama dan kemudian menjadi -Rp60 setelah pengambilan kedua.

Hasil tersebut menunjukkan race condition karena pemeriksaan dan pengurangan saldo tidak dilindungi mekanisme sinkronisasi. Kedua thread dapat menggunakan nilai saldo awal yang sama ketika memutuskan apakah pengambilan dapat dilakukan. Urutan kejadiannya:

1. Thread 1 memeriksa `balance >= 80`: benar (saldo 100).
2. Sebelum Thread 1 mengurangi saldo (ada `sleep`), Thread 2 ikut memeriksa: juga benar (saldo masih 100).
3. Thread 1 mengurangi saldo: 100 − 80 = 20.
4. Thread 2 mengurangi saldo: 20 − 80 = **-60**.

Penyebabnya, pemeriksaan dan pengurangan saldo tidak dijalankan sebagai satu kesatuan yang tidak bisa disela (tidak atomik).

**Visualisasi race condition:**

![Gambar Tangan Race Condition](images/gambar-race-condition.jpg)

*Dua thread sama-sama mengecek saldo 100 sebelum ada yang mengurangi, sehingga saldo akhir menjadi -60.*

Pada program `race-conditions-02.py`, digunakan `threading.Lock()` untuk melindungi bagian kode yang memeriksa dan mengurangi saldo. Dengan mekanisme tersebut, satu thread menyelesaikan pemeriksaan dan pengurangan saldo sebelum thread lainnya memasuki bagian yang dilindungi. Thread kedua baru memeriksa setelah saldo menjadi Rp20, sehingga `20 >= 80` bernilai salah dan pengambilan tidak dilakukan. Hasilnya, hanya satu pengambilan sebesar Rp80 yang berhasil dan saldo akhir tetap Rp20.

![Kode Race Condition](images/06-kode-race-condition.png)

![Hasil Race Condition](images/07-hasil-race-condition.png)

![Kode Race Condition dengan Lock](images/08-kode-race-condition-02.png)

![Hasil Race Condition dengan Lock](images/09-hasil-race-condition-02.png)

#### C. Deadlock

Pada program `deadlock-01.py`, thread pertama mengambil `lock_a` dan menunggu `lock_b`, sedangkan thread kedua mengambil `lock_b` dan menunggu `lock_a`. Kedua thread akhirnya saling menunggu karena lock yang dibutuhkan masih dipegang oleh thread lain. Kondisi ini menyebabkan program berhenti melanjutkan proses dan menunjukkan terjadinya deadlock. Program harus dihentikan manual dengan `Ctrl+C`.

Deadlock ini terjadi karena empat kondisi terpenuhi sekaligus: *mutual exclusion* (satu lock hanya boleh dipegang satu thread), *hold and wait* (thread memegang satu lock sambil menunggu lock lain), *no preemption* (lock tidak bisa direbut paksa), dan *circular wait* (T1 menunggu T2 dan T2 menunggu T1).

**Visualisasi deadlock:**

![Gambar Tangan Deadlock](images/gambar-deadlock.jpg)

*Thread 1 memegang Lock A dan menunggu Lock B, sedangkan Thread 2 memegang Lock B dan menunggu Lock A, sehingga keduanya saling menunggu.*

Pada program `deadlock-02.py`, lock dilepaskan sebelum thread mencoba mengambil lock berikutnya. Program juga menggunakan batas waktu saat mengambil lock (`timeout=5`). Hasil pengujian menunjukkan bahwa kedua thread dapat memperoleh lock secara bergantian dan program menampilkan `Execution Finished`. Deadlock tidak terjadi karena tidak ada thread yang memegang satu lock sambil menunggu lock lainnya (tidak ada *hold and wait* maupun *circular wait*), dan batas waktu mencegah thread menunggu selamanya.

![Kode Deadlock](images/10-kode-deadlock-01.png)

![Hasil Deadlock](images/11-hasil-deadlock-01.png)

![Kode Deadlock yang Diperbaiki Bagian 1](images/12-kode-deadlock-02-1.png)

![Kode Deadlock yang Diperbaiki Bagian 2](images/13-kode-deadlock-02-2.png)

![Hasil Deadlock yang Diperbaiki](images/14-hasil-deadlock-02.png)

### 3.4 Raft Consensus

#### A. Implementasi Program Raft

Program `raft.py` dijalankan menggunakan Python untuk mengamati proses pemilihan leader pada beberapa node. Program menampilkan status node, term, dan panjang log selama simulasi. Status node dapat berubah ketika terjadi proses pemilihan leader atau ketika node menerima heartbeat dari leader.

#### B. Hasil Pengujian Program Raft

Berdasarkan hasil pengujian program awal, Node 2 terpilih sebagai leader pada salah satu tahap simulasi, sedangkan node lainnya berstatus follower. Selama simulasi, leader menambahkan perintah ke dalam log secara berkala. Hal tersebut ditunjukkan oleh bertambahnya panjang log pada node leader.

#### C. Pembahasan Program Raft

Alur pemilihan leader pada simulasi ini:

1. Semua node (1, 2, 3) mulai sebagai **follower** dengan term 0 dan *election timeout* acak antara 1 sampai 2 detik.
2. Node yang timeout-nya habis lebih dulu, karena belum menerima heartbeat, menjadi **candidate**, menaikkan term (+1), dan memilih dirinya sendiri.
3. Candidate meminta suara dari node lain. Jika suara yang didapat lebih dari separuh jumlah node, ia menjadi **leader**. Pada simulasi ini node lain dianggap selalu memberi suara.
4. Leader mengirim heartbeat agar node lain tetap menjadi follower, dan menambahkan perintah (`command-N`) ke log secara berkala.
5. Jika heartbeat berhenti, follower akan timeout lagi dan pemilihan baru dimulai dengan term yang lebih tinggi.

Hasil pengujian memperlihatkan gambaran dasar proses pemilihan leader dan perubahan status node dalam sistem terdistribusi. Node yang berstatus leader dapat menambahkan perintah ke dalam log, sementara node lain berstatus follower. Simulasi ini membantu memahami peran leader dalam koordinasi antar-node, walaupun belum menerapkan seluruh mekanisme konsensus Raft yang sebenarnya.

**Visualisasi pemilihan leader pada Raft:**

![Gambar Tangan Raft](images/gambar-raft.jpg)

*Follower yang timeout menjadi candidate, menang vote menjadi leader, dan kembali menjadi follower jika ada term yang lebih tinggi.*

![Kode Raft Bagian 1](images/15-kode-raft-1.png)

![Kode Raft Bagian 2](images/16-kode-raft-2.png)

![Kode Raft Bagian 3](images/17-kode-raft-3.png)

![Kode Raft Bagian 4](images/18-kode-raft-4.png)

![Hasil Raft Bagian 1](images/hasil-raft-1.png)

![Hasil Raft Bagian 2](images/hasil-raft-2.png)

![Hasil Raft Bagian 3](images/hasil-raft-3.png)

![Hasil Raft Bagian 4](images/hasil-raft-4.png)

![Hasil Raft Bagian 5](images/hasil-raft-5.png)

![Hasil Raft Bagian 6](images/hasil-raft-6.png)

#### D. Pembuatan Modul Python Raft

Pada tahap ini, class `State` dan `RaftNode` dipisahkan ke dalam file `raft_module.py`. Selanjutnya, file `raft_simulation.py` dibuat untuk mengimpor modul tersebut dan menjalankan simulasi selama 20 langkah. Pemisahan ini membuat kode class dan kode simulasi berada pada file yang berbeda sehingga lebih mudah dibaca dan digunakan kembali.

![Kode Raft Module Bagian 1](images/19-kode-raft-module-1.png)

![Kode Raft Module Bagian 2](images/20-kode-raft-module-2.png)

![Kode Raft Module Bagian 3](images/21-kode-raft-module-3.png)

![Kode Raft Simulation](images/22-kode-raft-simulation-1.png)

#### E. Hasil Pengujian Modul Raft

Pada simulasi menggunakan modul Python, Node 1 terpilih menjadi leader pada term 1, sedangkan Node 2 dan Node 3 menjadi follower. Leader menambahkan perintah `command-5`, `command-10`, dan `command-15`. Pada akhir simulasi, panjang log Node 1 menjadi 3, sedangkan panjang log Node 2 dan Node 3 tetap 0.

![Hasil Raft Module Bagian 1](images/23--hasil-raft-module-1.png)

![Hasil Raft Module Bagian 2](images/24-hasil-raft-module-2.png)

#### F. Pembahasan Modul Raft

Hasil simulasi menunjukkan bahwa pemisahan kode ke dalam modul dapat digunakan untuk menjalankan simulasi melalui file yang berbeda. Perbedaan hasil pemilihan leader antara program awal dan simulasi modul dapat terjadi karena mekanisme simulasi yang digunakan tidak sama persis (timeout bersifat acak). Implementasi ini masih berupa penyederhanaan: pemungutan suara diasumsikan berhasil tanpa pertukaran pesan RequestVote yang sebenarnya, dan log belum direplikasi ke follower. Oleh karena itu, program ini digunakan untuk mempelajari konsep dasar Raft, bukan sebagai implementasi Raft lengkap.

## 4. Kesimpulan

Berdasarkan praktikum yang telah dilakukan, sinkronisasi waktu membantu komputer menggunakan acuan waktu yang lebih konsisten. Vector Clock dapat digunakan untuk mempelajari urutan kejadian pada sistem terdistribusi tanpa bergantung pada jam fisik. Pengujian multithreading menunjukkan bahwa urutan eksekusi thread dapat berubah, sedangkan race condition dapat menyebabkan perubahan data yang tidak sesuai jika tidak dilindungi mekanisme sinkronisasi. Pengujian deadlock memperlihatkan bahwa penggunaan lock yang tidak tepat dapat membuat thread saling menunggu, sementara pengelolaan lock dan batas waktu dapat membantu mengurangi risiko tersebut.

Pada bagian Raft, simulasi memperlihatkan perubahan status node, pemilihan leader, dan penambahan perintah ke dalam log. Pemisahan class ke dalam modul Python, baik untuk Vector Clock maupun Raft, membuat kode lebih terstruktur. Namun, simulasi Raft yang dibuat masih sederhana dan belum menerapkan seluruh mekanisme konsensus serta replikasi log seperti pada sistem Raft sebenarnya.

## 5. Referensi

1. Materi Praktikum Sistem Terdistribusi dan Terdesentralisasi, Modul 03: Sinkronisasi pada Sistem Terdistribusi.
2. Dokumentasi Python, *threading — Thread-based parallelism*. https://docs.python.org/3/library/threading.html
3. Dokumentasi Python, *enum — Support for enumerations*. https://docs.python.org/3/library/enum.html
4. Mills, D., et al. *Network Time Protocol Version 4: Protocol and Algorithms Specification*. RFC 5905. https://www.rfc-editor.org/rfc/rfc5905
5. Ongaro, D., & Ousterhout, J. (2014). *In Search of an Understandable Consensus Algorithm (Extended Version)*. USENIX Annual Technical Conference.