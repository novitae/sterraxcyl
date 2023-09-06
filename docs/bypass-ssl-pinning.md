# Bypass SSL Pinning
How to bypass Instagram's (and also Threads or Facebook) SSL Pinning on iOS.
## 1. Jailbreak your iPhone
- Download latest release of [palera1n](https://github.com/palera1n/palera1n/releases).
- Connect the iphone to computer.
- Jailbreak using `palera1n --setup-fakefs --fakefs`. This will setup fakefs to access to sudo later.
- Once phone is running, run `palera1n -f` to load fakefs. Do it everytime you restart the phone to rejailbreak it, no need to do previous step if the phone wasn't reset.
## 2. Requirements
- On the iPhone, with the app Sileo to install packages:
  - `openssh`
  - `AppSync Unified` from repository `https://cydia.akemi.ai/`
  - `Frida` from repository `https://build.frida.re/`
  - `TrollStore Helper`
    - In `TrollHelper` app install `TrollStore`
    - In `TrollStore` settings, install `Idid`
  - `Filza File Manager 64-bit` from repository `http://tigisoftware.com/repo/`
  - Instagram, Threads or Facebook app.
- On the computer:
  - `frida` (`pip install frida`)
  - `frida-ios-dump`
    - `git clone https://github.com/AloneMonkey/frida-ios-dump`
    - `cd frida-ios-dump`
    - `pip install -r requirements.txt`
  - `libimobiledevice` (https://libimobiledevice.org/#downloads)
  - Hopper Disassembler (paid) or Hopper Disassembler (demo) and https://hexfiend.com.
## 3. Steps
- Connection:
  - 1. Unlock your iphone, then connect it to your computer.
  - 2. On your computer terminal, run `idevicepair pair`.
  - 3. Accept on your iphone and fill the iphone code.
  - 4. Make sure you can ssh to the device, using `ssh mobile@<IPHONE IP>`. The password by default is `alpine`.
    - You can find the `<IPHONE IP>` in `Settings` -> `Wi-Fi` -> `i` next to the current Wi-Fi you are connected to. The IP is shown in field `IP Adress`.
- Dumping app:
  - 1. On a terminal window run `iproxy 2222 22`.
  - 2. On another one, do `cd frida-ios-dump`.
  - 3. Find the identifier of the app you want to dump using `frida-ps -Uai`.
    - Instagram is `com.burbn.instagram`.
  - 4. Do `python <app identifier> -u mobile -P alpine`. Dumping should start.
- Patching SSL pinning:
  - Unzip the `.ipa` file using `unzip Instagram.ipa`
  - Go to `Payload` -> `Instagram.app` -> `Frameworks` -> `FBSharedFramework`
  - Find the executable file `FBSharedFramework`, and load it in Hopper Disassembler (defaults settings are ok).
  - Wait until it disassemble all the file (the "working" with red circle at the lower right of the window will disappear when it will be the case).
  - Click on `str` at the top right corner of the window.
    ![](https://github.com/novitae/sterraxcyl/assets/85891169/b48cb082-7282-4ad2-8153-fb71c18971e9)
  - Search for `openssl cert verify error`, and click on the only result you should see.
    ![](https://github.com/novitae/sterraxcyl/assets/85891169/dcdcc897-5116-4bd7-b0f2-b42b172dc70c)
  - Double click on the `XREF` of the line (highlighted in yellow on the screenshot).
    ![](https://github.com/novitae/sterraxcyl/assets/85891169/91b43ac1-53f8-45ea-81e9-c88f097d331f)
  - Open `CFG` mode.
    ![](https://github.com/novitae/sterraxcyl/assets/85891169/2d4a53f5-a95d-4fab-86da-826ef453ad18)
  - Near the bottom of the tree, find a block of code going to the left and that leads nowhere, as on the screenshots. You can help yourself of the code you're seing in it.
    ![](https://github.com/novitae/sterraxcyl/assets/85891169/87b972f2-0846-439e-9dbe-d011bf99b4f7)
    ![](https://github.com/novitae/sterraxcyl/assets/85891169/e2eede8b-88ab-49a9-a926-4a0536a49cae)
  - On the block just before, find the line containing `cmp w0, #0x1`,
    ![](https://github.com/novitae/sterraxcyl/assets/85891169/51775583-263d-4afb-be57-58463c3ddbb1)
  - **For paid version of Hopper**:
    - Open `Hexdecimal mode` after made sure you clicked on the line once to select it.
      ![](https://github.com/novitae/sterraxcyl/assets/85891169/7e6306a1-386d-45cd-a6e0-d3c30d5b18b7)
    - The four hexdigits should be already selected.
    - Change them so they are now: `1F00006B`
      ![](https://github.com/novitae/sterraxcyl/assets/85891169/7c135c54-2c6b-437b-ba8f-26900579303c)
    - Make a copy of the `Payload` folder, without changing its name, and put it somewhere.
    - Go to `File` -> `Produce new executable`, `Keep invalid signature`.
    - Don't change the name of the file, and save it to your copy of `Payload` -> `Instagram.app` -> `Frameworks` -> `FBSharedFramework` and replace the current file with the same name.
  - **For demo version of Hopper**:
    - Note the end of the offset of the line (it is the dark blue long numbers at the left). For me it is `3deb78`.
    - Open the file `FBSharedFramework` in Hexfiend.
    - Go to `Edit` -> `Jump to Offset`, or `CMD + L`
    - Type `0x` and then paste your offset. Then hit `move`.
      ![](https://github.com/novitae/sterraxcyl/assets/85891169/f57b205f-87d5-43b3-811d-5d53da525818)
    - Your cursor should fall right on the correct instruction. You can verify it by making sure the hexdigits are the same where your cursor is than in the `Hexadecimal mode` in Hopper.
      ![](https://github.com/novitae/sterraxcyl/assets/85891169/54c93b54-9a04-42c5-851a-43ba09abc310)
    - Change the 4 hexdigits (for me `1F040071`) to `1F00006B`.
    - Make a copy of the `Payload` folder, without changing its name, and put it somewhere.
    - Go to `File` -> `Save as`, don't change the name of the file, and save it to your copy of `Payload` -> `Instagram.app` -> `Frameworks` -> `FBSharedFramework` and replace the current file with the same name.
- Packing and installing:
  - In your terminal, go to the folder containing the copy of `Payload`.
  - Do `zip -r Instagram.ipa Payload/`
  - `Instagram.ipa` is your new IPA, but it's signature is corrupted.
  - Copy the file to the phone, using scp, like `scp Instagram.ipa mobile@<IPHONE IP>:~`
  - On the iPhone, open `Filza`, go to the star, `[Root]`.
  - `var` -> `mobile` -> `Instagram.ipa` -> `Open in` -> `TrollStore` -> wait for the dialog window to open and click `Install`.
  - It should install without issues.
  - You can now use instagram with and without a proxy.
