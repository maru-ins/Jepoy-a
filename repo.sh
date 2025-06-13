#!/data/data/com.termux/files/usr/bin/bash

# Masukkan data kamu di sini:
OLD_USER="RxR00"
OLD_TOKEN="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"
NEW_USER="maru-ins"
NEW_TOKEN="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"

# Buat direktori kerja
mkdir -p repos && cd repos

# Ambil daftar repo dari akun lama (maks 100 repo)
REPOS=$(curl -s -u "$OLD_USER:$OLD_TOKEN" "https://api.github.com/users/$OLD_USER/repos?per_page=100" | grep -oP '"name": "\K[^"]+')

# Loop semua repo
for REPO in $REPOS; do
    echo "🚀 Menyalin repo: $REPO"

    # Clone dari akun lama
    git clone --mirror https://$OLD_USER:$OLD_TOKEN@github.com/$OLD_USER/$REPO.git

    cd $REPO.git

    # Tambahkan remote akun baru
    git remote set-url origin https://$NEW_USER:$NEW_TOKEN@github.com/$NEW_USER/$REPO.git

    # Push ke akun baru (termasuk semua branch & tag)
    git push --mirror

    cd ..
    echo "✅ Selesai: $REPO"
done

echo "🎉 Semua repo telah berhasil disalin!"
