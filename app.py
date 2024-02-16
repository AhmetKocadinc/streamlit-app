import pandas as pd
import streamlit
import warnings

from streamlit import cursor

warnings.filterwarnings('ignore')
import pickle

import plotly.express as px


with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

df = pd.read_csv('loan_data.csv')
df.head()

cat_cols = [col for col in df.columns if df[col].dtypes in ['object']]
num_but_cat = [col for col in df.columns if df[col].nunique()<=5 and df[col].dtype in ['float64','int64']]
cat_cols = cat_cols + num_but_cat

df[cat_cols].drop('Loan_ID',axis=1,inplace=True)

streamlit.set_page_config(page_title='Müşteri Kredi Uygunluğu Sorgulama')
tabs = ['Kredi Sonucu Tahmin','Müşteri Veritabanı', 'Veri Grafikleri', 'Hakkımda']

page = streamlit.sidebar.radio('Sekmeler', tabs)

if page == 'Kredi Sonucu Tahmin':
    streamlit.title('Kredi Sonuç Tahmin Sayfası')
    streamlit.write(
        """Bu sayfada gerekli bilgiler girilerek müşterinin krediye uygun olup olmadığı tahmini yapılmaktadır..""")
    streamlit.image("kredi.jpg", use_column_width=True, width=200)
    id = streamlit.text_input('Müşteri Numarası Giriniz')
    gender = streamlit.selectbox('Cinsiyet Seçiniz', ['1', '0'])
    married = streamlit.selectbox('Medeni Durum Seçiniz', ['1', '0'])
    Dependents = streamlit.selectbox('Kaç kişilik aileden sorumlu olduğu', ['0', '1', '2', '3', '4', '5'])
    Education = streamlit.selectbox('Eğitimi var mı ?', ['1', '0'])
    Self_Employed = streamlit.selectbox('Çalışıyor mu ?', ['1', '0'])
    LoanAmount = streamlit.text_input('Lütfen Bir Kredi Tutarını Girin')
    Loan_Amount_Term = streamlit.slider('Bir Kredi Vadesi Seçin', 0, 360, 50)
    button = streamlit.button('Sonucu Göster ve veritabanına ekle')

    if button:
        # Kullanıcıdan alınan girdileri modelin beklentilerine uygun bir formata dönüştürün
        input_data = {
            'Gender': [int(gender)],
            'Married': [int(married)],
            'Dependents': [int(Dependents)],
            'Education': [int(Education)],
            'Self_Employed': [int(Self_Employed)],
            'LoanAmount': [int(LoanAmount)],
            'Loan_Amount_Term': [int(Loan_Amount_Term)]
        }

        # Girdileri DataFrame'e çevirin
        input_df = pd.DataFrame(input_data)

        # Modeli kullanarak tahmin yapın
        prediction = model.predict(input_df)

        # Tahmin sonucunu kullanıcıya gösterin


        if prediction[0] == 1:
            streamlit.success("Müşteri krediye uygun")
        else:
            streamlit.error("Müşteri krediye uygun değil")

        # Sonucu DataFrame'de gösterin
        streamlit.write("Girdi Verisi:")
        input_df['Prediction'] = prediction
        streamlit.write(input_df)

if page == 'Veri Grafikleri':
    streamlit.title('Veri Grafikleri')
    streamlit.image("dashboard.png", use_column_width=True, width=200)

    for col in cat_cols:
        count_df = df[col].value_counts().reset_index()
        count_df.columns = [col, 'count']
        fig = px.bar(count_df, x=col, y='count', title=f'{col} Count Plot', labels={'count': 'Count'})
        streamlit.plotly_chart(fig, use_container_width=True)

if page == 'Hakkımda':
    streamlit.header('Ahmet KOCADİNÇ')
    streamlit.subheader('Veri Analisti / Veri Bilimci')

    streamlit.image("vesika.jpg", use_column_width=True, width=300)

    streamlit.write("""
    Merhaba, benim adım Ahmet Kocadinç.
    Veri Analizi pozisyonuna olan ilgimle birlikte İstanbul Bilgi Üniversitesi Yönetim Bilişim Sistemleri bölümünde yüksek lisansımı büyük veri ile üretimin geliştirilmesi konusunda yaptığım proje ile tamamladım. Şu anda da Kodlasam Akademi de veri analizi sertifikasyon eğitimine devam ediyorum. Ayrıca veri analizi ve veri bilimi alanlarında kalitelerini kanıtlamış olan miuul, udemy ve Turkcell geleceği yazanlar gibi kurumların sağlamış olduğu eğitimleri de alarak ve sürekli projeler yaparak kendimi en iyi şekilde geliştiriyorum. Veri analizine olan tutkum beni çok hızlı ve sürekli öğrenmeye itiyor. 
    """)

    streamlit.write("""
    ## Eğitim

    - Lisans: İşletme Fakültesi- Eskişehir Anadolu Üniversitesi- 2016
    - Yüksek Lisans: Yönetim Bilişim Sistemleri - 2018

    ## Yetenekler

    - Python programlama
    - Veri analizi ve makine öğrenimi
    - Tahmin üretme
    - SQL ile veri analizi
    
    ## Sosyal Medya Linkleri
    
    - [Linkedin](https://www.linkedin.com/in/ahmet-kocadin%C3%A7-500673174/)
    - [GitHub](https://github.com/AhmetKocadinc)
    - [Kaggle](https://www.kaggle.com/ahmetkocadinc)
    
    """)
