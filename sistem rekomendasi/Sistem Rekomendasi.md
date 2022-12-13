# Sistem Rekomendasi Destinasi Wisata Kota Semarang

## Project Overview
Wabah pandemi Covid-19 telah menginfeksi hampir seluruh belahan dunia yang berdampak pada semua sektor, mulai dari politik, sosial, ekonomi, maupun pariwisata. Dampak dari pandemi ini sangat dirasakan khususnya UMKM dan pariwisata karena sektor tersebut memiliki pengaruh yang sangat besar terhadap pertumbuhan ekonomi [[1]](http://jurnal.ft.umi.ac.id/index.php/losari/article/view/76). 

Setelah kurang lebih 2 tahun pandemi Covid-19 ini melanda, saat ini pemerintah telah memperbolehkan hampir semua sektor yang terdampak pandemi Covid-19 untuk beroperasi kembali salah satunya sektor pariwisata. Melihat antusias masyarakat yang sangat tinggi untuk mengunjungi tempat-tempat wisata ini menjadi momentum yang baik untuk pemulihan ekonomi negara maupun masyarakat.

Pada proyek ini saya membuat sistem rekomendasi berbasis *Collaborative Based Filtering* untuk menampilkan top-n recommendation destinasi wisata yang ada di Kota Semarang. Saya memilih Kota Semarang karena merupakan salah satu kota besar yang ada di Indonesia dan memiliki banyak tempat wisata. Diharapkan sistem rekomendasi ini mempermudah wisatawan untuk menentukan destinasi wisata yang ingin dikunjungi.

## Business Understanding
#### Problem Statements
- Bagaimana cara membuat sistem yang dapat merekomendasikan tempat wisata di suatu Kota?
- Bagaimana cara mendapatkan rekomendasi tempat wisata berdasarkan data pada user sebelumnya?
#### Goals
- Mengetahui cara membuat sistem yang dapat merekomendasikan tempat wisata di suatu Kota.
- Mengetahui cara mendapatkan rekomendasi tempat wisata berdasarkan data pada user sebelumnya.
#### Solution Statements
- Menggunakan *Collaborative Based Filtering* untuk mendapatkan rekomendasi tempat wisata.

## Data Understanding
Dataset yang digunakan untuk proyek ini dapat diunduh pada [[2]](https://www.kaggle.com/aprabowo/indonesia-tourism-destination). Dataset ini berisi beberapa tempat wisata di 5 kota besar di Indonesia yaitu Jakarta, Yogyakarta, Semarang, Bandung, dan Surabaya yang dihimpun sejak Mei 2021. Dataset ini terdiri dari 3 jenis data antara lain:
- Tourism_with_id.csv – berisi informasi tempat wisata di 5 Kota Besar di Indonesia
    - Place_Id (int) - berisi id unique tempat wisata
    - Place_Name (str) - berisi nama tempat wisata
    - Description (str) - berisi deskripsi dari tempat wisata
    - Category (str) - berisi kategori tempat wisata (Cagar Alam, Budaya, Taman Hiburan - Tempat Ibadah, Pusat Perbelanjaan)
    - City (str) - berisi nama kota dari tempat wisata
    - Price (int) - berisi harga masuk dari tempat wisata
    - Rating (float) - berisi rating rata-rata dari tempat wisata 
    - Lat (float) - berisi latitude dari tempat wisata
    - Long float) - berisi longitude dari tempat wisata.
- User.csv – berisi informasi pengguna
    - User_Id (int) - berisi id unique dari user
    - Location (str) - berisi asal kota dan provinsi dari user
    - Age (int) - berisi usia dari user.
- Tourism_rating.csv – berisi informasi pengguna, tempat wisata, dan rating
    - User_Id  (int) - berisi id dari user (turunan dari user.csv)
    - Place_Id (int) - berisi id tempat wisata yang diberi ratingnya oleh user
    - Place_Ratings (float) - berisi rating yang diberi oleh user terhadap PlaceId.

- Rating terbanyak tempat wisata di Kota Semarang dipimpin oleh Pantai Marina dan Grand Maerakaca seperti terlihat pada Gambar 1.

![1](https://raw.githubusercontent.com/affdn/sistem-rekomendasi/main/1.PNG)

Gambar 1. Wisata dengan jumlah rating terbanyak

- Kategori wisata di Kota Semarang didominasi oleh cagar alam lalu diikuti oleh kategori budaya dan taman hiburan terlihat pada Gambar 2.

![2](https://raw.githubusercontent.com/affdn/sistem-rekomendasi/main/2.PNG)

Gambar 2. Jumlah kategori wisata

- Pengunjung tempat wisata di Kota Semarang berusia sekitar 24 tahun hingga 34 tahun seperti yang ditunjukkan Gambar 4.

![3](https://raw.githubusercontent.com/affdn/sistem-rekomendasi/main/3.PNG)

Gambar 3. Distribusi usia user

- Harga masuk tempat wisata tertinggi di Kota Semarang sekitar Rp.25000 dan untuk harga termurah dibawah Rp.5000 seperti terlihat pada Gambar 4.

![4](https://raw.githubusercontent.com/affdn/sistem-rekomendasi/main/4.PNG)

Gambar 4. Distribusi harga masuk tempat wisata

- Pengunjung tempat wisata di Kota Semarang didominasi oleh pengunjung asal Bekasi diikuti Semarang dan beberapa daerah Jawa lain seperti terlihat pada Gambar 5.

![5](https://raw.githubusercontent.com/affdn/sistem-rekomendasi/main/5.PNG)

Gambar 5. Asal kota dari user

## Data Preparation
Berikut adalah langkah-langkah yang saya lakukan untuk mempersiapkan data:
- Preprocessing Data
    - Membuang kolom yang tidak digunakan, seperti kolom ‘Unnamed:11’, ’Unnamed: 12’, dan ‘Time_Minutes’ dari data tourism_with_id.csv.
    - Membuang tempat wisata yang bukan berasal dari Kota Semarang pada data tourism_with_id.csv.
    - Mencocokkan data user dan data rating agar hanya berisi tempat wisata di Kota Semarang pada data tourism_with_id.csv.
    - Membersihkan data duplikasi agar tidak muncul data yang sama sebanyak dua kali.
- Persiapan Data
    - Encoding label place dan user Ini dilakukan untuk memberi encode identifier kepada place dan user
    - Mapping label place dan user hasil encoding ke data rating setelah identifier dibuat, hasilnya dimasukan pada data tourism_rating.csv (rating) untuk persiapan memasuki tahap pemodelan
    - Normalisasi kolom rating Hal ini dilakukan agar rentang nilai pada label numerik hanya antara 0-1 sehingga dapat mempercepat komputasinya menggunakan *MinMaxScaler* dari *sklearn*.
## Modeling
Setelah dilakukan prepocessing data, selanjutnya membuat sistem rekomendasi *Collaborative Based Filtering*. Tahapan yang dilakukan pada *Collaborative Based Filtering* adalah:
- Membagi dataset menjadi train dan validation dengan persentase 80% data train dan 20% data validasi.
- Menginisialiasasi model RecommenderNet, pada proses ini dilakukan proses embedding terhadap data user dan place setelah itu dilakukan perkalian dot product antara embedding user dan place serta menambahkan bias untuk setiap user dan place. Skor kecocokkannya ditetapkan dalam skala [0,1] dengan fungsi aktivasi sigmoid melalui Class RecommenderNet
- Menginisialisasi *callbacks* untuk menghentikan proses pelatihan apabila nilai validasi <25%
- Melakukan training dengan model *RecommenderNet* setelah itu model decompile dengan Binary Crossentropy untuk menghitung *loss function*, Adam untuk optimizer, dan *RMSE* sebagai matriks evaluation
- Melakukan rekomendasi berdasarkan hasil encoded suatu User_Id, proses rekomendasi tersebut dilakukan dengan cara mengambil satu sampel user untuk dicari tempat wisata mana saja yang pernah dikunjungi kemudian User_Id dari user tersebut diambil untuk dicari hasil encodingnya dan dijadikan data testing dari model sebelumnya, setelah itu akan menghasilkan prediksi tempat wisata dan diurutkan untuk user tersebut.

Hasil rekomendasi dari salah satu user dapat dilihat pada Tabel 1.

Tabel 1. Hasil rekomendasi

Top 5 rekomendasi tempat wisata di Kota Semarang
| No | Nama Lokasi              | Kategori      | Harga Tiket | Rating |
|----|--------------------------|---------------|-------------|--------|
| 1  | Monumen Palagan Ambarawa | Budaya        | 7500        | 4.4    |
| 2  | Wisata Eling Bening      | Cagar Alam    | 25000       | 4.3    |
| 3  | Gua Maria Kerep Ambarawa | Cagar Alam    | 2000        | 4.8    |
| 4  | La Kana Chapel           | Taman Hiburan | 3500        | 4.5    |
| 5  | Kampoeng Kopi Banaran    | Taman Hiburan | 20000       | 4.3    |

## Evaluation
Proses evaluasi dilakukan untuk mengukur kinerja model RecommenderNet dengan menggunakan matriks *Root Mean Squared Error (RMSE)*. Matriks ini memprediksi Place_Ratings yang dinormalisasi berdasarkan User_Id dan Place_Id yang telah diencoded.

RMSE dihitung dengan cara mengkuadratkan error dari (predicted – observed) lalu dibagi jumlah data (n) setelah itu diakarkan. Formula matematisnya ditulis sebagai berikut:

$$ RMSE = \sqrt \frac {\Sigma({y}_i - \hat{y}_i)}{n}$$

Keterangan :

${RMSE}$ = nilai bobot root mean square error

${y}$ = nilai hasil observasi

$\hat{y}$ = nilai hasil prediksi

${i}$ = urutan data pada database

${n}$ = jumlah data

RMSE yang didapat pada model collaborative filtering ini berkisar 0.3725 dan sudah cukup untuk menampilkan hasil rekomendasi yang sesuai.

## Conclusion
Berdasarkan model yang telah dibuat, model ini dapat menampilkan 5 rekomendasi teratas tempat wisata di Kota Semarang. Model ini diharapkan dapat mempermudah wisatawan untuk mendapatkan tempat wisata di Kota Semarang dan meningkatkan jumlah wisatawan di Kota Semarang.

## References
Gunagama, M. G., Naurah, Y. R., Prabono, A. E. P., Arsitektur, D. J., Indonesia,
U. I., Arsitektur, M. J., Indonesia, U. I., Arsitektur, M. J., & Indonesia, U. I.
(2020). Pariwisata Pascapandemi: Pelajaran Penting dan Prospek
Pengembangan. LOSARI : Jurnal Arsitektur, Kota Dan Permukiman, 5(2), 56–68.




