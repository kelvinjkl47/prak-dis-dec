$P = (Split-Path -Leaf (Get-Location)).ToLower()

function dcu { docker compose up -d }
function dcd { docker compose down }
function dps { docker ps }
function der { docker exec -it "$P-postgres_replica-1" bash }
function dep { docker exec -it "$P-postgres_primary-1" bash }
function dlr { docker logs "$P-postgres_replica-1" }
function dlp { docker logs "$P-postgres_primary-1" }