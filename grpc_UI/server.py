import grpc
import absensi_pb2
import absensi_pb2_grpc
from concurrent import futures
from pymongo import MongoClient
from bson.objectid import ObjectId

class AbsensiService(absensi_pb2_grpc.AbsensiServiceServicer):

    def __init__(self):
        # Connect to MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['admin']  # Ganti 'nama_database' dengan nama database Anda
        self.collection = self.db['absensi']  # Ganti 'absensi' dengan nama koleksi Anda

    def CreateAbsensiMasuk(self, request, context):
        absensi_data = {
            "nama_karyawan": request.nama_karyawan,
            "tanggal": request.tanggal,
            "divisi": request.divisi,
            "waktu_masuk": request.waktu_masuk
        }
        result = self.collection.insert_one(absensi_data)
        inserted_id = str(result.inserted_id)  # Ambil _id dari MongoDB dan konversi ke string

        # Kirim kembali respons dengan bidang "_id" yang dimasukkan
        response = absensi_pb2.Absensi(
            id=inserted_id,
            nama_karyawan=request.nama_karyawan,
            tanggal=request.tanggal,
            divisi=request.divisi,
            waktu_masuk=request.waktu_masuk
        )
        return response
    
    def CreateAbsensiPulang(self, request, context):
        filter_query = {"_id": ObjectId(request.id)}  # Ubah id ke ObjectId
        update_query = {"$set": {"waktu_keluar": request.waktu_keluar}}
        result = self.collection.update_one(filter_query, update_query)
        if result.modified_count == 0:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Absensi masuk belum dibuat untuk karyawan pada tanggal tersebut.")
            return absensi_pb2.Absensi()
        else:
            # Ambil _id dari MongoDB dan konversi ke string
            response = absensi_pb2.Absensi(id=request.id, waktu_keluar=request.waktu_keluar)
            return response

    def UpdateAbsensi(self, request, context):
        filter_query = {"_id": ObjectId(request.id)}  # Ubah id ke ObjectId
        update_query = {
            "$set": {
                "nama_karyawan": request.nama_karyawan,
                "tanggal": request.tanggal,
                "divisi": request.divisi,
                "waktu_masuk": request.waktu_masuk,
                "waktu_keluar": request.waktu_keluar
            }
        }
        result = self.collection.find_one_and_update(filter_query, update_query, return_document=True)
        if result is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Absensi tidak ditemukan.")
            return absensi_pb2.Absensi()
        else:
            response = absensi_pb2.Absensi(
                id=request.id,
                nama_karyawan=result['nama_karyawan'],
                tanggal=result['tanggal'],
                divisi=result['divisi'],
                waktu_masuk=result['waktu_masuk'],
                waktu_keluar=result['waktu_keluar']
            )
            return response

    def ReadAbsensi(self, request, context):
        cursor = self.collection.find({"nama_karyawan": request.nama_karyawan, "tanggal": request.tanggal})
        for absensi_data in cursor:
            # Ambil _id dari MongoDB dan konversi ke string
            absensi_data['_id'] = str(absensi_data['_id'])
            yield absensi_pb2.Absensi(
                id=absensi_data['_id'],
                nama_karyawan=absensi_data['nama_karyawan'],
                tanggal=absensi_data['tanggal'],
                divisi=absensi_data['divisi'],
                waktu_masuk=absensi_data['waktu_masuk'],
                waktu_keluar=absensi_data['waktu_keluar']
            )

    def DeleteAbsensi(self, request, context):
        filter_query = {"_id": ObjectId(request.id)}  # Ubah id ke ObjectId
        result = self.collection.delete_one(filter_query)
        if result.deleted_count == 0:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Absensi tidak ditemukan.")
            return absensi_pb2.Absensi()
        else:
            return absensi_pb2.Absensi(id=request.id)
        
    def SearchAbsensiIdByNamaKaryawanAndTanggal(self, request, context):
        filter_query = {
            "nama_karyawan": request.nama_karyawan,
            "tanggal": request.tanggal
        }
        result = self.collection.find_one(filter_query)
        if result:
            return absensi_pb2.AbsensiId(id=str(result['_id']))
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Absensi tidak ditemukan.")
            return absensi_pb2.AbsensiId()
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    absensi_pb2_grpc.add_AbsensiServiceServicer_to_server(AbsensiService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
