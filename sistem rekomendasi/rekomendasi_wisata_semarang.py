# -*- coding: utf-8 -*-
"""Rekomendasi Wisata Semarang.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jfMJjOd6u1kjdQ22nXrwhfgFggRUKkLD

**MENGIMPOR LIBRARY YANG DIBUTUHKAN**
"""

# Commented out IPython magic to ensure Python compatibility.
# Untuk pengolahan data
import pandas as pd
import numpy as np
from zipfile import ZipFile
from pathlib import Path

# Untuk visualisasi data
import seaborn as sns
import matplotlib.pyplot as plt

# %matplotlib inline
sns.set_palette('Set1')
sns.set()

# Untuk pemodelan
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Untuk menghilangkan warnings saat plotting seaborn
import warnings
warnings.filterwarnings('ignore')

# Untuk mengupload file
import os

# install kaggle package
!pip install -q kaggle

# upload kaggle.json
from google.colab import files
files.upload()

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
!ls ~/.kaggle

"""**MENYIAPKAN DATASET**"""

# Download dataset
!kaggle datasets download -d aprabowo/indonesia-tourism-destination

"""**DATA UNDERSTANDING**"""

# unzip
!mkdir data
!unzip -qq indonesia-tourism-destination.zip -d data
!ls data

"""Menyimpan dataset ke dalam variabel"""

rating = pd.read_csv('data/tourism_rating.csv')
place = pd.read_csv('data/tourism_with_id.csv')
user = pd.read_csv('data/user.csv')

"""Melihat data place"""

place.head(5)

"""Menghapus kolom yang tidak diperlukan"""

place = place.drop(['Unnamed: 11','Unnamed: 12','Time_Minutes'],axis=1)
place.head(5)

"""Memilih data destinasi wisata di Kota Semarang"""

place = place[place['City']=='Semarang']
place.head(5)

place.info()

"""Melihat gambaran data rating"""

rating.head()

rating.info()

"""Merubah data rating agar hanya berisi rating pada tempat wisata dari Kota Semarang"""

rating = pd.merge(rating, place[['Place_Id']], how='right', on='Place_Id')
rating.head()

"""Melihat ukuran dataset rating untuk Kota Semarang"""

rating.shape

"""Melihat gambaran data user"""

user.head()

"""Merubah data user agar hanya berisi user yang pernah megunjungi wisata di Kota Semarang"""

user = pd.merge(user, rating[['User_Id']], how='right', on='User_Id').drop_duplicates().sort_values('User_Id')
user.head()

user.shape

"""**EKSPLORASI DATASET**

Membuat dataframe berisi lokasi dan membuat visualisasi wisata dengan jumlah rating terbanyak
"""

top_10 = rating['Place_Id'].value_counts().reset_index()[0:10]
top_10 = pd.merge(top_10, place[['Place_Id','Place_Name']], how='left', left_on='index', right_on='Place_Id')

plt.figure(figsize=(8,5))
sns.barplot('Place_Id_x', 'Place_Name', data=top_10)
plt.title('Jumlah Tempat Wisata dengan Rating Terbanyak', pad=20)
plt.ylabel('Jumlah Rating')
plt.xlabel('Nama Lokasi')
plt.show()

"""Membuat visualisasi perbandingan jumlah kategori wisata di Kota Semarang"""

sns.countplot(y='Category', data=place)
plt.title('Perbandingan Jumlah Kategori Wisata di Kota Semarang', pad=20)
plt.show()

"""Membuat visualisasi distribusi usia user"""

plt.figure(figsize=(5,3))
sns.boxplot(user['Age']);
plt.title('Distribusi Usia User', pad=20)
plt.show()

"""Membuat visualisasi distribusi harga masuk tempat wisata"""

plt.figure(figsize=(7,3))
sns.boxplot(place['Price'])
plt.title('Distribusi Harga Masuk Wisata di Kota Semarang', pad=20)
plt.show()

"""Memfilter dan memvisualisasi asal kota user"""

asalkota = user['Location'].apply(lambda x : x.split(',')[0])

plt.figure(figsize=(10,7))
sns.countplot(y=asalkota)
plt.title('Jumlah Asal Kota dari User')
plt.show()

"""**MENYIAPKAN DATA UNTUK PEMODALAN**

Membaca dataset untuk dilakukan encoding
"""

df = rating.copy()
df.head()

"""Membuat Fungsi untuk melakukan Encoding"""

def dict_encoder(col, data=df):

  # Mengubah kolom suatu dataframe menjadi list tanpa nilai yang sama
  unique_val = data[col].unique().tolist()

  # Melakukan encoding value kolom suatu dataframe ke angka
  val_to_val_encoded = {x: i for i, x in enumerate(unique_val)}

  # Melakukan proses encoding angka ke value dari kolom suatu dataframe
  val_encoded_to_val = {i: x for i, x in enumerate(unique_val)}
  return val_to_val_encoded, val_encoded_to_val

"""Encoding dan Mapping User_Id ke dataframe"""

user_to_user_encoded, user_encoded_to_user = dict_encoder('User_Id')

df['user'] = df['User_Id'].map(user_to_user_encoded)

"""Encoding dan Mapping Place_Id ke dataframe place"""

place_to_place_encoded, place_encoded_to_place = dict_encoder('Place_Id')

df['place'] = df['Place_Id'].map(place_to_place_encoded)

"""Mendapatkan jumlah user, place dan rating"""

num_users, num_place = len(user_to_user_encoded), len(place_to_place_encoded)
 
