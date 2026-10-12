Modul 02 — Komunikasi Antarproses pada Sistem Terdistribusi

1. Tujuan Praktikum

1. Memahami cara mengelola proses yang berjalan pada sistem operasi Windows.
2. Memahami penggunaan perintah Command Prompt untuk melihat, mencari, menghentikan, dan menjalankan proses.
3. Memahami komunikasi antara client dan server menggunakan GraphQL.
4. Mempraktikkan pengambilan data dari server GraphQL menggunakan Python.

2. Dasar Teori

2.1 Manajemen Proses Windows

Proses merupakan program yang sedang dijalankan oleh sistem operasi. Windows menyediakan Task Manager untuk melihat aplikasi dan proses yang berjalan. Selain itu, Command Prompt menyediakan perintah seperti `tasklist` untuk menampilkan proses, `findstr` untuk mencari teks tertentu, `taskkill` untuk menghentikan proses, dan `start` untuk menjalankan aplikasi.

2.2 Komunikasi Client-Server dengan GraphQL

GraphQL merupakan teknologi untuk meminta dan mengambil data dari server menggunakan query. Dalam model client-server, client mengirimkan permintaan kepada server, kemudian server memproses permintaan dan mengembalikan data yang diminta. Pada praktikum ini, Python digunakan untuk membuat client, sedangkan Strawberry digunakan untuk menyediakan server GraphQL.

3. Implementasi

3.1 Manajemen Proses Windows

Pada bagian ini dilakukan pengamatan proses melalui Task Manager dan Command Prompt. Perintah yang dipelajari meliputi `tasklist`, `findstr`, `taskkill`, dan `start`.

**Dokumentasi:**

Tambahkan screenshot Task Manager dan hasil praktik perintah Command Prompt di bagian ini.

3.2 Persiapan Lingkungan Python

Lingkungan Python disiapkan menggunakan `uv` dan virtual environment. Selanjutnya, dilakukan pemeriksaan versi Python serta pemasangan paket yang diperlukan untuk menjalankan server dan client GraphQL.

**Dokumentasi:**

Tambahkan screenshot persiapan lingkungan Python dan pemasangan paket setelah praktik selesai.

3.3 Pembuatan Server GraphQL

Server GraphQL dibuat menggunakan Strawberry untuk menyediakan data buku. Server kemudian dijalankan agar client dapat mengirimkan query dan menerima data dari server.

**Dokumentasi:**

Tambahkan kode server dan screenshot GraphQL Playground setelah pengujian berhasil.

3.4 Pembuatan Client GraphQL

Client dibuat menggunakan Python dan pustaka `requests`. Client mengirimkan permintaan GraphQL ke alamat server, menerima respons, dan menampilkan data buku yang dikembalikan server.

**Dokumentasi:**

Tambahkan kode `client.py` dan screenshot hasil menjalankan client.
4. Hasil dan Pembahasan

4.1 Manajemen Proses Windows

Praktik ini digunakan untuk memahami cara memantau dan mengelola proses yang sedang berjalan di Windows. Task Manager dan Command Prompt membantu pengguna melihat, mencari, menghentikan, serta menjalankan proses aplikasi.

4.2 Komunikasi Client-Server dengan GraphQL

Pengujian GraphQL dilakukan dengan menjalankan server dan mengirimkan query dari client. Jika server berjalan dengan benar, client akan menerima respons berisi data buku yang diminta. Hasil akhir akan didokumentasikan menggunakan screenshot pengujian.

5. Kesimpulan

Praktikum ini membahas manajemen proses pada Windows serta komunikasi client-server menggunakan GraphQL. Melalui kegiatan ini, mahasiswa mempelajari perintah untuk mengelola proses, menyiapkan lingkungan Python, menjalankan server GraphQL, dan mengambil data melalui client.

6. Referensi

1. Dokumentasi Python: https://docs.python.org/3/
2. Dokumentasi Strawberry GraphQL: https://strawberry.rocks/
3. Dokumentasi uv: https://docs.astral.sh/uv/
4. Dokumentasi GraphQL: https://graphql.org/

