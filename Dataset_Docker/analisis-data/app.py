from flask import Flask, render_template, request, redirect
from flask import send_file
from reportlab.pdfgen import canvas

app = Flask(__name__)

@app.template_filter('rupiah')
def rupiah(angka):
    return "{:,.0f}".format(angka).replace(",", ".")

transaksi = []


@app.route("/")
def dashboard():

    pemasukan = sum(
        x["jumlah"]
        for x in transaksi
        if x["jenis"] == "pemasukan"
    )

    pengeluaran = sum(
        x["jumlah"]
        for x in transaksi
        if x["jenis"] == "pengeluaran"
    )

    saldo = pemasukan - pengeluaran

    kategori = set(
        x["kategori"]
        for x in transaksi
    )

    grafik_label = []
    grafik_data = []

    for item in transaksi:

        if item["jenis"] == "pengeluaran":

            grafik_label.append(
                item["kategori"]
            )

            grafik_data.append(
                item["jumlah"]
            )

    return render_template(
        "index.html",
        transaksi=transaksi,
        pemasukan=pemasukan,
        pengeluaran=pengeluaran,
        saldo=saldo,
        jumlah_kategori=len(kategori),
        grafik_label=grafik_label,
        grafik_data=grafik_data
    )


@app.route("/analisis")
def analisis():

    kategori = {}

    for item in transaksi:

        if item["jenis"] == "pengeluaran":

            nama = item["kategori"]

            kategori[nama] = (
                kategori.get(nama, 0)
                + item["jumlah"]
            )

    terbesar = "-"
    nilai_terbesar = 0

    terkecil = "-"
    nilai_terkecil = 0

    if kategori:

        terbesar = max(
            kategori,
            key=kategori.get
        )

        nilai_terbesar = kategori[terbesar]

        terkecil = min(
            kategori,
            key=kategori.get
        )

        nilai_terkecil = kategori[terkecil]

    return render_template(
        "analisis.html",
        kategori=kategori,
        terbesar=terbesar,
        nilai_terbesar=nilai_terbesar,
        terkecil=terkecil,
        nilai_terkecil=nilai_terkecil
    )


@app.route("/wallet")
def wallet():

    pemasukan = sum(
        x["jumlah"]
        for x in transaksi
        if x["jenis"] == "pemasukan"
    )

    pengeluaran = sum(
        x["jumlah"]
        for x in transaksi
        if x["jenis"] == "pengeluaran"
    )

    saldo = pemasukan - pengeluaran

    return render_template(
        "wallet.html",
        transaksi=transaksi,
        pemasukan=pemasukan,
        pengeluaran=pengeluaran,
        saldo=saldo
    )


@app.route("/laporan")
def laporan():

    # Total pemasukan
    pemasukan = sum(
        item["jumlah"]
        for item in transaksi
        if item["jenis"] == "pemasukan"
    )

    # Total pengeluaran
    pengeluaran = sum(
        item["jumlah"]
        for item in transaksi
        if item["jenis"] == "pengeluaran"
    )

    # Saldo akhir
    saldo = pemasukan - pengeluaran

    # Persentase tabungan
    persentase = 0

    if pemasukan > 0:
        persentase = round(
            (saldo / pemasukan) * 100
        )

    # Data laporan dengan saldo berjalan
    laporan_data = []

    saldo_berjalan = 0

    for item in transaksi:

        if item["jenis"] == "pemasukan":

            saldo_berjalan += item["jumlah"]

            laporan_data.append({
                "kategori": item["kategori"],
                "pemasukan": item["jumlah"],
                "pengeluaran": 0,
                "saldo": saldo_berjalan,
                "status": "pemasukan"
            })

        else:

            saldo_berjalan -= item["jumlah"]

            laporan_data.append({
                "kategori": item["kategori"],
                "pemasukan": 0,
                "pengeluaran": item["jumlah"],
                "saldo": saldo_berjalan,
                "status": "pengeluaran"
            })

    # Kesimpulan otomatis
    if saldo > 0:

        kesimpulan = (
            f"Kondisi keuangan sehat. "
            f"Total pemasukan Rp {rupiah(pemasukan)} "
            f"lebih besar daripada pengeluaran "
            f"Rp {rupiah(pengeluaran)}. "
            f"Sisa saldo saat ini sebesar "
            f"Rp {rupiah(saldo)} "
            f"dengan tingkat tabungan {persentase}%."
        )

    elif saldo == 0:

        kesimpulan = (
            "Pemasukan dan pengeluaran seimbang. "
            "Tidak terdapat sisa saldo."
        )

    else:

        kesimpulan = (
            f"Pengeluaran melebihi pemasukan sebesar "
            f"Rp {rupiah(abs(saldo))}. "
            f"Perlu mengurangi pengeluaran "
            f"atau meningkatkan pemasukan."
        )

    return render_template(
        "laporan.html",
        transaksi=transaksi,
        laporan_data=laporan_data,
        pemasukan=pemasukan,
        pengeluaran=pengeluaran,
        saldo=saldo,
        persentase=persentase,
        kesimpulan=kesimpulan
    )


@app.route("/pengaturan")
def pengaturan():

    return render_template(
        "pengaturan.html"
    )


@app.route("/tambah", methods=["POST"])
def tambah():

    kategori = request.form["kategori"]

    jumlah = int(
        request.form["jumlah"]
    )

    jenis = request.form["jenis"]

    transaksi.append({
        "kategori": kategori,
        "jumlah": jumlah,
        "jenis": jenis,
        "tanggal": request.form["tanggal"]
    })

    return redirect("/wallet")

@app.route("/hapus/<int:index>")
def hapus(index):

    if 0 <= index < len(transaksi):
        transaksi.pop(index)

    return redirect("/wallet")

@app.route("/export_pdf")
def export_pdf():

    pdf_file = "laporan_keuangan.pdf"

    c = canvas.Canvas(pdf_file)

    # Judul
    c.setFont("Helvetica-Bold", 18)
    c.drawString(
        180,
        800,
        "Laporan Keuangan"
    )

    # Header tabel
    y = 750

    c.setFont("Helvetica-Bold", 12)

    c.drawString(50, y, "Kategori")
    c.drawString(220, y, "Jenis")
    c.drawString(350, y, "Nominal")

    y -= 20

    c.line(50, y, 550, y)

    y -= 20

    # Isi tabel
    c.setFont("Helvetica", 11)

    for item in transaksi:

        c.drawString(
            50,
            y,
            item["kategori"]
        )

        c.drawString(
            220,
            y,
            item["jenis"]
        )

        c.drawString(
            350,
            y,
            f"Rp {rupiah(item['jumlah'])}"
        )

        y -= 25

        # halaman baru jika penuh
        if y < 50:

            c.showPage()

            y = 800

    # Ringkasan
    y -= 20

    pemasukan = sum(
        x["jumlah"]
        for x in transaksi
        if x["jenis"] == "pemasukan"
    )

    pengeluaran = sum(
        x["jumlah"]
        for x in transaksi
        if x["jenis"] == "pengeluaran"
    )

    saldo = pemasukan - pengeluaran

    c.setFont("Helvetica-Bold", 12)

    c.drawString(
        50,
        y,
        f"Total Pemasukan : Rp {rupiah(pemasukan)}"
    )

    y -= 20

    c.drawString(
        50,
        y,
        f"Total Pengeluaran : Rp {rupiah(pengeluaran)}"
    )

    y -= 20

    c.drawString(
        50,
        y,
        f"Sisa Saldo : Rp {rupiah(saldo)}"
    )

    c.save()

    return send_file(
        pdf_file,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

