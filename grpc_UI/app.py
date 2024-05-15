from flask import Flask, request, jsonify, render_template
import grpc
import absensi_pb2
import absensi_pb2_grpc
from pymongo import MongoClient
from bson.objectid import ObjectId

# Inisialisasi koneksi ke server gRPC
channel = grpc.insecure_channel('localhost:50051')
absensi_stub = absensi_pb2_grpc.AbsensiServiceStub(channel)

# Inisialisasi koneksi ke MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['admin']  # Ganti 'nama_database' dengan nama database Anda
collection = db['absensi']  # Ganti 'nama_koleksi' dengan nama koleksi Anda

app = Flask(__name__, template_folder='public')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/landing_page')
def landing_():
    return render_template('landing_page.html')

@app.route('/contact_info')
def contact_():
    return render_template('contact_info.html')

@app.route('/create_absensi_masuk', methods=['POST', 'GET'])
def create_absensi_masuk():
    if request.method == 'POST':
        # Mengambil data dari form HTML
        nama_karyawan = request.form.get('nama_karyawan')
        tanggal = request.form.get('tanggal')
        divisi = request.form.get('divisi')
        waktu_masuk = request.form.get('waktu_masuk')

        # Panggil layanan gRPC untuk membuat entri absensi masuk
        response = absensi_stub.CreateAbsensiMasuk(
            absensi_pb2.Absensi(
                nama_karyawan=nama_karyawan,
                tanggal=tanggal,
                divisi=divisi,
                waktu_masuk=waktu_masuk
            )
        )
    return render_template('create_absensi_masuk.html')


@app.route('/create_absensi_pulang', methods=['POST', 'GET'])
def create_absensi_pulang():
    if request.method == 'POST':
        # Mengambil data dari form HTML
        nama_karyawan = request.form.get('nama_karyawan')
        tanggal = request.form.get('tanggal')
        waktu_keluar = request.form.get('waktu_keluar')

        # Panggil layanan gRPC untuk mencari ID absensi
        response_id = absensi_stub.SearchAbsensiIdByNamaKaryawanAndTanggal(
            absensi_pb2.AbsensiRequest(
                nama_karyawan=nama_karyawan,
                tanggal=tanggal
            )
        )

        # Jika ID absensi ditemukan, gunakan untuk membuat entri absensi pulang
        if response_id.id:
            response_pulang = absensi_stub.CreateAbsensiPulang(
                absensi_pb2.Absensi(
                    id=response_id.id,
                    waktu_keluar=waktu_keluar
                )
            )
        else:
            return "Absensi tidak ditemukan untuk karyawan dan tanggal tersebut."

    # Jika metode adalah GET, render halaman HTML untuk input data absensi pulang
    # Mulai dengan nilai ID kosong
    return render_template('create_absensi_pulang.html')
@app.route('/update_absensi', methods=['POST', 'GET'])
def update_absensi():
    if request.method == 'POST':
        # Mengambil data dari form HTML
        nama_karyawan = request.form.get('nama_karyawan')
        tanggal = request.form.get('tanggal')
        
        # Mencari ID absensi berdasarkan nama karyawan dan tanggal
        response_id = absensi_stub.SearchAbsensiIdByNamaKaryawanAndTanggal(
            absensi_pb2.AbsensiRequest(
                nama_karyawan=nama_karyawan,
                tanggal=tanggal
            )
        )
        
        if response_id.id:
            absensi_id = response_id.id
            
            # Mengirim permintaan untuk membaca data absensi yang saat ini tersimpan di database
            response_read = absensi_stub.ReadAbsensi(
                absensi_pb2.AbsensiRequest(
                    nama_karyawan=nama_karyawan,
                    tanggal=tanggal
                )
            )

            # Mendapatkan data absensi dari respons
            current_absensi = next(response_read, None)

            # Mengecek apakah data absensi ditemukan
            if current_absensi:
                # Memperbarui hanya bidang yang diubah
                bagian = request.form.get('bagian')
                nilai_baru = request.form.get('nilai_baru')
                
                absensi_update = absensi_pb2.Absensi(
                    id=absensi_id,
                    nama_karyawan=current_absensi.nama_karyawan,
                    tanggal=current_absensi.tanggal,
                    divisi=current_absensi.divisi,
                    waktu_masuk=current_absensi.waktu_masuk,
                    waktu_keluar=current_absensi.waktu_keluar
                )

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
                response = absensi_stub.UpdateAbsensi(absensi_update)
                
                # Mengirim data hasil update ke template HTML
                return render_template('update_absensi.html', response=response)

        else:
            return "Absensi tidak ditemukan untuk karyawan dan tanggal tersebut."

    # Jika metode adalah GET, render halaman HTML untuk input data absensi pulang
    return render_template('update_absensi.html')


@app.route('/read_absensi', methods=['POST', 'GET'])
def read_absensi():
    if request.method == 'POST':
        # Mengambil data dari form HTML
        nama_karyawan = request.form.get('nama_karyawan')
        tanggal = request.form.get('tanggal')
        
        # Mencari ID absensi berdasarkan nama karyawan dan tanggal
        response_id = absensi_stub.SearchAbsensiIdByNamaKaryawanAndTanggal(
            absensi_pb2.AbsensiRequest(
                nama_karyawan=nama_karyawan,
                tanggal=tanggal
            )
        )
        
        if response_id.id:
            absensi_id = response_id.id
            
            # Mengirim permintaan untuk membaca data absensi yang saat ini tersimpan di database
            response_read = absensi_stub.ReadAbsensi(
                absensi_pb2.AbsensiRequest(
                    nama_karyawan=nama_karyawan,
                    tanggal=tanggal
                )
            )

            # Mendapatkan data absensi dari respons
            absensi_list = []
            for current_absensi in response_read:
                absensi_list.append({
                    'id': current_absensi.id,
                    'nama_karyawan': current_absensi.nama_karyawan,
                    'tanggal': current_absensi.tanggal,
                    'divisi': current_absensi.divisi,
                    'waktu_masuk': current_absensi.waktu_masuk,
                    'waktu_keluar': current_absensi.waktu_keluar
                })

            return render_template('read_absensi.html', absensi_list=absensi_list)
        else:
            return "Absensi tidak ditemukan untuk karyawan dan tanggal tersebut."

    # Jika metode adalah GET, render halaman HTML untuk input data absensi pulang
    return render_template('read_absensi.html')

@app.route('/delete_absensi', methods=['POST', 'GET'])
def delete_absensi():
    if request.method == 'POST':
        # Mengambil data dari form HTML
        nama_karyawan = request.form.get('nama_karyawan')
        tanggal = request.form.get('tanggal')
        
        # Mencari ID absensi berdasarkan nama karyawan dan tanggal
        response_id = absensi_stub.SearchAbsensiIdByNamaKaryawanAndTanggal(
            absensi_pb2.AbsensiRequest(
                nama_karyawan=nama_karyawan,
                tanggal=tanggal
            )
        )
        
        if response_id.id:
            absensi_id = response_id.id
            
            # Menghapus absensi berdasarkan ID karyawan
            absensi_delete = absensi_pb2.AbsensiId(id=absensi_id)
            absensi_stub.DeleteAbsensi(absensi_delete)
    # Jika metode adalah GET, render halaman HTML untuk input data absensi pulang
    return render_template('delete_absensi.html')


if __name__ == '__main__':
    app.run(debug=True)
