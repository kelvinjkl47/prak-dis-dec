# Praktikum Minggu 04 — Konsistensi dan Replikasi pada Sistem Terdistribusi
# Praktikum Minggu 04 — Konsistensi dan Replikasi pada Sistem Terdistribusi

**Nama:** Arsenius Kelvin Jemudin  
**NIM:** 255410015  
**Kelas:** IF-1  
**Program Studi:** Informatika  
**Universitas:** Universitas Teknologi Digital Indonesia  
**Sistem Operasi:** Windows 11 (Docker Desktop dengan WSL 2)

## 1. Tujuan Praktikum

1. Memahami konsep replikasi data untuk menjaga konsistensi dan ketersediaan pada sistem terdistribusi.
2. Mengonfigurasi *streaming replication* PostgreSQL 18 dengan satu primary dan satu replica menggunakan Docker Compose.
3. Membuktikan bahwa perubahan data di primary direplikasi ke replica, dan bahwa replica hanya dapat dibaca.
4. Mempraktikkan *High Availability* dengan mempromosikan replica menjadi primary ketika primary mati.
5. Memahami replikasi *master-master* menggunakan cluster Apache Ignite 3 dengan tiga node.

## 2. Struktur Folder

```
04/
├── README.md
├── images/                      (screenshot hasil praktikum, 01 sampai 29)
├── streaming-replication/
│   ├── 00_init.sql
│   ├── docker-compose.yaml
│   └── env.ps1
└── ignite/
    ├── docker-compose.yml
    ├── sql.zip
    └── sql/
        ├── schema.sql
        ├── current_catalog.sql
        ├── media_and_genre.sql
        ├── tracks.sql
        ├── ee_and_cust.sql
        └── invoices.sql
```

## 3. Dasar Teori

### 3.1 Replikasi Data

Replikasi adalah proses menyalin data dari satu server ke server lain sehingga beberapa salinan data tersimpan di node yang berbeda. Tujuannya adalah meningkatkan ketersediaan (*availability*), menyebarkan beban baca, dan menjaga data tetap ada ketika salah satu node gagal. Konsekuensinya, sistem harus menjaga konsistensi antarsalinan data.

### 3.2 Streaming Replication pada PostgreSQL

PostgreSQL mencatat setiap perubahan data ke dalam *Write-Ahead Log* (WAL). Pada *streaming replication*, server **primary** mengalirkan catatan WAL tersebut secara terus-menerus ke server **replica** (*standby*). Replica memutar ulang WAL sehingga datanya sama dengan primary. Replica berjalan dalam mode *recovery* sehingga hanya melayani akses baca (*read-only*). Penerapan yang dipakai di praktikum ini bersifat **asinkron** (`sync_state = async`): primary tidak menunggu konfirmasi replica sebelum menyelesaikan transaksi.

*Replication slot* adalah mekanisme agar primary menyimpan WAL yang belum diterima replica, sehingga replica tidak ketinggalan walaupun sempat terputus.

### 3.3 High Availability

Model primary dan replica dapat dipakai untuk *High Availability* (HA). Jika primary mati, salah satu replica dapat **dipromosikan** (`pg_promote()`) menjadi primary baru sehingga layanan baca dan tulis tetap berjalan.

### 3.4 Replikasi Master-Master dan Apache Ignite

Pada replikasi master-master, semua node dapat menerima operasi baca dan tulis. Apache Ignite 3 membentuk *cluster* dari beberapa node sehingga perubahan yang dilakukan pada satu node dapat dilihat dari node lain dalam cluster yang sama.

## 4. Implementasi dan Hasil Pengujian

### 4.0 Persiapan Lingkungan

Praktikum dikerjakan di Windows, sehingga petunjuk Linux pada modul disesuaikan: Docker dijalankan melalui Docker Desktop yang memakai WSL 2.

1. **Cek virtualisasi.** Task Manager (tab *Performance*, CPU) menunjukkan prosesor AMD Ryzen 5 5625U dengan 6 core dan 12 prosesor logis, RAM 13,8 GB, dan *Virtualization: Enabled*.
2. **Pasang WSL 2** dengan `wsl --install` di PowerShell Administrator. Keluarannya menunjukkan Windows Subsystem for Linux 3.0.3 terpasang dan komponen *VirtualMachinePlatform* diaktifkan, tetapi perubahan baru berlaku setelah Windows di-*restart*.
3. **Pasang Docker Desktop**, lalu pastikan status *Engine running*. Dashboard Docker Desktop menampilkan halaman *Containers* yang masih kosong karena belum ada container yang dijalankan.
4. **Cek instalasi** dengan `docker --version` (Docker versi 29.9.2), `docker compose version` (Docker Compose v5.6.0), dan `docker run hello-world`.

