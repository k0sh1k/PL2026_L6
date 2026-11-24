#!/usr/bin/env bash
# Демо сквозной цепочки: curl -> gateway -> storage.
# Адрес gateway берется из окружения, по умолчанию локальный.
GATEWAY_URL="${GATEWAY_URL:-http://127.0.0.1:8000}"
JSON="Content-Type: application/json"

show() { echo; echo "### $1"; }

show "1. POST /devices (gateway -> storage, save)"
RESP=$(curl -s -w "\nHTTP %{http_code}" -X POST "$GATEWAY_URL/devices" -H "$JSON" \
  -d "{\"device_name\":\"Smart kettle $RANDOM\",\"room\":\"Kitchen\",\"power_consumption_watts\":1500}")
echo "$RESP"
ID=$(echo "$RESP" | sed -n 's/.*"id":\([0-9]*\).*/\1/p')

show "2. GET /devices/$ID (gateway -> storage, read)"
curl -s -w "\nHTTP %{http_code}\n" "$GATEWAY_URL/devices/$ID"

show "3. GET /devices/search?q=kettle"
curl -s -w "\nHTTP %{http_code}\n" "$GATEWAY_URL/devices/search?q=kettle"

show "4. GET /devices/999999 (expect 404)"
curl -s -w "\nHTTP %{http_code}\n" "$GATEWAY_URL/devices/999999"

show "5. Invalid power (expect 422, rejected by gateway without network call)"
curl -s -w "\nHTTP %{http_code}\n" -X POST "$GATEWAY_URL/devices" -H "$JSON" \
  -d '{"device_name":"Lamp","room":"Hall","power_consumption_watts":-5}'

echo
read -r -p "Stop the storage service now (Ctrl+C in its terminal), then press Enter... "

show "6. GET /devices/$ID with storage DOWN (expect 503)"
curl -s -w "\nHTTP %{http_code}\n" "$GATEWAY_URL/devices/$ID"
