# Tauron Outages for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

_Component to integrate with [tauron_outages][tauron_outages]._

**This component will set up the following platforms.**

| Platform        | Description                         |
| --------------- | ----------------------------------- |
| `binary_sensor` | Show something `True` or `False`.   |
| `sensor`        | Show info from blueprint API.       |

![example][exampleimg]

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `tauron_outages`.
4. Download _all_ the files from the `kubawolanin/ha-tauron-outages/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Tauron Outages"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
kubawolanin/ha-tauron-outages/translations/en.json
kubawolanin/ha-tauron-outages/translations/nb.json
kubawolanin/ha-tauron-outages/translations/sensor.nb.json
kubawolanin/ha-tauron-outages/__init__.py
kubawolanin/ha-tauron-outages/api.py
kubawolanin/ha-tauron-outages/binary_sensor.py
kubawolanin/ha-tauron-outages/config_flow.py
kubawolanin/ha-tauron-outages/const.py
kubawolanin/ha-tauron-outages/manifest.json
kubawolanin/ha-tauron-outages/sensor.py
```

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

---

[tauron_outages]: https://github.com/kubawolanin/ha-tauron-outages
[buymecoffee]: https://www.buymeacoffee.com/kubawolanin
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/kubawolanin/ha-tauron-outages.svg?style=for-the-badge
[commits]: https://github.com/kubawolanin/ha-tauron-outages/commits/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/kubawolanin/ha-tauron-outages.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Kuba%Wolanin%20%40kubawolanin-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/kubawolanin/ha-tauron-outages.svg?style=for-the-badge
[releases]: https://github.com/kubawolanin/ha-tauron-outages/releases