![Virtualisasi aktif](images/01-virtualisasi.png)

![Instalasi WSL](images/02-wsl-install.png)

![Docker Desktop berjalan](images/03-docker-desktop.png)

![Versi Docker](images/04-docker-versi.png)

![Docker hello-world](images/05-hello-world.png)

Hasil `hello-world` menampilkan pesan "Hello from Docker!", yang menandakan Docker daemon aktif dan dapat menjalankan container.

**Pembahasan.** Docker membutuhkan fitur virtualisasi pada CPU. Di Windows, Docker Desktop berjalan di atas WSL 2, yaitu lapisan Linux ringan yang memungkinkan container Linux (seperti PostgreSQL dan Apache Ignite) berjalan. Karena itu virtualisasi harus aktif (*Enabled*) dan WSL 2 terpasang sebelum Docker dipasang. Container berbeda dari mesin virtual penuh: container berbagi kernel dengan host, tetapi tiap container memiliki proses, jaringan, dan sistem berkas yang terisolasi. Keunggulannya, beberapa server (primary dan replica, atau tiga node Ignite) dapat disimulasikan dalam satu laptop dan dijalankan ulang dengan cepat. Keluaran `hello-world` membuktikan seluruh rantai berfungsi: client Docker menghubungi daemon, daemon mengunduh image dari Docker Hub, membuat container, dan menampilkan hasilnya.

### 4.1 Streaming Replication PostgreSQL 18

#### 4.1.1 File Konfigurasi

Semua file dibuat di folder `C:\dev\streaming-replication` (di luar OneDrive agar *bind-mount* Docker tidak bermasalah).

**`00_init.sql`** membuat user `replicator` dan slot replikasi `replication_slot` ketika primary pertama kali diinisialisasi:

```sql
CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';
SELECT pg_create_physical_replication_slot('replication_slot');
```

**`docker-compose.yaml`** mendefinisikan dua service: `postgres_primary` (port 5432) dan `postgres_replica` (port 5433). Primary dijalankan dengan `wal_level=replica`, `hot_standby=on`, `max_wal_senders=10`, `max_replication_slots=10`, dan `hot_standby_feedback=on`. Replica menyalin data primary dengan `pg_basebackup` lalu berjalan sebagai standby. Berikut versi akhir yang dipakai (perubahan pada bagian replica dijelaskan di bagian *Kendala dan Solusi*):

```yaml
x-postgres-common:
  &postgres-common
  image: postgres:18.3-alpine3.23
  user: postgres
  restart: always
  healthcheck:
    test: 'pg_isready -U zuser --dbname=zdb'
    interval: 10s
    timeout: 5s
    retries: 5

services:
  postgres_primary:
    <<: *postgres-common
    ports:
      - 5432:5432
    environment:
      POSTGRES_USER: zuser
      POSTGRES_DB: zdb
      POSTGRES_PASSWORD: zpass
      POSTGRES_HOST_AUTH_METHOD: "scram-sha-256\nhost replication replicator 0.0.0.0/0 md5"
      POSTGRES_INITDB_ARGS: "--auth-host=scram-sha-256"
    command: |
      postgres
      -c wal_level=replica
      -c hot_standby=on
      -c max_wal_senders=10
      -c max_replication_slots=10
      -c hot_standby_feedback=on
    volumes:
      - ./00_init.sql:/docker-entrypoint-initdb.d/00_init.sql

  postgres_replica:
    <<: *postgres-common
    ports:
      - 5433:5432
    environment:
      PGUSER: replicator
      PGPASSWORD: replicator_password
      PGDATA: /var/lib/postgresql/18/docker
    command: |
      bash -c "
      if [ ! -s /var/lib/postgresql/18/docker/PG_VERSION ]; then
        until pg_basebackup --pgdata=/var/lib/postgresql/18/docker -R --slot=replication_slot --host=postgres_primary --port=5432 -X stream; do
          echo 'pg_basebackup failed. Retrying in 5 seconds ...'
          sleep 5
        done
        echo 'Backup done, starting replica...'
        chmod 0700 /var/lib/postgresql/18/docker
      else
        echo 'Data directory already exists, skipping pg_basebackup...'
      fi
      postgres
      "
    depends_on:
      - postgres_primary
```

