# MODUL 04
# KONSISTENSI DAN REPLIKASI PADA SISTEM TERDISTRIBUSI

**Mata Kuliah:** Sistem Terdistribusi dan Terdesentralisasi  
**Nama:** Arsenius Kelvin Jemudin  
**NIM:** 255410015  
**Kelas:** IF-1  
**Program Studi:** Informatika  
**Fakultas:** Teknologi Informasi  
**Universitas:** Universitas Teknologi Digital Indonesia (UTDI)

## A. Pendahuluan

Sistem terdistribusi merupakan sistem yang terdiri dari beberapa komputer atau node yang saling berkomunikasi melalui jaringan untuk menjalankan layanan dan mengolah data. Dalam sistem terdistribusi, konsistensi dan replikasi data merupakan dua konsep penting yang berkaitan dengan ketersediaan dan kesesuaian informasi.

Replikasi data memungkinkan data diakses melalui beberapa node dalam sebuah cluster. Sementara itu, konsistensi berkaitan dengan kesesuaian data yang dibaca atau diperbarui oleh pengguna maupun proses yang berbeda.

Pada praktikum ini, Apache Ignite 3.1.0 digunakan untuk mempelajari akses data melalui cluster yang terdiri dari tiga node. Praktik dilakukan dengan menginisialisasi cluster, membuat skema database, memasukkan data, serta menjalankan query dari node2 dan node3. Hasil pengujian kedua node kemudian dibandingkan untuk mengamati kesamaan data yang dapat dibaca.

## B. Tujuan Praktikum

1. Memahami konsep konsistensi dan replikasi pada sistem terdistribusi.
2. Menjalankan cluster Apache Ignite 3.1.0 menggunakan Docker.
3. Membuat skema dan tabel database menggunakan perintah SQL.
4. Memasukkan data ke dalam database menggunakan file SQL.
5. Menguji pembacaan data melalui node yang berbeda.
6. Membandingkan hasil query pada node2 dan node3.

## C. Dasar Teori

### 1. Sistem Terdistribusi

Sistem terdistribusi adalah sistem yang terdiri dari beberapa komputer atau node yang bekerja sama melalui jaringan untuk menyediakan layanan atau mengolah data. Setiap node menjalankan perannya dalam sistem sehingga layanan dapat diakses melalui lingkungan yang saling terhubung.

### 2. Konsistensi Data

Konsistensi data berkaitan dengan kesesuaian informasi yang diperoleh ketika data diakses melalui node yang berbeda. Konsistensi diperlukan agar hasil pembacaan data tetap sesuai dengan keadaan data dalam sistem berdasarkan aturan konsistensi yang diterapkan.

### 3. Replikasi Data

Replikasi data merupakan proses menyediakan salinan data pada beberapa node. Replikasi dapat membantu meningkatkan ketersediaan data dan mendukung akses dari node yang berbeda. Keberhasilan replikasi bergantung pada mekanisme penyimpanan, pengaturan cluster, dan kebijakan replikasi yang digunakan.

### 4. Apache Ignite

Apache Ignite merupakan platform untuk penyimpanan dan pengolahan data terdistribusi. Apache Ignite menyediakan kemampuan untuk mengelola data dan menjalankan query dalam lingkungan cluster. Dalam praktikum ini, Apache Ignite 3.1.0 digunakan untuk menjalankan tiga node dan menguji akses data menggunakan SQL.

### 5. Docker

Docker merupakan platform untuk menjalankan aplikasi di dalam container. Pada praktikum ini, Docker digunakan untuk menjalankan node Apache Ignite secara terpisah. Penggunaan container mempermudah pengelolaan lingkungan praktikum dan penghentian layanan setelah pengujian selesai.

## D. Langkah Praktikum

