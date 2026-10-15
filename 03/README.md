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
7. Membuat dan menjalankan modul Python sederhana untuk simulasi Raft.

## 2. Dasar Teori

## 2.1 Sinkronisasi Waktu

Pada sistem terdistribusi, beberapa komputer atau proses dapat berjalan secara bersamaan dan berkomunikasi melalui jaringan. Setiap komputer memiliki jam masing-masing sehingga waktu yang ditampilkan tidak selalu sama. Sinkronisasi waktu diperlukan agar waktu antarperangkat lebih mendekati satu sama lain. Salah satu cara yang digunakan adalah Network Time Protocol (NTP), yaitu protokol untuk menyinkronkan waktu komputer dengan server waktu.

## 2.2 Vector Clock

Vector Clock merupakan metode untuk mencatat urutan kejadian pada sistem terdistribusi. Setiap proses memiliki vector yang berisi penghitung kejadian dari proses-proses yang terlibat. Nilainya bertambah ketika proses melakukan kejadian lokal dan diperbarui ketika menerima pesan dari proses lain. Vector Clock membantu menentukan apakah suatu kejadian terjadi sebelum kejadian lain (*happens-before*) atau apakah kedua kejadian tidak memiliki hubungan urutan yang dapat ditentukan.

## 2.3 Multithreading

Multithreading adalah teknik menjalankan beberapa thread dalam satu proses program. Thread dapat bekerja secara bersamaan sehingga program dapat menangani beberapa tugas tanpa harus menunggu satu tugas selesai terlebih dahulu. Namun, urutan eksekusi thread dapat berubah pada setiap program dijalankan karena penjadwalan sistem operasi.

## 2.4 Race Condition

Race condition terjadi ketika beberapa thread mengakses atau mengubah data bersama pada waktu yang berdekatan sehingga hasilnya bergantung pada urutan eksekusi. Contohnya adalah dua thread yang memeriksa saldo sebelum mengurangi saldo tersebut. Jika tidak ada pengamanan, keduanya dapat mengambil keputusan berdasarkan nilai saldo yang sama dan menyebabkan hasil yang tidak sesuai. Salah satu cara mengatasinya adalah menggunakan lock agar bagian program yang mengakses data bersama dijalankan secara bergantian.

## 2.5 Deadlock

Deadlock adalah kondisi ketika dua atau lebih thread saling menunggu sumber daya yang sedang dipegang oleh thread lain. Akibatnya, thread tidak dapat melanjutkan pekerjaannya. Deadlock dapat terjadi ketika beberapa lock diambil dalam urutan yang berbeda. Pengaturan urutan pengambilan lock dan pelepasan lock secara tepat dapat membantu menghindari kondisi tersebut.

## 2.6 Algoritma Raft

Raft merupakan algoritma konsensus yang digunakan untuk membantu beberapa node mencapai kesepakatan mengenai keadaan sistem. Dalam Raft, node dapat berstatus *follower*, *candidate*, atau *leader*. Leader bertugas menerima perintah dan mengoordinasikan pekerjaan dengan node lain. Jika follower tidak menerima heartbeat dalam waktu tertentu, node dapat memulai proses pemilihan leader. Praktikum ini menggunakan simulasi sederhana untuk mengamati perubahan status node, term, dan panjang log.

## 3. Implementasi dan Hasil Pengujian

## 3.1 Sinkronisasi Waktu

## Implementasi

Praktikum sinkronisasi waktu dilakukan menggunakan aplikasi NetTime pada Windows. Aplikasi dihubungkan dengan server NTP untuk menyinkronkan waktu komputer.

## Hasil Pengujian

Berdasarkan hasil pengujian, aplikasi NetTime menampilkan status *Time is synchronized*. Server yang digunakan adalah `0.nettime.pool.ntp.org`. Nilai offset yang ditampilkan sebesar -7 ms dan lag sebesar 33 ms. Status server menunjukkan *Good* dan tidak terdapat kesalahan pada proses sinkronisasi.
![Hasil Sinkronisasi Waktu](images/01-sinkronisasi-waktu.png)

## Pembahasan

Hasil tersebut menunjukkan bahwa NetTime berhasil melakukan sinkronisasi dengan server waktu yang digunakan. Nilai offset menunjukkan selisih waktu yang tercatat oleh aplikasi, sedangkan lag menunjukkan waktu komunikasi yang dilaporkan aplikasi. Sinkronisasi waktu membantu sistem memiliki acuan waktu yang lebih konsisten, terutama ketika beberapa komputer atau proses perlu mencatat kejadian berdasarkan waktu.

## 3.2 Vector Clock

## Implementasi

Program `vclocks.py` dijalankan menggunakan Python. Program melibatkan tiga proses, yaitu P0, P1, dan P2. Setiap proses memiliki Vector Clock yang diperbarui ketika terjadi aktivitas lokal dan pertukaran pesan. Program juga memeriksa hubungan *happens-before* dan konkurensi antara vector yang dihasilkan.

