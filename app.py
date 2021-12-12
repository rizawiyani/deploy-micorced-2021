from flask import Flask, render_template, request
import numpy as np
import joblib

model = joblib.load('ModelRF.joblib')
app = Flask(__name__)

categori = {
    "BAIK" : "Sedikit atau tidak ada risiko. Sekarang kondisi udara BAIK, silahkan nikmati kesegaran udara hari ini ^^",
    "SEDANG" : "Individu yang sangat sensitif mungkin mengalami gejala pernapasan. Mulai Waspada dan pakai Masker untuk melindungi dari polisi udara yang ada huft",
    "TIDAK SEHAT" : "Tetap di dalam ruangan dan tutup semua jendela dan bukaan yang memungkinkan masuknya udara yang tercemar, jika memungkinkan. Hari ini sesak banget euy"
}
def predict_air(pm25,pm10,so2,co,o3,no2):
    nums = np.reshape((pm10,pm25,so2,co,o3,no2),(1,-1))
    predicting_categori = model.predict(nums)
    return predicting_categori[0],categori[predicting_categori[0]]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predicting', methods=['POST'])
def predicting():
    if request.method == 'POST':
        pm25 = request.form['pm25']
        pm10 =request.form['pm10']
        so2 = request.form['so2']
        co = request.form['co']
        o3 = request.form['o3']
        no2 = request.form['no2']
        if pm25 == '' or pm10 == '' or so2 == '' or co == '' or o3 == '' or no2 == '':
            return render_template('index.html', message="Mohon masukkan semua variabel yang dibutuhkan untuk memprediksi kualitas udara")
        prediction = predict_air(int(pm25),int(pm10),int(so2),int(co),int(o3),int(no2))
        return render_template('index.html',prediction=prediction[0], categori=prediction[1])

if __name__ == '__main__':
    app.run()