**`env.ps1`** adalah versi PowerShell dari `env.sh` pada modul (Windows tidak memakai `sudo`). File ini mendefinisikan fungsi singkat: `dcu` (`docker compose up -d`), `dcd` (`docker compose down`), `dps` (`docker ps`), `dlr` dan `dlp` (log replica dan primary), serta `der` dan `dep` (masuk ke container).

![Struktur file](images/06-file-struktur.png)

Ukuran `docker-compose.yaml` pada gambar (1416 byte) adalah versi awal. Versi akhir yang dicantumkan di atas berukuran 1585 byte karena bagian replica diperbaiki kemudian (lihat bagian *Kendala dan Solusi*).

![Validasi konfigurasi compose](images/06c-compose-config.png)

`docker compose config --quiet` tidak menampilkan apa pun, artinya sintaks `docker-compose.yaml` valid.

**Pembahasan konfigurasi.** Pengaturan penting pada `docker-compose.yaml` dan fungsinya:

| Pengaturan | Fungsi |
|---|---|
| `wal_level=replica` | Primary mencatat WAL dengan tingkat detail yang cukup untuk replikasi. |
| `hot_standby=on` | Replica dapat melayani query baca walaupun sedang dalam mode recovery. |
| `max_wal_senders=10` | Jumlah maksimum proses pengirim WAL, satu untuk setiap koneksi replica. |
| `max_replication_slots=10` | Jumlah maksimum slot replikasi yang boleh dibuat. |
| `hot_standby_feedback=on` | Replica memberi tahu primary tentang query yang sedang berjalan agar baris yang masih dibutuhkan tidak langsung dibersihkan, sehingga query di replica lebih jarang dibatalkan. |
| `POSTGRES_HOST_AUTH_METHOD` (baris `host replication replicator 0.0.0.0/0 md5`) | Mengizinkan user `replicator` terhubung untuk keperluan replikasi. |
| `00_init.sql` | Membuat user `replicator` dengan hak replikasi dan slot fisik `replication_slot` ketika primary pertama kali dibuat. |
| `pg_basebackup -R --slot=replication_slot -X stream` | Menyalin seluruh data primary ke replica. Opsi `-R` membuat konfigurasi standby secara otomatis, `--slot` memakai slot replikasi, dan `-X stream` ikut mengalirkan WAL selama proses backup berlangsung. |
| `healthcheck` dengan `pg_isready` | Docker memeriksa secara berkala apakah PostgreSQL siap menerima koneksi, hasilnya tampil sebagai status *healthy*. |
| `depends_on` | Replica dibuat setelah container primary dibuat. |

Perlu dicatat bahwa `depends_on` hanya mengatur urutan pembuatan container, bukan menunggu primary benar-benar siap. Itu sebabnya replica memakai perulangan `until pg_basebackup ...` yang mencoba lagi setiap 5 detik sampai primary siap.

#### 4.1.2 Menjalankan Primary dan Replica

Setelah alias diaktifkan (`. .\env.ps1`), kedua server dijalankan dengan `dcu`. Pada pertama kali, image `postgres:18.3-alpine3.23` diunduh, lalu network dan dua container dibuat. Status container dicek dengan `dps`, dan kedua container berstatus **healthy**. Pada hasil `dcu`, image diunduh dalam 20,8 detik, network `streaming-replication_default` dibuat, dan container primary serta replica berstatus *Started* (masing-masing dalam sekitar 1 detik). `dps` menampilkan kedua container *Up 3 minutes (healthy)* dengan port **5432** untuk primary dan **5433** untuk replica.

![docker compose up](images/07-compose-up.png)

![docker ps](images/08-docker-ps.png)

Pada log replica (`dlr`), percobaan pertama `pg_basebackup` gagal terhubung ke `postgres_primary` (172.18.0.2) port 5432 dengan pesan `Connection refused`, lalu diulang setelah 5 detik. Log tersebut menunjukkan replica menunggu primary siap, lalu `pg_basebackup` berhasil, replica masuk mode standby, dan mulai menerima WAL dari primary. Beberapa baris `pg_basebackup failed. Retrying in 5 seconds` di awal wajar karena replica menunggu primary selesai dinyalakan.

![Log replica](images/09-log-replica.png)

