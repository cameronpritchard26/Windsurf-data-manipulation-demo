curl -k -X 'PUT' \
  'https://myexample.app/indicators/asvgpnpoc.hothouse-dn/metrics' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "bad": 9,
    "duration": 1800000000000,
    "good": 356091,
    "since": "2026-02-11T04:00:00.000Z",
    "total": 356100,
    "until": "2026-02-11T05:00:00.000Z",
    "valid": true
  }
]'