df['Place_Ratings'] = df['Place_Ratings'].values.astype(np.float32)
 
min_rating, max_rating = min(df['Place_Ratings']), max(df['Place_Ratings'])
 
print(f'Number of User: {num_users}, Number of Place: {num_place}, Min Rating: {min_rating}, Max Rating: {max_rating}')

"""Mengacak dataset"""

df = df.sample(frac=1, random_state=42)
df.head(5)

"""**PEMODELAN MACHINE LEARNING DENGAN RECOMMENDERNET**

Membagi data train dan data test
"""

x = df[['user', 'place']].values
 
# Membuat variabel y untuk membuat rating dari hasil 
y = df['Place_Ratings'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values
 
# Membagi menjadi 80% data train dan 20% data validasi
train_indices = int(0.8 * df.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:]
)

"""Inisialisasi Fungsi"""

class RecommenderNet(tf.keras.Model):
 
  # Insialisasi fungsi
  def __init__(self, num_users, num_places, embedding_size, **kwargs):
    super(RecommenderNet, self).__init__(**kwargs)
    self.num_users = num_users
    self.num_places = num_places
    self.embedding_size = embedding_size
    self.user_embedding = layers.Embedding( # layer embedding user
        num_users,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.user_bias = layers.Embedding(num_users, 1) # layer embedding user bias
    self.places_embedding = layers.Embedding( # layer embeddings places
        num_places,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.places_bias = layers.Embedding(num_places, 1) # layer embedding places bias
 
  def call(self, inputs):
    user_vector = self.user_embedding(inputs[:,0]) # memanggil layer embedding 1
    user_bias = self.user_bias(inputs[:, 0]) # memanggil layer embedding 2
    places_vector = self.places_embedding(inputs[:, 1]) # memanggil layer embedding 3
    places_bias = self.places_bias(inputs[:, 1]) # memanggil layer embedding 4
 
    dot_user_places = tf.tensordot(user_vector, places_vector, 2) 
 
    x = dot_user_places + user_bias + places_bias
    
    return tf.nn.sigmoid(x) # activation sigmoid

"""Inisialisasi Model"""

model = RecommenderNet(num_users, num_place, 50) # inisialisasi model
 
# model compile
model.compile(
    loss = tf.keras.losses.BinaryCrossentropy(),
    optimizer = keras.optimizers.Adam(learning_rate=0.0004),
    metrics=[tf.keras.metrics.RootMeanSquaredError()]
)

"""Inisialisasi Callback"""

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('val_root_mean_squared_error')<0.25):
      print('Lapor! Metriks validasi sudah sesuai harapan')
      self.model.stop_training = True

"""Memulai training"""

# Memulai training 
history = model.fit(
    x = x_train,
    y = y_train,
    epochs = 100,
    validation_data = (x_val, y_val),
    callbacks = [myCallback()]
)

"""Menampilkan plot loss dan validation"""

# Menampilkan plot loss dan validation

plt.plot(history.history['root_mean_squared_error'])
plt.plot(history.history['val_root_mean_squared_error'])
plt.title('model_metrics')
plt.ylabel('root_mean_squared_error')
plt.xlabel('epoch')
plt.ylim(ymin=0, ymax=0.4)
plt.legend(['train', 'test'], loc='center left')
plt.show()

"""**MEMPREDIKSI 5 TERATAS REKOMENDASI**

Menyiapkan dataframe
"""

place_df = place[['Place_Id','Place_Name','Category','Rating','Price']]
place_df.columns = ['id','place_name','category','rating','price']
df = rating.copy()

"""Mengambil sample user"""

user_id = df.User_Id.sample(1).iloc[0]
place_visited_by_user = df[df.User_Id == user_id]

"""Membuat data lokasi yang belum dikunjungi user"""

place_not_visited = place_df[~place_df['id'].isin(place_visited_by_user.Place_Id.values)]['id'] 
place_not_visited = list(
    set(place_not_visited)
    .intersection(set(place_to_place_encoded.keys()))
)
 
place_not_visited = [[place_to_place_encoded.get(x)] for x in place_not_visited]
user_encoder = user_to_user_encoded.get(user_id)
user_place_array = np.hstack(
    ([[user_encoder]] * len(place_not_visited), place_not_visited)
)

"""Mengambil top 5 rekomendasi"""

ratings = model.predict(user_place_array).flatten()
top_ratings_indices = ratings.argsort()[-5:][::-1]
recommended_place_ids = [
    place_encoded_to_place.get(place_not_visited[x][0]) for x in top_ratings_indices
]
 
print('Daftar rekomendasi untuk: {}'.format('User ' + str(user_id)))
print('===' * 15,'\n')
print('----' * 15)
print('Tempat dengan rating wisata paling tinggi dari user')
print('----' * 15)
 
top_place_user = (
    place_visited_by_user.sort_values(
        by = 'Place_Ratings',
        ascending=False
    )
    .head(5)
    .Place_Id.values
)
 
place_df_rows = place_df[place_df['id'].isin(top_place_user)]
for row in place_df_rows.itertuples():
    print(row.place_name, ':', row.category)

print('')
print('----' * 15)
print('Top 5 Tempat Wisata Di Semarang')
print('----' * 15)
 
recommended_place = place_df[place_df['id'].isin(recommended_place_ids)]
for row, i in zip(recommended_place.itertuples(), range(1,8)):
    print(i,'.', row.place_name, '\n    ', row.category, ',', 'Harga Tiket Masuk ', row.price, ',', 'Rating Wisata ', row.rating,'\n')

print('==='*15)