**Pembahasan.** Status *healthy* pada kedua container berarti healthcheck `pg_isready` berhasil, sehingga PostgreSQL di primary dan replica sudah menerima koneksi. Urutan di log replica menggambarkan proses replikasi dimulai: (1) `pg_basebackup` gagal sementara karena primary belum siap, lalu berhasil setelah primary menyala, (2) muncul `Backup done, starting replica...`, (3) PostgreSQL masuk ke mode standby (`entering standby mode`), (4) replica siap menerima koneksi baca (`ready to accept read-only connections`), dan (5) replica mulai menerima WAL dari primary (`started streaming WAL from primary`). Kegagalan di awal bukan error yang perlu dikhawatirkan, karena memang disiapkan lewat perulangan pada command replica.

#### 4.1.3 Pengujian Replikasi

*Catatan:* pengujian pada bagian ini dikerjakan setelah container dibuat ulang, sehingga tanggal dan nilai seperti `pid` berbeda dari log pada bagian 4.1.2 yang diambil pada sesi pertama. Database diakses dari dalam container dengan `docker exec -it streaming-replication-postgres_primary-1 psql -U zuser -d zdb` (primary) dan `docker exec -it streaming-replication-postgres_replica-1 psql -U zuser -d zdb` (replica), tanpa memakai alias `dep` dan `der` pada modul.

**Status replikasi di primary.** Query `SELECT * FROM pg_stat_replication;` menampilkan satu koneksi dari user `replicator` (`application_name = walreceiver`) dengan `client_addr` **172.18.0.3**, yaitu container replica. Proses walreceiver tersebut memiliki `pid` **60**. Kolom `state` bernilai `streaming`, dan nilai `sent_lsn`, `write_lsn`, `flush_lsn`, serta `replay_lsn` sama (**0/304B538**), sehingga replica tidak tertinggal dari primary. Nilai `sync_state = async` menunjukkan replikasi asinkron.

![pg_stat_replication](images/10-pg-stat-replication.png)

**Slot replikasi.** Query `SELECT * FROM pg_replication_slots;` menampilkan slot fisik `replication_slot` dengan `active = t`. Nilai `active_pid` (**60**) sama dengan `pid` walreceiver pada `pg_stat_replication`, sehingga slot ini sedang dipakai replica. Nilai `restart_lsn` (**0/304B538**) sama dengan posisi LSN replica. `wal_status = reserved` berarti WAL yang dibutuhkan masih tersimpan di primary.

![pg_replication_slots](images/11-pg-replication-slots.png)

**Status replica.** Query `SELECT pg_is_in_recovery();` pada replica bernilai `t` (true). Artinya server ini berjalan dalam mode standby yang hanya menerima data dari primary dan melayani akses baca.

![pg_is_in_recovery pada replica](images/12-replica-in-recovery.png)

**Percobaan manipulasi data.** Untuk melihat efek replikasi, dibuat tabel di primary dan hasilnya diperiksa di replica.

*Sebelum tabel dibuat*, perintah `\dt` di replica dan di primary sama-sama menampilkan "Did not find any tables."

![Replica sebelum tabel](images/13-replica-sebelum-tabel.png)

![Primary sebelum tabel](images/14-primary-sebelum-tabel.png)

*Di primary*, dibuat tabel `testrep` dan diisi dua baris:

```sql
CREATE TABLE testrep (first INT, second VARCHAR(15));
INSERT INTO testrep (first, second) VALUES (21, 'Test pertama');
INSERT INTO testrep (first, second) VALUES (23, 'Test ke dua');
SELECT * FROM testrep;
```

![Membuat tabel di primary](images/15-primary-buat-tabel.png)

`CREATE TABLE` berhasil, dan kedua perintah `INSERT` melaporkan `INSERT 0 1` (satu baris ditambahkan per perintah). `SELECT` menampilkan dua baris: `21 | Test pertama` dan `23 | Test ke dua`.

*Di replica*, `\dt` menampilkan tabel `public.testrep` dengan pemilik `zuser`, dan `SELECT * FROM testrep;` menampilkan kedua baris yang sama (`21 | Test pertama` dan `23 | Test ke dua`), tanpa pernah dibuat di replica. Ini membuktikan perubahan di primary direplikasi otomatis melalui streaming WAL.

![Replica setelah tabel dibuat](images/16-replica-sesudah-tabel.png)