1. Menyiapkan Apache Ignite 3.1.0 menggunakan Docker.
2. Menjalankan tiga node Apache Ignite, yaitu node1, node2, dan node3.
3. Menghubungkan CLI ke node1.
4. Menginisialisasi cluster dengan nama `ignite3` dan menentukan kelompok node untuk penyimpanan metadata.
5. Menjalankan file `schema.sql` untuk menyiapkan skema database.
6. Menjalankan file SQL yang disediakan untuk memasukkan data ke dalam tabel.
7. Memeriksa daftar tabel pada skema `PUBLIC`.
8. Menghubungkan CLI ke node2 dan menjalankan query jumlah invoice.
9. Menjalankan query ringkasan penjualan bulanan melalui node2.
10. Mengulangi pengujian jumlah invoice dan penjualan bulanan melalui node3.
11. Membandingkan hasil query dari node2 dan node3.
12. Menghentikan container Apache Ignite setelah seluruh pengujian selesai.

## E. Hasil dan Pembahasan

### 1. Inisialisasi Cluster Apache Ignite

Cluster Apache Ignite 3.1.0 berhasil diinisialisasi dengan nama `ignite3`. Cluster menggunakan tiga node, yaitu node1, node2, dan node3. Inisialisasi dilakukan setelah node dijalankan menggunakan Docker.

Tahap ini merupakan langkah awal agar lingkungan cluster siap digunakan untuk pembuatan skema database dan pengolahan data. Setelah cluster berhasil diinisialisasi, proses dilanjutkan dengan menjalankan perintah SQL.

**Dokumentasi:** `21-ignite-cluster-initialized.png`

### 2. Pembuatan Skema Database

Pembuatan skema database dilakukan dengan menjalankan file `schema.sql` melalui CLI Apache Ignite. File tersebut berisi perintah SQL untuk menyiapkan struktur database yang akan digunakan dalam praktikum.

Skema database diperlukan sebagai dasar untuk membuat tabel dan memasukkan data. Setelah file dijalankan, praktikum dilanjutkan ke tahap pengisian data dan pemeriksaan tabel.

**Dokumentasi:** `22-ignite-schema-executed.png`

### 3. Pengisian Data

Data dimasukkan ke dalam database menggunakan file SQL yang telah disediakan. Proses ini dilakukan setelah skema database disiapkan agar data dapat digunakan dalam pengujian selanjutnya.

Data pada tabel-tabel tersebut digunakan untuk menjalankan query, termasuk menghitung jumlah invoice dan menampilkan ringkasan penjualan bulanan. Dengan demikian, pengujian dilakukan menggunakan data yang tersedia di dalam database, bukan hanya memeriksa struktur tabel.

**Dokumentasi:** `23-ignite-load-sql-data.png`

### 4. Pemeriksaan Tabel Database

Pemeriksaan tabel dilakukan dengan menjalankan query untuk menampilkan daftar tabel pada skema `PUBLIC`. Hasilnya menunjukkan beberapa tabel, seperti `ALBUM`, `TRACK`, `CUSTOMER`, `EMPLOYEE`, `GENRE`, `INVOICE`, dan `INVOICELINE`, beserta tabel lainnya.

Pemeriksaan ini membantu memastikan bahwa tabel-tabel yang digunakan dalam praktikum tersedia untuk proses pengujian. Tabel `INVOICE` kemudian digunakan untuk menghitung jumlah data invoice, sedangkan query penjualan bulanan digunakan untuk menghasilkan ringkasan transaksi.

**Dokumentasi:** `24-ignite-tables-created.png`

### 5. Pengujian Data pada Node2

Pengujian pada node2 dilakukan dengan menjalankan query berikut:

`SELECT COUNT(*) FROM Invoice;`

Hasil query menunjukkan jumlah data invoice sebanyak **412 baris**. Hasil tersebut menunjukkan bahwa data invoice dapat dibaca melalui koneksi ke node2.

Selain itu, dijalankan query penjualan bulanan untuk menampilkan jumlah invoice, jumlah pelanggan, pendapatan bulanan, dan rata-rata nilai transaksi. Query tersebut menghasilkan ringkasan yang dapat digunakan untuk mengamati data transaksi berdasarkan bulan.

Pengujian ini menunjukkan bahwa node2 dapat digunakan untuk membaca dan mengolah data melalui perintah SQL.

**Dokumentasi:**

- `25-ignite-node2-invoice-count.png`
- `26-ignite-node2-monthly-sales.png`

### 6. Pengujian Data pada Node3

