# Kapasitetsvakt for Home Assistant

En tilpasset integrasjon (custom component) for Home Assistant som overvåker strømforbruket i sanntid og kobler ut/inn valgte laster i henhold til kapasitetsledd og marginer.

## Mappestruktur
- `manifest.json`: Metadata for integrasjonen.
- `const.py`: Konstanter og standardverdier.
- `config_flow.py`: Skjemaer for oppsett i UI med støtte for oversettelse.
- `sensor.py`: Sensorer for grenser og effekter.
- `number.py`: Styreingselementer for marginer og kW-grenser.
- `switch.py`: Hovedbryter for kapasitetsvakten.
- `strings.json` & `translations/nb.json`: Norske tekstbeskrivelser og feltnavn.