## Hasil Pengujian

Program berhasil dijalankan dan menghasilkan output berikut untuk pemeriksaan hubungan kejadian:

- `VC0 happens before VC1: True`
- `VC1 happens before VC0: False`
- `VC0 is concurrent with VC2: False`

## Pembahasan

Pada awal program, ketiga proses memiliki nilai clock `[0, 0, 0]`. Nilai tersebut berubah ketika proses melakukan aktivitas lokal dan bertukar pesan. Hasil `VC0 happens before VC1: True` menunjukkan bahwa menurut fungsi pemeriksaan pada program, VC0 memiliki hubungan urutan sebelum VC1. Sebaliknya, `VC1 happens before VC0: False` menunjukkan bahwa hubungan sebaliknya tidak terpenuhi.

Pemeriksaan `VC0 is concurrent with VC2: False` menunjukkan bahwa fungsi yang digunakan program tidak menganggap kedua vector tersebut sebagai kejadian yang konkuren. Hasil ini mengikuti urutan kejadian dan implementasi pemeriksaan dalam program.

![Kode Vector Clock Bagian 1](images/02-kode-vector-clock-1.png)

![Kode Vector Clock Bagian 2](images/02-kode-vector-clock-2.png)

![Kode Vector Clock Bagian 3](images/02-kode-vector-clock-3.png)

![Hasil Pengujian Vector Clock](images/03-hasil-vector-clock.png)

## 3.3 Problem Without Synchronization

## A. Multithreading

Program `multithreaded-example.py` menggunakan lima thread, yaitu A, B, C, D, dan E. Setiap thread menjalankan tugas dengan waktu tunggu lima detik. Program menggunakan `start()` untuk memulai thread dan `join()` untuk menunggu seluruh thread selesai.

Hasil pengujian menunjukkan bahwa urutan thread mulai dan selesai dapat berbeda pada setiap eksekusi. Hal ini terjadi karena penjadwalan thread dilakukan oleh sistem operasi. Meskipun seluruh thread menjalankan tugas yang sama, urutan tampilnya pesan tidak selalu tetap.

![Kode Multithreading](images/04-kode-multithreaded.png)

![Hasil Multithreading](images/05-hasil-multithreaded.png)

## B. Race Condition

Program `race-conditions-01.py` menggunakan saldo awal Rp100 dan menjalankan dua thread yang masing-masing mencoba mengambil Rp80. Pada hasil pengujian, kedua thread berhasil melewati pemeriksaan saldo sebelum perubahan saldo dilakukan. Akibatnya, saldo menjadi Rp20 setelah pengambilan pertama dan kemudian menjadi -Rp60 setelah pengambilan kedua.

Hasil tersebut menunjukkan race condition karena pemeriksaan dan pengurangan saldo tidak dilindungi mekanisme sinkronisasi. Kedua thread dapat menggunakan nilai saldo awal yang sama ketika memutuskan apakah pengambilan dapat dilakukan.

Pada program `race-conditions-02.py`, digunakan `threading.Lock()` untuk melindungi bagian kode yang memeriksa dan mengurangi saldo. Dengan mekanisme tersebut, satu thread menyelesaikan pemeriksaan dan pengurangan saldo sebelum thread lainnya memasuki bagian yang dilindungi. Hasilnya, hanya satu pengambilan sebesar Rp80 yang berhasil dan saldo akhir tetap Rp20.

![Kode Race Condition](images/06-kode-race-condition.png)

![Hasil Race Condition](images/07-hasil-race-condition.png)

![Kode Race Condition dengan Lock](images/08-kode-race-condition-02.png)

![Hasil Race Condition dengan Lock](images/09-hasil-race-condition-02.png)

## C. Deadlock

Pada program `deadlock-01.py`, thread pertama mengambil `lock_a` dan menunggu `lock_b`, sedangkan thread kedua mengambil `lock_b` dan menunggu `lock_a`. Kedua thread akhirnya saling menunggu karena lock yang dibutuhkan masih dipegang oleh thread lain. Kondisi ini menyebabkan program berhenti melanjutkan proses dan menunjukkan terjadinya deadlock.

Pada program `deadlock-02.py`, lock dilepaskan sebelum thread mencoba mengambil lock berikutnya. Program juga menggunakan batas waktu saat mengambil lock. Hasil pengujian menunjukkan bahwa kedua thread dapat memperoleh lock secara bergantian dan program menampilkan `Execution Finished`. Perubahan tersebut mengurangi kemungkinan kedua thread saling menunggu dalam kondisi deadlock seperti pada program pertama.

![Kode Deadlock](images/10-kode-deadlock-01.png)

![Hasil Deadlock](images/11-hasil-deadlock-01.png)

