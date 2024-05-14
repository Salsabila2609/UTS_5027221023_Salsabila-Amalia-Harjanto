| Nama | NRP | Kelas |
| ----------- | ----------- | ----------- |
| Salsabila Amalia Harjanto | 5027221023 | Integrasi SIstem B |

# Sistem Manajemen Absensi Karyawan
> Pada project ini, saya membuat sistem manajemen absensi karyawan dengan nama **AttendEase** yang menggunakan protokol gRPC Protobuf untuk komunikasi antara klien dan server.
> Project ini juga menggunakan koneksi ke MongoDB untuk menyimpan data hasil CRUD (Create, Read, Delete, Update).

---

## Proto
- Message (Pesan): Struktur data yang akan digunakan untuk berkomunikasi antara klien dan server.
- Service (Layanan): AbsensiService adalah layanan yang didefinisikan di sini. Layanan ini menyediakan beberapa operasi yang dapat dipanggil oleh klien. Setiap operasi memiliki input dan output yang sesuai dengan pesan yang didefinisikan sebelumnya.
- RPC (Remote Procedure Call): Ada enam operasi RPC yang didefinisikan di dalam layanan AbsensiService:
  - CreateAbsensiMasuk: Operasi untuk membuat catatan absensi saat karyawan masuk.
  - CreateAbsensiPulang: Operasi untuk membuat catatan absensi saat karyawan pulang.
  - UpdateAbsensi: Operasi untuk memperbarui catatan absensi.
  - ReadAbsensi: Operasi untuk membaca catatan absensi berdasarkan permintaan tertentu.
  - DeleteAbsensi: Operasi untuk menghapus catatan absensi.
  - SearchAbsensiIdByNamaKaryawanAndTanggal: Operasi untuk mencari ID absensi berdasarkan nama karyawan dan tanggal.
    
Setelah melakukan compiling untuk file .proto, dihasilkan 2 file baru:
- absensi_pb2.py: Kode dalam file ini mengatur cara membaca, menulis, dan memanipulasi pesan-pesan Protobuf. Kelas-kelas yang didefinisikan dalam file ini digunakan untuk membuat, mengisi, dan membaca pesan-pesan Protobuf di sisi klien dan server.
- absensi_pb2_grpc.py: File ini menyediakan kelas-kelas dan fungsi-fungsi yang dibutuhkan untuk membuat, menginisialisasi, dan menggunakan layanan gRPC yang didefinisikan. Kelas-kelas dan fungsi-fungsi dalam file ini digunakan untuk mengimplementasikan dan menggunakan layanan gRPC di sisi klien dan server Anda.

---

## Server.py
- Kelas AbsensiService: Ini adalah kelas yang berfungsi sebagai implementasi layanan gRPC. Ini mengimplementasikan metode-metode yang didefinisikan dalam absensi_pb2_grpc.AbsensiServiceServicer. Setiap metode yang didefinisikan di sini adalah implementasi dari operasi yang didefinisikan dalam layanan gRPC Anda.
- CreateAbsensiMasuk(self, request, context):  Data absensi yang diterima dari klien dalam bentuk objek request kemudian dimasukkan ke dalam database MongoDB. Setelah itu, ID unik dari catatan absensi yang baru dibuat dikirimkan kembali ke klien sebagai respons.
- CreateAbsensiPulang(self, request, context): Fungsi ini mencari catatan absensi dengan ID yang sesuai dalam database MongoDB dan memperbarui waktu keluarnya. Jika catatan berhasil diperbarui, fungsi mengirimkan respons yang berisi ID catatan absensi yang telah diperbarui dan waktu keluarnya.
- UpdateAbsensi(self, request, context): Fungsi menerima permintaan dari klien berupa data absensi yang sudah termasuk ID catatan absensi yang akan diperbarui. Kemudian, fungsi ini mencari catatan absensi dengan ID yang sesuai dalam database MongoDB dan memperbarui atribut-atributnya sesuai dengan data yang diterima dari klien. Setelah perubahan berhasil diterapkan, fungsi mengirimkan respons yang berisi detail catatan absensi yang diperbarui ke klien.
- ReadAbsensi(self, request, context): Fungsi menerima permintaan dari klien berupa data absensi yang berisi nama karyawan dan tanggal. Kemudian, fungsi ini mencari catatan absensi yang sesuai dalam database MongoDB berdasarkan kriteria yang diberikan, dan mengirimkan catatan absensi yang ditemukan satu per satu sebagai respons kepada klien menggunakan yield.
- DeleteAbsensi(self, request, context):  Fungsi menerima permintaan dari klien berupa ID catatan absensi yang akan dihapus. Kemudian, fungsi ini mencari catatan absensi dengan ID yang sesuai dalam database MongoDB dan menghapusnya. Jika catatan berhasil dihapus, fungsi mengirimkan respons yang berisi ID catatan absensi yang telah dihapus kepada klien. 
- SearchAbsensiIdByNamaKaryawanAndTanggal(self, request, context): Fungsi menerima permintaan dari klien berupa nama karyawan dan tanggal. Kemudian, fungsi ini mencari catatan absensi yang sesuai dalam database MongoDB berdasarkan kriteria yang diberikan, dan mengirimkan ID catatan absensi yang ditemukan sebagai respons kepada klien. 
- Metode serve(): Ini adalah metode yang digunakan untuk menjalankan server gRPC. Ini membuat server, menambahkan implementasi layanan AbsensiService ke dalamnya, menentukan port untuk server, dan kemudian menjalankan server.
- Main Block: Ini adalah bagian kode yang akan dijalankan saat file ini dieksekusi langsung. Ini memanggil metode serve() untuk memulai server gRPC.