*Uji tulis ke replica.* Perintah `INSERT INTO testrep (first, second) VALUES (99, 'Dari replica');` di replica ditolak dengan error `cannot execute INSERT in a read-only transaction`. Replica berada dalam mode recovery sehingga penulisan hanya dapat dilakukan lewat primary.

![Replica read-only](images/17-replica-read-only.png)

**Pembahasan pengujian replikasi.**

- **`pg_stat_replication`** adalah tampilan di primary tentang koneksi replikasi yang sedang berjalan. Nilai `streaming` pada `state` berarti WAL sedang dialirkan. Empat nilai LSN (*Log Sequence Number*, posisi di dalam WAL) menggambarkan seberapa jauh replica menyusul: `sent_lsn` adalah yang sudah dikirim primary, `write_lsn` yang sudah ditulis replica, `flush_lsn` yang sudah disimpan permanen, dan `replay_lsn` yang sudah diterapkan ke data. Karena keempatnya sama, replica tidak tertinggal. Nilai `sync_state = async` berarti primary tidak menunggu konfirmasi replica sebelum menyelesaikan transaksi, sehingga lebih cepat tetapi replica bisa tertinggal beberapa saat.
- **`pg_replication_slots`** menunjukkan slot fisik yang aktif (`active = t`). Slot membuat primary menyimpan WAL yang belum diterima replica, sehingga replica yang sempat terputus masih dapat menyusul.
- **`pg_is_in_recovery() = t`** membuktikan server tersebut adalah standby.
- **Pengujian tabel `testrep`.** Tabel dan data hanya dibuat di primary, tetapi muncul di replica. Ini terjadi karena perintah `CREATE TABLE` dan `INSERT` dicatat sebagai WAL di primary lalu diterapkan ulang oleh replica.
- **Uji tulis ke replica ditolak** karena replica berada dalam mode recovery. Semua penulisan harus lewat primary, dan inilah yang menjaga konsistensi: hanya ada satu sumber kebenaran untuk penulisan, sedangkan replica dipakai untuk membaca dan sebagai cadangan.

#### 4.1.4 High Availability

Skenario: primary mati, lalu replica dipromosikan menjadi primary baru.

1. **Primary dimatikan** dengan `docker stop streaming-replication-postgres_primary-1`. Sebelumnya, `docker ps` pertama gagal (*failed to connect to the docker API*) karena Docker Desktop belum berjalan. Setelah Docker Desktop menyala, `docker ps` menampilkan kedua container berstatus *healthy*. Container replica berumur lebih muda (*11 hours ago*) dibanding primary (*2 days ago*) karena replica dibuat ulang ketika konfigurasinya diperbaiki (lihat bagian *Kendala dan Solusi*). Setelah `docker stop`, container primary berhenti, sedangkan replica masih berjalan.

![Primary dimatikan](images/18-primary-down.png)

2. **Replica dipromosikan.** Di replica, `SELECT pg_is_in_recovery();` bernilai `t`. Setelah `SELECT pg_promote();` (hasil `t`), pemeriksaan ulang `pg_is_in_recovery()` bernilai `f`. Artinya server tersebut keluar dari mode recovery dan kini berfungsi sebagai primary yang dapat menerima operasi baca dan tulis.

![Replica dipromosikan](images/19-replica-promote.png)

3. **Seluruh container dihentikan.** `docker ps -a` menampilkan container replica dan primary berstatus *Exited (0)*, bersama container `hello-world` dari pengujian awal. Pada modul, container dimatikan dengan `docker compose down` yang menghapus container, sedangkan pada praktikum ini container hanya dihentikan sehingga masih terdaftar dan datanya tidak dihapus.

![Semua container dihentikan](images/20-all-containers-stopped.png)

Dengan cara ini layanan database tetap tersedia walaupun primary awal mati. Karena replikasi bersifat asinkron, data yang belum sempat diterima replica saat primary mati berpotensi hilang.

**Pembahasan High Availability.** `pg_promote()` mengubah replica dari mode recovery menjadi server yang menerima operasi baca dan tulis, dan hasil `pg_is_in_recovery()` berubah dari `t` menjadi `f`. Dengan begitu layanan database dapat berlanjut walaupun primary awal mati. Beberapa hal yang perlu diperhatikan pada pendekatan ini:

- **Failover dilakukan manual.** Tidak ada mekanisme otomatis yang mendeteksi kematian primary lalu memilih penggantinya. Pada sistem produksi biasanya dipakai alat tambahan untuk otomatisasi (misalnya Patroni).
- **Risiko kehilangan data.** Karena replikasi asinkron, transaksi yang sudah dikonfirmasi di primary tetapi belum sampai ke replica akan hilang saat failover.
- **Aplikasi harus diarahkan ulang** ke server baru (di praktikum ini port 5433), karena alamat primary berubah.
- **Primary lama tidak otomatis kembali menjadi replica.** Setelah replica dipromosikan, kedua server memiliki riwayat data yang bercabang, sehingga primary lama harus disiapkan ulang sebagai replica baru dari server yang baru.

### 4.2 Replikasi Master-Master dengan Apache Ignite 3

Pada bagian ini dibuat cluster Apache Ignite 3.1.0 dengan tiga node (`node1`, `node2`, `node3`) memakai Docker Compose. Port REST administratif node-node tersebut adalah **10300**, **10301**, dan **10302**, sedangkan port koneksi aplikasi adalah **10800** sampai **10802**. File `docker-compose.yml` dan `sql.zip` diambil dari dokumentasi Apache Ignite 3. Pada modul tertulis Ignite 3.0.0 di beberapa perintah, tetapi gambar dan alias memakai 3.1.0, sehingga yang dipakai adalah **3.1.0**.

**Inisialisasi cluster.** Setelah ketiga node berjalan, Ignite CLI dijalankan sebagai container (`apacheignite/ignite:3.1.0 cli`) dengan folder `sql` lokal di-*mount* ke `/opt/ignite/downloads/`. Saat CLI menawarkan koneksi ke `http://localhost:10300`, pilihan dijawab `n`, lalu CLI dihubungkan ke node 1 memakai nama container: `connect http://ignite3-node1-1:10300`. CLI menampilkan bahwa cluster belum diinisialisasi, sehingga cluster diinisialisasi dengan:

```
cluster init --name=ignite3 --metastorage-group=node1,node2,node3
```

CLI menampilkan `Cluster was initialized successfully`. Setelah cluster aktif, semua perubahan yang dikerjakan pada satu node direplikasi ke node lain dalam cluster yang sama.

![Cluster Ignite terinisialisasi](images/21-ignite-cluster-initialized.png)

**Menjalankan SQL.** Untuk menjalankan file SQL, CLI dijalankan dengan folder `sql` lokal di-*mount* ke `/opt/ignite/sql`, lalu file dieksekusi di node 1 dengan `sql --file=/opt/ignite/sql/<nama-file>`. Urutan yang dijalankan:

| Urutan | File | Keluaran (`Updated ... rows`) |
|---|---|---|
| 1 | `schema.sql` (membuat skema dan tabel) | `Updated 0 rows.` untuk setiap perintah DDL |
| 2 | `current_catalog.sql` | 275 dan 347 baris |
| 3 | `ee_and_cust.sql` | 8 dan 59 baris |
| 4 | `invoices.sql` | 412 baris, kemudian beberapa kali 1000 baris, 240, 18, dan terakhir 715 baris |
| 5 | `media_and_genre.sql` | 25 dan 5 baris |
| 6 | `tracks.sql` | beberapa kali 1000 baris |

Perintah DDL pada `schema.sql` melaporkan `Updated 0 rows` karena hanya membuat struktur (tabel), belum memasukkan data. Data baru masuk saat file-file berikutnya dijalankan.

![Skema dijalankan](images/22-ignite-schema-executed.png)

![Memuat data SQL](images/23-ignite-load-sql-data.png)

Setelah masuk ke mode SQL (`sql`), query `SELECT TABLE_NAME FROM SYSTEM.TABLES WHERE SCHEMA_NAME = 'PUBLIC';` menampilkan sebelas tabel yang dibuat: `ALBUM`, `PLAYLISTTRACK`, `TRACK`, `CUSTOMER`, `MEDIATYPE`, `PLAYLIST`, `ARTIST`, `INVOICELINE`, `EMPLOYEE`, `GENRE`, dan `INVOICE`.

![Tabel yang dibuat](images/24-ignite-tables-created.png)

**Pengecekan di node lain.** Data hanya dimasukkan lewat node 1. Untuk memeriksa apakah data sampai ke node lain, CLI dihubungkan ke node 2 dan node 3 (prompt CLI berubah menjadi `[node2]` dan `[node3]`).

