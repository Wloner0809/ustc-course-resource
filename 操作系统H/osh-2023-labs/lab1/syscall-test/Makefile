.PHONY: clean initramfs run

${shell mkdir -p build}

initramfs:
	cd initramfs && find . -print0 | cpio -ov --null -H newc | gzip -9> ../build/initramfs.img

clean:
	rm -rf build

run: 
	qemu-system-x86_64 \
		-kernel bzImage \
		-m 256M \
		-nographic \
		-initrd build/initramfs.img \
		-append "init=/init earlyprintk=serial.ttyS0 console=ttyS0"



