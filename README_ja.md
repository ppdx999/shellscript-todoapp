# Shellscript Todo App

ApacheとShellscriptを使用したTodoアプリケーションです。

## 使い方

### 必要なソフトウェアのインストール

- Apache
- POSIX互換のシェル(例: bash, zsh)

### Apacheの設定

Apacheの設定ファイルに以下の設定を追加してください。(osによって設定ファイルの場所が異なる場合があります。下記はarchlinuxの場合の例です。)

`/etc/httpd/conf/extra/todoapp.conf`

```
<VirtualHost *:80>
    ServerName todoapp.local
    DocumentRoot /srv/http/todoapp

    <Directory "/srv/http/todoapp">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog /var/log/httpd/todoapp_error.log
    CustomLog /var/log/httpd/todoapp_access.log combined
</VirtualHost>
```

`/etc/httpd/conf/httpd.conf`

```
# 最後の行に追加
Include conf/extra/todoapp.conf
```

Ubuntuの場合は`/etc/apache2/sites-available/`に`todoapp.conf`を作成する形が一般的です。


### ホスト名の設定

`/etc/hosts`に以下の設定を追加してください。

```
127.0.0.1 todoapp.local
```

### インストール

```
cp -r todoapp /srv/http/
sudo chown -R http:http /srv/http/todoapp
sudo chmod -R 755 /srv/http/todoapp
```

もしくはローカルで動かすだけであれば、シンボリックリンクを張ることもできます。

```
cd このリポジトリのトップディレクトリ
sudo ln -s $(pwd)/todoapp /srv/http/todoapp
```

### 起動

```
sudo systemctl start httpd
```


### 動作確認

ブラウザで`http://todoapp.local`にアクセスしてください。
