# ThermoMaven API Endpoints

Documentation des endpoints API découverts pour ThermoMaven.

## Base URL
```
https://api.iot.thermomaven.com
```

## Authentification

### Login
- **Endpoint**: `/app/account/login`
- **Method**: POST
- **Body**:
  ```json
  {
    "accountName": "email@example.com",
    "accountPassword": "md5_hash_of_password",
    "deviceInfo": "google sdk_gphone_x86_64 11"
  }
  ```
- **Response**: Retourne un token et userId

## Gestion utilisateur

### Get User Info
- **Endpoint**: `/app/user/get`
- **Method**: POST
- **Requires**: Token
- **Body**: `{}`
- **Description**: Récupère les informations du profil utilisateur

### Modify User
- **Endpoint**: `/app/user/modify`
- **Method**: POST
- **Requires**: Token

### User Settings Get
- **Endpoint**: `/app/user/setting/get`
- **Method**: POST
- **Requires**: Token

### User Settings Modify
- **Endpoint**: `/app/user/setting/modify`
- **Method**: POST
- **Requires**: Token

### Register
- **Endpoint**: `/app/user/register`
- **Method**: POST

### Delete User
- **Endpoint**: `/app/user/delete`
- **Method**: POST
- **Requires**: Token

## Gestion des appareils

### Device Models List
- **Endpoint**: `/app/device/model/list`
- **Method**: POST
- **Requires**: Token
- **Body**: `{}`
- **Description**: Liste tous les modèles d'appareils disponibles

### My Devices
- **Endpoint**: `/app/device/share/my/device/list`
- **Method**: POST
- **Requires**: Token
- **Body**: `{}`
- **Description**: Liste des appareils que vous possédez

### Shared Devices
- **Endpoint**: `/app/device/share/shared/device/list`
- **Method**: POST
- **Requires**: Token
- **Body**: `{}`
- **Description**: Liste des appareils partagés avec vous

### Bind Device
- **Endpoint**: `/app/device/bind`
- **Method**: POST
- **Requires**: Token
- **Description**: Lier un nouvel appareil

### Unbind Device
- **Endpoint**: `/app/device/unbind`
- **Method**: POST
- **Requires**: Token
- **Body**:
  ```json
  {
    "deviceId": "device_id_here"
  }
  ```

### Modify Device
- **Endpoint**: `/app/device/modify`
- **Method**: POST
- **Requires**: Token

### Bind Code Create
- **Endpoint**: `/app/device/bind/code/create`
- **Method**: POST
- **Requires**: Token

## Partage d'appareils

### Share Device - Invite
- **Endpoint**: `/app/device/share/invite`
- **Method**: POST
- **Requires**: Token
- **Body**:
  ```json
  {
    "deviceId": 123456,
    "toUserId": 789  // ou "toUserEmail": "email@example.com"
  }
  ```

### Share Device - Accept
- **Endpoint**: `/app/device/share/accept`
- **Method**: POST
- **Requires**: Token
- **Body**:
  ```json
  {
    "deviceShareId": 123456
  }
  ```

### Share Device - Decline
- **Endpoint**: `/app/device/share/decline`
- **Method**: POST
- **Requires**: Token
- **Body**:
  ```json
  {
    "deviceShareId": 123456
  }
  ```

### Share Device - Delete
- **Endpoint**: `/app/device/share/delete`
- **Method**: POST
- **Requires**: Token
- **Body**:
  ```json
  {
    "deviceShareId": 123456
  }
  ```

### Share Device - Detail
- **Endpoint**: `/app/device/share/detail`
- **Method**: POST
- **Requires**: Token

### Share Device - User Info
- **Endpoint**: `/app/device/share/user/info/get`
- **Method**: POST
- **Requires**: Token

## Notifications

### Notification Page
- **Endpoint**: `/app/notification/page`
- **Method**: POST
- **Requires**: Token

### Notification Settings Get
- **Endpoint**: `/app/notification/setting/get`
- **Method**: POST
- **Requires**: Token

### Notification Device List
- **Endpoint**: `/app/notification/setting/device/list`
- **Method**: POST
- **Requires**: Token
- **Body**: `{}`
- **Description**: Liste des appareils pour les paramètres de notification

### Has New Notification
- **Endpoint**: `/app/notification/has/new`
- **Method**: POST
- **Requires**: Token

### Delete Notification
- **Endpoint**: `/app/notification/delete`
- **Method**: POST
- **Requires**: Token
- **Body**:
  ```json
  {
    "notificationId": "notification_id"
  }
  ```

## Historique / Cuissons

### History Page
- **Endpoint**: `/app/history/page`
- **Method**: POST
- **Requires**: Token
- **Body**:
  ```json
  {
    "page": 1,
    "pageSize": 20
  }
  ```
- **Description**: Historique des cuissons avec pagination

### Modify History
- **Endpoint**: `/app/history/modify`
- **Method**: POST
- **Requires**: Token

### Delete History
- **Endpoint**: `/app/history/delete`
- **Method**: POST
- **Requires**: Token
- **Body**:
  ```json
  {
    "cookUuid": "cook_uuid_here"
  }
  ```

## MQTT

### Apply for MQTT Certificate
- **Endpoint**: `/app/mqtt/cert/apply`
- **Method**: POST
- **Requires**: Token
- **Body**: `{}`
- **Description**: Récupère le certificat P12 pour se connecter au serveur MQTT

## Notes importantes

### Headers requis
Tous les endpoints nécessitent les headers suivants :
- `x-appId`: ID de l'application
- `x-appVersion`: Version de l'app (ex: "1804")
- `x-deviceSn`: Numéro de série de l'appareil (16 caractères hexadécimaux)
- `x-lang`: Langue (ex: "en_US")
- `x-nonce`: UUID sans tirets
- `x-region`: Région (ex: "US")
- `x-timestamp`: Timestamp en millisecondes
- `x-token`: Token d'authentification (ou "none" avant login)
- `x-sign`: Signature MD5 calculée
- `Content-Type`: "application/json"
- `User-Agent`: "okhttp/4.12.0"

### Calcul de la signature
La signature est calculée comme suit :
```
sign_string = app_key + "|" + params_sorted + "|" + body_json
signature = MD5(sign_string)
```

où `params_sorted` est une chaîne des headers x-* triés alphabétiquement au format `key=value;key2=value2`

### MQTT
Les appareils semblent communiquer principalement via MQTT plutôt que via des endpoints REST directs. Le topic MQTT `user:device:list` est utilisé pour recevoir la liste des appareils en temps réel.

