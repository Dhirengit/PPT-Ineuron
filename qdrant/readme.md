Invoke-RestMethod -Uri "http://localhost:5000/insert" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}'
  
Invoke-RestMethod -Uri "http://localhost:5000/search" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"vector": [0.1, 0.2, 0.3, 0.4], "top_k": 3}'