- **Node 2.** `SELECT COUNT(*) FROM Invoice;` menghasilkan **412** baris. Query ringkasan penjualan bulanan juga menghasilkan data, misalnya bulan 2024-12 dengan 7 invoice, pendapatan 38.62, dan rata-rata 5.5171428571428571, serta bulan 2024-11 dengan pendapatan 49.62.

![Jumlah invoice di node 2](images/25-ignite-node2-invoice-count.png)

![Ringkasan penjualan bulanan di node 2](images/26-ignite-node2-monthly-sales.png)

- **Node 3.** `SELECT COUNT(*) FROM Invoice;` juga menghasilkan **412** baris, dan hasil query ringkasan penjualan bulanan sama dengan node 2 (nilai pendapatan 38.62, 49.62, dan 37.62 untuk bulan-bulan berikutnya).

![Jumlah invoice di node 3](images/27-ignite-node3-invoice-count.png)

![Ringkasan penjualan bulanan di node 3](images/28-ignite-node3-monthly-sales.png)

Jumlah invoice (412) di node 2 dan node 3 sama dengan jumlah baris pertama yang dimuat oleh `invoices.sql` di node 1 (`Updated 412 rows`), dan hasil query analitiknya identik di kedua node. Ini menunjukkan bahwa seluruh node berisi data yang sama, sehingga replikasi master-master pada cluster Apache Ignite 3.1.0 berfungsi.

Terakhir, seluruh node Ignite dimatikan dan dihapus. `docker ps -a` tidak lagi menampilkan container `ignite3-node1-1`, `ignite3-node2-1`, maupun `ignite3-node3-1`. Container yang tersisa adalah container PostgreSQL (berstatus *Up* kembali karena kebijakan `restart: always`) dan `hello-world` yang sudah *Exited*.

![Semua node Ignite dihentikan](images/29-ignite-all-nodes-stopped.png)

**Pembahasan Apache Ignite.**

- **Inisialisasi cluster.** Perintah `cluster init` memilih node-node yang menjadi *metastorage group* (di sini `node1`, `node2`, dan `node3`), yaitu kelompok node yang menyimpan metadata cluster. Setelah `cluster init` berhasil, ketiga node berfungsi sebagai satu cluster.
- **Memuat data lewat satu node.** Seluruh file SQL hanya dijalankan di node 1. Cluster yang meneruskan skema dan data ke node lain, sehingga tidak perlu menjalankan SQL di setiap node.
- **Bukti dari angka.** File `invoices.sql` melaporkan `Updated 412 rows` pada pemuatan pertama, dan `SELECT COUNT(*) FROM Invoice` di node 2 serta node 3 sama-sama menghasilkan 412. Angka yang sama di tiga node menunjukkan data yang dimasukkan lewat satu node benar-benar tersedia di node lain.
- **Pengecekan di node 2 dan node 3.** Jumlah baris `Invoice` dan hasil query analitik di kedua node sama dengan data yang dimasukkan lewat node 1. Ini membuktikan setiap node dalam cluster dapat melayani query atas data yang sama, tanpa langkah promosi seperti pada PostgreSQL.

**Perbandingan dengan streaming replication PostgreSQL.**

| Aspek | PostgreSQL (primary-replica) | Apache Ignite 3 (master-master) |
|---|---|---|
| Node yang menerima penulisan | Hanya primary | Semua node dalam cluster |
| Peran replica | Hanya baca (*read-only*) | Setiap node dapat dipakai untuk baca dan tulis |
| Jika node utama mati | Replica harus dipromosikan manual (`pg_promote()`) | Cluster tetap melayani selama node yang tersisa memadai |
| Cara replikasi | Streaming WAL (asinkron) | Replikasi data antarnode dalam cluster |
| Kompleksitas konfigurasi | Perlu slot, user replikasi, dan `pg_basebackup` | Cukup `cluster init` setelah node berjalan |

Hasil praktikum menunjukkan bahwa model master-master memudahkan pemakaian karena tidak ada pembagian peran primary dan replica yang kaku. Namun, pengujian ini hanya memverifikasi pembacaan data yang konsisten di tiga node. Perilaku saat terjadi penulisan bersamaan di beberapa node tidak diuji pada praktikum ini.

## 5. Kendala dan Solusi

**1. Docker Desktop menampilkan "Virtual Machine Platform is not enabled".** Fitur *Virtual Machine Platform* sudah diaktifkan oleh `wsl --install`, tetapi baru berlaku setelah Windows di-*restart*. Solusinya: restart Windows (bukan hanya menutup Docker Desktop), lalu buka kembali Docker Desktop.

