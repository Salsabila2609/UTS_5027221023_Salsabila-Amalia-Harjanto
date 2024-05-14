import grpc
import absensi_pb2
import absensi_pb2_grpc

def create_absensi_masuk(stub):
    nama_karyawan = input("Nama karyawan: ")
    tanggal = input("Tanggal: ")
    divisi = input("Divisi: ")
    waktu_masuk = input("Waktu masuk: ")
    absensi_masuk = absensi_pb2.Absensi(
        nama_karyawan=nama_karyawan,
        tanggal=tanggal,
        divisi=divisi,
        waktu_masuk=waktu_masuk
    )
    response = stub.CreateAbsensiMasuk(absensi_masuk)
    print("Response:", response)

def create_absensi_pulang(stub):
    nama_karyawan = input("Nama karyawan: ")
    tanggal = input("Tanggal: ")
    waktu_keluar = input("Waktu keluar: ")

    # Memanggil fungsi pencarian ID absensi berdasarkan nama karyawan dan tanggal
    absensi_request = absensi_pb2.AbsensiRequest(nama_karyawan=nama_karyawan, tanggal=tanggal)
    response = stub.SearchAbsensiIdByNamaKaryawanAndTanggal(absensi_request)

    if response.id:
        absensi_pulang = absensi_pb2.Absensi(
            id=response.id,
            waktu_keluar=waktu_keluar
        )
        response_pulang = stub.CreateAbsensiPulang(absensi_pulang)
        print("Response:", response_pulang)
    else:
        print("Absensi tidak ditemukan untuk karyawan dan tanggal tersebut.")

def update_absensi(stub):
    nama_karyawan = input("Nama karyawan: ")
    tanggal = input("Tanggal: ")
    
    # Mencari ID absensi berdasarkan nama karyawan dan tanggal
    absensi_request = absensi_pb2.AbsensiRequest(nama_karyawan=nama_karyawan, tanggal=tanggal)
    response = stub.SearchAbsensiIdByNamaKaryawanAndTanggal(absensi_request)
    
    if response.id:
        absensi_id = response.id
        
        # Mengirim permintaan untuk membaca data absensi yang saat ini tersimpan di database
        response_read = stub.ReadAbsensi(absensi_request)

        # Mendapatkan data absensi dari respons
        current_absensi = next(response_read, None)

        # Mengecek apakah data absensi ditemukan
        if current_absensi:
            # Menampilkan seluruh data absensi
            print("Data Absensi:")
            print(current_absensi)

            # Meminta input bagian mana yang ingin diubah
            bagian = input("Pilih bagian yang ingin diubah (nama_karyawan/tanggal/divisi/waktu_masuk/waktu_keluar): ")
            if bagian in ["nama_karyawan", "tanggal", "divisi", "waktu_masuk", "waktu_keluar"]:
                nilai_baru = input(f"Masukkan nilai baru untuk {bagian}: ")

                # Membuat objek Absensi baru dengan nilai yang ada
                absensi_update = absensi_pb2.Absensi(
                    id=current_absensi.id,
                    nama_karyawan=current_absensi.nama_karyawan,
                    tanggal=current_absensi.tanggal,
                    divisi=current_absensi.divisi,
                    waktu_masuk=current_absensi.waktu_masuk,
                    waktu_keluar=current_absensi.waktu_keluar
                )

                # Memperbarui hanya bidang yang diubah
                if bagian == "nama_karyawan":
                    absensi_update.nama_karyawan = nilai_baru
                elif bagian == "tanggal":
                    absensi_update.tanggal = nilai_baru
                elif bagian == "divisi":
                    absensi_update.divisi = nilai_baru
                elif bagian == "waktu_masuk":
                    absensi_update.waktu_masuk = nilai_baru
                elif bagian == "waktu_keluar":
                    absensi_update.waktu_keluar = nilai_baru

                # Mengirim permintaan pembaruan ke server
                response = stub.UpdateAbsensi(absensi_update)
                print("Response:", response)
            else:
                print("Bagian yang dipilih tidak valid.")
        else:
            print("Absensi tidak ditemukan untuk karyawan dan tanggal tersebut.")
    else:
        print("Absensi tidak ditemukan untuk karyawan dan tanggal tersebut.")

def read_absensi(stub):
    nama_karyawan = input("Nama karyawan: ")
    tanggal = input("Tanggal: ")
    
    # Mencari ID absensi berdasarkan nama karyawan dan tanggal
    absensi_request = absensi_pb2.AbsensiRequest(nama_karyawan=nama_karyawan, tanggal=tanggal)
    response = stub.SearchAbsensiIdByNamaKaryawanAndTanggal(absensi_request)
    
    if response.id:
        absensi_id = response.id
        
        # Mengirim permintaan untuk membaca data absensi yang saat ini tersimpan di database
        response_read = stub.ReadAbsensi(absensi_request)

        # Mendapatkan data absensi dari respons
        current_absensi = next(response_read, None)

        # Mengecek apakah data absensi ditemukan
        if current_absensi:
            # Menampilkan seluruh data absensi
            print("Data Absensi:")
            print(current_absensi)
    else:
        print("Absensi tidak ditemukan untuk karyawan dan tanggal tersebut.")

def delete_absensi(stub):
    nama_karyawan = input("Nama karyawan: ")
    tanggal = input("Tanggal: ")
    
    # Mencari ID absensi berdasarkan nama karyawan dan tanggal
    absensi_request = absensi_pb2.AbsensiRequest(nama_karyawan=nama_karyawan, tanggal=tanggal)
    response = stub.SearchAbsensiIdByNamaKaryawanAndTanggal(absensi_request)
    
    if response.id:
        absensi_id = response.id
        
        # Menghapus absensi berdasarkan ID karyawan
        absensi_delete = absensi_pb2.AbsensiId(id=absensi_id)
        response_delete = stub.DeleteAbsensi(absensi_delete)
        print("Response:", response_delete)
    else:
        print("Absensi tidak ditemukan untuk karyawan dan tanggal tersebut.")

def main():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = absensi_pb2_grpc.AbsensiServiceStub(channel)
        command = input("Masukkan nomor opsi yang diinginkan: ")
        if command == "1":
            create_absensi_masuk(stub)
        elif command == "2":
            create_absensi_pulang(stub)
        elif command == "3":
            update_absensi(stub)
        elif command == "4":
            read_absensi(stub)
        elif command == "5":
            delete_absensi(stub)
        else:
            print("Invalid command")

if __name__ == '__main__':
    main()