---

## App.py
- Import Library dan Modul: Pada bagian ini, beberapa modul diimpor, termasuk Flask untuk pembangunan web, grpc untuk berkomunikasi dengan server gRPC, serta absensi_pb2 dan absensi_pb2_grpc yang berisi definisi pesan dan layanan gRPC yang sudah Anda buat sebelumnya.
- Inisialisasi Koneksi: Koneksi ke server gRPC dan database MongoDB diinisialisasi. Koneksi ke server gRPC dilakukan melalui grpc.insecure_channel() dengan mengatur alamat dan port server. Koneksi ke MongoDB dilakukan dengan menggunakan MongoClient() dan menentukan host dan port MongoDB.
  
Fungsi-fungsi Route Flask:
- /: Route ini menampilkan halaman utama aplikasi web.
- /landing_page: Route ini menampilkan halaman untuk landing page.
- /contact_info: Route ini menampilkan halaman dengan informasi kontak.
- /create_absensi_masuk: Route ini menangani pembuatan catatan absensi saat karyawan masuk. Data absensi dikirim melalui form HTML, kemudian diproses dan disimpan menggunakan layanan gRPC.
- /create_absensi_pulang: Route ini menangani pembuatan catatan absensi saat karyawan pulang. Setelah mendapatkan ID absensi berdasarkan nama karyawan dan tanggal, waktu keluar dikirim melalui form HTML, kemudian diproses dan disimpan menggunakan layanan gRPC.
- /update_absensi: Route ini menangani pembaruan catatan absensi yang sudah ada. Setelah mendapatkan ID absensi berdasarkan nama karyawan dan tanggal, data yang ingin diperbarui dikirim melalui form HTML, kemudian diproses dan disimpan menggunakan layanan gRPC.
- /read_absensi: Route ini menampilkan catatan absensi berdasarkan nama karyawan dan tanggal yang dimasukkan. Data absensi diperoleh melalui layanan gRPC dan ditampilkan di halaman HTML.
- /delete_absensi: Route ini menangani penghapusan catatan absensi berdasarkan nama karyawan dan tanggal yang dimasukkan. Setelah mendapatkan ID absensi berdasarkan nama karyawan dan tanggal, catatan tersebut dihapus menggunakan layanan gRPC.
- Main Block: Pada bagian ini, aplikasi Flask dijalankan dengan memanggil app.run(). Debug mode diaktifkan untuk memudahkan debugging aplikasi.

---

## Cara menjalankan
1. Connect ke MongoDB compass
2. Buka folder grpc_UI
3. Jalankan server.py menggunakan command:
   ```
   python server.py
   ```
4. Jalankan app.py menggunakan command:
   ```
   python app.py
   ```
5. Buka aplikasi web.
6. Melakukan operasi CRUD pada aplikasi web.

---