<!-- Jika file screenshot ada, hapus tanda komentar pada baris di bawah.
![Error Virtual Machine Platform](images/03a-docker-error-vmp.png)
-->

**2. Skrip `env.ps1` tidak dapat dijalankan** (*running scripts is disabled on this system*). PowerShell memblokir skrip secara default. Solusinya: `Set-ExecutionPolicy -Scope Process Bypass`, yang hanya berlaku di jendela PowerShell yang sedang dipakai.

<!-- Jika file screenshot ada, hapus tanda komentar pada baris di bawah.
![Error execution policy](images/06d-error-execution-policy.png)
-->

**3. Container replica berstatus `unhealthy` setelah Docker dijalankan ulang.** Log replica menampilkan `pg_basebackup: error: directory "/var/lib/postgresql/18/docker" exists but is not empty` yang berulang. Penyebabnya, command replica pada modul selalu menjalankan `pg_basebackup`, padahal folder data sudah berisi hasil backup sebelumnya ketika container menyala kembali (`restart: always`). `pg_basebackup` menolak folder yang tidak kosong, sehingga PostgreSQL replica tidak pernah dijalankan.

Solusinya, command replica diubah agar `pg_basebackup` hanya dijalankan jika file `PG_VERSION` belum ada. Jika data sudah ada, PostgreSQL langsung dijalankan sebagai standby. Setelah perbaikan, log menampilkan `Data directory already exists, skipping pg_basebackup...`, lalu `entering standby mode` dan `started streaming WAL from primary`, dan replica kembali berstatus healthy (terlihat pada `docker ps` di bagian High Availability).

<!-- Jika file screenshot ada, hapus tanda komentar pada baris di bawah.
![Replica unhealthy](images/06e-replica-unhealthy.png)

![Log error pg_basebackup](images/06f-log-replica-error.png)
-->

![Replica setelah diperbaiki](images/06g-replica-diperbaiki.png)

**4. `docker ps` gagal dengan pesan `failed to connect to the docker API`.** Pesan ini muncul ketika Docker Desktop belum berjalan sehingga daemon belum aktif. Solusinya: buka Docker Desktop, tunggu status *Engine running*, lalu jalankan perintah lagi.

**5. Koneksi Ignite CLI memakai nama container, bukan `localhost`.** CLI dijalankan sebagai container sehingga koneksi ke node dilakukan dengan nama container di jaringan Docker (`http://ignite3-node1-1:10300`), bukan dengan `localhost` seperti pada modul.

## 6. Kesimpulan

1. Streaming replication PostgreSQL mengalirkan WAL dari primary ke replica secara terus-menerus, dan hasilnya terlihat pada `pg_stat_replication` (`state = streaming`) serta tabel yang dibuat di primary muncul otomatis di replica.
2. Replica berjalan dalam mode recovery sehingga hanya melayani akses baca, dan penulisan langsung ke replica ditolak.
3. Primary yang mati dapat digantikan dengan mempromosikan replica memakai `pg_promote()`. Karena replikasi bersifat asinkron, ada risiko kehilangan data yang belum diterima replica.
4. Pada cluster Apache Ignite 3 dengan tiga node, data yang dimasukkan lewat satu node dapat dibaca dari node lain, sehingga replikasi master-master berfungsi.
5. Penggunaan Docker Compose mempermudah pembuatan lingkungan replikasi, tetapi konfigurasi perlu memperhatikan keadaan container saat dijalankan ulang, seperti terlihat pada kendala `pg_basebackup`.

## 7. Referensi

1. Materi Praktikum Sistem Terdistribusi dan Terdesentralisasi, Modul 04: Konsistensi dan Replikasi pada Sistem Terdistribusi.
2. Eremeykin, "How to set up single primary PostgreSQL replication with Docker Compose". https://medium.com/@eremeykin/how-to-setup-single-primary-postgresql-replication-with-docker-compose-98c48f233bbf
3. Dokumentasi PostgreSQL, *High Availability, Load Balancing, and Replication*. https://www.postgresql.org/docs/current/high-availability.html
4. Dokumentasi Apache Ignite 3. https://ignite.apache.org/docs/ignite3/latest/index
5. Dokumentasi Docker Compose. https://docs.docker.com/compose/
