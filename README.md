# Crunchyisfun

Crunchyroll (Android) UI base on Funimation themes. but why?

| Home                  | Tab                  |
| --------------------- | -------------------- |
| [Home](./media/1.jpg) | [Tab](./media/2.jpg) |

## Disclaimer

This project does not affiliate with Funimation or Crunchyroll.

This is a fan-made project for educational purposes only.

All trademarks and copyrights belong to their respective owners.

This project is not intended for commercial use or distribution.

You are responsible for any legal consequences that may arise from using
or distributing this modified application.

### Setup

- Clone the repository

```bash
git clone https://github.com/Veha0001/crunchyisfun.git
```

- install dependencies

```bash
pip install typer demodapk --upgrade
```

- Create config

```bash
cp ./mods.json ./config.json
```

- Run the script

```bash
demodapk ./src/crunchyroll.apk -f
```

- Sign and install the apk on your device.

```bash
apksigner sign --key key.pk8 --cert cert.x509.pem ./build/Funimation/Funimation.apk
```

> [!NOTE]
> The command in `mods.json` is may not work on most platform than unix.
>
> You may need to adjust the command accordingly.

#### Patch

- Change primary color to Funimation purple
- Change App name to Funimation
- Change App icon to Funimation icon
- Change Splash screen to Funimation splash screen
- `patch.py` for enable hide ads.

### Credits

For Funimation logo and icon:

- [Wiki](https://en.wikipedia.org/wiki/Funimation)
- [streamlinehq](https://www.streamlinehq.com/icons/download/funimation--22636)

**Revanced** patches for reference on how to hide ads.

#### Need help? etc

open issue.

yes please. give me pull request. (free)

the code is writen in python and some are generated code.

##### Some plan ideas

More color themes?

> idk yet.