![Kode Deadlock yang Diperbaiki Bagian 1](images/12-kode-deadlock-02-1.png)

![Kode Deadlock yang Diperbaiki Bagian 2](images/13-kode-deadlock-02-2.png)

![Hasil Deadlock yang Diperbaiki](images/14-hasil-deadlock-02.png)

## 3.4 Raft Consensus

## A. Implementasi Program Raft

Program `raft.py` dijalankan menggunakan Python untuk mengamati proses pemilihan leader pada beberapa node. Program menampilkan status node, term, dan panjang log selama simulasi. Status node dapat berubah ketika terjadi proses pemilihan leader atau ketika node menerima heartbeat dari leader.

## B. Hasil Pengujian Program Raft

Berdasarkan hasil pengujian program awal, Node 2 terpilih sebagai leader pada salah satu tahap simulasi, sedangkan node lainnya berstatus follower. Selama simulasi, leader menambahkan perintah ke dalam log secara berkala. Hal tersebut ditunjukkan oleh bertambahnya panjang log pada node leader.

## C. Pembahasan Program Raft

Hasil pengujian memperlihatkan gambaran dasar proses pemilihan leader dan perubahan status node dalam sistem terdistribusi. Node yang berstatus leader dapat menambahkan perintah ke dalam log, sementara node lain berstatus follower. Simulasi ini membantu memahami peran leader dalam koordinasi antar-node, walaupun belum menerapkan seluruh mekanisme konsensus Raft yang sebenarnya.

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

## D. Pembuatan Modul Python Raft

Pada tahap ini, class `State` dan `RaftNode` dipisahkan ke dalam file `raft_module.py`. Selanjutnya, file `raft_simulation.py` dibuat untuk mengimpor modul tersebut dan menjalankan simulasi selama 20 langkah. Pemisahan ini membuat kode class dan kode simulasi berada pada file yang berbeda sehingga lebih mudah dibaca dan digunakan kembali.

## E. Hasil Pengujian Modul Raft

Pada simulasi menggunakan modul Python, Node 1 terpilih menjadi leader pada term 1, sedangkan Node 2 dan Node 3 menjadi follower. Leader menambahkan perintah `command-5`, `command-10`, dan `command-15`. Pada akhir simulasi, panjang log Node 1 menjadi 3, sedangkan panjang log Node 2 dan Node 3 tetap 0.

## F. Pembahasan Modul Raft

Hasil simulasi menunjukkan bahwa pemisahan kode ke dalam modul dapat digunakan untuk menjalankan simulasi melalui file yang berbeda. Perbedaan hasil pemilihan leader antara program awal dan simulasi modul dapat terjadi karena mekanisme simulasi yang digunakan tidak sama persis. Implementasi ini masih berupa penyederhanaan: pemungutan suara diasumsikan berhasil tanpa pertukaran pesan RequestVote yang sebenarnya, dan log belum direplikasi ke follower. Oleh karena itu, program ini digunakan untuk mempelajari konsep dasar Raft, bukan sebagai implementasi Raft lengkap.

## 4. Kesimpulan

Berdasarkan praktikum yang telah dilakukan, sinkronisasi waktu membantu komputer menggunakan acuan waktu yang lebih konsisten. Vector Clock dapat digunakan untuk mempelajari urutan kejadian pada sistem terdistribusi. Pengujian multithreading menunjukkan bahwa urutan eksekusi thread dapat berubah, sedangkan race condition dapat menyebabkan perubahan data yang tidak sesuai jika tidak dilindungi mekanisme sinkronisasi. Pengujian deadlock memperlihatkan bahwa penggunaan lock yang tidak tepat dapat membuat thread saling menunggu, sementara pengelolaan lock dan batas waktu dapat membantu mengurangi risiko tersebut.

Pada bagian Raft, simulasi memperlihatkan perubahan status node, pemilihan leader, dan penambahan perintah ke dalam log. Pemisahan class ke dalam modul Python membuat kode lebih terstruktur. Namun, simulasi Raft yang dibuat masih sederhana dan belum menerapkan seluruh mekanisme konsensus serta replikasi log seperti pada sistem Raft sebenarnya.

## 5. Referensi

1. Materi Praktikum Sistem Terdistribusi dan Terdesentralisasi, Modul 03: Sinkronisasi pada Sistem Terdistribusi.
2. Dokumentasi Python, *threading — Thread-based parallelism*. https://docs.python.org/3/library/threading.html
3. Dokumentasi Python, *enum — Support for enumerations*. https://docs.python.org/3/library/enum.html
4. Mills, D., et al. *Network Time Protocol Version 4: Protocol and Algorithms Specification*. RFC 5905. https://www.rfc-editor.org/rfc/rfc5905
5. Ongaro, D., & Ousterhout, J. (2014). *In Search of an Understandable Consensus Algorithm (Extended Version)*. USENIX Annual Technical Conference.