Pengujian selanjutnya dilakukan dengan menghubungkan CLI ke node3. Query yang digunakan sama dengan pengujian pada node2 agar hasilnya dapat dibandingkan.

Query `SELECT COUNT(*) FROM Invoice;` menghasilkan jumlah **412 baris**, sama dengan hasil pada node2. Query penjualan bulanan juga menampilkan informasi yang sama dengan hasil pengujian sebelumnya.

Kesamaan hasil tersebut menunjukkan bahwa data yang diuji dapat dibaca melalui node2 dan node3 dalam cluster. Hal ini memberikan gambaran mengenai akses data melalui beberapa node dalam sistem terdistribusi.

Namun, pengujian ini terbatas pada pembacaan dan perbandingan hasil query. Pengujian belum mencakup seluruh kondisi konsistensi, seperti penulisan data secara bersamaan atau perubahan data ketika terjadi kegagalan node.

**Dokumentasi:**

- `27-ignite-node3-invoice-count.png`
- `28-ignite-node3-monthly-sales.png`

### 7. Penghentian Container Apache Ignite

Setelah seluruh pengujian selesai, container Apache Ignite dihentikan menggunakan perintah `docker compose down`. Pemeriksaan kemudian dilakukan dengan perintah `docker ps -a` untuk melihat status container.

Hasil pemeriksaan menunjukkan bahwa container node Apache Ignite sudah tidak berjalan. Container PostgreSQL dari praktikum lain tetap dibiarkan berjalan karena bukan bagian dari cluster Apache Ignite yang sedang diuji.

Tahap ini dilakukan untuk memastikan bahwa layanan Apache Ignite yang digunakan dalam praktikum telah dihentikan setelah pengujian selesai.

**Dokumentasi:** `29-ignite-all-nodes-stopped.png`

### 8. Pembahasan Umum

Berdasarkan hasil praktikum, cluster Apache Ignite 3.1.0 berhasil diinisialisasi dan digunakan untuk menjalankan pengolahan data melalui perintah SQL. Skema database berhasil disiapkan, data dimasukkan, dan daftar tabel dapat diperiksa.

Pengujian pada node2 dan node3 menunjukkan bahwa keduanya dapat membaca 412 baris data invoice. Selain itu, query penjualan bulanan menghasilkan informasi yang sama pada kedua node. Hasil tersebut menunjukkan bahwa data yang diuji dapat diakses melalui node yang berbeda dalam cluster.

Praktikum ini memberikan gambaran mengenai penggunaan cluster dan pemeriksaan data melalui beberapa node. Meskipun hasil query kedua node sama, pengujian ini belum cukup untuk membuktikan seluruh aspek konsistensi dan ketahanan sistem terhadap kegagalan. Pengujian lebih lanjut diperlukan untuk memeriksa kondisi tersebut secara menyeluruh.

## F. Kesimpulan

Praktikum konsistensi dan replikasi pada sistem terdistribusi menggunakan Apache Ignite 3.1.0 berhasil dilakukan. Cluster yang terdiri dari node1, node2, dan node3 berhasil diinisialisasi. Skema database dibuat, data dimasukkan menggunakan file SQL, dan tabel-tabel yang tersedia berhasil diperiksa.

Hasil pengujian menunjukkan bahwa node2 dan node3 dapat membaca 412 baris data invoice serta menghasilkan ringkasan penjualan bulanan yang sama. Hasil tersebut memberikan pemahaman mengenai akses data melalui beberapa node dalam cluster. Namun, pengujian yang dilakukan masih terbatas pada pembacaan data dan belum mencakup seluruh kondisi konsistensi maupun penanganan kegagalan node.

## G. Referensi

1. Apache Software Foundation. (n.d.). *Apache Ignite 3 Documentation*. https://ignite.apache.org/docs/ignite3/latest/
2. Docker, Inc. (n.d.). *Docker Compose Documentation*. https://docs.docker.com/compose/
3. Universitas Teknologi Digital Indonesia. (n.d.). *Konsistensi dan Replikasi pada Sistem Terdistribusi*. Modul Praktikum Sistem Terdistribusi dan Terdesentralisasi.