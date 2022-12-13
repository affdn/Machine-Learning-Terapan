# Laporan Proyek *Machine Learning* - Afifudin

## *Project Overview*

Dataset Titanic banyak digunakan oleh para data scientist pemula untuk mencoba membuat suatu proyek salah satunya yang dilakukan oleh Kaggle yang membuat kompetisi berjudul "Titanic – *Machine Learning from Disaster*”. 

RMS Titanic merupakan sebuah kapal penumpang yang berasal Britania Raya yang tenggelam di Samudra Atlantik Utara pada tanggal 15 April 1912 setelah menabrak sebuah gunung es pada pelayaran perdananya dari Southampton, Inggris ke New York City. Tenggelamnya Titanic merenggut 1514 nyawa penumpang dari total 2224 penumpang dan menjadi salah satu bencana maritim paling mematikan sepanjang sejarah [[1]](https://www.researchgate.net/profile/Rizkiana-Rahmadina/publication/341398068_Pre-processing_Data_dan_Analisis_MANOVA_One-Way_terhadap_Data_Kecelakaan_Kapal_Titanic/links/5efc1e45a6fdcc4ca4408eed/Pre-processing-Data-dan-Analisis-MANOVA-One-Way-terhadap-Data-Kecelakaan-Kapal-Titanic.pdf).

Pada proyek ini akan dibuat model untuk memprediksi penumpang lainnya apakah selamat atau tidak berdasarkan data train. Model yang akan digunakan untuk memprediksi masalah ini adalah model klasifikasi yaitu XGBClassifier.
## *Business Understanding*
#### *Problem Statements*
- Apakah para penumpang kapal RMS Titanic selamat atau tidak?
#### Goals
- Memprediksi keselamatan para penumpang kapal RMS Titanic?
#### *Solution Statements*
- Menggunakan  Exploratory Data Analysis (EDA) untuk melihat fitur – fitur yang berkorelasi dan berpengaruh terhadap keselamatan penumpang RMS Titanic.
- Menggunakan model *machine learning* XGBClassifier untuk mengetahui kemungkinan terbesar para penumpang yang selamat.

## *Data Understanding*
Dataset yang digunakan untuk proyek ini dapat diunduh pada [[3]](https://www.kaggle.com/c/titanic/data). Dataset ini terdiri dari 10 variabel dengan 9 fitur dan 1 label. Berikut penjelasan dari variabel pada dataset yaitu :
- Survival – Berisi informasi penumpang selamat (0) atau tidak (1).
- Pclass – Berisi kelas tiket yang dibeli oleh penumpang.
- Sex – Berisi jenis kelamin penumpang.
- Age – Berisi informasi umur penumpang.
- Sibsp – Berisi berapa banyak saudara atau pasangan penumpang.
- Parch – Berisi banyak orang tua atau anak penumpang.
- Ticket – Berisi informasi tiket penumpang.
- Fare – Berisi informasi harga tiket penumpang.
- Cabin – Berisi nomor kabin penumpang.
- Embarked – Berisi lokasi penumpang berangkat. Apabila penumpang berangkat dari Cherbourg (C), dari Queenstown (Q), dan Southampton (S).

##### *Univariate Analysis*
- Barplot pertama

![1](https://raw.githubusercontent.com/affdn/Machine-Learning-Terapan/main/1.PNG)

Gambar 1. Perbandingan penumpang selamat dan meninggal

Berdasarkan Gambar 1, dapat disimpulkan bahwa lebih banyak penumpang yang meninggal dibandingkan dengan yang selamat.

- Barplot kedua

![2](https://raw.githubusercontent.com/affdn/Machine-Learning-Terapan/main/2.PNG)

Gambar 2. Perbandingan kelas tiket yang dibeli oleh penumpang

Berdasarkan Gambar 2, daoat disimpulkan bahwa lebih banyak penumpang dengan kelas ekonomi menengah karena banyak penumpang yang membeli tiket kelas ketiga. 

- Barplot ketiga

![3](https://raw.githubusercontent.com/affdn/Machine-Learning-Terapan/main/3.PNG)

Gambar 3. Perbandingan antara penumpang laki-laki dan perempuan

Pada Gambar 3, dapat dilihat bahwa lebih banyak penumpang berjenis kelamin laki-laki dibandingkan penumpang perempuan.

- Barplot keempat

![4](https://raw.githubusercontent.com/affdn/Machine-Learning-Terapan/main/4.PNG)

Gambar 4. Asal kota penumpang

Berdasarkan Gambar 4, dapat dilihat bahwa penumpang terbanyak berasal dari kota Southampton diikut Cherbourg dan Queenstown.

- Barplot kelima

![5](https://raw.githubusercontent.com/affdn/Machine-Learning-Terapan/main/5.PNG)

Gambar 5. Nomor tiket penumpang

Pada barplot terakhir yaitu Gambar 5, terlihat banyak sekali nomor tiket yang dimiliki oleh para penumpang, oleh karena itu dilakukan drop pada kolom tiket pada saat training.

##### *Multivariate Analysis*
Dari heatmap yaitu Gambar 6, dapat dilihat beberapa fitur yang tidak berkorelasi salah satunya Parch bahkan fitur Pclass memiliki kolerasi negative (-0.24) sehingga didrop.

![6](https://raw.githubusercontent.com/affdn/Machine-Learning-Terapan/main/6.PNG)

Gambar 6. Korelasi matriks

## *Data Preparation*
Langkah-langkah yang dilakukan sebelum memasukkan data ke model antara lain adalah:
- Encoding fitur menggunakan fitur get_dummies dilakukan pada variabel sex dan embark karena model machine learning hanya bisa menerima data bentuk numerik.
- Men-drop kolom PassengerId, sex, embarked, name, dan ticket pada dataset.
- Membagi dataset menjadi data latih dan data validasi dengan persentase 20% dan 80% sebelum melatih model, ini dilakukan untuk melakukan validasi tanpa bias dari model.
- Melakukan standardisasi pada kolom age, Sibsp, dan Fare untuk membantu model machine learning agar lebih mudah diolah dengan fitur StandardScaler.

## *Modeling*
Model yang digunakan pada proyek ini adalah XGBClassifier. XGBClassifier adalah salah satu gradient boosting algorithm  yang efisien dan fleksibel, selain itu memiliki parallel tree boosting. Parameter yang digunakan pada model ini adalah verbosity dengan nilai false, parameter ini digunakan untuk mencetak pesan. Berikut merupakan hasil modeling menggunakan XGBClassifier. 

| *Accuracy* | *Precision* | *Recall* | *F1 score* |
|----------|-----------|--------|----------|
| 0.76     | 0.594     | 0.559  | 0.576    |

## *Evaluation*
Proses evaluasi dilakukan untuk mengukur kinerja model menggunakan beberapa matriks yaitu *accuracy*, *precision*, *recall*, dan *F1 score*. Matriks evaluasi dihitung menggunakan rumus berikut:

![rumus](https://raw.githubusercontent.com/affdn/Machine-Learning-Terapan/main/evaluasi.PNG)

Gambar 7.Persamaan matriks evaluasi

Keterangan : 
*True Positive* (TP) – Merupakan data positif yang diprediksi benar.

*True Negative* (TN) – Merupakan data negatif yang diprediksi benar.

*False Positive* (FP) – Merupakan data negatif namun diprediksi sebagai data positif.

*False Negative* (FN) – Merupakan data positif namun diprediksi sebagai data negatif.

Berikut merupakan tabel evaluasi dari keempat model (Tabel 1) dan hasil prediksi model XGBClassifier (Tabel 2).

Tabel 1. matriks evaluasi
| *Accuracy* | *Precision* | *Recall* | *F1 score* |
|----------|-----------|--------|----------|
| 0.76     | 0.594     | 0.559  | 0.576    |

Tabel 2. Hasil prediksi
|   | PassengerId | Survived |
|---|-------------|----------|
| 0 | 892         | 0        |
| 1 | 893         | 0        |
| 2 | 894         | 0        |
| 3 | 895         | 0        |
| 4 | 896         | 1        |

## Referensi
[1] Rahmadina, Rizkiana Prima, dkk. 2019. "Pre-processing Data dan Analisis MANOVA OneWay terhadap Data Kecelakaan Kapal Titanic". Jurnal pada Jurusan
Statistika Institut Teknologi Sepuluh November. Surabaya.