# rpi4-xen-on-suse
XEN on rpi4 with openSUSE Tumbleweed


Raspbery Pi4にXENが来てから数か月経過しているが、2021年４月現在、Distroの公式パッケージが見当たらないので自分でパッケージをビルドしました。

そのうち公式なパッケージがリリースされると思うのでこのページは近い将来に削除されます。

用意するもの：

* Raspberry Pi4 本体
* USBシリアルケーブル（MUSTではないがあった方が便利）
* USB-SSD（MicroSDでの動作は未確認）
* openSUSE Tumbleweed（Leapでは未確認）


やること：
* device tree generation Ignore な XEN のビルド
* CONFIG_XEN=y なカーネルのビルド

ビルドに必要なパッケージは zypper で全て用意できます


![xen-xl](https://user-images.githubusercontent.com/84007765/117802975-0d6a3b80-b291-11eb-8fb6-7a3169a25786.PNG)

## 制限事項
* HDMI が機能しない
* reboot コマンドで reboot してこない
* 他にもあるかもしれないが、未調査（ホビー用途でXENが使えれば私は満足）

## 検証環境
    # cat /etc/os-release
    NAME="openSUSE Tumbleweed"
    # VERSION="20210504"
    ID="opensuse-tumbleweed"
    ID_LIKE="opensuse suse"
    VERSION_ID="20210504"
    PRETTY_NAME="openSUSE Tumbleweed"
    
## 元にしたイメージ

これ↓を USB-SSD に dd しました。

    # xzcat openSUSE-Tumbleweed-ARM-KDE-raspberrypi.aarch64.raw.xz | dd bs=4M of=/dev/sde iflag=fullblock oflag=direct status=progress; sync

## ソースリポジトリの有効化

起動後、src.rpm が欲しいのでリポジトリを有効化します。

    # cat /etc/zypp/repos.d/repo-source.repo
    [repo-source]
    name=openSUSE-Tumbleweed-Source
    enabled=1   ★
    autorefresh=1

## XEN のビルド
[OBS](https://build.opensuse.org/)を利用した方がよいのかもしれないが、rpi4で野良ビルド※した。

※使い方を習得するのに時間がかかりそうだった（野良ビルドした方が早いと判断した）。そのうち習得します。

ソースを持ってきて、patch を入れてビルドするだけ。

    # zypper in -t srcpackage -d xen
    # rpm -ivh /var/cache/zypp/packages/repo-source/src/xen-4.14.1_16-1.1.src.rpm
    # cd /usr/src/packages/SPECS/
    # cp ~/rpi4-xen-on-suse/xen-dt-generation-failed.patch SOURCES/
    # cp ~/rpi4-xen-on-suse/xen-yinose.spec SPEC/xen.spec
    # rpmbuild -ba SPEC/xen.spec

## カーネルのビルド
ソースを持ってきて、patch を入れてビルド。

以下の作業は   [OpenSUSE 13: カーネルを再ビルドする](https://www.hiroom2.com/2016/12/26/opensuse-13-%E3%82%AB%E3%83%BC%E3%83%8D%E3%83%AB%E3%82%92%E5%86%8D%E3%83%93%E3%83%AB%E3%83%89%E3%81%99%E3%82%8B/) を参考にした。

    # zypper in -t srcpackage -d kernel-default kernel-source
    # rpm -ivh /var/cache/zypp/packages/repo-source/nosrc/kernel-default-5.12.0-2.1.nosrc.rpm
    # rpm -ivh /var/cache/zypp/packages/repo-source/src/kernel-source-5.12.0-2.1.src.rpm
    # cp /usr/src/packages/SOURCES/config.tar.bz2 ~/
    # cd ~/
    # tar jxvf config.tar.bz2
    # cp rpi4-xen-on-suse/config/arm64/default config/arm64/
    # tar jcvf config.tar.bz2 config
    # mv config.tar.bz2 /usr/src/packages/SPECS/SOURCES/
    # cd /usr/src/packages/SPEC
    # cp ~/rpi4-xen-on-suse/kernel-yinose.spec kernel-default.spec
    # rpmbuild -ba kernel-default.spec
    
## インストール


    # rpm -ivh kernel-default-5.12.0-xen.aarch64.rpm
    # rpm -ivh xen-4.14.1_16_rpi4-0.aarch64.rpm xen-libs-4.14.1_16_rpi4-0.aarch64.rpm xen-tools-4.14.1_16_rpi4-0.aarch64.rpm

## ブートの設定

/etc/default/grub の GRUB_CMDLINE_XEN を書く

これらのパラメータは[XEN ON RASPBERRY PI 4 ADVENTURES](https://xenproject.org/2020/09/29/xen-on-raspberry-pi-4-adventures/)やEVE OSを参考にした。

    # Xen boot parameters for all Xen boots
    -GRUB_CMDLINE_XEN=""
    +GRUB_CMDLINE_XEN="console=dtuart sync_console dom0_mem=2048M,max:2048M dom0_max_vcpus=2 loglvl=all"
    
ダミーファイルを /boot 配下に置いておく（XENのエントリ作成用のダミー。grub2-mkconfig の実行時に /etc/grub.d/20_linux_xen でファイルの有無を判断しているため。grub2-mkconfig 実行時には /usr/share/efi/aarch64/ に置いてあるイメージが /boot/efi/EFI/opensuse/配下にコピーされるので、/boot配下の xen.gz はダミーで問題ないっぽい）

    # cd /boot
    # touch xen-4.14.1_16_rpi4-0.gz
    # cp Image-5.12.0-xen-default vmlinux-5.12.0-xen-default
    
grub2-mkconfig の実行

    # grub2-mkconfig -o /boot/grub2/grub.cfg
    Generating grub configuration file ...
    Found theme: /boot/grub2/themes/openSUSE/theme.txt
    Found linux image: /boot/Image-5.12.0-xen-default
    Found initrd image: /boot/initrd-5.12.0-xen-default
    Found linux image: /boot/Image-5.11.11-2-default
    Found initrd image: /boot/initrd-5.11.11-2-default
    Found hypervisor: /boot/xen-4.14.1_16_rpi4-0.gz      ★エントリが作成された
    Found linux image: /boot/vmlinux-5.12.0-xen-default
    Found initrd image: /boot/initrd-5.12.0-xen-default
    done

## dtbo の配置

    # cd ~/rpi4-xen-on-suse/
    # dtc -I dts -O dtb -o pi4-64-xen.dtbo pi4-64-xen.dts
    # cp pi4-64-xen.dtbo /boot/efi/overlays
    
## config.txt の編集

/boot/efi/config.txt に以下を追加

    dtoverlay=pi4-64-xen.dtbo


## XENの設定
[XEN ON RASPBERRY PI 4 ADVENTURES](https://xenproject.org/2020/09/29/xen-on-raspberry-pi-4-adventures/)を参考にコンソールの設定をしておく。

    # cat /boot/efi/EFI/opensuse/xen-4.14.1_16_rpi4-0.cfg
    # disclaimer
    [global]
    #default=
    
    [config.1]
    options=console=dtuart sync_console dom0_mem=2048M,max:2048M dom0_max_vcpus=2 loglvl=all
    kernel=vmlinux-5.12.0-xen-default root=/dev/sda3 loglevel=3 console=ttyS0,115200n8 console=hvc0
    ramdisk=initrd-5.12.0-xen-default                                                  ^^^^^^^^^^^^^★
    
## Reboot
あとは起動時に XEN のエントリを選べば Dom0 が起動する。

![grub2-xen](https://user-images.githubusercontent.com/84007765/117802843-e875c880-b290-11eb-85f2-3e4e75b74232.PNG)

![xen-boot](https://user-images.githubusercontent.com/84007765/117803072-2d016400-b291-11eb-8cd4-0f1d8f85407d.PNG)
