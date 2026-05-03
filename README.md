# Helios Election System

[Helios Repository](https://github.com/benadida/helios-server)

MHN-Wahlserver (http://wahl.mind-hochschul-netzwerk.de)

## Container lokal bauen und starten

### Abhängigkeiten

[traefik](https://github.com/Mind-Hochschul-Netzwerk/traefik) und [ldap](https://github.com/Mind-Hochschul-Netzwerk/ldap) müssen laufen.

### Konfiguration

`env.sample` als Vorlage für `.env` verwenden und diese dann bearbeiten

### bauen und starten

    $ make up
    $ make createadmin

Der Login ist dann im Browser unter [https://wahl.docker.localhost/auth/password/login](https://wahl.docker.localhost/auth/password/login) erreichbar. Die Sicherheitswarnung wegen des Zertifikates kann weggeklickt werden.

* Benutzername: Webteam
* Passwort: webteam1
